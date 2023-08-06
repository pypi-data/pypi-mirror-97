"""
@author  : MG
@Time    : 2020/11/12 10:04
@File    : constants.py
@contact : mmmaaaggg@163.com
@desc    : 用于保存部分公共常数
"""
import collections
import typing
from datetime import time


def get_symbol_size_dic():
    import json
    from vnpy_extra.db.utils import execute_sql
    from vnpy_extra.utils.enhancement import get_instrument_type, PATTERN_INSTRUMENT_TYPE_RESTRICT
    sql_str = "SELECT trade_code, contractmultiplier FROM md_integration.wind_future_info"
    symbol_size_dic = {
        get_instrument_type(trade_code, PATTERN_INSTRUMENT_TYPE_RESTRICT): contractmultiplier
        for trade_code, contractmultiplier in execute_sql(sql_str)
        if get_instrument_type(trade_code, PATTERN_INSTRUMENT_TYPE_RESTRICT) is not None
    }
    print(json.dumps(symbol_size_dic, indent=4))


def get_minute_count_dic():
    import json
    from vnpy_extra.db.orm import database
    import logging
    sql_str = """SELECT adj.instrument_type, Contract FROM md_integration.wind_future_continuous_adj adj
        inner join (select max(trade_date) trade_date_max, instrument_type 
        from md_integration.wind_future_continuous_adj group by instrument_type) t
        on adj.trade_date = t.trade_date_max
        and adj.instrument_type = t.instrument_type
    """
    sql_counter_str = """SELECT round(count(1)/COUNT(DISTINCT `trade_date`), -1)
        FROM md_integration.wind_future_min
        where wind_code = %s"""
    minute_count_dic = {}
    for instrument_type, symbol in database.execute_sql(sql_str):
        ret_val = database.execute_sql(sql_counter_str, [symbol]).fetchone()[0]
        if ret_val is not None:
            ret_val = int(ret_val)
            if ret_val > 0:
                minute_count_dic[instrument_type] = ret_val
            else:
                logging.warning("%s 结果为 0", symbol)
        else:
            logging.warning("%s 没有数据", symbol)

    print(json.dumps(minute_count_dic, indent=4))


def get_price_tick_dic():
    import json
    from vnpy_extra.db.utils import execute_sql
    from vnpy_extra.utils.enhancement import get_instrument_type, PATTERN_INSTRUMENT_TYPE_RESTRICT
    sql_str = "SELECT trade_code, mfprice FROM md_integration.wind_future_info"
    symbol_size_dic = {
        get_instrument_type(trade_code, PATTERN_INSTRUMENT_TYPE_RESTRICT): price_tick
        for trade_code, price_tick in execute_sql(sql_str)
        if get_instrument_type(trade_code, PATTERN_INSTRUMENT_TYPE_RESTRICT) is not None
    }
    print(json.dumps(symbol_size_dic, indent=4))


# 记录每个合约乘数的dict
SYMBOL_SIZE_DIC = collections.defaultdict(
    lambda: 10, {
        "CU": 5.0,
        "ZC": 100.0,
        "PP": 5.0,
        "V": 5.0,
        "C": 10.0,
        "SN": 1.0,
        "AL": 5.0,
        "P": 10.0,
        "IC": 200.0,
        "ZN": 5.0,
        "L": 5.0,
        "RB": 10.0,
        "M": 10.0,
        "T": 10000.0,
        "SR": 10.0,
        "CS": 10.0,
        "IH": 300.0,
        "CF": 5.0,
        "JM": 60.0,
        "TA": 5.0,
        "ME": 50.0,
        "RU": 10.0,
        "A": 10.0,
        "PB": 5.0,
        "B": 10.0,
        "OI": 10.0,
        "FG": 20.0,
        "JD": 10.0,
        "AU": 1000.0,
        "AG": 15.0,
        "RO": 5.0,
        "TF": 10000.0,
        "Y": 10.0,
        "TC": 200.0,
        "NI": 1.0,
        "BU": 10.0,
        "J": 100.0,
        "TS": 20000.0,
        "HC": 10.0,
        "SC": 1000.0,
        "IF": 300.0,
        "MA": 10.0,
        "RM": 10.0,
        "I": 100.0,
        "LU": 10.0,
        "RR": 10.0,
        "WR": 10.0,
        "FB": 500.0,
        "PM": 50.0,
        "EB": 5.0,
        "UR": 20.0,
        "SP": 10.0,
        "NR": 10.0,
        "SM": 5.0,
        "SS": 5.0,
        "JR": 20.0,
        "WH": 20.0,
        "CY": 5.0,
        "FU": 10.0,
        "PG": 20.0,
        "BB": 500.0,
        "RS": 10.0,
        "SA": 20.0,
        "CJ": 5.0,
        "PF": 5.0,
        "SF": 5.0,
        "BC": 5.0,
        "EG": 10.0,
        "RI": 20.0,
        "AP": 10.0,
        "LR": 20.0,
        "IM": 10.0,
        "ER": 10.0,
        "WS": 10.0,
        "WT": 10.0,
    })

# 记录每个合约每天分钟数的dict
SYMBOL_MINUTES_COUNT_DIC = collections.defaultdict(
    lambda: 350, {
        "CF": 370,
        "LU": 340,
        "ZN": 380,
        "UR": 230,
        "SN": 390,
        "T": 260,
        "Y": 340,
        "MA": 370,
        "I": 340,
        "JD": 230,
        "J": 340,
        "IH": 240,
        "FB": 230,
        "V": 340,
        "TF": 260,
        "PF": 340,
        "SF": 230,
        "CY": 370,
        "B": 340,
        "PM": 230,
        "P": 340,
        "TS": 260,
        "CU": 390,
        "RI": 230,
        "EB": 340,
        "AP": 230,
        "HC": 340,
        "AG": 460,
        "OI": 370,
        "JR": 230,
        "ZC": 370,
        "CJ": 230,
        "SR": 370,
        "RS": 230,
        "RR": 340,
        "PB": 380,
        "SP": 340,
        "SM": 230,
        "IF": 240,
        "NI": 390,
        "RU": 340,
        "CS": 340,
        "AL": 390,
        "SA": 340,
        "M": 340,
        "L": 340,
        "FG": 370,
        "PG": 330,
        "SS": 390,
        "BU": 340,
        "RM": 370,
        "SC": 460,
        "WR": 230,
        "IC": 240,
        "A": 340,
        "AU": 460,
        "FU": 340,
        "C": 340,
        "NR": 340,
        "PP": 340,
        "BB": 230,
        "RB": 340,
        "JM": 340,
        "WH": 230,
        "EG": 340,
        "LR": 230,
        "BC": 380
    })

_INSTRUMENT_TRADE_TIME_PAIR_DIC = collections.defaultdict(
    lambda: ["9:00:00", "15:00:00"], {
        "IF": ["9:30:00", "15:00:00"],
        "IC": ["9:30:00", "15:00:00"],
        "IH": ["9:30:00", "15:00:00"],
        "T": ["9:30:00", "15:15:00"],
        "AU": ["21:00:00", "2:30:00"],
        "AG": ["21:00:00", "2:30:00"],
        "CU": ["21:00:00", "1:00:00"],
        "AL": ["21:00:00", "1:00:00"],
        "ZN": ["21:00:00", "1:00:00"],
        "PB": ["21:00:00", "1:00:00"],
        "NI": ["21:00:00", "1:00:00"],
        "SN": ["21:00:00", "1:00:00"],
        "RB": ["21:00:00", "23:00:00"],
        "I": ["21:00:00", "23:00:00"],
        "HC": ["21:00:00", "23:00:00"],
        "SS": ["21:00:00", "1:00:00"],
        "SF": ["9:00:00", "15:00:00"],
        "SM": ["9:00:00", "15:00:00"],
        "JM": ["21:00:00", "23:00:00"],
        "J": ["21:00:00", "23:00:00"],
        "ZC": ["21:00:00", "23:00:00"],
        "FG": ["21:00:00", "23:00:00"],
        "SP": ["21:00:00", "23:00:00"],
        "FU": ["21:00:00", "23:00:00"],
        "LU": ["21:00:00", "23:00:00"],
        "SC": ["21:00:00", "2:30:00"],
        "BU": ["21:00:00", "23:00:00"],
        "PG": ["21:00:00", "23:00:00"],
        "RU": ["21:00:00", "23:00:00"],
        "NR": ["21:00:00", "23:00:00"],
        "L": ["21:00:00", "23:00:00"],
        "TA": ["21:00:00", "23:00:00"],
        "V": ["21:00:00", "23:00:00"],
        "EG": ["21:00:00", "23:00:00"],
        "MA": ["21:00:00", "23:00:00"],
        "PP": ["21:00:00", "23:00:00"],
        "EB": ["21:00:00", "23:00:00"],
        "UR": ["9:00:00", "15:00:00"],
        "SA": ["21:00:00", "23:00:00"],
        "C": ["21:00:00", "23:00:00"],
        "A": ["21:00:00", "23:00:00"],
        "CS": ["21:00:00", "23:00:00"],
        "B": ["21:00:00", "23:00:00"],
        "M": ["21:00:00", "23:00:00"],
        "Y": ["21:00:00", "23:00:00"],
        "RM": ["21:00:00", "23:00:00"],
        "OI": ["21:00:00", "23:00:00"],
        "P": ["21:00:00", "23:00:00"],
        "CF": ["21:00:00", "23:00:00"],
        "SR": ["21:00:00", "23:00:00"],
        "JD": ["9:00:00", "15:00:00"],
        "AP": ["9:00:00", "15:00:00"],
        "CJ": ["9:00:00", "15:00:00"]
    })
INSTRUMENT_TRADE_TIME_PAIR_DIC: typing.Dict[str, typing.Tuple[time, time]] = {
    key: (
        time(*[int(_) for _ in values[0].split(':')]),
        time(*[int(_) for _ in values[1].split(':')]),
    )
    for key, values in _INSTRUMENT_TRADE_TIME_PAIR_DIC.items()}

INSTRUMENT_PRICE_TICK_DIC = collections.defaultdict(
    lambda: 1, {
        "CU": 10.0,
        "ZC": 0.2,
        "PP": 1.0,
        "V": 5.0,
        "C": 1.0,
        "SN": 10.0,
        "AL": 5.0,
        "P": 2.0,
        "IC": 0.2,
        "ZN": 5.0,
        "L": 5.0,
        "RB": 1.0,
        "M": 1.0,
        "T": 0.005,
        "SR": 1.0,
        "CS": 1.0,
        "IH": 0.2,
        "CF": 5.0,
        "JM": 0.5,
        "TA": 2.0,
        "ME": 1.0,
        "RU": 5.0,
        "A": 1.0,
        "PB": 5.0,
        "B": 1.0,
        "OI": 1.0,
        "FG": 1.0,
        "JD": 1.0,
        "AU": 0.02,
        "AG": 1.0,
        "RO": 2.0,
        "TF": 0.005,
        "Y": 2.0,
        "TC": 0.2,
        "NI": 10.0,
        "BU": 2.0,
        "J": 0.5,
        "TS": 0.005,
        "HC": 1.0,
        "SC": 0.1,
        "IF": 0.2,
        "MA": 1.0,
        "RM": 1.0,
        "I": 0.5,
        "LU": 1.0,
        "RR": 1.0,
        "WR": 1.0,
        "FB": 0.5,
        "PM": 1.0,
        "EB": 1.0,
        "UR": 1.0,
        "SP": 2.0,
        "NR": 5.0,
        "SM": 2.0,
        "SS": 5.0,
        "JR": 1.0,
        "WH": 1.0,
        "CY": 5.0,
        "FU": 1.0,
        "PG": 1.0,
        "BB": 0.05,
        "RS": 1.0,
        "SA": 1.0,
        "CJ": 5.0,
        "PF": 2.0,
        "SF": 2.0,
        "BC": 10.0,
        "EG": 1.0,
        "RI": 1.0,
        "AP": 1.0,
        "LR": 1.0,
        "IM": 0.2,
        "ER": 1.0,
        "WS": 1.0,
        "WT": 1.0
    })


def get_rate_dic(file_path, bigger=1.0) -> dict:
    import pandas as pd
    import json
    df = pd.read_excel(file_path, skiprows=[0])
    rate_dic = df.set_index([' 合约代码'])[' 开仓手续费(按金额)'].to_dict()
    rate_dic = {k.upper(): v * bigger for k, v in rate_dic.items() if k[-1] not in '1234567890'}
    print(json.dumps(rate_dic, indent=4))
    return rate_dic


def _test_():
    file_path = r"e:\工作\交易\当前投资者合约手续费率_2021-01-13.xlsx"
    get_rate_dic(file_path)


INSTRUMENT_RATE_DIC = collections.defaultdict(
    lambda: 6e-05, {
        'IC': 2.4230000000000003e-05,
        'IF': 2.4230000000000003e-05,
        'IH': 2.4230000000000003e-05,
        'T': 6e-05,
        'TF': 6e-05,
        'TS': 6e-05,
        'AP': 6e-05,
        'CF': 6e-05,
        'CJ': 6e-05,
        'CY': 6e-05,
        'FG': 6e-05,
        'JR': 6e-05,
        'LR': 6e-05,
        'MA': 6e-05,
        'OI': 6e-05,
        'PF': 6e-05,
        'PM': 6e-05,
        'RI': 6e-05,
        'RM': 6e-05,
        'RS': 6e-05,
        'SA': 6e-05,
        'SF': 6e-05,
        'SM': 6e-05,
        'SR': 6e-05,
        'TA': 6e-05,
        'UR': 6e-05,
        'WH': 6e-05,
        'ZC': 6e-05,
        'A': 6e-05,
        'B': 4e-05,
        'BB': 1.7e-4,
        'C': 6e-05,
        'CS': 6e-05,
        'EB': 6e-05,
        'EG': 6e-05,
        'FB': 1.7e-4,
        'I': 7.974257236443843e-4,
        'J': 9.409269028085699e-5,
        'JD': 0.00015758000000000002,
        'JM': 4.01e-04,
        'L': 6e-05,
        'LH': 0.00021008,
        'M': 6e-05,
        'P': 6e-05,
        'PG': 6e-05,
        'PP': 6e-05,
        'RR': 6e-05,
        'V': 6e-05,
        'Y': 6e-05,
        'BC': 1.058e-05,
        'LU': 6e-05,
        'NR': 6e-05,
        'SC': 6e-05,
        'SC_TAS': 6e-05,
        'AG': 1.058e-05,
        'AL': 6e-05,
        'AU': 6e-05,
        'BU': 1.7e-4,
        'CU': 5.258e-05,
        'FU': 1.058e-05,
        'HC': 1.785797218987349e-4,
        'NI': 6e-05,
        'PB': 4.2080000000000006e-05,
        'RB': 1.637651848101266e-4,
        'RU': 6e-05,
        'SN': 6e-05,
        'SP': 5.258e-05,
        'SS': 6e-05,
        'WR': 4.2080000000000006e-05,
        'ZN': 6e-05
    })

if __name__ == '__main__':
    _test_()
