#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/10/27 16:11
@File    : engine.py
@contact : mmmaaaggg@163.com
@desc    : 在 vnpy.app.portfolio_strategy.backtesting.BacktestingEngine 基础上继续拿修改
"""
import os
from collections import OrderedDict, defaultdict
from datetime import datetime, date
from multiprocessing import Lock
from typing import List, Dict

import ffn  # NOQA
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from ibats_utils.mess import date_2_str
from pandas import DataFrame
from plotly.subplots import make_subplots
from vnpy.app.portfolio_strategy.backtesting import BacktestingEngine as BacktestingEngineBase, \
    PortfolioDailyResult as PortfolioDailyResultBase
from vnpy.trader.constant import Direction, Status, Interval
from vnpy.trader.object import TradeData, BarData

from vnpy_extra.backtest import CrossLimitMethod
from vnpy_extra.config import logging

plt.switch_backend('Agg')


class PortfolioDailyResult(PortfolioDailyResultBase):

    def add_trade(self, trade: TradeData) -> None:
        """"""
        contract_result = self.contract_results[trade.vt_symbol.upper()]
        contract_result.add_trade(trade)


class BacktestingEngine(BacktestingEngineBase):

    def __init__(self):
        super().__init__()
        self.cross_limit_method: CrossLimitMethod = CrossLimitMethod.open_price
        self.logger = logging.getLogger(self.__class__.__name__)

    def set_parameters(
            self,
            vt_symbols: List[str],
            interval: Interval,
            start: datetime,
            rates: Dict[str, float],
            slippages: Dict[str, float],
            sizes: Dict[str, float],
            priceticks: Dict[str, float],
            capital: int = 0,
            end: datetime = None,
            cross_limit_method: CrossLimitMethod = CrossLimitMethod.open_price
    ) -> None:
        """"""
        self.vt_symbols = [_.upper() for _ in vt_symbols]
        self.interval = interval

        self.rates = {k.upper(): v for k, v in rates.items()}
        self.slippages = {k.upper(): v for k, v in slippages.items()}
        self.sizes = {k.upper(): v for k, v in sizes.items()}
        self.priceticks = {k.upper(): v for k, v in priceticks.items()}

        self.start = start
        self.end = end
        self.capital = capital
        self.cross_limit_method = cross_limit_method
        if cross_limit_method not in CrossLimitMethod:
            raise ValueError(f"cross_limit_method={self.cross_limit_method} 无效")

    def cross_limit_order(self) -> None:
        """
        Cross limit order with last bar/tick data.
        """
        for order in list(self.active_limit_orders.values()):
            bar = self.bars[order.vt_symbol]

            long_cross_price = bar.low_price
            short_cross_price = bar.high_price
            if self.cross_limit_method == CrossLimitMethod.open_price:
                long_best_price = bar.open_price
                short_best_price = bar.open_price
            elif self.cross_limit_method == CrossLimitMethod.mid_price:
                long_best_price = (bar.open_price + bar.high_price + bar.low_price + bar.close_price) / 4
                short_best_price = (bar.open_price + bar.high_price + bar.low_price + bar.close_price) / 4
            elif self.cross_limit_method == CrossLimitMethod.worst_price:
                long_best_price = (bar.open_price * 4 + bar.high_price * 3 + bar.low_price * 2 + bar.close_price) / 10
                short_best_price = (bar.open_price * 4 + bar.high_price * 2 + bar.low_price * 3 + bar.close_price) / 10
            else:
                raise ValueError(f"cross_limit_method={self.cross_limit_method} 无效")

            # Push order update with status "not traded" (pending).
            if order.status == Status.SUBMITTING:
                order.status = Status.NOTTRADED
                self.strategy.update_order(order)

            # Check whether limit orders can be filled.
            long_cross = (
                    order.direction == Direction.LONG
                    and order.price >= long_cross_price > 0
            )

            short_cross = (
                    order.direction == Direction.SHORT
                    and order.price <= short_cross_price
                    and short_cross_price > 0
            )

            if not long_cross and not short_cross:
                continue

            # Push order update with status "all traded" (filled).
            order.traded = order.volume
            order.status = Status.ALLTRADED
            self.strategy.update_order(order)

            self.active_limit_orders.pop(order.vt_orderid)

            # Push trade update
            self.trade_count += 1

            if long_cross:
                trade_price = min(order.price, long_best_price)
            else:
                trade_price = max(order.price, short_best_price)

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

            self.strategy.update_trade(trade)
            self.trades[trade.vt_tradeid] = trade

    def update_daily_close(self, bars: Dict[str, BarData], dt: datetime) -> None:
        """"""
        d = dt.date()

        close_prices = {}
        for bar in bars.values():
            # 2021-02-06 bar.vt_symbol.upper() 行情数据中 vt_symbol 与 CTP接口中 vt_symbol 可能存在大小写不一致情况，
            # 导致后续计算出现KeyError，这里统一使用大写
            close_prices[bar.vt_symbol.upper()] = bar.close_price

        daily_result = self.daily_results.get(d, None)

        if daily_result:
            daily_result.update_close_prices(close_prices)
        else:
            self.daily_results[d] = PortfolioDailyResult(d, close_prices)

    def calculate_statistics(self, df: DataFrame = None, output=True) -> dict:
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
            annual_return = df['balance'].calc_cagr()  # total_return / total_days * 240
            daily_return = df["return"].mean() * 100
            return_std = df["return"].std() * 100

            pnl_std = df["net_pnl"].std()

            if return_std:
                # sharpe_ratio = daily_return / return_std * np.sqrt(240)
                sharpe_ratio = np.round(df['balance'].calc_sharpe(0.03, 252), 2)
            else:
                sharpe_ratio = 0

            # 计算 info ratio
            # 1. 计算资金曲线收益率
            rr_s = df["balance"] / df["balance"].iloc[0]
            # 2. 计算行情收益率
            # 记录 leg2的乘数
            if hasattr(self.strategy, "leg_fractions"):
                leg_fractions = getattr(self.strategy, "leg_fractions")
            else:
                leg_fractions = 1

            # 计算 spread
            vt_symbols_close_df = DataFrame(
                [
                    [d, result.close_prices[self.vt_symbols[0]], result.close_prices[self.vt_symbols[1]]]
                    for d, result in self.daily_results.items()
                ],
                columns=['trade_date', self.vt_symbols[0], self.vt_symbols[1]],
            ).set_index('trade_date').sort_index()
            spread_s = vt_symbols_close_df.iloc[:, 0] - vt_symbols_close_df.iloc[:, 1] * leg_fractions
            rr_spread_s = spread_s / spread_s.iloc[0]
            rr_spread_mdd_s = rr_spread_s.calc_max_drawdown()
            if rr_spread_mdd_s != 0:
                rr_spread_s = rr_spread_s * rr_s.calc_max_drawdown() / rr_spread_s.calc_max_drawdown()
                info_ratio = np.round(rr_s.calc_information_ratio(rr_spread_s), 2)
            else:
                info_ratio = 0

            return_drawdown_ratio = np.round(df['balance'].calc_calmar_ratio(), 2)  # 此处vnpy，原始函数计算有错误

        is_unavailable = (
                total_return <= 0
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
        title_traces_dic["Daily Price"] = []
        vt_symbols_close_df = DataFrame(
            [
                [d, result.close_prices[self.vt_symbols[0]], result.close_prices[self.vt_symbols[1]]]
                for d, result in self.daily_results.items()
            ],
            columns=['trade_date', self.vt_symbols[0], self.vt_symbols[1]],
        ).set_index('trade_date').sort_index()
        charts_data["Daily Price"] = dict(
            title=['trade_date', self.vt_symbols[0], self.vt_symbols[1]],
            data=[[date_2_str(_[0]), _[1], _[2]] for _ in vt_symbols_close_df.reset_index().to_numpy().tolist()],
        )
        for vt_symbol in self.vt_symbols:
            close_line = go.Scatter(
                x=vt_symbols_close_df.index,
                y=vt_symbols_close_df[vt_symbol],
                mode="lines",
                name=vt_symbol
            )
            title_traces_dic["Daily Price"].append(close_line)

        if show_indexes is not None:
            # 目前仅支持 spread
            for index_name in show_indexes:
                if index_name == 'spread':
                    # 记录 leg2的乘数
                    if hasattr(self.strategy, "leg_fractions"):
                        leg_fractions = getattr(self.strategy, "leg_fractions")
                    else:
                        leg_fractions = 1

                    # 计算 spread
                    vt_symbols_close_df = DataFrame(
                        [
                            [d, result.close_prices[self.vt_symbols[0]], result.close_prices[self.vt_symbols[1]]]
                            for d, result in self.daily_results.items()
                        ],
                        columns=['trade_date', self.vt_symbols[0], self.vt_symbols[1]],
                    ).set_index('trade_date').sort_index()
                    spread_s = vt_symbols_close_df.iloc[:, 0] - vt_symbols_close_df.iloc[:, 1] * leg_fractions
                    spread_line = go.Scatter(
                        x=spread_s.index,
                        y=spread_s,
                        mode="lines",
                        name="spread"
                    )
                    title_traces_dic[index_name.upper()] = [spread_line]

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
            name="Drawdown"
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
        bins = 100
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
                # 如果组件环境变量这支不成功，可以考虑通过如下方式这是环境路径
                # plotly.io.orca.config.executable = '/path/to/orca'
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
