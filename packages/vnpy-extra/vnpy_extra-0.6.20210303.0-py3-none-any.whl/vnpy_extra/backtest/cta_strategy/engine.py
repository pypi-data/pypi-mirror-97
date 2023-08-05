"""
@author  : MG
@Time    : 2020/10/9 13:23
@File    : engine.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import logging
import os
from collections import OrderedDict, defaultdict
from datetime import date, datetime
from multiprocessing import Lock
from typing import Dict
import matplotlib.pyplot as plt
import ffn  # NOQA
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from ibats_utils.mess import date_2_str
from pandas import DataFrame
from plotly.subplots import make_subplots
from vnpy.app.cta_strategy.backtesting import BacktestingEngine as BacktestingEngineBase
from vnpy.app.cta_strategy.base import BacktestingMode
from vnpy.trader.constant import Interval, Exchange, Direction, Status
from vnpy.trader.object import TradeData

from vnpy_extra.backtest import CrossLimitMethod
plt.switch_backend('Agg')

class BacktestingEngine(BacktestingEngineBase):

    def __init__(self):
        super().__init__()
        self.cross_limit_method: CrossLimitMethod = CrossLimitMethod.open_price
        self.logger = logging.getLogger(self.__class__.__name__)

    def calculate_result(self):
        """"""
        self.output("开始计算逐日盯市盈亏")

        if not self.trades:
            self.output("成交记录为空，无法计算")
            return

        # Add trade data into daily reuslt.
        for trade in self.trades.values():
            try:
                d = trade.datetime.date()
            except AttributeError:
                d = trade.time.date()

            daily_result = self.daily_results[d]
            daily_result.add_trade(trade)

        # Calculate daily result by iteration.
        pre_close = 0
        start_pos = 0

        for daily_result in self.daily_results.values():
            daily_result.calculate_pnl(
                pre_close,
                start_pos,
                self.size,
                self.rate,
                self.slippage,
                self.inverse
            )

            pre_close = daily_result.close_price
            start_pos = daily_result.end_pos

        # Generate dataframe
        results = defaultdict(list)

        for daily_result in self.daily_results.values():
            for key, value in daily_result.__dict__.items():
                results[key].append(value)

        self.daily_df = DataFrame.from_dict(results).set_index("date")

        self.output("逐日盯市盈亏计算完成")
        return self.daily_df

    def set_parameters(
            self,
            vt_symbol: str,
            interval: Interval,
            start: datetime,
            rate: float,
            slippage: float,
            size: float,
            pricetick: float,
            capital: int = 0,
            end: datetime = None,
            mode: BacktestingMode = BacktestingMode.BAR,
            inverse: bool = False,
            cross_limit_method: CrossLimitMethod = CrossLimitMethod.open_price
    ):
        """"""
        self.mode = mode
        self.vt_symbol = vt_symbol
        self.interval = Interval(interval)
        self.rate = rate
        self.slippage = slippage
        self.size = size
        self.pricetick = pricetick
        self.start = start

        self.symbol, exchange_str = self.vt_symbol.split(".")
        self.exchange = Exchange(exchange_str)

        self.capital = capital
        self.end = end
        self.mode = mode
        self.inverse = inverse
        self.cross_limit_method = cross_limit_method
        if cross_limit_method not in CrossLimitMethod:
            raise ValueError(f"cross_limit_method={self.cross_limit_method} 无效")

    def cross_limit_order(self):
        """
        Cross limit order with last bar/tick data.
        """
        if self.mode == BacktestingMode.BAR:
            bar = self.bar
            long_cross_price = bar.low_price
            short_cross_price = bar.high_price
            if self.cross_limit_method == CrossLimitMethod.open_price:
                long_best_price = bar.open_price
                short_best_price = bar.open_price
            elif self.cross_limit_method == CrossLimitMethod.mid_price:
                long_best_price = (bar.open_price + bar.high_price + bar.low_price + bar.close_price) / 4
                short_best_price = (bar.open_price + bar.high_price + bar.low_price + bar.close_price) / 4
            elif self.cross_limit_method == CrossLimitMethod.worst_price:
                long_best_price = max(
                    bar.open_price,
                    (bar.open_price * 4 + bar.high_price * 3 + bar.low_price * 2 + bar.close_price) / 10)
                short_best_price = min(
                    bar.open_price,
                    (bar.open_price * 4 + bar.high_price * 2 + bar.low_price * 3 + bar.close_price) / 10)
            else:
                raise ValueError(f"cross_limit_method={self.cross_limit_method} 无效")

        else:
            long_cross_price = self.tick.ask_price_1
            short_cross_price = self.tick.bid_price_1
            long_best_price = long_cross_price
            short_best_price = short_cross_price

        for order in list(self.active_limit_orders.values()):
            # Push order update with status "not traded" (pending).
            if order.status == Status.SUBMITTING:
                order.status = Status.NOTTRADED
                self.strategy.on_order(order)

            # Check whether limit orders can be filled.
            long_cross = (
                    order.direction == Direction.LONG
                    and order.price > long_cross_price > 0
            )

            short_cross = (
                    order.direction == Direction.SHORT
                    and order.price < short_cross_price
                    and short_cross_price > 0
            )

            if not long_cross and not short_cross:
                continue

            # Push order update with status "all traded" (filled).
            order.traded = order.volume
            order.status = Status.ALLTRADED
            self.strategy.on_order(order)

            self.active_limit_orders.pop(order.vt_orderid)

            # Push trade update
            self.trade_count += 1

            if long_cross:
                pos_change = order.volume
                if self.cross_limit_method == CrossLimitMethod.open_price:
                    trade_price = min(order.price, long_best_price)
                else:
                    trade_price = long_best_price
            else:
                pos_change = -order.volume
                # 这里写成else没有问题，因为前面已经判断过  long_cross short_cross 必有一个是 True
                if self.cross_limit_method == CrossLimitMethod.open_price:
                    trade_price = max(order.price, short_best_price)
                else:
                    trade_price = short_best_price

            trade = TradeData(
                symbol=order.symbol,
                exchange=order.exchange,
                orderid=order.orderid,
                tradeid=str(self.trade_count),
                direction=order.direction,
                offset=order.offset,
                price=trade_price,
                volume=order.volume,
                datetime=self.datetime,
                gateway_name=self.gateway_name,
            )

            self.strategy.pos += pos_change
            self.strategy.on_trade(trade)

            self.trades[trade.vt_tradeid] = trade

    def calculate_statistics(self, df: DataFrame = None, output=True):
        """"""
        self.output("开始计算策略统计指标")

        # Check DataFrame input exterior
        if df is None:
            df = self.daily_df

        # Check for init DataFrame
        if df is None:
            # Set all statistics to 0 if no trade.
            start_date = ""
            end_date = ""
            total_days = 0
            profit_days = 0
            loss_days = 0
            end_balance = 0
            max_drawdown = 0
            max_ddpercent = 0
            max_drawdown_duration = 0
            max_new_higher_duration = 0
            total_net_pnl = 0
            daily_net_pnl = 0
            total_commission = 0
            daily_commission = 0
            total_slippage = 0
            daily_slippage = 0
            total_turnover = 0
            daily_turnover = 0
            total_trade_count = 0
            daily_trade_count = 0
            total_return = 0
            annual_return = 0
            daily_return = 0
            return_std = 0
            sharpe_ratio = 0
            info_ratio = 0
            return_drawdown_ratio = 0
        else:
            # Calculate balance related time series data
            df["balance"] = df["net_pnl"].cumsum() + self.capital
            df["return"] = np.log(df["balance"] / df["balance"].shift(1)).fillna(0)
            df["highlevel"] = (
                df["balance"].rolling(
                    min_periods=1, window=len(df), center=False).max()
            )
            df["drawdown"] = df["balance"] - df["highlevel"]
            df["ddpercent"] = df["drawdown"] / df["highlevel"] * 100

            # Calculate statistics value
            start_date = df.index[0]
            end_date = df.index[-1]

            total_days = len(df)
            profit_days = len(df[df["net_pnl"] > 0])
            loss_days = len(df[df["net_pnl"] < 0])

            end_balance = df["balance"].iloc[-1]
            max_drawdown = df["drawdown"].min()
            max_ddpercent = df["ddpercent"].min()
            max_drawdown_end = df["drawdown"].idxmin()

            if isinstance(max_drawdown_end, date):
                max_drawdown_start = df["balance"][:max_drawdown_end].idxmax()
                max_drawdown_duration = (max_drawdown_end - max_drawdown_start).days
            else:
                max_drawdown_duration = 0

            highlevel = df["highlevel"]
            max_new_higher_duration = highlevel.groupby(by=highlevel).count().max()

            total_net_pnl = df["net_pnl"].sum()
            daily_net_pnl = total_net_pnl / total_days

            total_commission = df["commission"].sum()
            daily_commission = total_commission / total_days

            total_slippage = df["slippage"].sum()
            daily_slippage = total_slippage / total_days

            total_turnover = df["turnover"].sum()
            daily_turnover = total_turnover / total_days

            total_trade_count = df["trade_count"].sum()
            daily_trade_count = np.round(total_trade_count / total_days, 2)

            total_return = (end_balance / self.capital - 1) * 100
            annual_return = df['balance'].calc_cagr()  # total_return / total_days * 240  # 此处vnpy，原始函数计算有错误
            daily_return = df["return"].mean() * 100
            return_std = df["return"].std() * 100

            if return_std:
                sharpe_ratio = np.round(df['balance'].calc_sharpe(0.03, 252), 2)  # daily_return / return_std * np.sqrt(240)
            else:
                sharpe_ratio = 0

            rr = df["balance"] / df["balance"].iloc[0]
            close_price = df["close_price"]
            rr_close = close_price / close_price.iloc[0]
            rr_close_mdd = rr_close.calc_max_drawdown()
            if rr_close_mdd != 0:
                rr_close = rr_close * rr.calc_max_drawdown() / rr_close.calc_max_drawdown()
                info_ratio = np.round(rr.calc_information_ratio(rr_close), 2)
            else:
                info_ratio = 0

            return_drawdown_ratio = np.round(df['balance'].calc_calmar_ratio(), 2)  # 此处vnpy，原始函数计算有错误

        is_unavailable = (
                total_return <= 0
                or info_ratio < 0
                or daily_trade_count < 0.2  # 1/0.2 每一次交易平仓再开仓需要2次交易，因此相当于10天交易一次
                or return_drawdown_ratio < 2
                or max_new_higher_duration >= 180  # 最长不创新高周期<180
                or max_new_higher_duration / total_days > 0.5  # 最长不创新高周期超过一半的总回测天数
                or df is None  # 没有交易
                or np.sum((df["balance"] - self.capital) <= 0) / total_days > 0.5  # 50%以上交易日处于亏损状态
        )

        # Output
        if output:
            self.output("-" * 30)
            self.output("|      指标    |     数值      |")
            self.output("|:-----------|------------:|")
            self.output(f"|首个交易日| \t{start_date}|")
            self.output(f"|最后交易日| \t{end_date}|")

            self.output(f"|总交易日| \t{total_days}|")
            self.output(f"|盈利交易日| \t{profit_days}|")
            self.output(f"|亏损交易日| \t{loss_days}|")

            self.output(f"|起始资金| \t{self.capital:,.2f}|")
            self.output(f"|结束资金| \t{end_balance:,.2f}|")

            self.output(f"|总收益率| \t{total_return:,.2f}%")
            self.output(f"|年化收益| \t{annual_return:,.2f}%")
            self.output(f"|最大回撤| \t{max_drawdown:,.2f}|")
            self.output(f"|百分比最大回撤| {max_ddpercent:,.2f}%")
            self.output(f"|最长回撤天数| \t{max_drawdown_duration}|")
            self.output(f"|最长再创新高周期| \t{max_new_higher_duration}|")

            self.output(f"|总盈亏| \t{total_net_pnl:,.2f}|")
            self.output(f"|总手续费| \t{total_commission:,.2f}|")
            self.output(f"|总滑点| \t{total_slippage:,.2f}|")
            self.output(f"|总成交金额| \t{total_turnover:,.2f}|")
            self.output(f"|总成交笔数| \t{total_trade_count}|")

            self.output(f"|日均盈亏| \t{daily_net_pnl:,.2f}|")
            self.output(f"|日均手续费| \t{daily_commission:,.2f}|")
            self.output(f"|日均滑点| \t{daily_slippage:,.2f}|")
            self.output(f"|日均成交金额| \t{daily_turnover:,.2f}|")
            self.output(f"|日均成交笔数| \t{daily_trade_count:,.3f}|")

            self.output(f"|日均收益率| \t{daily_return:,.2f}%|")
            self.output(f"|收益标准差| \t{return_std:,.2f}%|")
            self.output(f"|Sharpe Ratio| \t{sharpe_ratio:,.2f}|")
            self.output(f"|Info Ratio| \t{info_ratio:,.2f}|")
            self.output(f"|收益回撤比| \t{return_drawdown_ratio:,.2f}|")

            self.output(f"|available| \t{not is_unavailable}|")

        statistics = OrderedDict([
            ("start_date", start_date),
            ("end_date", end_date),
            ("total_days", total_days),
            ("profit_days", profit_days),
            ("loss_days", loss_days),
            ("capital", self.capital),
            ("end_balance", end_balance),
            ("max_drawdown", max_drawdown),
            ("max_ddpercent", max_ddpercent),
            ("max_drawdown_duration", max_drawdown_duration),
            ("max_new_higher_duration", max_new_higher_duration),
            ("total_net_pnl", total_net_pnl),
            ("daily_net_pnl", daily_net_pnl),
            ("total_commission", total_commission),
            ("daily_commission", daily_commission),
            ("total_slippage", total_slippage),
            ("daily_slippage", daily_slippage),
            ("total_turnover", total_turnover),
            ("daily_turnover", daily_turnover),
            ("total_trade_count", total_trade_count),
            ("daily_trade_count", daily_trade_count),
            ("total_return", total_return),
            ("annual_return", annual_return),
            ("daily_return", daily_return),
            ("return_std", return_std),
            ("sharpe_ratio", sharpe_ratio),
            ("info_ratio", info_ratio),
            ("return_drawdown_ratio", return_drawdown_ratio),
            ("available", not is_unavailable),
        ])

        # Filter potential error infinite value
        for key, value in statistics.items():
            if value in (np.inf, -np.inf):
                value = 0
            statistics[key] = np.nan_to_num(value)

        self.output("策略统计指标计算完成")
        return statistics

    def show_chart(self, df: DataFrame = None,
                   image_file_name=None, open_browser_4_charts=True,
                   show_indexes=None,
                   lock: Lock = None,
                   ) -> Dict[str, Dict[str, list]]:
        """"""
        charts_data = defaultdict(dict)
        # Check DataFrame input exterior
        if df is None:
            df = self.daily_df

        # Check for init DataFrame
        if df is None:
            return charts_data

        title_traces_dic = OrderedDict()
        # close_df = DataFrame(
        #     [{'trade_date': _, 'close_price': r.close_price}
        #      for _, r in self.daily_results.items()]
        # ).set_index('trade_date').sort_index()
        charts_data["Daily Price"] = dict(
            title=['trade_date', self.vt_symbol],
            data=[[date_2_str(_[0]), _[1]] for _ in df["close_price"].reset_index().to_numpy().tolist()],
        )
        daily_price = go.Scatter(
            x=df.index,
            y=df["close_price"],
            mode="lines",
            name="Daily Price"
        )
        title_traces_dic["Daily Price"] = daily_price
        if show_indexes is not None:
            import pandas as pd
            from vnpy_extra.utils.enhancement import BarGenerator
            from vnpy_extra.utils.enhancement import ArrayManager
            from vnpy.trader.constant import Interval
            from vnpy.trader.object import BarData
            # 建立队列
            am = ArrayManager(size=len(self.history_data))
            am_index = []

            def update_am_bar(am_bar: BarData):
                am.update_bar(am_bar)
                am_index.append(am_bar.datetime.date())

            # 通过 BarGenerator 合成日线数据
            bg = BarGenerator(
                # 更新 tick 数据合成 1min bar后调用的函数，只在Tick级测试的时候才需要
                # 当前无用，所以设置了空操作
                lambda x: x,
                window=1,
                on_window_bar=update_am_bar,
                interval=Interval.DAILY
            )
            # 加载历史数据，出发 bg.on_window_bar 更新 am 数据
            for bar in self.history_data:
                bg.update_bar(bar)

            am_index_len = len(am_index)
            # md_df = pd.DataFrame({
            #     'trade_date': am_index,
            #     'open': am.open[-am_index_len:],
            #     'high': am.high[-am_index_len:],
            #     'low': am.low[-am_index_len:],
            #     'close': am.close[-am_index_len:],
            # }).drop_duplicates(
            #     subset=['trade_date'], keep='last'
            # ).set_index('trade_date').sort_index()

            # 输出指标
            for index_name in show_indexes:
                index_name = index_name.lower()
                if index_name == 'kdj':
                    k, d, j = am.kdj(9, 3, 3, array=True)
                    index_df = pd.DataFrame({
                        'K': k[-am_index_len:],
                        'D': d[-am_index_len:],
                        'J': j[-am_index_len:]
                    }, index=am_index)
                    merged_df = df.join(index_df, how='left')
                    k_line = go.Scatter(
                        x=merged_df.index,
                        y=merged_df['K'],
                        mode="lines",
                        name="K",
                        line=dict(color='rgba(0,0,0,1)')
                    )
                    d_line = go.Scatter(
                        x=merged_df.index,
                        y=merged_df['D'],
                        mode="lines",
                        name="D",
                        line=dict(color='rgba(201,55,86,1)')
                    )
                    j_line = go.Scatter(
                        x=merged_df.index,
                        y=merged_df['J'],
                        mode="lines",
                        name="J",
                        line=dict(color='rgba(141,75,187,1)')
                    )
                    title_traces_dic[index_name.upper()] = [k_line, d_line, j_line]

        profit_s = df["balance"] - self.capital
        profit_line = go.Scatter(
            x=df.index,
            y=profit_s,
            mode="lines",
            name="profit"
        )
        total_cost_s = (df["commission"] + df["slippage"]).cumsum()
        profit_without_cost_s = profit_s + total_cost_s
        profit_fee0_line = go.Scatter(
            x=df.index,
            y=profit_without_cost_s,
            mode="lines",
            name="profit without cost",
            line=dict(color='rgba(255,179,167,1)', dash='dashdot')  # ffb3a7
        )
        fee_line = go.Scatter(
            x=df.index,
            y=total_cost_s,
            mode="lines",
            name="total cost",
            line=dict(color='rgba(117,138,153,1)', dash='dashdot')  # 758a99
        )
        title_traces_dic["profit vs total cost"] = [fee_line, profit_fee0_line, profit_line]
        charts_data["profit vs total cost"] = dict(
            title=['trade_date', 'profit', "profit without cost", "total cost"],
            data=[[date_2_str(_[0]), _[1], _[2], _[3]] for _ in DataFrame(
                [profit_s, profit_without_cost_s, total_cost_s]).T.reset_index().to_numpy().tolist()],
        )
        drawdown_scatter = go.Scatter(
            x=df.index,
            y=df["drawdown"],
            fillcolor="red",
            fill='tozeroy',
            mode="lines",
            name="Drawdown",
            line=dict(color='rgba(68,206,246,1)')  # 44cef6
        )
        title_traces_dic["Drawdown"] = drawdown_scatter
        charts_data["Drawdown"] = dict(
            title=['trade_date', 'drawdown'],
            data=[[date_2_str(_[0]), _[1]] for _ in df["drawdown"].reset_index().to_numpy().tolist()],
        )
        pnl_bar = go.Bar(y=df["net_pnl"], name="Daily Pnl")
        title_traces_dic["Daily Pnl"] = pnl_bar
        charts_data["Daily Pnl"] = dict(
            title=['trade_date', 'net_pnl'],
            data=[[date_2_str(_[0]), _[1]] for _ in df["net_pnl"].reset_index().to_numpy().tolist()],
        )
        bins=100
        pnl_histogram = go.Histogram(x=df["net_pnl"], nbinsx=bins, name="Days")
        title_traces_dic["Pnl Distribution"] = pnl_histogram
        nums, bins_v, _ = plt.hist(df["net_pnl"], bins=bins)
        charts_data["Pnl Distribution"] = dict(
            title=['net_pnl', 'count'],
            data=[
                [(bins_v[_] + bins_v[_ + 1]) / 2 for _ in range(len(nums))],
                list(nums),
            ],
        )
        # 生成图表
        row_count = len(title_traces_dic)
        fig = make_subplots(
            rows=row_count,
            cols=1,
            subplot_titles=list(title_traces_dic.keys()),
            vertical_spacing=0.04
        )
        for n, (title, traces) in enumerate(title_traces_dic.items(), start=1):
            if isinstance(traces, list):
                for _ in traces:
                    fig.add_trace(_, row=n, col=1)
            else:
                fig.add_trace(traces, row=n, col=1)

        _, file_name = os.path.split(image_file_name)
        file_name, _ = os.path.splitext(file_name)
        fig.update_layout(
            title=file_name,
            height=row_count * 200, width=1200
        )
        if open_browser_4_charts:
            fig.show()

        if image_file_name is not None:
            if lock is not None:
                lock.acquire()  # 锁住共享变量

            try:
                pio.write_image(fig, image_file_name)
            except ValueError:
                try:
                    try:
                        from kaleido.scopes.plotly import PlotlyScope
                        pio.write_image(fig, image_file_name, engine='orca')
                    except ImportError:
                        pio.write_image(fig, image_file_name, engine='kaleido')
                except ValueError:
                    self.logger.exception("save file to %s error", image_file_name)
            finally:
                if lock is not None:
                    lock.release()  # 释放共享变量

        return charts_data

if __name__ == "__main__":
    pass
