"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import json
import threading
from datetime import datetime
from typing import List, Dict, Optional

from ibats_utils.mess import datetime_2_str
from vnpy.app.portfolio_strategy import StrategyTemplate as StrategyTemplateBase
from vnpy.trader.constant import Direction, Offset
from vnpy.trader.object import BarData, TickData, TradeData

from vnpy_extra.backtest import STOP_OPENING_POS_PARAM, ENABLE_COLLECT_DATA_PARAM, StopOpeningPos, \
    check_datetime_trade_available
from vnpy_extra.backtest import check_datetime_available
from vnpy_extra.config import logging
from vnpy_extra.db.orm import AccountStrategyStatusEnum
from vnpy_extra.report.collector import trade_data_collector, order_data_collector, latest_price_collector
from vnpy_extra.report.monitor import AccountStrategyStatusMonitor
from vnpy_extra.utils.enhancement import BarGenerator


class StrategyTemplate(StrategyTemplateBase):
    # 该标识位默认为0（关闭状态）。为1时开启，程序一旦平仓后则停止后续交易。该标识位用于在切换合约时使用
    stop_opening_pos = StopOpeningPos.open_available.value

    def __init__(self, strategy_engine, strategy_name, vt_symbols, setting):
        super().__init__(strategy_engine, strategy_name, vt_symbols, setting)
        # setting 不包含 stop_opening_pos key
        self.setting = {k: v for k, v in setting.items() if k in self.parameters}
        self.parameters.append(STOP_OPENING_POS_PARAM)  # 增加 stop_opening_pos 用于合约切换是关闭当前线程
        self.logger = logging.getLogger(f'strategies.portfolio.{strategy_name}')
        # 写日志
        self.logger.info(f"{strategy_name} on {vt_symbols} setting=\n{json.dumps(setting, indent=4)}")
        # 仅用于 on_order 函数记录上一个 order 使用，解决vnpy框架重复发送order的问题
        self._last_order = {}
        self.received_trade_list = []  # 记录所有成交数据
        self.current_bars: Optional[Dict[str, BarData]] = None
        self.bar_count = 0
        # 是否实盘环境
        self._is_realtime_mode = self.strategy_name is not None and self.strategy_name != self.__class__.__name__
        self._strategy_status = AccountStrategyStatusEnum.Created
        # 是否收集申请单以及交易单记录
        self.enable_collect_data = ENABLE_COLLECT_DATA_PARAM in setting and setting[ENABLE_COLLECT_DATA_PARAM]
        self._strategy_status_monitor: Optional[AccountStrategyStatusMonitor] = None
        self._lock: Optional[threading.Lock] = None

        # 最近一个tick的时间
        self.last_tick_time: Optional[datetime] = None
        # 最近一次下单的时间
        self.last_order_dt: Dict[str, datetime] = {}
        # 最近一条提示信息
        self._last_msg = ''

        def on_bar(bar: BarData):
            """"""
            pass

        self.bgs: Dict[str, BarGenerator] = {}
        for vt_symbols in self.vt_symbols:
            self.bgs[vt_symbols] = BarGenerator(on_bar)

    def set_is_realtime_mode(self, is_realtime_mode):
        self._is_realtime_mode = is_realtime_mode

    def get_id_name(self):
        return '_'.join([str(self.setting[key]) for key in self.parameters
                         if key in self.setting and key != STOP_OPENING_POS_PARAM])

    def _set_strategy_status(self, status: AccountStrategyStatusEnum):
        if not self._is_realtime_mode:
            # 仅针对实时交易是使用
            return
        if self._strategy_status == status:
            return

        if status == AccountStrategyStatusEnum.RunPending and self._strategy_status not in (
                AccountStrategyStatusEnum.Created, AccountStrategyStatusEnum.Running
        ):
            # AccountStrategyStatusEnum.RunPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_start 先把状态调整过来
                self._strategy_status = status
                self.write_log(f"策略 {self.strategy_name} {self.vt_symbols} 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程启动")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_start()

        elif status == AccountStrategyStatusEnum.StopPending and self._strategy_status == AccountStrategyStatusEnum.Running:
            # AccountStrategyStatusEnum.StopPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_stop 先把状态调整过来
                self._strategy_status = status
                self.write_log(f"策略 {self.strategy_name} {self.vt_symbols} 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程停止")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_stop()
        else:
            self.write_log(f"策略 {self.strategy_name} {self.vt_symbols} 状态 "
                           f"{self._strategy_status.name} -> {status.name}")
            self._strategy_status = status

    def _get_strategy_status(self) -> AccountStrategyStatusEnum:
        return self._strategy_status

    def on_init(self) -> None:
        super().on_init()
        self.bar_count = 0
        if self._is_realtime_mode:
            self._set_strategy_status(AccountStrategyStatusEnum.Initialized)

        if self._is_realtime_mode and self._strategy_status_monitor is None:
            # 该语句一定不能放在 __init__ 中
            # 因为 strategy_name 在回测阶段模块中，在 __init__ 后可能会被重写赋值
            self._strategy_status_monitor = AccountStrategyStatusMonitor(
                self.strategy_name,
                self._get_strategy_status,
                self._set_strategy_status,
                self.vt_symbols,
                self.setting
            )
            self._lock = self._strategy_status_monitor.lock

        if self._strategy_status_monitor is not None and not self._strategy_status_monitor.is_alive():
            self._strategy_status_monitor.start()

        self.enable_collect_data |= self._is_realtime_mode
        if self.enable_collect_data:
            trade_data_collector.queue_timeout = 90 if self._is_realtime_mode else 1
            order_data_collector.queue_timeout = 90 if self._is_realtime_mode else 1

    def on_start(self) -> None:
        super().on_start()
        if self._is_realtime_mode:
            self._set_strategy_status(AccountStrategyStatusEnum.Running)
        # 整理持仓信息
        if len(self.pos) == 0:
            self.write_log(f"策略启动，当前初始持仓：(无)")
        else:
            pos_str = '\t'.join([f"{k}: {v}" for k, v in self.pos.items()])
            self.write_log(f"策略启动，当前初始持仓：\n{pos_str}")

        self.put_event()

        # 初始化相关数据,可以在重启策略时清空历史订单对当前策略的影响.
        # 仅用于 on_order 函数记录上一个 order 使用，解决vnpy框架重复发送order的问题
        self._last_order = {}
        self.received_trade_list = []  # 记录所有成交数据
        # 最近一次下单的时间
        self.last_order_dt: Dict[str, datetime] = {}
        # if self._is_realtime_mode:
        #     start_strategy_position_monitor()

    def on_tick(self, tick: TickData) -> bool:
        """判断当前tick数据是否有效,如果无效数据直接返回 False,否则更新相应bar数据"""
        super().on_tick(tick)
        is_available = check_datetime_available(tick.datetime)
        if not is_available:
            return is_available

        if (
                self.last_tick_time
                and self.last_tick_time.minute != tick.datetime.minute
        ):
            bars = {}
            for vt_symbol, bg in self.bgs.items():
                bars[vt_symbol] = bg.generate()
            self.on_bars(bars)

        bg: BarGenerator = self.bgs[tick.vt_symbol]
        bg.update_tick(tick)
        latest_price_collector.put_nowait(tick)
        self.last_tick_time = tick.datetime.replace(tzinfo=None)
        return is_available

    def on_bars(self, bars: Dict[str, BarData]) -> None:
        super().on_bars(bars)
        self.current_bars: Dict[str, BarData] = bars
        self.bar_count += 1

    def send_order(self,
                   vt_symbol: str,
                   direction: Direction,
                   offset: Offset,
                   price: float,
                   volume: float,
                   lock: bool = False
                   ) -> List[str]:
        current_pos = int(self.get_pos(vt_symbol))
        order_datetime = self.current_bars[vt_symbol].datetime \
            if self.current_bars is not None and vt_symbol in self.current_bars else None
        ignore_order = False
        if price <= 0.0:
            log_level = 'error'
            msg = '【价格无效】'
            ignore_order = True
        elif order_datetime is not None and not check_datetime_trade_available(order_datetime):
            log_level = 'warning'
            msg = '【非交易时段】'
            ignore_order = True
        elif self.stop_opening_pos != StopOpeningPos.open_available.value and offset == Offset.OPEN:
            log_level = 'warning'
            msg = '【禁止开仓】'
            ignore_order = True
        else:
            log_level = 'debug'
            msg = ''

        if offset == Offset.OPEN:
            if self.stop_opening_pos != StopOpeningPos.stop_opening_and_nolog.value:
                self.write_log(
                    f"{vt_symbol:>11s} {direction.value} {offset.value:4s} {price:.1f} "
                    f"{current_pos:+d} {volume:+.0f} "
                    if order_datetime is None else
                    f"{datetime_2_str(order_datetime)} {vt_symbol} {direction.value} {offset.value:4s} {price:.1f} "
                    f"{current_pos:+d} {volume:+.0f}{msg}",
                    log_level
                )

            if self.stop_opening_pos != StopOpeningPos.open_available.value:
                self.write_log(f"当前策略 stop_opening_pos="
                               f"{self.stop_opening_pos}<{StopOpeningPos(self.stop_opening_pos).name}>，"
                               f"所有开仓操作将被屏蔽（用于主力合约切换,或关闭失效策略使用）", log_level)
                self.stop_opening_pos = StopOpeningPos.stop_opening_and_nolog.value

        else:
            self.write_log(
                f"{vt_symbol:>11s} {direction.value} {offset.value:4s} {price:.1f} "
                f"      {current_pos:+d} {-volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {vt_symbol} {direction.value} {offset.value:4s} {price:.1f} "
                f"      {current_pos:+d} {-volume:+.0f}{msg}",
                log_level
            )

        if order_datetime is None:
            order_datetime = datetime.now()

        if ignore_order:
            return []

        if vt_symbol in self._last_order:
            # 记录订单情况，跳过重复订单
            last_order = self._last_order[vt_symbol]
            if last_order['direction'] != direction.value \
                    or last_order['offset'] != offset.value \
                    or last_order['price'] != price \
                    or last_order['volume'] != volume:
                is_not_duplicate_order = True
            else:
                is_not_duplicate_order = False
        else:
            is_not_duplicate_order = True

        if is_not_duplicate_order:
            symbol, exchange = vt_symbol.split('.')
            order = {
                "datetime": order_datetime,
                "symbol": symbol,
                "exchange": exchange,
                "direction": direction.value,
                "offset": offset.value,
                "price": price,
                "volume": volume,
            }
            if self.enable_collect_data:
                order_data_collector.put_nowait(self.strategy_name, order)

            self._last_order[vt_symbol] = order

        self.last_order_dt[vt_symbol] = datetime.now()
        return super().send_order(vt_symbol, direction, offset, price, volume, lock)

    def on_stop(self):
        super().on_stop()
        if self._is_realtime_mode:
            self._set_strategy_status(AccountStrategyStatusEnum.Stopped)
        self.put_event()

    def update_trade(self, trade: TradeData):
        super().update_trade(trade)
        self.received_trade_list.append(trade)
        if self.enable_collect_data:
            trade_data_collector.put_nowait(self.strategy_name, trade)

    def write_log(self, msg: str, logger_method='info'):
        if self._last_msg == msg:
            return
        msg = f"{self.strategy_name} {msg}"
        super().write_log(msg)
        getattr(self.logger, logger_method)(msg)
        self._last_msg = msg


if __name__ == "__main__":
    pass
