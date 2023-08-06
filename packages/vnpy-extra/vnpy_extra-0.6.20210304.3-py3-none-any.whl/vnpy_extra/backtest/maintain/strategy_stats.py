"""
@author  : MG
@Time    : 2021/1/19 16:16
@File    : strategy_stats.py
@contact : mmmaaaggg@163.com
@desc    : 用于更新策略统计表的状态
"""
import logging
import os

import pandas as pd

from vnpy_extra.db.orm import StrategyBacktestStats

logger = logging.getLogger()


def update_strategy_stats_by_df(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == '.csv':
        df = pd.read_csv(file_path,
                         encoding="GBK"
                         # encoding="utf-8-sig"  # 旧版本的数据是 utf-8 编码
                         )
    else:
        df = pd.read_excel(file_path)

    if "short_name" not in df:
        df['short_name'] = ''

    if "shown_name" not in df:
        df['shown_name'] = ''

    df = df[['strategy_class_name', 'id_name', 'symbols', 'cross_limit_method', 'backtest_status',
             'short_name', 'shown_name']]
    # 历史版本有个bug，这里修正一下。以后可以删除这段代码
    df['strategy_class_name'] = df['strategy_class_name'].apply(lambda x: x.lstrip("('").rstrip("',)"))
    strategy_class_name = df['strategy_class_name'].iloc[0]
    update_count = StrategyBacktestStats.update_backtest_status([
        {k: None if isinstance(v, str) and v == '' else v for k, v in record.items()}
        for record in df.to_dict('record')])
    logger.info("%s %d 条记录被更新", strategy_class_name, update_count)
    return update_count


def run_update_strategy_stats_by_df():
    folder_path = r'd:\github\quant_vnpy\strategies\tb_transfer\p169_moving_average_cross_over\output\bulk_RB9999.SHFE'
    file_name = 'RB9999.SHFE_0_open_price_2021-03-02.csv'
    file_path = os.path.join(folder_path, file_name)
    update_strategy_stats_by_df(file_path)


if __name__ == "__main__":
    run_update_strategy_stats_by_df()
