"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import json
import threading
import time
from collections import defaultdict
from datetime import datetime
from typing import Optional, Dict, List, Tuple

import numpy as np
from ibats_utils.mess import datetime_2_str
from vnpy.app.cta_strategy import CtaTemplate as CtaTemplateBase, TargetPosTemplate as TargetPosTemplateBase
from vnpy.trader.constant import Offset, Direction
from vnpy.trader.object import OrderData, BarData, TickData, TradeData, Status

from vnpy_extra.backtest import STOP_OPENING_POS_PARAM, ENABLE_COLLECT_DATA_PARAM, check_datetime_available, \
    StopOpeningPos, check_datetime_trade_available
from vnpy_extra.config import logging
from vnpy_extra.constants import INSTRUMENT_PRICE_TICK_DIC
from vnpy_extra.db.orm import AccountStrategyStatusEnum
from vnpy_extra.report.collector import trade_data_collector, order_data_collector, latest_price_collector
from vnpy_extra.report.monitor import AccountStrategyStatusMonitor
from vnpy_extra.utils.enhancement import BarGenerator, get_instrument_type


class CtaTemplate(CtaTemplateBase):
    # 该标识位默认为0（关闭状态）。为1时开启，程序一旦平仓后则停止后续交易。该标识位用于在切换合约时使用
    stop_opening_pos = StopOpeningPos.open_available.value

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        # setting 不包含 stop_opening_pos key
        self.setting = {k: v for k, v in setting.items() if k in self.parameters}
        self.parameters.append(STOP_OPENING_POS_PARAM)  # 增加 stop_opening_pos 用于合约切换是关闭当前线程
        self.logger = logging.getLogger(f'strategies.cta.{strategy_name}')
        # 写日志
        self.logger.info(f"{strategy_name} on {vt_symbol} setting=\n{json.dumps(setting, indent=4)}")
        # 基于假设：相同 direction, offset 的操作不会短期内连续发生，
        # 因此，对每一类交易单独记录订单的发送时间，避免出现时间记录混淆的问题
        self.send_and_on_order_dt_dic: Dict[
            Tuple[Direction, Offset],
            List[Optional[datetime], Optional[datetime], Optional[Status]]] = defaultdict(lambda: [None, None, None])
        # 记录所有订单数据
        self.send_order_dic: Dict[str, OrderData] = {}
        self.send_order_dic_lock = threading.Lock()
        # 仅用于 on_order 函数记录上一个 order 使用，解决vnpy框架重复发送order的问题
        self._last_order: Optional[OrderData] = None
        self._trades = []  # 记录所有成交数据
        self.current_bar: Optional[BarData] = None
        self.bar_count = 0
        self.bg = BarGenerator(self.on_bar)
        # 是否实盘环境
        self._is_realtime_mode = self.strategy_name is not None and self.strategy_name != self.__class__.__name__
        self._strategy_status = AccountStrategyStatusEnum.Created
        # 最近一个tick的时间
        self.last_tick_time: Optional[datetime] = None
        # 最近一次接受到订单回报的时间，被 send_and_on_order_dt_dic 替代
        # self.last_order_dt: Optional[datetime] = None
        # 最近一次发送订单的时间，被 send_and_on_order_dt_dic 替代
        # self.last_send_order_dt: Optional[datetime] = None
        # 是否收集申请单以及交易单记录
        self.enable_collect_data = ENABLE_COLLECT_DATA_PARAM in setting and setting[ENABLE_COLLECT_DATA_PARAM]
        self._strategy_status_monitor: Optional[AccountStrategyStatusMonitor] = None
        self._lock: Optional[threading.Lock] = None
        # 最近一条提示信息
        self._last_msg = ''
        # 最近一个 tick
        self.last_tick: Optional[TickData] = None
        self.latest_reject_response_order: Optional[OrderData] = None

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
                self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程启动")
                self._strategy_status = status
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_start()

        elif status == AccountStrategyStatusEnum.StopPending \
                and self._strategy_status == AccountStrategyStatusEnum.Running:
            # AccountStrategyStatusEnum.StopPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_stop 先把状态调整过来
                self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程停止")
                self._strategy_status = status
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_stop()
        else:
            self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 "
                           f"{self._strategy_status.name} -> {status.name}")
            self._strategy_status = status

    def _get_strategy_status(self) -> AccountStrategyStatusEnum:
        return self._strategy_status

    def on_init(self) -> None:
        super().on_init()
        self.bar_count = 0
        self._set_strategy_status(AccountStrategyStatusEnum.Initialized)
        if self._is_realtime_mode and self._strategy_status_monitor is None:
            # 该语句一定不能放在 __init__ 中
            # 因为 strategy_name 在回测阶段模块中，在 __init__ 后可能会被重写赋值
            self._strategy_status_monitor = AccountStrategyStatusMonitor(
                self.strategy_name,
                self._get_strategy_status,
                self._set_strategy_status,
                self.vt_symbol,
                self.setting,
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
        self._set_strategy_status(AccountStrategyStatusEnum.Running)
        # 整理持仓信息
        self.write_log(f"策略启动，当前初始持仓： {self.vt_symbol} {self.pos}")
        self.put_event()
        # 初始化相关数据,可以在重启策略时清空历史订单对当前策略的影响.
        self.send_and_on_order_dt_dic: Dict[
            Tuple[Direction, Offset],
            List[Optional[datetime], Optional[datetime], Optional[Status]]] = defaultdict(lambda: [None, None, None])
        # 记录所有订单数据
        self.send_order_dic: Dict[str, OrderData] = {}
        # 仅用于 on_order 函数记录上一个 order 使用，解决vnpy框架重复发送order的问题
        self._last_order: Optional[OrderData] = None
        self._trades = []  # 记录所有成交数据

        # if self._is_realtime_mode:
        #     start_strategy_position_monitor()

    def on_tick(self, tick: TickData) -> bool:
        """判断当前tick数据是否有效,如果无效数据直接返回 False,否则更新相应bar数据"""
        super().on_tick(tick)
        self.last_tick = tick
        is_available = check_datetime_available(tick.datetime)
        if not is_available:
            return is_available

        # 激活分钟线 on_bar
        self.bg.update_tick(tick)
        latest_price_collector.put_nowait(tick)
        self.last_tick_time = tick.datetime.replace(tzinfo=None)
        return is_available

    def on_bar(self, bar: BarData):
        super().on_bar(bar)
        self.current_bar: BarData = bar
        self.bar_count += 1

    def cancel_order(self, vt_orderid):
        if vt_orderid in self.send_order_dic:
            order = self.send_order_dic[vt_orderid]
            key = (order.direction,
                   Offset.CLOSE if order.offset in (Offset.CLOSE, Offset.CLOSETODAY, Offset.CLOSEYESTERDAY)
                   else order.offset)
            with self.send_order_dic_lock:
                self.send_and_on_order_dt_dic[key][0] = datetime.now()
        else:
            self.write_log(
                f"订单{vt_orderid} 不在 send_order_dic 列表中。send_order_dic.keys={self.send_order_dic.keys()}",
                'warning')

        super().cancel_order(vt_orderid)

    def send_order(
            self,
            direction: Direction,
            offset: Offset,
            price: float,
            volume: float,
            stop: bool = False,
            lock: bool = False
    ):
        vt_symbol = self.vt_symbol
        current_pos = int(self.pos)
        order_datetime = self.last_tick_time if self.last_tick_time is not None else None
        ignore_order = False
        log_level = 'debug'
        msg = ''
        if price <= 0.0:
            log_level = 'warning'
            if self.current_bar is not None and self.current_bar.close_price > 0:
                price = self.current_bar.close_price
                msg = '【价格无效】，使用上一根K线收盘价'
            elif self.last_tick is not None:
                # 使用被动价格
                price = self.last_tick.bid_price_1 if direction == Direction.LONG else self.last_tick.ask_price_1
                msg = f'【价格无效】，使用上一Tick{"买1价格" if direction == Direction.LONG else "卖1价格"}'
            else:
                msg = f'【价格无效】'
                log_level = 'error'
                ignore_order = True

        if order_datetime is not None and not check_datetime_trade_available(order_datetime):
            log_level = 'warning'
            msg += '【非交易时段】'
            ignore_order = True
        elif self.stop_opening_pos != StopOpeningPos.open_available.value and offset == Offset.OPEN:
            log_level = 'warning'
            msg += '【禁止开仓】'
            ignore_order = True
        elif self.latest_reject_response_order is not None:
            dt = self.latest_reject_response_order.datetime.replace(tzinfo=None)
            if abs(datetime.now() - dt).seconds <= 300 and \
                    self.latest_reject_response_order.offset == offset and \
                    self.latest_reject_response_order.direction == direction and \
                    self.latest_reject_response_order.price == price and \
                    self.latest_reject_response_order.volume == volume:
                log_level = 'warning'
                msg += '【与上一个被拒单相同】'
                ignore_order = True

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

        if ignore_order:
            return []

        key = (direction,
               Offset.CLOSE if offset in (Offset.CLOSE, Offset.CLOSETODAY, Offset.CLOSEYESTERDAY)
               else offset)
        with self.send_order_dic_lock:
            self.send_and_on_order_dt_dic[key][0] = datetime.now()

        return super().send_order(direction, offset, price, volume, stop, lock)

    def on_order(self, order: OrderData):
        super().on_order(order)
        # 2021-02-02 不能使用服务器时间，与本地时间作比较。
        # if order.datetime is not None:
        #     # 本地时间与服务器时间存在时差，将会导致判断异常。
        #     last_order_dt = order.datetime.replace(tzinfo=None)
        #     if self.last_order_dt is None or self.last_order_dt < last_order_dt:
        #         self.last_order_dt = last_order_dt
        #         self.write_log(f"last_order_dt={last_order_dt}")
        #     self.last_order_dt = datetime.now()
        if not self._is_realtime_mode:
            return
        key = (order.direction,
               Offset.CLOSE if order.offset in (Offset.CLOSE, Offset.CLOSETODAY, Offset.CLOSEYESTERDAY)
               else order.offset)
        with self.send_order_dic_lock:
            self.send_and_on_order_dt_dic[key][1] = datetime.now()
            self.send_and_on_order_dt_dic[key][2] = order.status
            self.send_order_dic[order.vt_orderid] = order

        self._last_order = order
        # self.write_log(f'on_order:   key={key}, send_dt, on_dt={self.send_and_on_order_dt_dic[key]}')
        current_pos = int(self.pos)
        order_datetime = order.datetime
        if order.status is None:
            order_status_str = ''
        else:
            order_status_str = order.status.value
            if order.status == Status.REJECTED:
                if order.datetime is None:
                    order.datetime = datetime.now()
                self.latest_reject_response_order = order

        if order.offset == Offset.OPEN:
            self.write_log(
                f"{'order.datetime=None' if order_datetime is None else datetime_2_str(order_datetime)} "
                f"{order.vt_symbol} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f} {current_pos:+d} {order.volume:+.0f} "
                f"{order_status_str}[{order.orderid}]"
            )

        else:
            self.write_log(
                f"{'order.datetime=None' if order_datetime is None else datetime_2_str(order_datetime)} "
                f"{order.vt_symbol} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f}       {current_pos:+d} {-order.volume:+.0f} "
                f"{order_status_str}[{order.orderid}]"
            )

        if self.enable_collect_data and (self._last_order is None or self._last_order.orderid != order.orderid):
            order_data_collector.put_nowait(self.strategy_name, order)

        # debug use only
        # with self.send_order_dic_lock:
        #     order_count = len(self.send_order_dic)
        #     for num, order in enumerate(self.send_order_dic.values(), start=1):
        #         if order.is_active():
        #             self.write_log(
        #                 f"{num}/{order_count}) on order: {order.orderid} {order.offset}
        #                 active={order.is_active()} dt={order.datetime}")

    def on_trade(self, trade: TradeData):
        super().on_trade(trade)
        self._trades.append(trade)
        if self.enable_collect_data:
            trade_data_collector.put_nowait(self.strategy_name, trade)

    def on_stop(self):
        super().on_stop()
        if self._is_realtime_mode:
            self._set_strategy_status(AccountStrategyStatusEnum.Stopped)
        self.put_event()

    def write_log(self, msg: str, logger_method='info'):
        if self._last_msg == msg:
            return
        msg = f"{self.strategy_name} {msg}"
        super().write_log(msg)
        getattr(self.logger, logger_method)(msg)
        self._last_msg = msg


class TargetPosAndPriceTemplate(CtaTemplate):
    # 目标仓位
    target_pos = 0
    # 目标价格
    target_price = 0
    # 建仓基数，建立空头或多头仓位的数量
    base_position = 1

    variables = ["target_pos", "target_price", "bar_count"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        # 算法交易线程
        self.algo_trading_thread = None
        self.algo_trading_running = True
        # 部分情况下服务器响应比较慢,测试中存在5秒钟才给返回状态的情况,因此这里将等待延迟加长到 20s
        self.send_order_wait_seconds = 20
        self.vt_symbol_price_tick = INSTRUMENT_PRICE_TICK_DIC[get_instrument_type(self.vt_symbol)]

    def on_start(self) -> None:
        super().on_start()
        if self._is_realtime_mode:
            # 实盘情况，执行异步算法交易
            self.algo_trading_running = True
            self.algo_trading_thread = threading.Thread(target=self._algo_trading_2_target_pos_thread, daemon=True)
            self.algo_trading_thread.start()

    def set_target_pos(self, target_pos, price=None):
        """设置目标持仓以及价格"""
        if price is None:
            self.target_price = self.current_bar.close_price
        else:
            self.target_price = np.round(price / self.vt_symbol_price_tick) * self.vt_symbol_price_tick

        self.target_pos = int(target_pos)
        if not self.trading:
            return

        if target_pos != self.pos:
            self.write_log(f"最新持仓目标 {target_pos} {self.target_price}", 'debug')

        if not self._is_realtime_mode:
            # 回测环境下走同步交易
            self.handle_pos_2_target()

    def handle_pos_2_target(self):
        """按目标价格及持仓进行处理(仅回测使用)"""
        if not self.trading:
            return

        self.cancel_all()
        current_pos = self.pos
        price = self.target_price
        volume = abs(self.target_pos - current_pos)
        if 0 <= self.target_pos < current_pos:
            # 减仓
            # self.write_log(f"平多 {current_pos} - > {self.target_pos}")
            self.sell(price, volume)
        elif self.target_pos < 0 < current_pos:
            # 多翻空
            # self.write_log(f"多翻空 {current_pos} - > {self.target_pos}")
            self.sell(price, abs(current_pos))
            self.short(price, abs(self.target_pos))  # 实盘情况会造成丢单现象
        elif self.target_pos < current_pos <= 0:
            volume = abs(self.target_pos - current_pos)
            # self.write_log(f"开空 {current_pos} - > {self.target_pos}")
            self.short(price, volume)
        elif current_pos < self.target_pos <= 0:
            # self.write_log(f"平空 {current_pos} - > {self.target_pos}")
            volume = abs(self.target_pos - current_pos)
            self.cover(price, volume)
        elif current_pos < 0 < self.target_pos:
            # self.write_log(f"空翻多 {current_pos} - > {self.target_pos}")
            self.cover(price, abs(current_pos))
            self.buy(price, abs(self.target_pos))  # 实盘情况会造成丢单现象
        elif 0 <= current_pos < self.target_pos:
            # self.write_log(f"开多 {current_pos} - > {self.target_pos}")
            volume = abs(self.target_pos - current_pos)
            self.buy(price, volume)

    def _algo_trading_2_target_pos_thread(self):
        self.write_log("开启算法交易")
        try:
            while self.algo_trading_running:
                time.sleep(0.5)
                if not self._can_do_algo_trading():
                    continue
                # self.write_log('可以执行算法交易')
                self.algo_trading_2_target_pos()
        except:
            self.write_log(f"{self.strategy_name} 算法交易异常", 'error')
            self.logger.exception("%s 算法交易异常", self.strategy_name)
        finally:
            self.write_log("关闭算法交易")

    def _can_do_algo_trading(self) -> bool:
        """检查是否可以执行算法交易"""
        if not self.trading:
            return False
        if self.last_tick_time is None:
            # 未开盘期间不进行算法交易
            return False
        now = datetime.now()
        # 多线程情况下可能存在 last_tick_time > now 的情况，因此用绝对值
        seconds_since_last_tick = abs(now - self.last_tick_time).seconds
        if seconds_since_last_tick > 5:
            return False
        if self.latest_reject_response_order is not None:
            dt = self.latest_reject_response_order.datetime.replace(tzinfo=None)
            if abs(datetime.now() - dt).seconds <= 60:
                return False

        # 检查所有类型的交易是否存在均处于有效状态。
        # 如果存在已经发报，但尚未得到服务器响应的情况则需要等待服务器响应后继续后续的操作
        with self.send_order_dic_lock:
            for num, ((direction, offset), (send_dt, on_dt, status)) in enumerate(
                    self.send_and_on_order_dt_dic.items(), start=1):
                if send_dt is None:
                    self.write_log(f"交易状态存在异常，send_dt={send_dt}，on_dt={on_dt}, status={status}", 'error')
                    return False
                if on_dt is None or send_dt > on_dt:
                    if abs(min(now, self.last_tick_time) - send_dt).seconds > self.send_order_wait_seconds:
                        # 发送订单 回应时间超时
                        # 无须取消订单，因为服务端没有确认收到订单
                        continue
                    else:
                        self.write_log(
                            f"订单已发送，但尚未得到回应，且尚未超时，继续等待，"
                            f"send_dt={send_dt}，on_dt={on_dt}, status={status}",
                            'warning'
                        )
                        return False
                elif status == Status.SUBMITTING:
                    # 2021-02-27
                    # 夜盘时,有时会发生服务器返回 submit 状态后,不再处理的清空.导致订单堵塞,无法进行后续交易.
                    # 以下代码针对此种清空进行了修补及相关数据的清理.
                    if abs(min(now, self.last_tick_time) - send_dt).seconds > self.send_order_wait_seconds * 2:
                        # 发送订单 回应时间严重超时 不等待回应,继续执行后面的交易逻辑
                        self.write_log(
                            f"订单已提交，且严重超时,取消订单后继续后面的交易逻辑."
                            f"send_dt={send_dt}，on_dt={on_dt}, status={status}, "
                            f"orderid={self._last_order.orderid if self._last_order is not None else '(None)'}",
                            'warning'
                        )
                        # 清理无效订单:包括非活跃,以及严重超时订单
                        for vt_orderid in list(self.send_order_dic.keys()):
                            order = self.send_order_dic[vt_orderid]
                            order_status = Offset.CLOSE if order.offset in (
                                Offset.CLOSE, Offset.CLOSETODAY, Offset.CLOSEYESTERDAY) else order.offset
                            if not (order.is_active()):
                                del self.send_order_dic[vt_orderid]
                            if order.direction == direction and (order_status == offset):
                                del self.send_order_dic[vt_orderid]

                    if abs(min(now, self.last_tick_time) - send_dt).seconds > self.send_order_wait_seconds:
                        # 发送订单 回应时间超时 取消订单
                        self.cancel_order(self._last_order.vt_orderid)
                        self.write_log(
                            f"订单已提交，且超时,取消订单."
                            f"send_dt={send_dt}，on_dt={on_dt}, status={status}, "
                            f"orderid={self._last_order.orderid if self._last_order is not None else '(None)'}",
                            'warning'
                        )
                        return False
                    else:
                        self.write_log(
                            f"订单已提交，但未进一步处理，存在被拒绝可能，需要等待结果方可进行后续操作，"
                            f"send_dt={send_dt}，on_dt={on_dt}, status={status}, "
                            f"orderid={self._last_order.orderid if self._last_order is not None else '(None)'}",
                            'warning'
                        )
                        return False

        return True

    def is_same_as_order(self, order: OrderData, direction: Direction, vol: int, price: float):
        return order.direction == direction \
               and order.volume == vol \
               and np.round(order.price / self.vt_symbol_price_tick) == np.round(price / self.vt_symbol_price_tick)

    def algo_trading_2_target_pos(self):
        """
        算计交易，绝对下单实际
        """
        # 检查持仓
        # 计算是否存在仓位不匹配情况
        current_pos = self.pos
        volume = abs(self.target_pos - current_pos)
        if volume == 0:
            return
        if self.target_price <= 0.0:
            if self.current_bar is not None and self.current_bar.close_price > 0:
                self.target_price = self.current_bar.close_price
                msg = 'target_price 价格无效，使用上一根K线收盘价'
                self.write_log(msg, 'warning')
            elif self.last_tick is not None:
                # 使用被动价格
                self.target_price = self.last_tick.bid_price_1 \
                    if self.target_pos > current_pos else self.last_tick.ask_price_1
                msg = f'target_price 价格无效，使用上一Tick{"买1价格" if self.target_pos > current_pos else "卖1价格"}'
                self.write_log(msg, 'warning')

        price = self.target_price
        # self.write_log('运行算法交易')
        # 检查是否存在未成交订单
        active_order_close: Optional[OrderData] = None
        active_order_open: Optional[OrderData] = None
        has_unavailable_order = False
        # list(self.active_order_list) 为了防止将 self.active_order_list 锁住，
        # 避免影响交易
        with self.send_order_dic_lock:
            active_order_list = list(self.send_order_dic.values())
            order_count = len(self.send_order_dic)

        for num, (_, order) in enumerate(self.send_order_dic.items(), start=1):
            if not order.is_active():
                # 仅选取活跃订单
                continue
            order_dt = order.datetime
            # 即使 order_dt is None 依然需要被算作服务器已经接受到order，否则会出现重复下单的情况
            # if order_dt is None:
            #     # order_dt is None 代表订单还没有被服务器处理
            #     continue
            # self.write_log(
            #     f"{num}/{order_count}) algo thread: {order.orderid} {order.offset}
            #     active={order.is_active()} dt={order.datetime}")
            if order.offset == Offset.OPEN:
                active_order_open = order
            else:
                active_order_close = order

            if order_dt is not None:
                now = datetime.now().replace(tzinfo=order_dt.tzinfo)
                if abs(now - order_dt).seconds >= 60 and order.status == Status.SUBMITTING:
                    # 取消超时未成交订单
                    # order.create_cancel_request()
                    self.write_log("取消超过时限未响应的订单")
                    self.cancel_order(order.vt_orderid)
                    has_unavailable_order = True
                    continue

        if has_unavailable_order:
            # 待所有无效订单取消后才可以下新的订单
            return

        # if active_order_close is not None:
        #     self.write_log("存在未成交的平仓单")
        # if active_order_open is not None:
        #     self.write_log("存在未成交的开仓单")

        if 0 <= self.target_pos < current_pos:
            # 平多
            if active_order_open:
                # 如果存在开仓操作，直接取消
                # self.last_send_order_dt = datetime.now()
                # active_order_open.create_cancel_request()
                self.write_log("平多 取消已存在的开仓单")
                self.cancel_order(active_order_open.vt_orderid)

            elif active_order_close:
                # 检查现存订单是否与当前订单一致：
                # 如果一致，则不再重新下单
                # 如果不一致，取消原有订单，且原订单取消确认后（无有效订单），才可以下新订单
                if self.is_same_as_order(active_order_close, Direction.SHORT, volume, price):
                    # 与当前订单一致
                    # self.write_log("平多 目标订单与当前订单一致")
                    pass
                else:
                    # 与当前订单不一致
                    self.write_log("平多 目标订单与当前订单不一致， 取消原订单")
                    # self.last_send_order_dt = datetime.now()
                    # active_order_close.create_cancel_request() 无效
                    self.cancel_order(active_order_close.vt_orderid)
            else:
                self.write_log(f"平多 {current_pos} - > {self.target_pos}")
                self.sell(price, volume)

        elif self.target_pos < 0 < current_pos:
            # 多翻空
            # 先检查平仓单是否已经下出去了
            # 如果平仓单已经下出去了，再下开仓单
            is_close_available = True
            close_pos = abs(current_pos)
            if active_order_close:
                # 检查现存订单是否与当前订单一致：
                # 如果一致，则不再重新下单
                # 如果不一致，取消原有订单，且原订单取消确认后（无有效订单），才可以下新订单
                if self.is_same_as_order(active_order_close, Direction.SHORT, close_pos, price):
                    # 与当前订单一致
                    # self.write_log("多翻空 平仓操作目标订单与当前订单一致")
                    pass
                else:
                    # 与当前订单不一致
                    self.write_log("多翻空 平仓操作目标订单与当前订单不一致， 取消原订单")
                    # self.last_send_order_dt = datetime.now()
                    # active_order_close.create_cancel_request() 无效
                    self.cancel_order(active_order_close.vt_orderid)
                    is_close_available = False
            else:
                self.write_log(f"多翻空 {current_pos} - > {self.target_pos} 先平仓")
                self.sell(price, close_pos)
                is_close_available = False

            if active_order_close:
                open_pos = abs(self.target_pos)
                if active_order_open:
                    if not is_close_available:
                        self.write_log("多翻空 平仓单未生效前，现存开仓单需要取消")
                        self.cancel_order(active_order_open.vt_orderid)
                    elif self.is_same_as_order(active_order_open, Direction.SHORT, open_pos, price):
                        # 检查现存订单是否与当前订单一致：
                        # 如果一致，则不再重新下单
                        # 如果不一致，取消原有订单，且原订单取消确认后（无有效订单），才可以下新订单
                        # 与当前订单一致
                        # self.write_log("多翻空 开仓操作目标订单与当前订单一致")
                        pass
                    else:
                        # 与当前订单不一致
                        self.write_log("多翻空 开仓操作目标订单与当前订单不一致， 取消原订单")
                        # self.last_send_order_dt = datetime.now()
                        # active_order_open.create_cancel_request()
                        self.cancel_order(active_order_open.vt_orderid)
                elif is_close_available:
                    if self.stop_opening_pos != StopOpeningPos.stop_opening_and_nolog.value:
                        self.write_log(f"多翻空 {current_pos} - > {self.target_pos} 再开仓")
                        self.short(price, open_pos)
                else:
                    self.write_log(f"多翻空 平仓单未生效前，开仓单暂不下单")

        elif self.target_pos < current_pos <= 0:
            # 开空
            volume = abs(self.target_pos - current_pos)
            if active_order_close:
                # 如果存在平仓操作，直接取消
                # self.last_send_order_dt = datetime.now()
                # active_order_close.create_cancel_request()
                self.write_log("开空 取消已存在的平仓单")
                self.cancel_order(active_order_close.vt_orderid)

            elif active_order_open:
                # 检查现存订单是否与当前订单一致：
                # 如果一致，则不再重新下单
                # 如果不一致，取消原有订单，且原订单取消确认后（无有效订单），才可以下新订单
                if self.is_same_as_order(active_order_open, Direction.SHORT, volume, price):
                    # 与当前订单一致
                    # self.write_log("开空 目标订单与当前订单一致")
                    pass
                else:
                    # 与当前订单不一致
                    self.write_log("开空 目标订单与当前订单不一致， 取消原订单")
                    # self.last_send_order_dt = datetime.now()
                    # active_order_open.create_cancel_request() 无效
                    self.cancel_order(active_order_open.vt_orderid)
            else:
                if self.stop_opening_pos != StopOpeningPos.stop_opening_and_nolog.value:
                    self.write_log(f"开空 {current_pos} - > {self.target_pos}")
                    self.short(price, volume)

        elif current_pos < self.target_pos <= 0:
            # 平空
            if active_order_open:
                # 如果存在开仓操作，直接取消
                # self.last_send_order_dt = datetime.now()
                # active_order_open.create_cancel_request()
                self.write_log("平空 取消已存在的开仓单")
                self.cancel_order(active_order_open.vt_orderid)

            elif active_order_close:
                # 检查现存订单是否与当前订单一致：
                # 如果一致，则不再重新下单
                # 如果不一致，取消原有订单，且原订单取消确认后（无有效订单），才可以下新订单
                if self.is_same_as_order(active_order_close, Direction.LONG, volume, price):
                    # 与当前订单一致
                    # self.write_log("平空 目标订单与当前订单一致")
                    pass
                else:
                    # 与当前订单不一致
                    self.write_log("平空 目标订单与当前订单不一致， 取消原订单")
                    # self.last_send_order_dt = datetime.now()
                    # active_order_close.create_cancel_request() 无效
                    self.cancel_order(active_order_close.vt_orderid)
            else:
                self.write_log(f"平空 {current_pos} - > {self.target_pos}")
                volume = abs(self.target_pos - current_pos)
                self.cover(price, volume)

        elif current_pos < 0 < self.target_pos:
            # 空翻多
            # 先检查平仓单是否已经下出去了
            # 如果平仓单已经下出去了，再下开仓单
            is_close_available = True
            close_pos = abs(current_pos)
            if active_order_close:
                # 检查现存订单是否与当前订单一致：
                # 如果一致，则不再重新下单
                # 如果不一致，取消原有订单，且原订单取消确认后（无有效订单），才可以下新订单
                if self.is_same_as_order(active_order_close, Direction.LONG, close_pos, price):
                    # 与当前订单一致
                    # self.write_log("空翻多 平仓操作目标订单与当前订单一致")
                    pass
                else:
                    # 与当前订单不一致
                    self.write_log("空翻多 平仓操作目标订单与当前订单不一致， 取消原订单")
                    # self.last_send_order_dt = datetime.now()
                    # active_order_close.create_cancel_request() 无效
                    self.cancel_order(active_order_close.vt_orderid)
                    is_close_available = False
            else:
                self.write_log(f"空翻多 {current_pos} - > {self.target_pos} 先平仓")
                self.cover(price, close_pos)
                is_close_available = False

            if active_order_close:
                open_pos = abs(self.target_pos)
                if active_order_open:
                    if not is_close_available:
                        self.write_log("空翻多 平仓单未生效前，现存开仓单需要取消")
                        self.cancel_order(active_order_open.vt_orderid)
                    elif self.is_same_as_order(active_order_open, Direction.LONG, open_pos, price):
                        # 检查现存订单是否与当前订单一致：
                        # 如果一致，则不再重新下单
                        # 如果不一致，取消原有订单，且原订单取消确认后（无有效订单），才可以下新订单
                        # 与当前订单一致
                        # self.write_log("空翻多 开仓操作目标订单与当前订单一致")
                        pass
                    else:
                        # 与当前订单不一致
                        self.write_log("空翻多 开仓操作目标订单与当前订单不一致， 取消原订单")
                        # self.last_send_order_dt = datetime.now()
                        # active_order_open.create_cancel_request() 无效
                        self.cancel_order(active_order_open.vt_orderid)
                elif is_close_available:
                    if self.stop_opening_pos != StopOpeningPos.stop_opening_and_nolog.value:
                        self.write_log(f"空翻多 {current_pos} - > {self.target_pos} 再开仓")
                        self.buy(price, open_pos)
                else:
                    self.write_log(f"空翻多 平仓单未生效前，开仓单暂不下单")

        elif 0 <= current_pos < self.target_pos:
            # 开多
            if active_order_close:
                # 如果存在平仓操作，直接取消
                # self.last_send_order_dt = datetime.now()
                # active_order_close.create_cancel_request() 无效
                self.write_log("开多 取消已存在的平仓单")
                self.cancel_order(active_order_close.vt_orderid)

            elif active_order_open:
                # 检查现存订单是否与当前订单一致：
                # 如果一致，则不再重新下单
                # 如果不一致，取消原有订单，且原订单取消确认后（无有效订单），才可以下新订单
                if self.is_same_as_order(active_order_open, Direction.LONG, volume, price):
                    # 与当前订单一致
                    # self.write_log("开多 目标订单与当前订单一致")
                    pass
                else:
                    # 与当前订单不一致
                    self.write_log(f"开多 目标订单与当前订单不一致，取消原订单。"
                                   f"\n原订单 {active_order_open.volume} {active_order_open.price}。"
                                   f"\n新订单 {volume} {price}")
                    # self.last_send_order_dt = datetime.now()
                    # active_order_open.create_cancel_request() 无效
                    self.cancel_order(active_order_open.vt_orderid)
            else:
                if self.stop_opening_pos != StopOpeningPos.stop_opening_and_nolog.value:
                    self.write_log(f"开多 {current_pos} - > {self.target_pos} {price}")
                    volume = abs(self.target_pos - current_pos)
                    self.buy(price, volume)


class TargetPosTemplate(TargetPosTemplateBase, CtaTemplate):
    """
        CtaTemplateBase(vnpy原始的 CtaTemplate)
               ↖
        TargetPosTemplateBase               CtaTemplateMixin
                            ↖               ↗
                            TargetPosTemplate
    """

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)


if __name__ == "__main__":
    pass
