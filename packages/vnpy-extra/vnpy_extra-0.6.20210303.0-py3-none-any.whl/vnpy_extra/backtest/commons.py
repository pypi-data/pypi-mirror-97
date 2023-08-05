"""
@author  : MG
@Time    : 2021/1/8 7:42
@File    : run.py
@contact : mmmaaaggg@163.com
@desc    : 用于作为回测方法的公共方法
"""
import itertools
import json
import os
from collections import OrderedDict
from collections import defaultdict
from datetime import date
from multiprocessing import Pool, cpu_count, Manager
from multiprocessing import Queue, Lock
from queue import Empty
from typing import Optional, Union, Type, List, Callable, Iterator, Dict, Tuple

import pandas as pd
from ibats_utils.mess import date_2_str
from tqdm import tqdm
from vnpy.app.cta_strategy import CtaTemplate
from vnpy.app.portfolio_strategy import StrategyTemplate
from vnpy.trader.constant import Interval

from vnpy_extra.backtest import CrossLimitMethod, STOP_OPENING_POS_PARAM, ENABLE_COLLECT_DATA_PARAM
from vnpy_extra.backtest import DEFAULT_STATIC_ITEMS, CleanupOrcaServerProcessIntermittent
from vnpy_extra.backtest.cta_strategy.engine import BacktestingEngine as CtaBacktestingEngine
from vnpy_extra.backtest.portfolio_strategy.engine import BacktestingEngine as PortfolioBacktestingEngine
from vnpy_extra.config import logging
from vnpy_extra.constants import SYMBOL_SIZE_DIC, INSTRUMENT_PRICE_TICK_DIC, INSTRUMENT_RATE_DIC
from vnpy_extra.db.orm import set_account_backtest, StrategyBacktestStats, StrategyBacktestStatusEnum
from vnpy_extra.report.collector import trade_data_collector, order_data_collector
from vnpy_extra.utils.enhancement import get_instrument_type

logger = logging.getLogger()
HAS_PANDAS_EXCEPTION = False


def get_output_file_path(*args, root_folder_name=None):
    """
    获取输出文件的目录
    root_folder_name 为根目录，None则为当前系统日期
    """
    if root_folder_name is None or root_folder_name == "":
        root_folder_name = date_2_str(date.today())
    file_path = os.path.join('output', root_folder_name, *[_ for _ in args if _ is not None])
    dir_path, _ = os.path.split(file_path)
    os.makedirs(dir_path, exist_ok=True)
    return file_path


def run_backtest(
        strategy_class: Union[Type[CtaTemplate], Type[StrategyTemplate]],
        multi_symbols: bool,
        engine_kwargs: dict,
        strategy_kwargs: Optional[dict] = None,
        root_folder_name=None,
        file_name_header=None,
        engine=None,
        output_available_only=False,
        open_browser_4_charts=False,
        log_statistic_markdown=False,
        show_indexes=None,
        output_statistics=True,
        lock: Optional[Lock] = None,
        enable_collect_data=False,
        save_stats: Optional[bool] = None,
        strategy_stats_original: Optional[StrategyBacktestStats] = None,
        enable_join_collector=True
) -> dict:
    """
    本地化运行策略回测程序
    :param strategy_class 策略类
    :param multi_symbols 是否多合约
    :param engine_kwargs 回测引擎参数，或者回测引擎参数列表
    :param strategy_kwargs 策略类 参数数组字典,key为参数名称, value 为数组
    :param file_name_header 自定义文件头名称，默认为None，所有["参数名+参数", ...]用下划线链接
    :param engine 回测引擎
    :param output_available_only
    :param open_browser_4_charts
    :param root_folder_name 策略类 保存跟目录名称,None 时为当前系统日期
    :param log_statistic_markdown Markdown 格式记录统计数据
    :param show_indexes 展示指标
    :param output_statistics 输出统计结果
    :param lock 进程锁
    :param enable_collect_data 是否运行收集数据
    :param save_stats 保存统计数据，默认情况下只记录 CrossLimitMethod.open_price 的回测结果数据
    :param strategy_stats_original 此前回测的统计数据对象
    :param enable_join_collector 是否交易结束后关闭 collector
    """
    set_account_backtest()
    # 整理参数
    engine_kwargs = engine_kwargs.copy()
    engine_kwargs.setdefault('capital', 100000)
    start = engine_kwargs.setdefault("start", date(2017, 1, 1))
    end = engine_kwargs.setdefault("end", date(2022, 12, 31))
    interval = engine_kwargs.setdefault("interval", Interval.MINUTE)
    cross_limit_method = engine_kwargs.setdefault("cross_limit_method", CrossLimitMethod.open_price)
    if save_stats is None:
        # 默认情况下只记录 CrossLimitMethod.open_price 的回测结果数据
        save_stats = cross_limit_method == CrossLimitMethod.open_price

    if multi_symbols:
        vt_symbols = engine_kwargs["vt_symbols"]
        vt_symbol_str = "_".join(vt_symbols)
        engine_kwargs.setdefault('sizes', {vt_symbol: SYMBOL_SIZE_DIC[get_instrument_type(vt_symbol)]
                                           for vt_symbol in vt_symbols})
        engine_kwargs.setdefault('rates', {vt_symbol: INSTRUMENT_RATE_DIC[get_instrument_type(vt_symbol)]
                                           for vt_symbol in vt_symbols})
        engine_kwargs.setdefault('slippages', {vt_symbol: 0 for vt_symbol in vt_symbols})
        engine_kwargs.setdefault('priceticks', {vt_symbol: INSTRUMENT_PRICE_TICK_DIC[get_instrument_type(vt_symbol)]
                                                for vt_symbol in vt_symbols})
    else:
        vt_symbol = engine_kwargs["vt_symbol"]
        vt_symbol_str = vt_symbol
        instrument_type = get_instrument_type(vt_symbol)
        engine_kwargs.setdefault('size', SYMBOL_SIZE_DIC[instrument_type])
        engine_kwargs.setdefault("rate", INSTRUMENT_RATE_DIC[instrument_type])
        engine_kwargs.setdefault("slippage", 0)
        engine_kwargs.setdefault('pricetick', INSTRUMENT_PRICE_TICK_DIC[instrument_type])

    # 初始化引擎
    load_data = True
    if engine is None:
        if multi_symbols:
            engine = PortfolioBacktestingEngine()
        else:
            engine = CtaBacktestingEngine()
    else:
        if multi_symbols:
            vt_symbols = [_.upper() for _ in engine_kwargs["vt_symbols"]]
            load_data = not (
                    engine.vt_symbols == vt_symbols
                    and engine.start == start
                    and engine.end == end
                    and engine.interval == interval)
        else:
            vt_symbol = engine_kwargs["vt_symbol"]
            load_data = not (
                    engine.vt_symbol == vt_symbol
                    and engine.start == start
                    and engine.end == end
                    and engine.interval == interval)

        # 清除上一轮测试数据
        engine.clear_data()

    # 设置环境参数
    engine.set_parameters(**engine_kwargs)

    # 设置策略参数
    if strategy_kwargs is None:
        logger.warning('%s 回测没有设置参数项，使用默认参数', strategy_class.__name__)
        strategy_kwargs = {}

    if enable_collect_data:
        strategy_kwargs['enable_collect_data'] = enable_collect_data

    engine.add_strategy(strategy_class=strategy_class, setting=strategy_kwargs)
    engine.strategy.set_is_realtime_mode(False)

    if strategy_stats_original is not None:
        if strategy_stats_original.short_name is not None:
            engine.strategy.strategy_name = strategy_stats_original.short_name

        # 如果 strategy_stats_original 不为空，则沿用此前回测时使用的 id_name
        # 该逻辑将作为第一原则，覆盖掉此前所有的 file_name_header 赋值
        file_name_header = strategy_stats_original.id_name
    elif file_name_header is None or file_name_header == "":
        file_name_header = engine.strategy.get_id_name()

    if strategy_stats_original is not None:
        backtest_status: StrategyBacktestStatusEnum = StrategyBacktestStatusEnum(
            strategy_stats_original.backtest_status)
        backtest_status_path = f"{backtest_status.value}{backtest_status.name}"
    else:
        backtest_status_path = None

    image_file_name = get_output_file_path(
        vt_symbol_str, cross_limit_method.name, backtest_status_path, 'images',
        f'{file_name_header}.png', root_folder_name=root_folder_name)
    stat_file_name = get_output_file_path(
        vt_symbol_str, cross_limit_method.name, backtest_status_path, 'stats',
        f'{file_name_header}_stats.md', root_folder_name=root_folder_name)
    daily_result_file_name = get_output_file_path(
        vt_symbol_str, cross_limit_method.name, backtest_status_path, 'data',
        f'{file_name_header}_result.csv', root_folder_name=root_folder_name)
    param_file_name = get_output_file_path(
        vt_symbol_str, cross_limit_method.name, backtest_status_path, 'params',
        f'{file_name_header}_param.json', root_folder_name=root_folder_name)

    # 加载历史数据
    if load_data:
        if lock is not None:
            with lock:
                engine.load_data()
        else:
            engine.load_data()

    # 开始回测
    if enable_collect_data:
        # 删除策略历史交易数据
        from vnpy_extra.db.orm import TradeDataModel
        TradeDataModel.clear_by_strategy_name(strategy_class.__name__)

    engine.run_backtesting()
    if enable_collect_data and enable_join_collector:
        # 仅用于测试 trade_data_collector 使用，一般回测状态下不进行数据采集
        trade_data_collector.join_queue()
        order_data_collector.join_queue()
        trade_data_collector.is_running = False
        order_data_collector.is_running = False

    # 统计结果
    df: pd.DataFrame = engine.calculate_result()
    # 统计绩效
    statistics = engine.calculate_statistics(output=output_statistics)
    statistics["module_name"] = strategy_class.__module__
    statistics["strategy_class_name"] = strategy_class.__name__
    statistics["id_name"] = file_name_header
    statistics['symbols'] = vt_symbol_str
    statistics["cross_limit_method"] = cross_limit_method.value

    if output_available_only and not statistics['available']:
        pass
    else:
        if df is not None:
            # engine.output(df)
            df[[_ for _ in df.columns if _ != "trades"]].to_csv(daily_result_file_name)
            # 展示图表
            charts_data = engine.show_chart(
                image_file_name=image_file_name,
                open_browser_4_charts=open_browser_4_charts,
                show_indexes=show_indexes,
                lock=lock,
            )
        else:
            charts_data = None

        image_file_url = image_file_name.replace('\\', '/')
        statistics["image_file_url"] = f"![img]({image_file_url})"
        statistics["image_file_path"] = image_file_name

        # 保存参数
        with open(param_file_name, 'w') as fp:
            json.dump(strategy_kwargs, fp=fp)

        try:
            # 保存绩效结果
            statistics_s = pd.Series(statistics)
            statistics_s.name = file_name_header
            statistics_s.index.rename('item', inplace=True)
            if log_statistic_markdown:
                logger.info("\n:%s", statistics_s.to_markdown())

            with open(stat_file_name, 'w') as f:
                statistics_s.to_markdown(f, 'w')

            logger.info("策略绩效(保存到文件：%s)", stat_file_name)  # , statistics_s.to_markdown()
        except AttributeError:
            global HAS_PANDAS_EXCEPTION
            if not HAS_PANDAS_EXCEPTION:
                logger.warning("pandas 需要 1.0.0 以上版本才能够支持此方法")
                HAS_PANDAS_EXCEPTION = True

        # 将回测结果保存到数据库
        if save_stats:
            try:
                if strategy_stats_original is not None:
                    backtest_status = strategy_stats_original.backtest_status
                    statistics['backtest_status'] = backtest_status
                    statistics['short_name'] = strategy_stats_original.short_name
                    statistics['shown_name'] = strategy_stats_original.shown_name

                StrategyBacktestStats.update_stats(
                    {k: v for k, v in strategy_kwargs.items()
                     if k not in (ENABLE_COLLECT_DATA_PARAM, STOP_OPENING_POS_PARAM)},
                    engine_kwargs, statistics, charts_data,
                )
            except:
                logger.exception("StrategyBacktestStats.update_stats 异常,不影响回测")

    if enable_collect_data and enable_join_collector:
        trade_data_collector.join()
        order_data_collector.join()

    return statistics


def run_backtest_from_queue(strategy_cls, task_queue: Queue, results_dic: dict, lock: Lock,
                            statistic_items, multi_valued_param_name_list, name, multi_symbols: bool):
    """
    :param strategy_cls 策略类
    :param task_queue 任务参数队列
    :param results_dic 执行结果队列
    :param lock 进程锁
    :param statistic_items 统计项
    :param multi_valued_param_name_list 参数名称
    :param name 进程名称
    :param multi_symbols 是否多合约
    """
    logger.info("启动子进程 %s 监控任务队列 task_queue,结果返回给 results_dic", name)
    if multi_symbols:
        engine = PortfolioBacktestingEngine()
    else:
        engine = CtaBacktestingEngine()

    job_count = 0
    while True:
        try:
            # 阻塞等待消息队列传递参数
            key, backtest_param_kwargs = task_queue.get(block=True, timeout=5)
            job_count += 1
            logger.debug('process %s %d task| key=%s, backtest_param_kwargs=%s',
                         name, job_count, key, backtest_param_kwargs)
            try:
                statistics_dic = run_backtest(
                    strategy_cls,
                    multi_symbols=multi_symbols,
                    engine=engine,
                    output_statistics=False,
                    lock=lock,
                    **backtest_param_kwargs
                )
            except Exception:
                logger.exception("%s run_backtest error", name)
                task_queue.task_done()
                continue

            task_queue.task_done()
            strategy_kwargs = backtest_param_kwargs["strategy_kwargs"]
            statistics_dic = OrderedDict([(k, v) for k, v in statistics_dic.items() if k in statistic_items])
            statistics_dic.update({k: v for k, v in strategy_kwargs.items() if k in multi_valued_param_name_list})

            with lock:
                # 多进程 dict 对象只能使用 赋值 操作。不可以使用 [].append 的操作。
                # 因此不可以使用 setdefault(key, []).append()
                if key in results_dic:
                    results = results_dic[key]
                    results.append(statistics_dic)
                else:
                    results = [statistics_dic]

                results_dic[key] = results

            logger.debug('process %s %d task| key=%s finished',
                         name, job_count, key)
        except Empty:
            logger.warning("Process '%s' 没有收到任务信息,结束进程，累计完成 %d 个任务",
                           name, job_count)
            break


def get_param_values_iter(param_values_dic: Union[dict, List[dict]]):
    if isinstance(param_values_dic, dict):
        param_values_dic_list = [param_values_dic]
    elif isinstance(param_values_dic, list):
        param_values_dic_list = param_values_dic
    else:
        raise ValueError(f"param_values_dic {type(param_values_dic)} 参数类型不支持")

    param_name_list = None
    param_values_iter_source = []
    for param_values_dic in param_values_dic_list:
        if param_name_list is None:
            param_name_list = list(param_values_dic.keys())

        param_iter = itertools.product(*[
            param_values_dic[_] if _ in param_values_dic else [None] for _ in param_name_list
        ])
        param_values_iter_source.append(param_iter)

    param_values_iter = itertools.chain(*param_values_iter_source)
    return param_name_list, param_values_iter


def get_backtest_params_iter(
        backtest_param_dic_list: Union[dict, List[dict]],
        param_values_dic: Union[dict, List[dict]],
) -> Tuple[List[str], Iterator[Tuple[dict, list, Optional[StrategyBacktestStats]]]]:
    """
    返回参数参数名称列表以及迭代器兑现
    :param backtest_param_dic_list 合约列表(可以是 str 数组,或者 tuple 数组,如果是 tuple 对应 (vt_symbol, slippage, size)
    :param param_values_dic 策略类 参数数组字典,key为参数名称, value 为数组
    """
    param_name_list, param_values_iter = get_param_values_iter(param_values_dic)

    if isinstance(backtest_param_dic_list, dict):
        backtest_param_dic_list = [backtest_param_dic_list]

    backtest_params_iter = itertools.product(backtest_param_dic_list, param_values_iter, [None])
    return param_name_list, backtest_params_iter


def bulk_backtest(
        strategy_cls: Union[Type[StrategyTemplate], Type[CtaTemplate]],
        multi_symbols: bool,
        engine_param_dic_list: Union[dict, List[dict]],
        strategy_param_dic_list: Union[Dict[str, list], List[Dict[str, list]]],
        available_backtest_params_check_func: Optional[Callable] = None,
        file_name_func: Optional[Callable] = None,
        statistic_items: Optional[list] = None,
        engine_param_key_func: Optional[Callable] = None,
        output_available_only: bool = True,
        open_browser_4_charts: bool = False,
        root_folder_name: Optional[str] = None,
        multi_process: int = 0,
        save_stats: Optional[bool] = None,
        enable_collect_data=False,
):
    """
    :param strategy_cls 策略类
    :param multi_symbols 是否多合约
    :param engine_param_dic_list 回测引擎参数，或者回测引擎参数列表
    :param strategy_param_dic_list 策略类 参数数组字典,key为参数名称, value 为数组
    :param available_backtest_params_check_func 如果希望忽略部分参数组合，可以自定义函数，对每一个组合进行筛选，False为忽略该参数
    :param file_name_func 自定义文件头名称，默认为None，所有["参数名+参数", ...]用下划线链接
    :param statistic_items 策略类 统计项默认 DEFAULT_STATIC_ITEMS
    :param engine_param_key_func engine param key
    :param output_available_only
    :param open_browser_4_charts
    :param root_folder_name 策略类 保存跟目录名称,None 时为当前系统日期
    :param multi_process 0 单进程, -1 为CPU数量,正数为对应的进程数
    :param save_stats 保存统计数据，默认情况下只记录 CrossLimitMethod.open_price 的回测结果数据
    :param enable_collect_data 是否运行收集数据
    """
    if root_folder_name is None:
        root_folder_name = f'bulk_backtest_{date_2_str(date.today())}'

    # 整理参数
    param_name_list, backtest_params_iter = get_backtest_params_iter(engine_param_dic_list, strategy_param_dic_list)
    bulk_backtest_with_backtest_params_iter(
        strategy_cls=strategy_cls,
        multi_symbols=multi_symbols,
        param_name_list=param_name_list,
        backtest_params_iter=backtest_params_iter,
        available_backtest_params_check_func=available_backtest_params_check_func,
        file_name_func=file_name_func,
        statistic_items=statistic_items,
        engine_param_key_func=engine_param_key_func,
        output_available_only=output_available_only,
        open_browser_4_charts=open_browser_4_charts,
        root_folder_name=root_folder_name,
        multi_process=multi_process,
        save_stats=save_stats,
        enable_collect_data=enable_collect_data,
    )


def bulk_backtest_with_backtest_params_iter(
        strategy_cls: Union[Type[StrategyTemplate], Type[CtaTemplate]],
        multi_symbols: bool,
        param_name_list: List[str],
        backtest_params_iter: Iterator[Tuple[dict, list, Optional[StrategyBacktestStats]]],
        available_backtest_params_check_func: Optional[Callable] = None,
        file_name_func: Optional[Callable] = None,
        statistic_items: Optional[list] = None,
        engine_param_key_func: Optional[Callable] = None,
        output_available_only: bool = True,
        open_browser_4_charts: bool = False,
        root_folder_name: Optional[str] = None,
        multi_process: int = 0,
        save_stats: Optional[bool] = None,
        enable_collect_data=False,
):
    """
    :param strategy_cls 策略类
    :param multi_symbols 是否多合约
    :param param_name_list 回测参数名称列表
    :param backtest_params_iter 回测参数迭代器，
    :param available_backtest_params_check_func 如果希望忽略部分参数组合，可以自定义函数，对每一个组合进行筛选，False为忽略该参数
    :param file_name_func 自定义文件头名称，默认为None，所有["参数名+参数", ...]用下划线链接
    :param statistic_items 策略类 统计项默认 DEFAULT_STATIC_ITEMS
    :param engine_param_key_func engine param key
    :param output_available_only
    :param open_browser_4_charts
    :param root_folder_name 策略类 保存跟目录名称,None 时为当前系统日期
    :param multi_process 0 单进程, -1 为CPU数量,正数为对应的进程数
    :param save_stats 保存统计数据，默认情况下只记录 CrossLimitMethod.open_price 的回测结果数据
    :param enable_collect_data 是否运行收集数据
    """
    if statistic_items is None:
        statistic_items = DEFAULT_STATIC_ITEMS

    data, backtest_params_list = [], []
    for _ in backtest_params_iter:
        data.append(_[1])
        backtest_params_list.append(_)

    params_df = pd.DataFrame(data, columns=param_name_list)
    backtest_params_count = params_df.shape[0]
    # 记录所有 单一值 变量的名字
    single_valued_param_name_set = set()
    for name in param_name_list:
        if params_df[name].unique().shape[0] == 1:
            single_valued_param_name_set.add(name)

    multi_valued_param_name_list = [_ for _ in param_name_list if _ not in single_valued_param_name_set]
    logger.info(
        f'开始批量运行，包含 {len(param_name_list)} 个参数，总计 {backtest_params_count:,d} 个回测')

    # 重新包装迭代器
    backtest_params_iter = tqdm(enumerate(backtest_params_list), total=backtest_params_count)

    # 多进程情况启动进程池
    is_multi_process = multi_process not in (0, 1)
    if is_multi_process:
        # 多进程情况下启动子进程,等待消息带回来传递参数
        if multi_process == -1:
            # 默认CPU数量
            multi_process = cpu_count()

        engine = None
        pool = Pool(processes=multi_process)
        manager = Manager()
        # task_queue = JoinableQueue(multi_process * 2)
        task_queue = manager.Queue(multi_process * 2)
        results_dic = manager.dict()
        lock = manager.Lock()
        # 建立子进程实例
        for _ in range(multi_process):
            name = f"process_{_}"
            logger.debug("启动子进程 %s", name)

            def print_error(value):
                logger.error("%s 启动 error: %s", name, value)

            pool.apply_async(
                run_backtest_from_queue,
                args=(strategy_cls, task_queue, results_dic, lock,
                      statistic_items, multi_valued_param_name_list, name, multi_symbols),
                error_callback=print_error
            )

        cleanup_thread = CleanupOrcaServerProcessIntermittent()
        cleanup_thread.start()
    else:
        # 单进程准备好回测引擎
        if multi_symbols:
            engine = PortfolioBacktestingEngine()
        else:
            engine = CtaBacktestingEngine()

        pool = None
        task_queue = None
        cleanup_thread = None
        results_dic = defaultdict(list)

    # 开始对每一种参数组合进行回测
    vt_symbol_str = ''
    for n, (engine_kwargs, param_values, strategy_stats_original) in backtest_params_iter:
        # 设置参数
        strategy_kwargs = {k: v for k, v in zip(param_name_list, param_values)}
        backtest_param_kwargs = dict(
            engine_kwargs=engine_kwargs,
            strategy_kwargs=strategy_kwargs,
            output_available_only=output_available_only,
            open_browser_4_charts=open_browser_4_charts,
            save_stats=save_stats,
            strategy_stats_original=strategy_stats_original,
            enable_collect_data=enable_collect_data,
            enable_join_collector=False,
        )
        # 检查参数有效性
        if available_backtest_params_check_func is not None and not available_backtest_params_check_func(
                **backtest_param_kwargs):
            continue
        cross_limit_method = engine_kwargs["cross_limit_method"] \
            if "cross_limit_method" in engine_kwargs else CrossLimitMethod.open_price
        # 设置 engine_param_key
        engine_param_key = engine_param_key_func(**engine_kwargs)
        # 设置 root_folder_name, file_name_header 参数
        root_folder_name_curr = root_folder_name
        file_name_header = None
        if strategy_stats_original is not None:
            file_name_header = strategy_stats_original.id_name
        elif file_name_func is not None:
            file_name_header = file_name_func(cross_limit_method=cross_limit_method, **backtest_param_kwargs)
            if isinstance(file_name_header, tuple):
                root_folder_name_ret, file_name_header = file_name_header
                if root_folder_name_ret is not None:
                    root_folder_name_curr = os.path.join(root_folder_name_curr, root_folder_name_ret)

        # 2021-02-01
        # 默认文件名可以为 None，以下代码废弃
        # if file_name_header is None:
        #     file_name_header = '_'.join([f"{k}{v}" for k, v in zip(param_name_list, param_values)]) \
        #                        + f'_{cross_limit_method.value}{cross_limit_method.name}'

        backtest_param_kwargs["file_name_header"] = file_name_header
        backtest_param_kwargs["root_folder_name"] = root_folder_name_curr
        # 设置进度条显示名称
        if multi_symbols:
            vt_symbol_str = "_".join(engine_kwargs["vt_symbols"])
            description = " vs ".join(engine_kwargs["vt_symbols"])
        else:
            vt_symbol_str = engine_kwargs["vt_symbol"]
            description = vt_symbol_str

        if file_name_header is not None:
            description += f" <{file_name_header}>"

        backtest_params_iter.set_description(description)
        # 开始回测
        if is_multi_process:
            logger.debug("put key=%s task=%s in queue", engine_param_key, backtest_param_kwargs)
            # 多进程 参数加入队列
            task_queue.put((engine_param_key, backtest_param_kwargs), block=True)
        else:
            # 单进程直接调用
            statistics_dic = run_backtest(
                strategy_cls,
                multi_symbols=multi_symbols,
                engine=engine,
                output_statistics=False,
                **backtest_param_kwargs
            )
            # strategy_kwargs.update({k: v for k, v in statistics_dic.items() if k in statistic_items})
            # 剔除 single_valued_param_name_set
            statistics_dic = OrderedDict([(k, v) for k, v in statistics_dic.items() if k in statistic_items])
            statistics_dic.update({k: v for k, v in strategy_kwargs.items() if k in multi_valued_param_name_list})
            # statistics_dic["file_name_header"] = file_name_header
            results_dic[engine_param_key].append(statistics_dic)

    # 如果是多进程，则等待全部进程结束
    if is_multi_process:
        logger.info("等待清空任务队列")
        task_queue.join()
        logger.debug("等待所有进程结束")
        pool.close()
        logger.info("关闭进程池（pool）不再接受新的任务")
        cleanup_thread.is_running = False
        cleanup_thread.join()
        logger.debug("关闭 CleanupOrcaServerProcessIntermittent 线程")
        pool.join()
        logger.info("进程池（pool）所有任务结束")

    keys_list = list(results_dic.keys())
    backtest_params_count = len(keys_list)
    logger.info("keys_list %s", keys_list)
    logger.info("param_name_list %s", param_name_list)
    logger.info("multi_valued_param_name_list %s", multi_valued_param_name_list)
    column_rename_dic = {
        "max_new_higher_duration": "新高周期",
        "daily_trade_count": "交易频度",
        "info_ratio": "信息比",
        "return_drawdown_ratio": "卡玛比",
    }
    if backtest_params_count == 0:
        result_df = None
        result_available_df = None
    else:
        # 根据 keys_list 单独生成每一个结果集文件
        df_list = [
            pd.DataFrame(
                results_dic[_]
            ).set_index(
                multi_valued_param_name_list
            ).rename(
                columns=column_rename_dic
            ).drop_duplicates() for _ in keys_list]
        keys = ['_'.join([
            f"{_.value}{_.name}" if isinstance(_, CrossLimitMethod) else str(_) for _ in k
        ]) for k in keys_list]
        for key, df in zip(keys, df_list):
            csv_file_path = get_output_file_path(
                f'{key}_{date_2_str(date.today())}.csv', root_folder_name=root_folder_name)
            xls_file_path = get_output_file_path(
                f'{key}_{date_2_str(date.today())}.xlsx', root_folder_name=root_folder_name)
            df['backtest_status'] = StrategyBacktestStatusEnum.Unavailable.value
            df['short_name'] = ''
            df['shown_name'] = ''
            available_df = df[df['available']]
            available_df.to_csv(csv_file_path, encoding='GBK', index=False)
            available_df.to_excel(xls_file_path, index=False)

        if backtest_params_count == 1:
            result_df = pd.DataFrame(results_dic[keys_list[0]]).rename(columns=column_rename_dic)
            result_available_df = result_df[result_df['available']].reset_index()
            result_df.reset_index(inplace=True)
        else:
            # is_available 取交集
            is_available_s = df_list[0]['available']
            for df in df_list[1:]:
                is_available_s = is_available_s | df['available']

            # 根据 keys 横向连接 DataFrame 便于进行比较
            try:
                result_df = pd.concat(
                    df_list,
                    keys=keys,
                    axis=1,
                )
                result_available_df = result_df[is_available_s].reset_index()
                result_df.reset_index(inplace=True)
            except ValueError:
                logger.exception("合并 DataFrame 异常")
                df_list = []
                for key, df in zip(keys, df_list):
                    df['key'] = key
                    df_list.append(df)

                result_df = pd.concat(
                    df_list,
                ).reset_index()
                result_available_df = pd.concat(
                    [df[df['available']] for df in df_list],
                ).reset_index()

    if result_df is not None and result_df.shape[0] > 0:
        result_df.drop_duplicates(inplace=True)
        csv_file_path = get_output_file_path(
            f'result_{vt_symbol_str}_{date_2_str(date.today())}.csv', root_folder_name=root_folder_name)
        result_df.to_csv(csv_file_path, index=False, encoding='GBK')
        logger.info("总计 %d 条测试记录被保存到 %s", result_df.shape[0], csv_file_path)
        csv_file_path = get_output_file_path(
            f'result_{vt_symbol_str}_{date_2_str(date.today())}.xlsx', root_folder_name=root_folder_name)
        # Writing to Excel with MultiIndex columns and no index ('index'=False) is not yet implemented.
        result_df.to_excel(csv_file_path)

    if result_available_df is not None and result_available_df.shape[0] > 0:
        result_available_df.drop_duplicates(inplace=True)
        csv_file_path = get_output_file_path(
            f'available_result_{vt_symbol_str}_{date_2_str(date.today())}.csv', root_folder_name=root_folder_name)
        result_available_df.to_csv(csv_file_path, index=False, encoding='GBK')
        csv_file_path = get_output_file_path(
            f'available_result_{vt_symbol_str}_{date_2_str(date.today())}.xlsx', root_folder_name=root_folder_name)
        # Writing to Excel with MultiIndex columns and no index ('index'=False) is not yet implemented.
        result_available_df.to_excel(csv_file_path)

    # enable_join_collector
    if trade_data_collector.is_alive():
        trade_data_collector.join_queue()
    if order_data_collector.is_alive():
        order_data_collector.join_queue()

    return result_df
