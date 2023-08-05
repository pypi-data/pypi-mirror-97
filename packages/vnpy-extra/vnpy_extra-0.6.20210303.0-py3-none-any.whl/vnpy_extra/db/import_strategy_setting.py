"""
@author  : MG
@Time    : 2021/1/28 13:29
@File    : import_strategy_setting.py
@contact : mmmaaaggg@163.com
@desc    : 用于将 cta_strategy_setting.json, portfolio_strategy_setting.json 文件加载
同时将策略配置信息整理，导入 strategy_backtest_stats 表中，供追踪分析使用。
该功能主要是为了将老版本的 setting 信息收集起来。
"""
import json
import logging
import os
from typing import Dict

from ibats_utils.mess import create_instance

from vnpy_extra.backtest import CrossLimitMethod, STOP_OPENING_POS_PARAM, ENABLE_COLLECT_DATA_PARAM
from vnpy_extra.backtest.cta_strategy.template import CtaTemplate
from vnpy_extra.backtest.portfolio_strategy.template import StrategyTemplate
from vnpy_extra.db.orm import StrategyBacktestStatusEnum, StrategyBacktestStats, StrategyInfo
from vnpy_extra.utils.enhancement import get_instrument_type

logger = logging.getLogger()


def change_main_contract(vt_symbol) -> str:
    """将某一个合约品种变为主力连续合约"""
    new_vt_symbol = get_instrument_type(vt_symbol) + '9999.' + vt_symbol.split('.')[-1]
    return new_vt_symbol


def import_from_json_file(file_path, cls_module_dic: Dict[str, str]):
    with open(file_path, 'r') as f:
        strategy_setting_dic: dict = json.load(f)

    settings = []
    data_count = len(strategy_setting_dic)
    for num, (strategy_name, json_settings) in enumerate(strategy_setting_dic.items(), start=1):
        is_cta = 'vt_symbol' in json_settings
        strategy_class_name = json_settings['class_name']
        module_name = cls_module_dic[strategy_class_name]
        strategy_settings = json_settings['setting']
        if STOP_OPENING_POS_PARAM in strategy_settings:
            del strategy_settings[STOP_OPENING_POS_PARAM]
        if ENABLE_COLLECT_DATA_PARAM in strategy_settings:
            del strategy_settings[ENABLE_COLLECT_DATA_PARAM]

        for is_9999 in [False, True]:
            # 增加对应主力合约的回测记录
            if is_cta:
                symbols = json_settings['vt_symbol']
                if is_9999:
                    # 将实际合约转换为 9999 主连合约
                    symbols = change_main_contract(symbols)

                if 'class_name' in strategy_settings:
                    del strategy_settings['class_name']
                stg_obj: CtaTemplate = create_instance(
                    module_name, strategy_class_name,
                    cta_engine=None, strategy_name=strategy_class_name, vt_symbol=symbols,
                    setting=strategy_settings.copy())
                engine_kwargs = {
                    "vt_symbol": symbols,
                    "cross_limit_method": CrossLimitMethod.open_price.value,
                }
            else:
                vt_symbols = json_settings['vt_symbols']
                if is_9999:
                    vt_symbols = [change_main_contract(_) for _ in vt_symbols]

                stg_obj: StrategyTemplate = create_instance(
                    module_name, strategy_class_name,
                    strategy_engine=None, strategy_name=strategy_class_name, vt_symbols=vt_symbols,
                    setting=strategy_settings.copy())
                engine_kwargs = {
                    "vt_symbols": vt_symbols,
                    "cross_limit_method": CrossLimitMethod.open_price.value,
                }
                symbols = '_'.join(vt_symbols)

            id_name = stg_obj.get_id_name()
            cross_limit_method = CrossLimitMethod.open_price.value
            if is_9999:
                # short_name, shown_name 存在 UNIQUE KEY 因此主连回测的情况下值为空
                short_name = None
                shown_name = None
                backtest_status = StrategyBacktestStatusEnum.QuasiOnline.value
            else:
                short_name = strategy_name
                shown_name = strategy_name
                backtest_status = StrategyBacktestStatusEnum.CompareTradeData.value

            logger.info(
                "%s %d/%d) %s[%s]%s '%s'<'%s'>",
                'cta' if is_cta else 'portfolio', num, data_count, strategy_class_name, symbols,
                '[主连]' if is_9999 else '', id_name, short_name,
            )
            settings.append(dict(
                strategy_class_name=strategy_class_name,
                module_name=module_name,
                symbols=symbols,
                strategy_settings=strategy_settings,
                id_name=id_name,
                cross_limit_method=cross_limit_method,
                short_name=short_name,
                shown_name=shown_name,
                backtest_status=backtest_status,
                engine_kwargs=engine_kwargs,
            ))

    StrategyBacktestStats.import_by_settings(settings)


def run_import(folder_path):
    file_names = ["cta_strategy_setting.json", "portfolio_strategy_setting.json"]
    # cta_module_name = 'strategies.trandition.period_resonance.period_resonance_configurable_2020_12_15.period_m_vs_n_strategies'
    # portfolio_module_name = 'strategies.spread.pair_trading_reversion_algo_trading.pair_trading_reversion_algo_trading_strategy'
    # cls_module_dic = {
    #     'RsiOnlyStrategy': cta_module_name,
    #     'KdjOnlyStrategy': cta_module_name,
    #     'MacdOnlyStrategy': cta_module_name,
    #     'MacdRsiStrategy': cta_module_name,
    #     'PairTradingReversionAlgoTradingStrategy': portfolio_module_name,
    # }
    cls_module_dic = StrategyInfo.get_cls_module_dic()
    for _ in file_names:
        file_path = os.path.join(folder_path, _)
        import_from_json_file(file_path, cls_module_dic=cls_module_dic)


def test_run_import():
    folder_path = r"d:\TradeTools\vnpy\jianxin_11859077\.vntrader"
    run_import(folder_path)


if __name__ == "__main__":
    test_run_import()
