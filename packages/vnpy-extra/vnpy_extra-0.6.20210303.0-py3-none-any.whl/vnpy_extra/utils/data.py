#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2020/10/27 9:16
@File    : data.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import logging
import typing
from datetime import date

import numpy as np
import pandas as pd

logger = logging.getLogger()


def filter_available(
        factor_df: pd.DataFrame, y_s: pd.Series, shift_n: int, n_std=3, recent_n_days=None
) -> typing.Union[
    typing.Tuple[np.ndarray, pd.DataFrame, np.ndarray, np.ndarray],
    typing.Tuple[np.ndarray, pd.DataFrame, np.ndarray, np.ndarray, date, date]
]:
    """
    对 factor 以及 y 进行切片，对齐，剔除无效数据等操作
    :param factor_df
    :param y_s
    :param shift_n factor_df 与 y_s 存在 shift_n 的位移
    :param n_std 剔除 n_std 倍 std 以外的值
    :param recent_n_days 选取近 n 天数据
    :return
    """
    assert factor_df.shape[0] == y_s.shape[0], \
        f"因子数据 x{factor_df.shape}长度要与训练目标数据 y{y_s.shape}长度一致"
    original_len = factor_df.shape[0]
    factor_df = factor_df.iloc[:-shift_n]
    factor_arr = factor_df.to_numpy()
    datetime_s = pd.Series(factor_df.index)
    y_s = y_s[shift_n:]
    y_arr = y_s.to_numpy()
    is_not_available = (
            np.isinf(y_arr)
            | np.isnan(y_arr)
            | np.any(np.isnan(factor_arr), axis=1)
            | np.any(np.isinf(factor_arr), axis=1)
            | (datetime_s - datetime_s.shift(shift_n) > pd.Timedelta('3H'))  # 过滤掉隔日或夜盘数据,防止跳空缺口导致的数据不准确
            | (np.abs(y_arr) > y_arr.std() * n_std)  # 过滤掉极端波动 3倍std占比1.1% 2倍std占比3.4%
    ).to_numpy()
    # 日期区间筛选
    if recent_n_days is not None:
        # 将过去 stat_n_days 日期内的数据截取出来
        available_factor_df_date_s = pd.Series(
            factor_df.index, index=factor_df.index
        ).apply(lambda x: x.date())
        # Unique 日期序列
        dates = pd.Series(available_factor_df_date_s.unique()).iloc[-recent_n_days:]
        date_from, date_to = pd.to_datetime(dates.min()), pd.to_datetime(dates.max())
        # date_filter = (
        #         (date_from <= available_factor_df_date_s) & (available_factor_df_date_s <= date_to)
        # ).to_numpy()
        date_filter = (available_factor_df_date_s < date_from).to_numpy()
        # 旧方法
        # latest_datetime = factor_df.index[-1]
        # until_datetime = latest_datetime - pd.to_timedelta(recent_n_days, unit='D')
        # date_filter = factor_df.index < until_datetime
        is_not_available |= date_filter
    else:
        date_from, date_to = None, None

    # 合并筛选结果
    is_available = ~is_not_available
    available_factor_df = factor_df[is_available]
    x_arr = available_factor_df.to_numpy()
    y_arr = y_s[is_available].to_numpy()
    # assert x_arr.shape[0] == y_arr.shape[0], \
    #     f"因子数据 x{x_arr.shape}长度要与训练目标数据 y{y_arr.shape}长度一致"
    new_len = available_factor_df.shape[0]
    logger.debug(
        "整理前后长度 %d -> %d，减少 %d(%.2f%%)",
        original_len, new_len, original_len - new_len, (original_len - new_len) / original_len * 100)
    if recent_n_days is None:
        return is_available, available_factor_df, x_arr, y_arr
    else:
        return is_available, available_factor_df, x_arr, y_arr, date_from, date_to
