"""
@author  : MG
@Time    : 2020/10/9 12:00
@File    : __init__.py.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import enum
import time
from datetime import datetime
from threading import Thread


def check_datetime_trade_available(dt: datetime) -> bool:
    """判断可发送交易请求的时间段（中午11:30以后交易）"""
    hour = dt.hour
    minute = dt.minute
    is_available = 0 <= hour < 3 or 9 <= hour <= 10 or (11 == hour and minute < 30) or 13 <= hour < 15 or (21 <= hour)
    return is_available


def check_datetime_available(dt: datetime) -> bool:
    hour = dt.hour
    is_available = 0 <= hour < 3 or 9 <= hour < 15 or 21 <= hour
    return is_available


class CrossLimitMethod(enum.IntEnum):
    open_price = 0
    mid_price = 1
    worst_price = 2


class CleanupOrcaServerProcessIntermittent(Thread):

    def __init__(self, sleep_time=5, interval=1800):
        super().__init__()
        self.is_running = True
        self.interval = interval
        self.sleep_time = sleep_time
        self.sleep_count = interval // sleep_time

    def run(self) -> None:
        from plotly.io._orca import cleanup
        count = 0
        while self.is_running:
            time.sleep(self.sleep_time)
            count += 1
            if count % self.sleep_count == 0 or not self.is_running:
                cleanup()
                count = 0


DEFAULT_STATIC_ITEMS = [
    "available", "info_ratio",
    "max_new_higher_duration", "daily_trade_count", "return_drawdown_ratio",
    "image_file_url",
    "strategy_class_name", "id_name", "symbols", "cross_limit_method", "backtest_status",
]

STOP_OPENING_POS_PARAM = "stop_opening_pos"
ENABLE_COLLECT_DATA_PARAM = "enable_collect_data"


class StopOpeningPos(enum.IntEnum):
    open_available = 0
    stop_opening_and_log = 1
    stop_opening_and_nolog = 2
