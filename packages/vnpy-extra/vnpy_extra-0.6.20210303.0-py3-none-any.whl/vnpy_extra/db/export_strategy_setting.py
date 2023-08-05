#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/2/1 9:32
@File    : export_strategy_setting.py
@contact : mmmaaaggg@163.com
@desc    : 用于导出 策略设置 生成 json 文件，该文件用于覆盖
.vntrader\cta_strategy_setting.json
.vntrader\portfolio_strategy_setting.json
文件
"""
import json
import os
from collections import OrderedDict
from datetime import date
from typing import List

from ibats_utils.mess import date_2_str

from vnpy_extra.db.orm import StrategyBacktestStats, StrategyBacktestStatusEnum


def generate_strategy_setting_file():
    stats_list: List[StrategyBacktestStats] = StrategyBacktestStats.get_by_status(
        StrategyBacktestStatusEnum.CompareTradeData.value)
    cta_dic = OrderedDict()
    portfolio_dic = OrderedDict()
    for stats in stats_list:
        symbols = stats.symbols_info.symbols
        vt_symbols = symbols.split('_')
        if len(vt_symbols) == 1:
            cta_dic[stats.short_name] = dic = OrderedDict()
            dic["class_name"] = stats.stg_info.strategy_class_name
            dic["vt_symbol"] = vt_symbols[0]
            dic["setting"] = settings = OrderedDict()
            settings['class_name'] = stats.stg_info.strategy_class_name
            for k, v in stats.strategy_settings.items():
                settings[k] = v
        else:
            portfolio_dic[stats.short_name] = dic = OrderedDict()
            dic["class_name"] = stats.stg_info.strategy_class_name
            dic["vt_symbols"] = vt_symbols
            dic["setting"] = stats.strategy_settings

    folder_path = os.path.join("output", "strategy_settings", date_2_str(date.today()))
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, "cta_strategy_setting.json")
    with open(file_path, 'w') as f:
        json.dump(cta_dic, f, indent=4)

    file_path = os.path.join(folder_path, "portfolio_strategy_setting.json")
    with open(file_path, 'w') as f:
        json.dump(portfolio_dic, f, indent=4)

    return file_path


if __name__ == "__main__":
    pass
