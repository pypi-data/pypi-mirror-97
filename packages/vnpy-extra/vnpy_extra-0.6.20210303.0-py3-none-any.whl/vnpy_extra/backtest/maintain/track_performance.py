"""
@author  : MG
@Time    : 2021/1/20 9:31
@File    : track_performance.py
@contact : mmmaaaggg@163.com
@desc    : 用于对有效策略每日持续更新绩效表现
"""
from datetime import date, timedelta
from typing import List, Dict, Tuple, Iterator

from ibats_utils.mess import date_2_str, load_class
from vnpy.trader.constant import Interval

from vnpy_extra.backtest import CrossLimitMethod, ENABLE_COLLECT_DATA_PARAM
from vnpy_extra.backtest.commons import bulk_backtest_with_backtest_params_iter
from vnpy_extra.db.orm import StrategyBacktestStats, StrategyBacktestStatsArchive, StrategyBacktestStatusEnum


def get_backtest_params_iter_from_stats_list(
        stats_list: List[StrategyBacktestStats]
) -> Tuple[List[str], Iterator[Tuple[dict, list, StrategyBacktestStats]]]:
    """
    整理 StrategyBacktestStats 列表，重新设置回测日期区间，返回参数名称及 回测引擎及参数迭代器
    """
    param_name_list = None
    engine_kwargs_list, param_values_list = [], []
    for stats in stats_list:
        if stats.strategy_settings is None:
            stats.strategy_settings = {}

        if param_name_list is None:
            param_name_list = list(stats.strategy_settings.keys())

        engine_kwargs = stats.engine_kwargs
        # 整理回测日期区间
        engine_kwargs['end'] = date.today()
        engine_kwargs['start'] = date.today() - timedelta(days=365 * 3)
        engine_kwargs['cross_limit_method'] = CrossLimitMethod(stats.cross_limit_method)
        if 'interval' in engine_kwargs:
            engine_kwargs['interval'] = Interval(engine_kwargs['interval'])
        engine_kwargs_list.append(engine_kwargs)
        param_values_list.append([stats.strategy_settings[_] for _ in param_name_list])

    return param_name_list, zip(engine_kwargs_list, param_values_list, stats_list)


def backtest_all_strategies(symbols_only=None):
    """每日策略自动回测"""
    # @formatter:off
    # from strategies.trandition.period_resonance.period_resonance_configurable_2020_12_15.period_resonance_configurable import PeriodResonanceConfigurable  # noqa
    # from strategies.trandition.period_resonance.period_resonance_configurable_2020_12_15.period_m_vs_n_strategies import MacdRsiStrategy,MacdOnlyStrategy,MacdKdjStrategy,MacdMacdStrategy,RsiMacdStrategy,RsiOnlyStrategy,RsiRisStrategy,KdjOnlyStrategy  # NOQA
    # from strategies.spread.reversion_with_algo_20201216.reversion_with_algo_trading_strategy import PTReversionWithAlgoTradingStrategy  # NOQA
    # @formatter:on
    stats_list_dic: Dict[Tuple[str, str], List[StrategyBacktestStats]] = \
        StrategyBacktestStats.get_available_status_group_by_strategy(symbols_only)
    StrategyBacktestStatsArchive.archive(stats_list_dic)
    for (module_name, strategy_class_name, symbols), stats_list in stats_list_dic.items():
        strategy_cls = load_class(module_name, strategy_class_name)
        multi_symbols = len(symbols.split('_')) > 1
        if multi_symbols:
            from vnpy_extra.backtest.portfolio_strategy.run import default_engine_param_key_func
        else:
            from vnpy_extra.backtest.cta_strategy.run import default_engine_param_key_func

        param_name_list, backtest_params_iter = get_backtest_params_iter_from_stats_list(stats_list)
        bulk_backtest_with_backtest_params_iter(
            strategy_cls=strategy_cls,
            multi_symbols=multi_symbols,
            param_name_list=param_name_list,
            backtest_params_iter=backtest_params_iter,
            engine_param_key_func=default_engine_param_key_func,
            output_available_only=False,
            open_browser_4_charts=False,
            save_stats=True,
            enable_collect_data=True,
        )


if __name__ == "__main__":
    backtest_all_strategies()
