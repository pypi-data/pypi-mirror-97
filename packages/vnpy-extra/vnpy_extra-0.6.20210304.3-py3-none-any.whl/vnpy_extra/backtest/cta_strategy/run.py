"""
@author  : MG
@Time    : 2020/10/9 12:01
@File    : run.py
@contact : mmmaaaggg@163.com
@desc    : 用于对策略进行回测
"""
from datetime import date
from enum import Enum
from multiprocessing import Lock
from typing import Type, Union, Optional, List, Callable, Tuple, Dict

from vnpy.app.cta_strategy import CtaTemplate
from vnpy.trader.constant import Interval

from vnpy_extra.backtest import CrossLimitMethod
from vnpy_extra.backtest.commons import run_backtest as run_backtest_pub, bulk_backtest as bulk_backtest_pub
from vnpy_extra.config import logging

logger = logging.getLogger()
HAS_PANDAS_EXCEPTION = False


def run_backtest(
        strategy_class: Type[CtaTemplate],
        engine_kwargs: dict,
        strategy_kwargs: Optional[dict] = None,
        root_folder_name=None,
        file_name_header="",
        engine=None,
        output_available_only=False,
        open_browser_4_charts=False,
        log_statistic_markdown=False,
        show_indexes=None,
        output_statistics=True,
        lock: Optional[Lock] = None,
        enable_collect_data=False,
        save_stats: Optional[bool] = None,
) -> dict:
    """
    本地化运行策略回测程序
    """
    return run_backtest_pub(
        strategy_class=strategy_class,
        multi_symbols=False,
        engine_kwargs=engine_kwargs,
        strategy_kwargs=strategy_kwargs,
        root_folder_name=root_folder_name,
        file_name_header=file_name_header,
        engine=engine,
        output_available_only=output_available_only,
        open_browser_4_charts=open_browser_4_charts,
        log_statistic_markdown=log_statistic_markdown,
        show_indexes=show_indexes,
        output_statistics=output_statistics,
        lock=lock,
        enable_collect_data=enable_collect_data,
        save_stats=save_stats,
    )


def _test_run_backtest():
    from strategies.double_ma_strategy import DoubleMA4Test
    engine_kwargs = dict(
        vt_symbol="RB9999.SHFE",
        interval=Interval.MINUTE,
        start=date(2017, 1, 1),
        rate=2.5e-4,
        slippage=1,
        size=10,
        pricetick=1,
        capital=100000,
        end=date(2022, 1, 1),
        cross_limit_method=CrossLimitMethod.open_price,
    )
    run_backtest(
        DoubleMA4Test,
        engine_kwargs=engine_kwargs,
        open_browser_4_charts=True
    )


def default_engine_param_key_func(**kwargs) -> Optional[Tuple[str]]:
    """
    将 engine_kwargs 生成一个默认的 key
    处于常用案例考虑，当前key不考虑起止时间、interval。
    如果需要进行key处理，需要单独写相应的函数
    """
    keys = ["vt_symbol", "rate", "slippage", "size", "pricetick", "cross_limit_method"]
    rets = []
    for key in keys:
        if key not in kwargs:
            continue
        value = kwargs[key]
        if isinstance(value, list):
            rets.append('_'.join([str(_) for _ in value]))
        elif isinstance(value, Enum):
            rets.append(str(value.name))
        else:
            rets.append(str(value))

    ret = tuple(rets)
    return ret


def bulk_backtest(
        strategy_cls: Type[CtaTemplate],
        engine_param_dic_list: Union[dict, List[dict]],
        strategy_param_dic_list: Union[Dict[str, list], List[Dict[str, list]]],
        available_backtest_params_check_func: Optional[Callable] = None,
        file_name_func: Optional[Callable] = None,
        statistic_items: Optional[list] = None,
        engine_param_key_func: Callable = default_engine_param_key_func,
        output_available_only: bool = True,
        open_browser_4_charts: bool = False,
        root_folder_name: Optional[str] = None,
        multi_process: int = 0,
        save_stats: Optional[bool] = None,
):
    """
    :param strategy_cls 策略类
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
    """
    return bulk_backtest_pub(
        strategy_cls=strategy_cls,
        multi_symbols=False,
        engine_param_dic_list=engine_param_dic_list,
        strategy_param_dic_list=strategy_param_dic_list,
        available_backtest_params_check_func=available_backtest_params_check_func,
        file_name_func=file_name_func,
        statistic_items=statistic_items,
        engine_param_key_func=engine_param_key_func,
        output_available_only=output_available_only,
        open_browser_4_charts=open_browser_4_charts,
        root_folder_name=root_folder_name,
        multi_process=multi_process,
        save_stats=save_stats,
    )


def _test_bulk_backtest_double_ma():
    from strategies.double_ma_strategy import DoubleMA4Test
    from vnpy_extra.config import set_log_level
    set_log_level('INFO')
    engine_param_dic_list_dic = {
        "RB9999.SHFE": [
            dict(
                vt_symbol="RB9999.SHFE",
                cross_limit_method=CrossLimitMethod.open_price,
            ),
            dict(
                vt_symbol="RB9999.SHFE",
                cross_limit_method=CrossLimitMethod.worst_price,
            ),
        ],
        "I9999.DCE": [
            dict(
                vt_symbol="I9999.DCE",
                cross_limit_method=CrossLimitMethod.open_price,
            ),
            dict(
                vt_symbol="I9999.DCE",
                cross_limit_method=CrossLimitMethod.worst_price,
            ),
        ],
        "HC9999.SHFE": [
            dict(
                vt_symbol="HC9999.SHFE",
                cross_limit_method=CrossLimitMethod.open_price,
            ),
            dict(
                vt_symbol="HC9999.SHFE",
                cross_limit_method=CrossLimitMethod.worst_price,
            ),
        ],
    }
    for vt_symbol, engine_param_dic_list in engine_param_dic_list_dic.items():
        result_df = bulk_backtest(
            DoubleMA4Test,
            engine_param_dic_list=engine_param_dic_list,
            strategy_param_dic_list=dict(
                fast_window=[20, 30],
            ),
            multi_process=0,
            root_folder_name=f'bulk_{vt_symbol}'
        )


def bulk_backtest_separated_by_symbol(
        strategy_cls: Type[CtaTemplate],
        vt_symbol_info_list: List[Union[
            Tuple[str, Union[float, int]],
            Tuple[str, Union[float, int], Union[float, int]]
        ]],
        cross_limit_methods: List[CrossLimitMethod],
        strategy_param_dic_list: List[Dict[str, List]],
        **kwargs
):
    for _ in vt_symbol_info_list:
        engine_param_dic = {}
        if len(_) == 1:
            vt_symbol = _[0]
            engine_param_dic['vt_symbol'] = vt_symbol
        elif len(_) == 2:
            vt_symbol, slippage = _
            engine_param_dic['vt_symbol'] = vt_symbol
            engine_param_dic['slippage'] = slippage
        elif len(_) == 3:
            vt_symbol, slippage, rate = _
            engine_param_dic['vt_symbol'] = vt_symbol
            engine_param_dic['slippage'] = slippage
            engine_param_dic['rate'] = rate
        else:
            raise ValueError(f"vt_symbol_info = {_} 无效")

        engine_param_dic_list = []
        for cross_limit_method in cross_limit_methods:
            engine_param_dic['cross_limit_method'] = cross_limit_method
            engine_param_dic_list.append(engine_param_dic.copy())

        bulk_backtest(
            strategy_cls=strategy_cls,
            engine_param_dic_list=engine_param_dic_list,
            strategy_param_dic_list=strategy_param_dic_list,
            root_folder_name=f'bulk_{vt_symbol}',
            **kwargs
        )


if __name__ == "__main__":
    _test_run_backtest()
    # _test_bulk_backtest_double_ma()
