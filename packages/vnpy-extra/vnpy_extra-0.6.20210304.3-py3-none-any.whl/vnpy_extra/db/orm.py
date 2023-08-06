"""
@author  : MG
@Time    : 2020/11/24 11:05
@File    : object.py
@contact : mmmaaaggg@163.com
@desc    : 用于创建数据库表结构

为方便调试 StrategyBacktestStats 使用，建议新建一个视图

CREATE
    ALGORITHM = UNDEFINED
    DEFINER = `root`@`localhost`
    SQL SECURITY DEFINER
VIEW `strategy_backtest_stats_view` AS
    SELECT
        `si`.`module_name` AS `module_name`,
        `si`.`strategy_class_name` AS `strategy_class_name`,
        `syi`.`symbols` AS `symbols`,
        `stats`.`stg_info_id` AS `stg_info_id`,
        `stats`.`symbols_info_id` AS `symbols_info_id`,
        `stats`.`id_name` AS `id_name`,
        `stats`.`cross_limit_method` AS `cross_limit_method`,
        `stats`.`short_name` AS `short_name`,
        `stats`.`shown_name` AS `shown_name`,
        `stats`.`strategy_settings` AS `strategy_settings`,
        `stats`.`engine_kwargs` AS `engine_kwargs`,
        `stats`.`backtest_status` AS `backtest_status`,
        `stats`.`available` AS `available`,
        `stats`.`update_dt` AS `update_dt`,
        `stats`.`start_date` AS `start_date`,
        `stats`.`end_date` AS `end_date`,
        `stats`.`total_days` AS `total_days`,
        `stats`.`profit_days` AS `profit_days`,
        `stats`.`loss_days` AS `loss_days`,
        `stats`.`capital` AS `capital`,
        `stats`.`end_balance` AS `end_balance`,
        `stats`.`total_return` AS `total_return`,
        `stats`.`annual_return` AS `annual_return`,
        `stats`.`max_drawdown` AS `max_drawdown`,
        `stats`.`max_ddpercent` AS `max_ddpercent`,
        `stats`.`max_drawdown_duration` AS `max_drawdown_duration`,
        `stats`.`max_new_higher_duration` AS `max_new_higher_duration`,
        `stats`.`total_net_pnl` AS `total_net_pnl`,
        `stats`.`total_commission` AS `total_commission`,
        `stats`.`total_slippage` AS `total_slippage`,
        `stats`.`total_turnover` AS `total_turnover`,
        `stats`.`total_trade_count` AS `total_trade_count`,
        `stats`.`daily_net_pnl` AS `daily_net_pnl`,
        `stats`.`daily_commission` AS `daily_commission`,
        `stats`.`daily_slippage` AS `daily_slippage`,
        `stats`.`daily_turnover` AS `daily_turnover`,
        `stats`.`daily_trade_count` AS `daily_trade_count`,
        `stats`.`daily_return` AS `daily_return`,
        `stats`.`return_std` AS `return_std`,
        `stats`.`sharpe_ratio` AS `sharpe_ratio`,
        `stats`.`info_ratio` AS `info_ratio`,
        `stats`.`return_drawdown_ratio` AS `return_drawdown_ratio`,
        `stats`.`image_file_path` AS `image_file_path`
    FROM
        ((`strategy_backtest_stats` `stats`
        LEFT JOIN `strategy_info` `si` ON ((`stats`.`stg_info_id` = `si`.`id`)))
        LEFT JOIN `symbols_info` `syi` ON ((`stats`.`symbols_info_id` = `syi`.`id`)))

"""
import enum
import os
import typing
from collections import defaultdict, OrderedDict
from datetime import datetime, date

import pandas as pd
from ibats_utils.mess import date_2_str, datetime_2_str
from peewee import (
    PrimaryKeyField,
    ForeignKeyField,
    CharField,
    SmallIntegerField,
    DateField,
    DateTimeField,
    DoubleField,
    BooleanField,
    IntegerField,
    Model,
    CompositeKey,
    fn,
    SQL,
    InternalError,
)
# Peewee provides an alternate database implementation
# for using the mysql-connector driver.
# The implementation can be found in playhouse.mysql_ext.
from playhouse.mysql_ext import MySQLConnectorDatabase, JSONField, TextField
from vnpy.trader.constant import Offset
from vnpy.trader.setting import get_settings

from vnpy_extra.config import logging
from vnpy_extra.utils.enhancement import get_instrument_type

logger = logging.getLogger()


class AccountStrategyStatusEnum(enum.IntEnum):
    NotYet = -1
    Created = 0
    Initialized = 1
    RunPending = 2
    Running = 3
    StopPending = 4
    Stopped = 5


class StrategyBacktestStatusEnum(enum.IntEnum):
    Unavailable = 0  # 标记无效策略
    MaybeAvailable = 1  # 可能有效，需要进一步跟踪验证
    TrackingBacktest = 2  # 每日滚动更新回测状态，寻找合适的入场时机
    QuasiOnline = 3  # 准上线策略,策略的合约为"主连合约",因此,上线策略需要被转换为当期实际主力合约
    CompareTradeData = 4  # 策略已经启动，每日对比实盘交易数据与回测交易数据是否存在较大差异


def init_db():
    settings = get_settings("database.")
    keys = {"database", "user", "password", "host", "port"}
    settings = {k: v for k, v in settings.items() if k in keys}
    db = MySQLConnectorDatabase(**settings)
    return db


_USER_NAME: typing.Optional[str] = None
_BROKER_ID: typing.Optional[str] = None


def get_account() -> typing.Tuple[str, str]:
    global _USER_NAME, _BROKER_ID
    if _USER_NAME is None or _BROKER_ID is None:
        from vnpy.trader.utility import load_json
        filename: str = f"connect_ctp.json"
        connect_dic = load_json(filename)
        if len(connect_dic) == 0:
            _USER_NAME, _BROKER_ID = "test user", "0000"
        else:
            _USER_NAME = connect_dic["用户名"]
            _BROKER_ID = connect_dic["经纪商代码"]

        logger.info(f"user name='{_USER_NAME}', broker_id='{_BROKER_ID}'")

    return _USER_NAME, _BROKER_ID


def set_account(user_name, broker_id):
    global _USER_NAME, _BROKER_ID
    _USER_NAME, _BROKER_ID = user_name, broker_id


def set_account_backtest():
    user_name, broker_id = "test user", "0000"
    set_account(user_name, broker_id)


database = init_db()


def dict_2_jsonable(dic: dict) -> dict:
    new_dic = {}
    for k, _ in dic.items():
        if isinstance(_, enum.Enum):
            v = _.value
        elif isinstance(_, date):
            v = date_2_str(_)
        elif isinstance(_, datetime):
            v = datetime_2_str(_)
        else:
            v = _
        new_dic[k] = v

    return new_dic


class StrategyInfo(Model):
    module_name: str = CharField(max_length=150, help_text="策略的类名称")
    strategy_class_name: str = CharField(max_length=80, help_text="策略的类名称")
    backtest_folder_path: str = CharField(
        max_length=255, null=True,
        help_text="策略回测时，回测文件所在的根目录（不包含output目录）。"
                  "该目录与 StrategyBacktestStats 的 image_file_path 拼接可组成绝对路径",
    )

    class Meta:
        database = database
        legacy_table_names = False
        # table_settings = "ENGINE = MYISAM"
        indexes = (
            # 2021-02-22
            # 考虑到 strategy_class_name 相同可能会使得 StrategyInfo.get_cls_module_dic() 存在一对多的歧义情况，
            # 另外便于管理，因此，此处强制要求 strategy_class_name 必须唯一
            # create a unique on strategy_class_name
            # (('module_name', 'strategy_class_name'), True),
            (('strategy_class_name',), True),
        )

    @staticmethod
    def get_cls_id_dict() -> typing.Dict[str, int]:
        try:
            cls_id_dic = {
                stg_info.strategy_class_name: stg_info.id
                for stg_info in StrategyInfo.select().where(
                    StrategyInfo.module_name != '__main__'
                ).execute()
            }
            return cls_id_dic
        finally:
            StrategyInfo._meta.database.close()

    @staticmethod
    def get_cls_module_dic() -> typing.Dict[str, str]:
        try:
            cls_module_dic = {
                stg_info.strategy_class_name: stg_info.module_name
                for stg_info in StrategyInfo.select().where(
                    StrategyInfo.module_name != '__main__'
                ).execute()
            }
            return cls_module_dic
        finally:
            StrategyInfo._meta.database.close()


class SymbolsInfo(Model):
    id: int = PrimaryKeyField()
    symbols: str = TextField(
        help_text="合约列表，以数组形势进行存储，匹配原则是完全匹配，顺序也要保持一致")

    class Meta:
        database = database
        legacy_table_names = False
        # table_settings = "ENGINE = MYISAM"

    @staticmethod
    def get_symbols_id_dict() -> typing.Dict[str, int]:
        try:
            cls_id_dic = {
                obj.symbols: obj.id
                for obj in SymbolsInfo.select().execute()
            }
            return cls_id_dic
        finally:
            SymbolsInfo._meta.database.close()


class FutureAdjFactor(Model):
    instrument_type: str = CharField(max_length=20, help_text="合约类型")
    trade_date = DateField(help_text="交易日")
    method: str = CharField(max_length=20, help_text="因子计算方法")
    instrument_id_main: str = CharField(null=True, max_length=50, help_text="主力合约名称")
    adj_factor_main: str = DoubleField(null=True, help_text="主力调整因子")
    instrument_id_secondary = CharField(null=True, max_length=50, help_text="次主力合约名称")
    adj_factor_secondary = DoubleField(null=True, help_text="次主力调整因子")

    class Meta:
        database = database
        table_name = 'wind_future_adj_factor'
        primary_key = CompositeKey('instrument_type', 'trade_date', 'method')

    @staticmethod
    def change_curr_contract(symbols) -> str:
        """将当前合约替换为当期主力合约"""
        instrument_type = get_instrument_type(symbols)
        exch = symbols.split('.')[1]
        obj = FutureAdjFactor.select(
        ).where(
            FutureAdjFactor.instrument_type == instrument_type
        ).order_by(-FutureAdjFactor.trade_date).get()
        curr_contract = f"{obj.instrument_id_main.split('.')[0]}.{exch}"
        return curr_contract


class StrategyBacktestStats(Model):
    stg_info: int = ForeignKeyField(StrategyInfo, on_delete='cascade', on_update='cascade',
                                    help_text="StrategyInfo 信息")
    # strategy_class_name: str = CharField(max_length=55, help_text="策略的类名称")
    symbols_info: int = ForeignKeyField(SymbolsInfo, on_delete='cascade', on_update='cascade',
                                        help_text="SymbolsInfo 信息")
    id_name: str = CharField(max_length=300, help_text="生成相关图片等文件时使用的文件名头部标示")
    # symbols: str = CharField(max_length=25, help_text="合约列表")
    cross_limit_method: str = SmallIntegerField(help_text="CrossLimitMethod：0:open_price 1:mid_price 2:worst_price")
    short_name: str = CharField(null=True, help_text="用于策略运行时使用的唯一标示名")
    shown_name: str = CharField(null=True, help_text="用于策略报表展示时使用的唯一标示名")
    backtest_status: int = SmallIntegerField(
        constraints=[SQL(f'DEFAULT {StrategyBacktestStatusEnum.Unavailable.value}')],
        help_text="手动标示该策略是否有效:0无效 1可能有效 2滚动更新状态 3对比实盘交易数据"
    )
    strategy_settings = JSONField(help_text="策略创建时传入的 settings 参数")
    engine_kwargs = JSONField(help_text="回测引擎创建时传入的参数")
    available = BooleanField(help_text="回测程序自动判断策略是否有效")
    update_dt = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')], help_text="更新时间")
    start_date = DateField(null=True, help_text="首个交易日")
    end_date = DateField(null=True, help_text="最后交易日")
    total_days = IntegerField(null=True, help_text="总交易日")
    profit_days = IntegerField(null=True, help_text="盈利交易日")
    loss_days = IntegerField(null=True, help_text="亏损交易日")
    capital = DoubleField(null=True, help_text="起始资金")
    end_balance = DoubleField(null=True, help_text="结束资金")
    total_return = DoubleField(null=True, help_text="总收益率")
    annual_return = DoubleField(null=True, help_text="年化收益")
    max_drawdown = DoubleField(null=True, help_text="最大回撤")
    max_ddpercent = DoubleField(null=True, help_text="百分比最大回撤")
    max_drawdown_duration = DoubleField(null=True, help_text="最长回撤天数")
    max_new_higher_duration = DoubleField(null=True, help_text="最长再创新高周期")
    total_net_pnl = DoubleField(null=True, help_text="总盈亏")
    total_commission = DoubleField(null=True, help_text="总手续费")
    total_slippage = DoubleField(null=True, help_text="总滑点")
    total_turnover = DoubleField(null=True, help_text="总成交金额")
    total_trade_count = IntegerField(null=True, help_text="总成交笔数")
    daily_net_pnl = DoubleField(null=True, help_text="日均盈亏")
    daily_commission = DoubleField(null=True, help_text="日均手续费")
    daily_slippage = DoubleField(null=True, help_text="日均滑点")
    daily_turnover = DoubleField(null=True, help_text="日均成交金额")
    daily_trade_count = DoubleField(null=True, help_text="日均成交笔数")
    daily_return = DoubleField(null=True, help_text="日均收益率")
    return_std = DoubleField(null=True, help_text="收益标准差")
    sharpe_ratio = DoubleField(null=True, help_text="Sharpe Ratio")
    info_ratio = DoubleField(null=True, help_text="Info Ratio")
    return_drawdown_ratio = DoubleField(null=True, help_text="收益回撤比")
    image_file_path = CharField(null=True, max_length=1024, help_text="生成资金曲线图片路径")
    charts_data = JSONField(null=True, help_text="构建charts所需要的数据")

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('stg_info', 'symbols_info', 'id_name', 'cross_limit_method')
        indexes = (
            # create a unique on short_name
            (('short_name',), True),
            # create a unique on shown_name
            (('shown_name',), True),
        )

    @staticmethod
    def update_stats(
            strategy_settings: dict, engine_kwargs: dict, statistics: dict,
            charts_data: dict,
            backtest_folder_path: typing.Optional[str] = None,
    ):
        if len(statistics) == 0 or ('total_days' in statistics and statistics['total_days'] == 0):
            return
        try:
            module_name = statistics.pop('module_name')
            strategy_class_name = statistics['strategy_class_name']
            symbols = statistics['symbols']
            if backtest_folder_path is None:
                backtest_folder_path = os.path.abspath(os.path.curdir)

            stg_info, created = StrategyInfo.get_or_create(
                module_name=module_name, strategy_class_name=strategy_class_name,
                defaults=dict(backtest_folder_path=backtest_folder_path)
            )
            if (not created) and stg_info.backtest_folder_path != backtest_folder_path:
                stg_info.backtest_folder_path = backtest_folder_path
                stg_info.save()

            symbols_info, _ = SymbolsInfo.get_or_create(symbols=symbols)
            StrategyBacktestStats.insert(
                stg_info=stg_info,
                symbols_info=symbols_info,
                strategy_settings=dict_2_jsonable(strategy_settings),
                engine_kwargs=dict_2_jsonable(engine_kwargs),
                charts_data=charts_data,
                update_dt=datetime.now(),
                **{k: v for k, v in statistics.items() if k not in (
                    'module_name', 'strategy_class_name', 'symbols', 'image_file_url',
                )}
            ).on_conflict(
                update=dict(
                    # stg_info_id=stg_info_id,
                    # symbols_info_id=symbols_curr_info.id,
                    strategy_settings=dict_2_jsonable(strategy_settings),
                    engine_kwargs=dict_2_jsonable(engine_kwargs),
                    charts_data=charts_data,
                    update_dt=datetime.now(),
                    **{k: v for k, v in statistics.items() if k not in (
                        'module_name', 'strategy_class_name', 'symbols', 'image_file_url', 'id_name',
                    )}
                )
            ).execute()
        finally:
            TradeDataModel._meta.database.close()

    @staticmethod
    def update_backtest_status(data_dic_list: typing.List[typing.Dict]) -> int:
        """

        :param data_dic_list: 每个 item 至少包含如下字段 [
            'strategy_class_name', 'id_name', 'symbols', 'cross_limit_method', 'backtest_status',
             'short_name', 'shown_name']
        :return:
        """
        counter = 0
        try:
            cls_id_dic = StrategyInfo.get_cls_id_dict()
            symbols_id_dic = SymbolsInfo.get_symbols_id_dict()
            with database.atomic():
                for data_dic in data_dic_list:
                    if 'index' in data_dic:
                        del data_dic['index']

                    backtest_status = data_dic.pop("backtest_status")
                    stg_info_id = cls_id_dic[data_dic.pop('strategy_class_name')]
                    symbols = data_dic.pop('symbols')
                    symbols_info_id = symbols_id_dic[symbols]
                    if backtest_status == StrategyBacktestStatusEnum.QuasiOnline.value:
                        # 获取源对象
                        stats_obj: StrategyBacktestStats = StrategyBacktestStats.select().where(
                            StrategyBacktestStats.id_name == data_dic['id_name'],
                            StrategyBacktestStats.stg_info_id == stg_info_id,
                            StrategyBacktestStats.symbols_info_id == symbols_info_id,
                        ).get()
                        stats_obj.backtest_status = backtest_status
                        stats_obj.save()
                        # 插入主力合约，对应状态 StrategyBacktestStatusEnum.CompareTradeData.value
                        # 去除 short_name, shown_name 两个字段仅用于
                        # 当期主力合约 StrategyBacktestStatusEnum.CompareTradeData 的情况
                        short_name = data_dic.pop('short_name')
                        shown_name = data_dic.pop('shown_name')
                        if short_name is None or short_name == '' or pd.isna(short_name):
                            raise ValueError(f'id_name={data_dic["id_name"]} on {symbols} short_name 不能为空')
                        if shown_name is None or shown_name == '' or pd.isna(shown_name):
                            raise ValueError(f'id_name={data_dic["id_name"]} on {symbols} shown_name 不能为空')

                        symbol_list = symbols.split('_')
                        is_portfolio = len(symbol_list) > 1
                        symbols_curr_list = [FutureAdjFactor.change_curr_contract(_) for _ in symbol_list]
                        symbols_curr = '_'.join(symbols_curr_list)
                        symbols_curr_info, _ = SymbolsInfo.get_or_create(symbols=symbols_curr)
                        engine_kwargs = stats_obj.engine_kwargs.copy()
                        if is_portfolio:
                            engine_kwargs["vt_symbols"] = symbols_curr_list
                        else:
                            engine_kwargs["vt_symbol"] = symbols_curr_list[0]

                        StrategyBacktestStats.insert(
                            stg_info_id=stg_info_id,
                            symbols_info_id=symbols_curr_info.id,
                            backtest_status=StrategyBacktestStatusEnum.CompareTradeData.value,
                            short_name=short_name,
                            shown_name=shown_name,
                            update_dt=datetime.now(),
                            engine_kwargs=engine_kwargs,
                            strategy_settings=stats_obj.strategy_settings,
                            **data_dic
                        ).on_conflict(
                            update=dict(
                                # stg_info_id=stg_info_id,
                                # symbols_info_id=symbols_curr_info.id,
                                update_dt=datetime.now(),
                                backtest_status=StrategyBacktestStatusEnum.CompareTradeData.value,
                                short_name=short_name,
                                shown_name=shown_name,
                                engine_kwargs=engine_kwargs,
                                strategy_settings=stats_obj.strategy_settings,
                                # id_name=data_dic["id_name"],
                            )
                        ).execute()
                        counter += 1
                    else:
                        # 仅更新 backtest_status 状态
                        counter += StrategyBacktestStats.update(
                            backtest_status=backtest_status,
                            update_dt=datetime.now()
                        ).where(
                            StrategyBacktestStats.id_name == data_dic['id_name'],
                            StrategyBacktestStats.stg_info_id == stg_info_id,
                            StrategyBacktestStats.symbols_info_id == symbols_info_id,
                        ).execute()
                        counter += 1

            return counter
        finally:
            StrategyBacktestStats._meta.database.close()

    @staticmethod
    def get_available_status_group_by_strategy(symbols=None) -> typing.Dict[typing.Tuple[str, str], list]:
        ret_data = OrderedDict()
        try:
            query = StrategyBacktestStats.select(
                StrategyBacktestStats, StrategyInfo, SymbolsInfo
            ).join(
                StrategyInfo, on=StrategyBacktestStats.stg_info == StrategyInfo.id
            ).join(
                SymbolsInfo, on=StrategyBacktestStats.symbols_info == SymbolsInfo.id
            ).where(
                StrategyBacktestStats.backtest_status > StrategyBacktestStatusEnum.Unavailable.value
            ).order_by(
                StrategyBacktestStats.symbols_info_id,
                StrategyBacktestStats.stg_info_id,
                StrategyBacktestStats.short_name
            )
            if symbols is not None:
                query = query.where(StrategyBacktestStats.symbols_info == SymbolsInfo.get_or_none(symbols=symbols))

            for obj in query.execute():
                key = (
                    obj.stg_info.module_name,
                    obj.stg_info.strategy_class_name,
                    obj.symbols_info.symbols
                )
                ret_data.setdefault(key, []).append(obj)

            return ret_data
        finally:
            StrategyBacktestStats._meta.database.close()

    @staticmethod
    def get_by_status(status: StrategyBacktestStatusEnum = StrategyBacktestStatusEnum.CompareTradeData.value
                      ) -> list:
        ret_data = []
        try:
            for obj in StrategyBacktestStats.select(
                    StrategyBacktestStats, StrategyInfo, SymbolsInfo
            ).join(
                StrategyInfo, on=StrategyBacktestStats.stg_info == StrategyInfo.id
            ).join(
                SymbolsInfo, on=StrategyBacktestStats.symbols_info == SymbolsInfo.id
            ).where(
                StrategyBacktestStats.backtest_status == status
            ).order_by(
                StrategyBacktestStats.short_name
            ).execute():
                ret_data.append(obj)

            return ret_data
        finally:
            StrategyBacktestStats._meta.database.close()

    @staticmethod
    def import_by_settings(stats_list: typing.List[dict]):
        try:
            with database.atomic():
                for stats in stats_list:
                    module_name = stats.pop('module_name')
                    strategy_class_name = stats.pop('strategy_class_name')
                    symbols = stats.pop('symbols')
                    stg_info, _ = StrategyInfo.get_or_create(
                        module_name=module_name, strategy_class_name=strategy_class_name)
                    symbols_str = '_'.join(symbols) if isinstance(symbols, list) else symbols
                    symbols_info, _ = SymbolsInfo.get_or_create(symbols=symbols_str)
                    id_name = stats.pop('id_name')
                    cross_limit_method = stats.pop('cross_limit_method')

                    StrategyBacktestStats.insert(
                        stg_info=stg_info,
                        symbols_info=symbols_info,
                        id_name=id_name,
                        cross_limit_method=cross_limit_method,
                        available=True,
                        update_dt=datetime.now(),
                        **stats
                    ).on_conflict(
                        update=dict(
                            available=True,
                            update_dt=datetime.now(),
                            **stats
                        )
                    ).execute()
        finally:
            StrategyBacktestStats._meta.database.close()


class StrategyBacktestStatsArchive(StrategyBacktestStats):
    id: int = PrimaryKeyField()

    @staticmethod
    def archive(stats_list_dic: typing.Dict[typing.Tuple[str, str], typing.List[StrategyBacktestStats]]):
        """将现有 StrategyBacktestStats 中的策略统计数据进行归档"""
        try:
            with database.atomic():
                for stats_list in stats_list_dic.values():
                    if len(stats_list) == 0:
                        continue
                    fields = list(stats_list[0]._meta.fields.keys())
                    StrategyBacktestStatsArchive.insert_many(
                        [[getattr(stats, _) for _ in fields] for stats in stats_list],
                        fields=fields
                    ).execute()

        finally:
            StrategyBacktestStatsArchive._meta.database.close()

    class Meta:
        database = database
        legacy_table_names = False
        # indexes = ((("strategy_class_name", "id_name", "symbols", "cross_limit_method"), True),)
        # table_settings = 'ENGINE = MYISAM'


class StrategyStatus(Model):
    """
    策略状态信息
    * strategy_name 策略名称
    * status 策略状态
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    strategy_name: str = CharField()
    shown_name: str = CharField(null=True, help_text="生成报告需要的对外展示用名，如果没有则使用 strategy_name")
    status: int = SmallIntegerField()
    symbols: str = CharField(max_length=255)
    strategy_settings = JSONField(null=True, help_text="策略创建时传入的 settings 参数")
    backtest_status: int = SmallIntegerField(default=StrategyBacktestStatusEnum.CompareTradeData.value)
    description: str = CharField(null=True)
    update_dt = DateTimeField()

    @staticmethod
    def is_table_exists():
        try:
            is_exists = StrategyStatus.table_exists()
            return is_exists
        except:
            return False
        finally:
            StrategyStatus._meta.database.close()

    @staticmethod
    def set_status(strategy_name, status: int):
        try:
            user_name, broker_id = get_account()
            ret_data = StrategyStatus.update(
                status=status, update_dt=datetime.now()
            ).where(
                StrategyStatus.user_name == user_name,
                StrategyStatus.broker_id == broker_id,
                StrategyStatus.strategy_name == strategy_name,
            ).execute()
            logger.debug("%s[%s] %s status=%d", user_name, broker_id, strategy_name, status)
        finally:
            StrategyStatus._meta.database.close()
        return ret_data

    @staticmethod
    def query_status(strategy_name) -> int:
        try:
            user_name, broker_id = get_account()
            ss: StrategyStatus = StrategyStatus.get_or_none(
                StrategyStatus.user_name == user_name,
                StrategyStatus.broker_id == broker_id,
                StrategyStatus.strategy_name == strategy_name,
            )
            if ss is None:
                status = -1
            else:
                status = ss.status

            logger.debug("%s[%s] %s status=%d", user_name, broker_id, strategy_name, status)
            return status
        finally:
            StrategyStatus._meta.database.close()

    @staticmethod
    def register_strategy(strategy_name, status: int, symbols: str, strategy_settings: dict):
        try:
            user_name, broker_id = get_account()
            ret_data = StrategyStatus.insert(
                user_name=user_name, broker_id=broker_id,
                strategy_name=strategy_name, status=status, strategy_settings=strategy_settings,
                symbols=symbols, update_dt=datetime.now(),
                backtest_status=StrategyBacktestStatusEnum.CompareTradeData.value
            ).on_conflict(
                preserve=[StrategyStatus.user_name, StrategyStatus.broker_id, StrategyStatus.strategy_name],
                update={
                    StrategyStatus.status: status,
                    StrategyStatus.strategy_settings: strategy_settings,
                    StrategyStatus.update_dt: datetime.now(),
                    StrategyStatus.backtest_status: StrategyBacktestStatusEnum.CompareTradeData.value,
                }
            ).execute()
            logger.debug("%s[%s] %s status=%d", user_name, broker_id, strategy_name, status)
            return ret_data
        finally:
            StrategyStatus._meta.database.close()

    @staticmethod
    def query_all():
        user_name, broker_id = get_account()
        try:
            ret_data = [_ for _ in StrategyStatus.select().where(
                StrategyStatus.user_name == user_name,
                StrategyStatus.broker_id == broker_id,
            ).execute()]
        finally:
            StrategyStatus._meta.database.close()

        return ret_data

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'strategy_name')
        table_settings = "ENGINE = MYISAM"
        # table_settings = "ENGINE = MEMORY"


class OrderDataModel(Model):
    """
    策略状态信息
    实际生产环境中 orderid 可以唯一确定
    但是，回测环境下，需要与策略名称，品种进行配合才行
    * strategy_name 策略名称
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    strategy_name: str = CharField()
    orderid: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    order_type: str = CharField(max_length=20)
    direction: str = CharField(max_length=8)
    offset: str = CharField(max_length=8)
    price = DoubleField()
    volume = DoubleField()
    status: str = CharField(max_length=20)
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'strategy_name', 'orderid', 'symbol')
        # indexes = ((("strategy_name", "symbol"), True),)

    @staticmethod
    def bulk_replace(data_dic_list: typing.List[dict]):
        user_name, broker_id = get_account()
        try:
            with database.atomic():
                for data_dic in data_dic_list:
                    data_dic['user_name'] = user_name
                    data_dic['broker_id'] = broker_id
                    OrderDataModel.replace(**data_dic).execute()

        finally:
            OrderDataModel._meta.database.close()


class TradeDataModel(Model):
    """
    策略状态信息
    实际生产环境中 tradeid 可以唯一确定
    但是，回测环境下，需要与策略名称，品种进行配合才行
    * strategy_name 策略名称
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    strategy_name: str = CharField()
    tradeid: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    orderid: str = CharField()
    direction: str = CharField(max_length=8)
    offset: str = CharField(max_length=8)
    price = DoubleField()
    volume = DoubleField()
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'strategy_name', 'tradeid', 'symbol')
        # indexes = ((("strategy_name", "symbol"), True),)

    @staticmethod
    def get_latest_open_trade_data():
        """
        获取各个策略最近的一笔开仓交易单
        """
        user_name, broker_id = get_account()
        sql_str = """select trades.* from trade_data_model trades inner join (
            select strategy_name, max(`datetime`) dt from trade_data_model 
            where user_name=%s and broker_id=%s and offset=%s
            group by strategy_name) latest
            on trades.strategy_name = latest.strategy_name
            and trades.`datetime` = latest.dt
            where user_name=%s and broker_id=%s and offset=%s
            """
        strategy_symbol_latest_open_trade_data_dic = defaultdict(dict)
        try:
            for trade_data in TradeDataModel.raw(
                    sql_str, user_name, broker_id, Offset.OPEN.value,
                    user_name, broker_id, Offset.OPEN.value, ).execute():
                strategy_symbol_latest_open_trade_data_dic[trade_data.strategy_name][trade_data.symbol] = trade_data
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_latest_open_trade_data_dic

    @staticmethod
    def query_latest_n_trade_date_list(latest_n) -> typing.List[date]:
        user_name, broker_id = get_account()
        sql_str = f"select distinct Date(`datetime`) from trade_data_model" \
                  f" where user_name=%s and broker_id=%s" \
                  f" order by Date(`datetime`) desc limit {latest_n}"
        trade_date_list = []
        try:
            for trade_date in database.execute_sql(sql_str, [user_name, broker_id]):
                trade_date_list.append(trade_date[0])
        finally:
            database.close()

        return trade_date_list

    @staticmethod
    def query_trade_data_by_strategy_since(
            strategy_name: str = None, trade_dt: datetime = None
    ) -> typing.Dict[str, list]:
        """
        :param strategy_name
        :param trade_dt 可以为空，非空情况下，返回大于此（不包含）时间的全部交易数据
        """
        user_name, broker_id = get_account()
        strategy_symbol_trade_data_list_dic = defaultdict(list)
        try:
            if trade_dt is None:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.strategy_name == strategy_name
                ).order_by(TradeDataModel.datetime, TradeDataModel.tradeid).execute():
                    strategy_symbol_trade_data_list_dic[_.symbol].append(_)
            else:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.strategy_name == strategy_name,
                        TradeDataModel.datetime > trade_dt
                ).order_by(TradeDataModel.datetime, TradeDataModel.tradeid).execute():
                    strategy_symbol_trade_data_list_dic[_.symbol].append(_)
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_trade_data_list_dic

    @staticmethod
    def query_trade_data_by_strategy_symbol_since(
            strategy_name: str, symbol: str, trade_dt: datetime = None
    ) -> list:
        """
        :param strategy_name
        :param trade_dt 可以为空，非空情况下，返回大于此（不包含）时间的全部交易数据
        """
        user_name, broker_id = get_account()
        strategy_symbol_trade_data_list = []
        try:
            if trade_dt is None:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.strategy_name == strategy_name,
                        TradeDataModel.symbol == symbol,
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list.append(_)
            else:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.strategy_name == strategy_name,
                        TradeDataModel.symbol == symbol,
                        TradeDataModel.datetime > trade_dt
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list.append(_)
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_trade_data_list

    @staticmethod
    def query_trade_data_since(
            update_dt: datetime = None
    ) -> typing.Dict[str, typing.Dict[str, list]]:
        """
        :param update_dt 可以为空，非空情况下，返回大于此（不包含）时间的全部交易数据
        """
        user_name, broker_id = get_account()
        strategy_symbol_trade_data_list_dic = defaultdict(lambda: defaultdict(list))
        try:
            if update_dt is None:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.strategy_name][_.symbol].append(_)
            else:
                for _ in TradeDataModel.select().where(
                        TradeDataModel.user_name == user_name,
                        TradeDataModel.broker_id == broker_id,
                        TradeDataModel.datetime > update_dt
                ).order_by(TradeDataModel.datetime).execute():
                    strategy_symbol_trade_data_list_dic[_.strategy_name][_.symbol].append(_)
        finally:
            TradeDataModel._meta.database.close()

        return strategy_symbol_trade_data_list_dic

    @staticmethod
    def bulk_replace(data_dic_list: typing.List[dict]):
        user_name, broker_id = get_account()
        try:
            with database.atomic():
                for data_dic in data_dic_list:
                    data_dic['user_name'] = user_name
                    data_dic['broker_id'] = broker_id
                    TradeDataModel.replace(**data_dic).execute()

        finally:
            TradeDataModel._meta.database.close()

    @staticmethod
    def clear_by_strategy_name(strategy_name):
        user_name, broker_id = get_account()
        try:
            TradeDataModel.delete().where(
                TradeDataModel.user_name == user_name,
                TradeDataModel.broker_id == broker_id,
                TradeDataModel.strategy_name == strategy_name).execute()
        except InternalError:
            logger.exception("strategy_name='%s' and use_name='%s' clean exception", strategy_name, user_name)
        finally:
            TradeDataModel._meta.database.close()


class LatestTickPriceModel(Model):
    """
    策略状态信息
    * symbol 产品名称
    """
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    price = DoubleField()
    volume = DoubleField()
    datetime = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('symbol')
        table_settings = "ENGINE = MEMORY"

    @staticmethod
    def query_latest_price(symbol):
        """
        获取各个策略最近的一笔开仓交易单
        """
        try:
            data: LatestTickPriceModel = LatestTickPriceModel.get_or_none(LatestTickPriceModel.symbol == symbol)
        finally:
            LatestTickPriceModel._meta.database.close()

        return data

    @staticmethod
    def query_all_latest_price() -> dict:
        """
        获取各个策略最近的一笔开仓交易单
        """
        try:
            symbol_tick_dic: typing.Dict[str, LatestTickPriceModel] = {
                _.symbol: _ for _ in LatestTickPriceModel.select()}
        finally:
            LatestTickPriceModel._meta.database.close()

        return symbol_tick_dic


class PositionStatusModel(Model):
    """
    策略持仓信息
    * strategy_name 策略名称
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    tradeid: str = CharField()
    strategy_name: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    trade_date = DateField()
    trade_dt = DateTimeField()
    direction: str = CharField(max_length=8)
    avg_price = DoubleField()  # 平均持仓成本
    latest_price = DoubleField()  # 最新价格
    volume = DoubleField()
    holding_gl = DoubleField()  # holding gain and loss 持仓盈亏
    offset_gl = DoubleField()  # offset gain and loss 平仓盈亏
    offset_daily_gl = DoubleField()  # daily offset gain and loss 平仓盈亏
    offset_acc_gl = DoubleField()  # accumulate offset gain and loss 平仓盈亏
    update_dt = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'tradeid', 'strategy_name', 'symbol')

    @staticmethod
    def query_position_status_list_until(trade_date) -> list:
        user_name, broker_id = get_account()
        sql_str = """select pos.* 
            from position_status_model pos 
            inner join (
                select strategy_name, max(trade_dt) trade_dt 
                from position_status_model 
                where user_name=%s and broker_id=%s
                and trade_date <= %s
                group by strategy_name, symbol) latest
            on pos.strategy_name = latest.strategy_name
            and pos.trade_dt = latest.trade_dt
            where user_name=%s and broker_id=%s"""

        try:
            position_status_list = [
                _ for _ in PositionStatusModel.raw(
                    sql_str, user_name, broker_id, date_2_str(trade_date), user_name, broker_id
                ).execute()]
        finally:
            PositionStatusModel._meta.database.close()

        return position_status_list

    @staticmethod
    def query_latest_position_status() -> typing.Dict[str, dict]:
        """
        获取各个策略最近的一笔开仓交易单
        """
        user_name, broker_id = get_account()
        sql_str = """select pos.* from position_status_model pos inner join (
            select strategy_name, max(trade_dt) trade_dt from position_status_model 
            where user_name=%s and broker_id=%s
            group by strategy_name, symbol) latest
            on pos.strategy_name = latest.strategy_name
            and pos.trade_dt = latest.trade_dt
            where user_name=%s and broker_id=%s"""
        strategy_symbol_pos_status_dic = defaultdict(dict)
        try:
            for pos_status in PositionStatusModel.raw(
                    sql_str, user_name, broker_id, user_name, broker_id).execute():
                strategy_symbol_pos_status_dic[pos_status.strategy_name][pos_status.symbol] = pos_status
        finally:
            PositionStatusModel._meta.database.close()

        return strategy_symbol_pos_status_dic

    @staticmethod
    def query_strategy_symbol_count_dic(from_date, to_date) -> typing.Dict[typing.Tuple[str, str], int]:
        user_name, broker_id = get_account()
        sql_str = """select strategy_name, symbol, count(1) from position_status_model pos 
            where user_name=%s and broker_id=%s and trade_date between %s and %s
            group by strategy_name, symbol"""
        strategy_symbol_count_dic = {}
        try:
            for strategy_name, symbol, count in database.execute_sql(
                    sql_str, params=[user_name, broker_id, from_date, to_date]):
                strategy_symbol_count_dic[(strategy_name, symbol)] = count
        finally:
            PositionStatusModel._meta.database.close()

        return strategy_symbol_count_dic

    @staticmethod
    def bulk_replace(pos_status_new_list: typing.List[dict]):
        user_name, broker_id = get_account()
        try:
            with database.atomic():
                for data_dic in pos_status_new_list:
                    data_dic['user_name'] = user_name
                    data_dic['broker_id'] = broker_id
                    PositionStatusModel.replace(**data_dic).execute()

        finally:
            PositionStatusModel._meta.database.close()


class PositionDailyModel(Model):
    """
    策略持仓信息
    * strategy_name 策略名称
    """
    user_name: str = CharField(max_length=50)
    broker_id: str = CharField(max_length=20)
    strategy_name: str = CharField()
    symbol: str = CharField(max_length=20)
    exchange: str = CharField(max_length=20)
    trade_date = DateField()
    trade_dt = DateTimeField()
    direction: str = CharField(max_length=8)
    avg_price = DoubleField()  # 平均持仓成本
    latest_price = DoubleField()  # 最新价格
    volume = DoubleField()
    holding_gl = DoubleField()  # holding gain and loss 持仓盈亏
    offset_gl = DoubleField()  # offset gain and loss 平仓盈亏
    offset_daily_gl = DoubleField()  # daily offset gain and loss 平仓盈亏
    offset_acc_gl = DoubleField()  # accumulate offset gain and loss 平仓盈亏
    update_dt = DateTimeField()

    class Meta:
        database = database
        legacy_table_names = False
        primary_key = CompositeKey('user_name', 'broker_id', 'strategy_name', 'symbol', 'trade_date')

    @staticmethod
    def bulk_replace(position_daily_list: typing.List[dict]):
        user_name, broker_id = get_account()
        try:
            with database.atomic():
                for data_dic in position_daily_list:
                    data_dic['user_name'] = user_name
                    data_dic['broker_id'] = broker_id
                    PositionDailyModel.replace(**data_dic).execute()

        finally:
            PositionDailyModel._meta.database.close()

    @staticmethod
    def query_latest_position_daily() -> typing.Dict[str, dict]:
        """
        获取各个策略最近的一笔开仓交易单
        """
        user_name, broker_id = get_account()
        sql_str = """select pos.* from position_daily_model pos inner join (
            select strategy_name, max(trade_date) trade_date from position_daily_model 
            where user_name=%s and broker_id=%s
            group by strategy_name, symbol) latest
            on pos.strategy_name = latest.strategy_name
            and pos.trade_date = latest.trade_date
            where user_name=%s and broker_id=%s"""
        strategy_symbol_pos_daily_dic = defaultdict(dict)
        try:
            for pos_status in PositionDailyModel.raw(
                    sql_str, user_name, broker_id, user_name, broker_id).execute():
                strategy_symbol_pos_daily_dic[pos_status.strategy_name][pos_status.symbol] = pos_status
        finally:
            PositionDailyModel._meta.database.close()

        return strategy_symbol_pos_daily_dic


class TradeDateModel(Model):
    """
    策略状态信息
    * strategy_name 策略名称
    * status 策略状态
    """
    trade_date = DateField(primary_key=True)

    class Meta:
        database = database
        legacy_table_names = False
        table_settings = "ENGINE = MYISAM"

    @staticmethod
    def get_latest_trade_date():
        try:
            obj: TradeDateModel = TradeDateModel.select(fn.MAX(TradeDateModel.trade_date)).first()
        finally:
            TradeDateModel._meta.database.close()

        return None if obj.trade_date is None else obj.trade_date

    @staticmethod
    def bulk_replace(data_dic_list: typing.List[dict]):
        try:
            with database.atomic():
                for data_dic in data_dic_list:
                    TradeDateModel.replace(**data_dic).execute()

        finally:
            TradeDateModel._meta.database.close()

    @staticmethod
    def get_trade_date_dic() -> typing.Tuple[typing.Dict[date, date], typing.Dict[date, date]]:
        trade_date_df = pd.read_sql("SELECT * FROM trade_date_model order by trade_date", database)
        trade_date_df['trade_date_next'] = trade_date_df['trade_date'].shift(-1)
        trade_date_df['trade_date_last'] = trade_date_df['trade_date'].shift(1)
        next_trade_date_dic = trade_date_df.set_index('trade_date')['trade_date_next'].to_dict()
        last_trade_date_dic = trade_date_df.set_index('trade_date')['trade_date_last'].to_dict()
        return next_trade_date_dic, last_trade_date_dic


def init_models():
    # try:
    #     StrategyStatus.create_table()  # 创建表  # engine='MEMORY'
    # except peewee.OperationalError:
    #     logger.warning("StrategyStatus table already exists!")
    #
    # try:
    #     TradeDataModel.create_table()  # 创建表  # engine='MEMORY'
    # except peewee.OperationalError:
    #     logger.warning("TradeDataModel table already exists!")

    database.connect()
    database.create_tables([
        StrategyStatus, OrderDataModel, TradeDataModel,
        LatestTickPriceModel, PositionStatusModel, PositionDailyModel,
        TradeDateModel,
        StrategyInfo, SymbolsInfo,
        StrategyBacktestStats, StrategyBacktestStatsArchive,
        FutureAdjFactor
    ])
    # import inspect
    # import peewee
    # models = [
    #     obj for name, obj in inspect.getmembers(
    #         "__main__", lambda obj: type(obj) == type and issubclass(obj, peewee.Model)
    #     )
    # ]
    # peewee.create_model_tables(models)


def _test_record_strategy_status():
    strategy_name = 'asdf11'
    user_name, broker_id = get_account()
    status = AccountStrategyStatusEnum.Running
    StrategyStatus.register_strategy(
        strategy_name=strategy_name, status=status.value, symbols='rb2101.SHFE',
        strategy_settings={})
    ss: StrategyStatus = StrategyStatus.get_or_none(
        StrategyStatus.user_name == user_name, StrategyStatus.broker_id == broker_id,
        StrategyStatus.strategy_name == strategy_name)
    assert ss.status == status.value
    assert ss.description == ''
    StrategyStatus.set_status(strategy_name=strategy_name, status=status.value)
    ss: StrategyStatus = StrategyStatus.get_or_none(
        StrategyStatus.user_name == user_name, StrategyStatus.broker_id == broker_id,
        StrategyStatus.strategy_name == strategy_name)
    print(ss, ss.status)
    ss.status = AccountStrategyStatusEnum.Stopped.value
    ss.update()
    ss._meta.database.close()
    print(ss, ss.status)


if __name__ == "__main__":
    init_models()
    # _test_record_strategy_status()
