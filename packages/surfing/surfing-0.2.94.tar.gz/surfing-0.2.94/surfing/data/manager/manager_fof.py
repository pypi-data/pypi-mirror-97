
from typing import List, Optional, Tuple, Union, Dict
from collections import defaultdict
import re
import datetime
import json
import io
import traceback
import math

import numpy as np
import pandas as pd

from sqlalchemy.orm import sessionmaker

from ...util.singleton import Singleton
from ...util.wechat_bot import WechatBot
from ...util.calculator import Calculator
from ...util.aip_calc import xirr
from ...constant import FundStatus, HoldingAssetType, FOFStatementStatus, FOFTradeStatus
from ..api.basic import BasicDataApi
from ..api.derived import DerivedDataApi
from ..view.basic_models import HedgeFundInfo, FOFInfo, FOFManually, HedgeFundNAV, FOFInvestorPosition, FOFEstimateFee, FOFEstimateInterest, FOFTransitMoney, FOFAccountStatement
from ..view.derived_models import FOFNav, FOFPosition, FOFInvestorData, FOFPositionDetail
from ..wrapper.mysql import BasicDatabaseConnector, DerivedDatabaseConnector
from ..nav_reader.hedge_fund_nav_reader import HedgeFundNAVReader


# def IncentiveFeeMode(enum.IntEnum):
#     ASSET_HW = 1  # 基金资产高水位方法
#     ASSET_HW_WITH_EXTRA = 2  # 基金资产高水位方法
#     SINGLE_CUSTOM_HW = 3  # 基金资产高水位）赎回时补充计提法
#     SINGLE_CUSTOM_HW_FIXED_WITH_EXTRA = 4  # （单客户高水位）固定时点扣减份额和赎回时补充计提法
#     SINGLE_CUSTOM_HW_DIVIDEND_WITH_EXTRA = 5  # （单客户高水位）分红时计提和赎回时补充计提法
#     SINGLE_CUSTOM_HW_OPEN_DAY = 6   # （单客户高水位）单客户开放日扣减净值计提法


class FOFDataManager(metaclass=Singleton):

    # 从EXCEL读取数据的路径，一般用不到
    _FILE_PATH = './nav_data/FOF运营计算逻辑.xlsx'

    # TODO: 暂时只支持一个FOF
    _FOF_ID = 'SLW695'

    _FEES_FLAG: List[int] = [1, 1, 1, 1, -1, -1, -1]
    _DAYS_PER_YEAR_FOR_INTEREST = 360

    def __init__(self):
        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.float_format', lambda x: '%.4f' % x)
        self._start_date: Optional[str] = None
        self._end_date: Optional[str] = None
        self._date_list: Optional[np.ndarray] = None
        self._fof_scale: Optional[pd.DataFrame] = None
        self._asset_allocation: Optional[pd.DataFrame] = None
        self._hedge_pos: Optional[pd.DataFrame] = None
        self._hedge_nav: Optional[pd.DataFrame] = None
        self._fund_pos: Optional[pd.DataFrame] = None
        self._manually: Optional[pd.DataFrame] = None
        self._incidental_trading: Optional[pd.DataFrame] = None
        self._fof_nav: Optional[pd.DataFrame] = None
        self._fof_position: Optional[pd.DataFrame] = None
        self._fof_investor_pos: Optional[pd.DataFrame] = None
        self._fof_fee_details: Optional[pd.DataFrame] = None
        self._fof_cash_details: Optional[pd.DataFrame] = None
        self._fof_position_details: Optional[pd.DataFrame] = None
        self._total_net_assets: float = None
        self._total_shares: float = None

        self._wechat_bot = WechatBot()

    def _get_days_this_year_for_fee(self, the_date: datetime.date) -> int:
        '''计算今年一共有多少天'''
        return pd.Timestamp(year=the_date.year, month=12, day=31).dayofyear

    @staticmethod
    def _do_calc_v_net_value(nav: Union[pd.Series, pd.DataFrame, float], unit_total, acc_nav: pd.Series, init_water_line: pd.Series, incentive_fee_ratio: Union[pd.Series, float], decimals: Union[pd.Series, float]) -> pd.Series:
        # 盈利
        excess_ret = acc_nav - init_water_line
        # 盈 或 亏
        earn_con = (excess_ret > 0).astype('int')
        # 费
        pay_mng_fee = ((unit_total * excess_ret * earn_con).round(2) * incentive_fee_ratio).round(2)
        # 通过MV来算出净值
        unit_total_sum = unit_total.sum()
        mv = (nav * unit_total_sum).round(2)
        mv -= pay_mng_fee.sum()
        v_nav = (mv / unit_total_sum).round(decimals)
        return v_nav

    @staticmethod
    def _do_calc_v_net_value_by_nav(nav: Union[pd.Series, pd.DataFrame, float], acc_nav: pd.Series, init_water_line: pd.Series, incentive_fee_ratio: Union[pd.Series, float], decimals: Union[pd.Series, float]) -> pd.Series:
        # 盈利
        excess_ret = acc_nav - init_water_line
        # 盈 或 亏
        earn_con = (excess_ret > 0).astype('int')
        # 费
        pay_mng_fee = ((excess_ret * earn_con).round(2) * incentive_fee_ratio).round(2)
        # 净值
        v_nav = (nav - pay_mng_fee).round(decimals)
        return v_nav

    @staticmethod
    def _calc_virtual_net_value(fund_list, asset_allocation=None):
        '''计算虚拟净值'''
        fund_info = FOFDataManager.get_hedge_fund_info(fund_list)
        # TODO: 目前只支持高水位法计算
        fund_info = fund_info.loc[fund_info.incentive_fee_mode == '高水位法']
        fund_info = fund_info.set_index('fund_id')
        incentive_fee_ratio = fund_info['incentive_fee_ratio'].to_dict()
        v_nav_decimals = fund_info['v_nav_decimals'].to_dict()

        df = FOFDataManager.get_hedge_fund_nav(fund_list)
        df = df[df.fund_id.isin(fund_info.index.array)]

        if asset_allocation is None:
            asset_allocation = FOFDataManager.get_fof_asset_allocation([FOFDataManager._FOF_ID])
        asset_allocation = asset_allocation.loc[asset_allocation.asset_type == HoldingAssetType.HEDGE, :]
        asset_allocation = asset_allocation.set_index('confirmed_date')

        trading_day_list = BasicDataApi().get_trading_day_list(start_date=df.datetime.sort_values().array[0], end_date=datetime.datetime.now().date())
        nav = df.pivot(index='datetime', columns='fund_id', values=['net_asset_value', 'acc_unit_value']).reindex(trading_day_list.datetime).ffill().stack().reset_index(level='fund_id')

        v_nav_result = []
        datas_to_calc_v = defaultdict(list)
        for row in nav.itertuples():
            try:
                one = asset_allocation.loc[[row.Index], :].loc[asset_allocation.fund_id == row.fund_id, :]
            except KeyError:
                pass
            else:
                for one_in_date in one.itertuples():
                    if one_in_date.event_type in (FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD) and one_in_date.status == FundStatus.DONE:
                        assert one_in_date.fund_id in datas_to_calc_v, '!!!!'
                        fund_data = datas_to_calc_v[one_in_date.fund_id]
                        if one_in_date.event_type == FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME:
                            total_share = one_in_date.share
                        else:
                            total_share = -one_in_date.share
                        for a_trade in fund_data:
                            assert a_trade[1] < one_in_date.Index, '!!!'
                            total_share += a_trade[2]
                        datas_to_calc_v[one_in_date.fund_id] = [(one_in_date.fund_id, one_in_date.Index, total_share, one_in_date.water_line)]
                    if one_in_date.event_type in (FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE, FOFTradeStatus.DIVIDEND_VOLUME) and one_in_date.status == FundStatus.DONE:
                        datas_to_calc_v[one_in_date.fund_id].append((one_in_date.fund_id, one_in_date.Index, one_in_date.share, one_in_date.water_line))

            df = pd.DataFrame(datas_to_calc_v[row.fund_id], columns=['fund_id', 'datetime', 'unit_total', 'water_line'])
            if df.empty:
                continue
            v_nav = FOFDataManager._do_calc_v_net_value(row.net_asset_value, df.unit_total, row.acc_unit_value, df.water_line, incentive_fee_ratio[row.fund_id], v_nav_decimals[row.fund_id])
            v_nav_result.append({'datetime': row.Index, 'fund_id': row.fund_id, 'v_nav': v_nav})
        df = pd.DataFrame.from_dict(v_nav_result)
        df = df.pivot(index='datetime', columns='fund_id', values='v_nav')
        return df

    def init(self, debug_mode=False):
        def _calc_water_line_and_confirmed_nav(x):
            x = x.reset_index()
            x_with_water_line = x[x.water_line.notna()]
            return pd.Series({'confirmed_nav': json.dumps(x[['share', 'nav']].to_dict(orient='records')),
                              'water_line': json.dumps(x_with_water_line[['share', 'water_line']].to_dict(orient='records'))})

        # 获取fof基本信息
        fof_info: Optional[pd.DataFrame] = FOFDataManager.get_fof_info([FOFDataManager._FOF_ID])
        assert fof_info is not None, f'get fof info for {FOFDataManager._FOF_ID} failed'

        self._MANAGEMENT_FEE_PER_YEAR = fof_info.management_fee
        self._CUSTODIAN_FEE_PER_YEAR = fof_info.custodian_fee
        self._ADMIN_SERVICE_FEE_PER_YEAR = fof_info.administrative_fee
        self._DEPOSIT_INTEREST_PER_YEAR = fof_info.current_deposit_rate
        self._SUBSCRIPTION_FEE = fof_info.subscription_fee
        self._ESTABLISHED_DATE = fof_info.established_date
        self._INCENTIVE_FEE_MODE = fof_info.incentive_fee_mode
        # FIXME 先hard code
        self._LAST_RAISING_PERIOD_INTEREST_DATE = datetime.date(2020, 12, 20)
        if debug_mode:
            print(f'fof info: (id){FOFDataManager._FOF_ID} (management_fee){self._MANAGEMENT_FEE_PER_YEAR} (custodian_fee){self._CUSTODIAN_FEE_PER_YEAR} '
                  f'(admin_service_fee){self._ADMIN_SERVICE_FEE_PER_YEAR} (current_deposit_rate){self._DEPOSIT_INTEREST_PER_YEAR} (subscription_fee){self._SUBSCRIPTION_FEE} '
                  f'(incentive fee mode){self._INCENTIVE_FEE_MODE}')

        # 获取FOF份额变化信息
        fof_scale = FOFDataManager.get_fof_scale_alteration([FOFDataManager._FOF_ID])
        # 客户认购/申购记录
        self._fof_scale = fof_scale[fof_scale.event_type.isin([FOFTradeStatus.SUBSCRIBE, FOFTradeStatus.PURCHASE])].set_index('applied_date')
        self._start_date = self._fof_scale.index.min()
        # 客户赎回记录
        self._fof_redemp = fof_scale[fof_scale.event_type.isin([FOFTradeStatus.REDEEM, ])].set_index('deposited_date')

        # trading_day_list = BasicDataApi().get_trading_day_list(start_date=self._start_date, end_date=datetime.datetime.now().date())
        # 将昨天作为end_date
        self._end_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        if debug_mode:
            print(f'(start_date){self._start_date} (end_date){self._end_date}')
        self._date_list: np.ndarray = pd.date_range(self._start_date, self._end_date).date

        # 获取fof持仓
        self._asset_allocation: Optional[pd.DataFrame] = FOFDataManager.get_fof_asset_allocation([FOFDataManager._FOF_ID])
        assert self._asset_allocation is not None, f'get fof pos for {FOFDataManager._FOF_ID} failed'

        # 这里不需要在途的持仓
        positions = self._asset_allocation.loc[self._asset_allocation.event_type.isin([FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE]) & (self._asset_allocation.status == FundStatus.DONE), :]

        self._water_line_and_confirmed_nav = positions.groupby(by='fund_id', sort=False).apply(_calc_water_line_and_confirmed_nav)
        self._total_cost = positions.pivot(index='confirmed_date', columns=['fund_id'], values='amount').sum()

        positions = positions.pivot(index='confirmed_date', columns=['asset_type', 'fund_id'], values='share')
        positions = positions.reindex(index=self._date_list).cumsum().ffill()
        # 持仓中的公募基金
        try:
            self._fund_pos = positions[HoldingAssetType.MUTUAL]
        except KeyError:
            print('no fund pos found')

        # 持仓中的私募基金
        try:
            self._hedge_pos = positions[HoldingAssetType.HEDGE]
        except KeyError:
            print('no hedge pos found')
        if debug_mode:
            print(self._hedge_pos)

        # 获取私募基金净值数据
        hedge_fund_list = list(self._hedge_pos.columns.unique())
        hedge_fund_nav = FOFDataManager.get_hedge_fund_nav(hedge_fund_list)
        hedge_fund_nav = hedge_fund_nav.pivot(index='datetime', columns='fund_id').reindex(index=self._date_list)
        self._hedge_nav = hedge_fund_nav['v_net_value']
        self._all_latest_nav = hedge_fund_nav['net_asset_value'].ffill().iloc[-1, :]
        self._all_latest_acc_nav = hedge_fund_nav['acc_unit_value'].ffill().iloc[-1, :]
        self._latest_nav_date = hedge_fund_nav['net_asset_value'].apply(lambda x: x[x.notna()].index.array[-1])

        # 我们自己算一下虚拟净值 然后拿它对_hedge_nav查缺补漏
        v_nav_calcd = FOFDataManager._calc_virtual_net_value(hedge_fund_list, self._asset_allocation)
        # 最后再ffill
        self._hedge_nav = self._hedge_nav.combine_first(v_nav_calcd.reindex(index=self._date_list)).ffill()
        if debug_mode:
            print(self._hedge_nav)
        self._hedge_latest_v_nav = self._hedge_nav.iloc[-1, :]

        # 获取人工手工校正信息
        manually = BasicDataApi().get_fof_manually([FOFDataManager._FOF_ID])
        self._manually = manually.set_index('datetime')

        incidental_trading = BasicDataApi().get_fof_incidental_statement([FOFDataManager._FOF_ID])
        self._incidental_trading = incidental_trading.set_index('datetime')

    def _get_hedge_mv(self) -> float:
        return (self._hedge_nav * self._hedge_pos).round(2).sum(axis=1).fillna(0)

    def _insert_errors_to_db_from_file(self, path: str = ''):
        '''将人工手工校正信息写入DB'''
        if not path:
            path = FOFDataManager._FILE_PATH
        errors: pd.DataFrame = pd.read_excel(path, sheet_name='2-1资产估值表（净值发布）', header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        errors = errors.loc[:, ['每日管理费误差', '每日行政服务费误差', '每日托管费误差']]
        errors = errors.droplevel(level=[0, 2], axis=0).droplevel(level=[1, 2], axis=1).rename_axis(columns='')
        errors = errors.rename_axis(index=['datetime']).reset_index()
        errors = errors.rename(columns={'每日管理费误差': 'management_fee_error', '每日行政服务费误差': 'admin_service_fee_error', '每日托管费误差': 'custodian_fee_error'})
        errors = errors[errors.notna().any(axis=1)].set_index('datetime').sort_index()

        manually = BasicDataApi().get_fof_manually([FOFDataManager._FOF_ID]).drop(columns=['update_time', 'create_time', 'is_deleted'])
        manually = manually.set_index('datetime')
        manually = manually.combine_first(errors)
        manually['fof_id'] = FOFDataManager._FOF_ID
        manually = manually.reset_index()
        print(manually)
        manually.to_sql(FOFManually.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')

    def _insert_nav_info_to_db_from_file(self, path: str = ''):
        '''将私募基金净值数据写入DB'''
        if not path:
            path = FOFDataManager._FILE_PATH
        nav: pd.DataFrame = pd.read_excel(path, sheet_name=1, header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        nav = nav.droplevel(level=0)
        nav = nav['私募标的净值']
        nav = nav.loc[(slice(None), 1), :]
        nav = nav.droplevel(level=1)
        nav = nav.stack(0).rename_axis(index=['datetime', 'fund_id'])
        nav = nav.rename(columns={'单位净值': 'net_asset_value', '累计净值': 'acc_unit_value', '虚拟净值': 'v_net_value'})
        nav = nav[nav.notna().any(axis=1)].sort_index(axis=0, level=0).reset_index()
        prog = re.compile('^.*[（(](.*)[）)]$')
        fund_id_list = [prog.search(one) for one in nav.fund_id]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        nav['fund_id'] = fund_id_list
        print(nav)
        nav.to_sql(HedgeFundNAV.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')

    def _read_data_from_file(self):
        # 解析私募基金净值数据
        nav: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=1, header=[0, 1, 2], index_col=[0, 1, 2], skipfooter=2)
        nav = nav['私募标的净值']
        nav = nav.swaplevel(axis=1)
        nav = nav['虚拟净值']
        prog = re.compile('^.*[（(](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in nav.columns]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        nav = nav.set_axis(labels=fund_id_list, axis=1)
        nav = nav.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        nav = nav[nav.trading_flag == 1]
        nav = nav.drop(columns=['id', 'trading_flag']).set_index('datetime')
        nav = nav.set_axis(pd.to_datetime(nav.index, infer_datetime_format=True).date, axis=0)
        nav = nav[nav.notna().any(axis=1)].sort_index()

        # 解析持仓公募基金数据
        whole_pos: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=2, header=[0, 1, 2], index_col=[0, 1, 2])
        mutual_fund_pos = whole_pos.loc[:, ('公募标的（份额）', slice(None), '份额')]
        mutual_fund_pos = mutual_fund_pos.droplevel(level=[0, 2], axis=1)
        mutual_fund_pos = mutual_fund_pos.loc[:, mutual_fund_pos.notna().any(axis=0)]
        prog = re.compile('^.*\n[（()](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in mutual_fund_pos.columns]
        assert None not in fund_id_list, 'parse mutual fund id failed!!'
        fund_id_list = [one.group(1) + '!0' for one in fund_id_list]
        mutual_fund_pos = mutual_fund_pos.set_axis(labels=fund_id_list, axis=1)
        mutual_fund_pos = mutual_fund_pos.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        mutual_fund_pos = mutual_fund_pos[mutual_fund_pos.trading_flag == 1]
        mutual_fund_pos = mutual_fund_pos.drop(columns=['id', 'trading_flag']).set_index('datetime')
        mutual_fund_pos = mutual_fund_pos.set_axis(pd.to_datetime(mutual_fund_pos.index, infer_datetime_format=True).date, axis=0)
        self._fund_pos = mutual_fund_pos[mutual_fund_pos.notna().any(axis=1)].sort_index()
        self._start_date = self._fund_pos.index.min()
        self._end_date = self._fund_pos.index.max()
        print(f'start date: {self._start_date}')
        print(f'end date: {self._end_date}')

        # 解析持仓私募基金数据
        pos: pd.DataFrame = whole_pos.loc[:, '私募标的']
        pos = pos.swaplevel(axis=1)
        pos = pos['份额']
        prog = re.compile('^.*\n[（()](.*)[）)]$')
        fund_id_list = [prog.search(col) for col in pos.columns]
        assert None not in fund_id_list, 'parse hedge fund id failed!!'
        fund_id_list = [one.group(1) for one in fund_id_list]
        pos = pos.set_axis(labels=fund_id_list, axis=1)
        pos = pos.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        pos = pos[pos.trading_flag == 1]
        pos = pos.drop(columns=['id', 'trading_flag']).set_index('datetime')
        pos = pos.set_axis(pd.to_datetime(pos.index, infer_datetime_format=True).date, axis=0)
        pos = pos[pos.notna().any(axis=1)].sort_index()
        self._hedge_nav = nav
        self._hedge_pos = pos

        # 解析杂项费用、收入数据
        misc_fees: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name=2, header=[0, 1, 2], index_col=[0, 1, 2])
        misc_fees = misc_fees.loc[:, ['银行活期', '在途资金', '累计应收银行\n存款利息', '应收募集期\n利息', '累计计提\n管理费\n（修正）', '累计计提行政\n服务费\n（修正）', '累计计提\n托管费\n（修正）']]
        misc_fees = misc_fees.droplevel(level=[1, 2], axis=1).rename_axis(columns='')
        misc_fees = misc_fees.rename_axis(index=['id', 'datetime', 'trading_flag']).reset_index()
        misc_fees = misc_fees[misc_fees.trading_flag == 1]
        misc_fees = misc_fees.drop(columns=['id', 'trading_flag']).set_index('datetime')
        misc_fees = misc_fees.set_axis(pd.to_datetime(misc_fees.index, infer_datetime_format=True).date, axis=0)
        misc_fees = misc_fees[misc_fees.notna().any(axis=1)].sort_index()
        self._misc_fees = (misc_fees * FOFDataManager._FEES_FLAG).fillna(0).sum(axis=1)

        # 解析投资人持仓数据
        investor_share: pd.DataFrame = pd.read_excel(FOFDataManager._FILE_PATH, sheet_name='4-2投资人份额变更表', header=0, index_col='到账日期', parse_dates=True)
        investor_share = investor_share.rename_axis(index='datetime')
        self._investor_share = investor_share['确认份额'].groupby(level=0).sum().cumsum()

    def calc_fof_nav(self, dump_to_db=True, is_from_excel=False, debug_mode=False):
        if is_from_excel:
            self._read_data_from_file()
        else:
            self.init(debug_mode)

        # 根据公募基金持仓获取相应基金的净值
        fund_nav: Optional[pd.DataFrame] = BasicDataApi().get_fund_nav_with_date_range(start_date=self._start_date, end_date=self._end_date, fund_list=self._fund_pos.columns.to_list())
        assert fund_nav is not None, f'get fund nav of {self._fund_pos.columns.to_list()} failed'
        fund_nav = fund_nav.pivot(index='datetime', columns='fund_id')
        self._latest_nav_date = self._latest_nav_date.append(fund_nav['unit_net_value'].apply(lambda x: x[x.notna()].index.array[-1].date()))
        fund_nav = fund_nav.reindex(index=self._date_list).ffill()
        self._all_latest_acc_nav = self._all_latest_acc_nav.append(fund_nav['acc_net_value'].iloc[-1, :])
        fund_nav = fund_nav['unit_net_value']
        self._all_latest_nav = self._all_latest_nav.append(fund_nav.iloc[-1, :])
        # 公募基金总市值
        fund_mv: pd.DataFrame = (self._fund_pos * fund_nav).round(2).sum(axis=1).fillna(0)

        if is_from_excel:
            # 净资产 = 公募基金总市值 + 私募基金总市值 + 其他各项收入、费用的净值
            net_assets = fund_mv.add(self._get_hedge_mv(), fill_value=0).add(self._misc_fees, fill_value=0)
            print(net_assets)

            # NAV = 净资产 / 总份额
            investor_share = self._investor_share.reindex(index=net_assets.index).ffill()
            self._fof_nav = net_assets / investor_share
            print(self._fof_nav.round(4))
        else:
            # 获取FOF资产配置信息
            asset_alloc = self._asset_allocation.set_index('deposited_date')
            asset_redemp = self._asset_allocation.set_index('confirmed_date')

            hedge_fund_mv = self._get_hedge_mv()

            # 循环遍历每一天来计算
            shares_list = pd.Series(dtype='float64', name='share')
            cash_list = pd.Series(dtype='float64', name='cash')
            fof_nav_list = pd.Series(dtype='float64', name='nav')
            today_fund_mv_list = pd.Series(dtype='float64', name='total_fund_mv')
            today_hedge_mv_list = pd.Series(dtype='float64', name='total_hedge_mv')
            net_assets_list = pd.Series(dtype='float64', name='net_asset')
            net_assets_fixed_list = pd.Series(dtype='float64', name='net_asset_fixed')
            misc_fees_list = pd.Series(dtype='float64', name='misc_fees')
            misc_amount_list = pd.Series(dtype='float64', name='misc_amount')
            deposit_interest_list = pd.Series(dtype='float64', name='deposit_interest')
            positions_list = pd.Series(dtype='float64', name='positions')
            other_debt_list = pd.Series(dtype='float64', name='other_debt')
            investor_pos_list = []
            trades_in_transit = {}
            redemps_in_transit = {}
            deposit_in_transit = []
            fee_details_part_list = []
            cash_details_part_list = []
            cash_in_transit_part_list = []
            cash_flow_amount_list = []
            for date in self._date_list:
                try:
                    # 看看当天有没有申请买入FOF 以申请日期做KEY
                    scale_data = self._fof_scale.loc[[date], :]
                except KeyError:
                    pass
                else:
                    # 后边都是汇总信息了 所以在这里先加一下记录
                    investor_pos_list.append(scale_data.loc[:, ['fof_id', 'investor_id', 'amount', 'share', 'event_type']])

                    deposited_date = scale_data.iloc[0, :].deposited_date
                    confirmed_date = scale_data.iloc[0, :].datetime
                    deposit_in_transit.append([confirmed_date, deposited_date, scale_data.amount.sum(), scale_data.share.sum(), False])

                total_amount = 0
                share_increased = 0
                if cash_list.empty:
                    total_cash = 0
                else:
                    total_cash = cash_list.iat[-1]

                # 计算那些仍然在途的入金和份额增加
                deposit_done = []
                deposit_amount_in_transit = 0
                other_debt_sum = 0
                for one in deposit_in_transit:
                    if (date < one[0]) and (date < one[1]):
                        continue
                    if one[0] < one[1]:
                        # 先是确认日期 再是交割日期 份额增加了但资金稍后进来 即存在应收账款
                        if not one[4]:
                            assert not pd.isnull(one[3]), '!!!'
                            share_increased += one[3]
                            one[4] = True
                        if date >= one[1]:
                            assert not pd.isnull(one[2]), '!!!'
                            total_amount += one[2]
                            cash_flow_amount_list.append({'datetime': one[1], 'event_type': FOFStatementStatus.IN_INVESTOR, 'amount': one[2]})
                            deposit_done.append(deposit_in_transit.index(one))
                        else:
                            # 如果没到，也要把他们统计进来，不计算利息，但应该计入净资产中
                            deposit_amount_in_transit += one[2]
                    elif one[1] < one[0]:
                        # 先是交割日期 再是确认日期 资金进来了但份额稍后增加 即存在应付账款
                        if not one[4]:
                            assert not pd.isnull(one[2]), '!!!'
                            total_amount += one[2]
                            other_debt_sum += one[2]
                            cash_flow_amount_list.append({'datetime': one[1], 'event_type': FOFStatementStatus.IN_INVESTOR, 'amount': one[2]})
                            one[4] = True
                        if date >= one[0]:
                            assert not pd.isnull(one[3]), '!!!'
                            share_increased += one[3]
                            other_debt_sum -= one[2]
                            deposit_done.append(deposit_in_transit.index(one))
                    else:
                        if date >= one[0]:
                            assert not pd.isnull(one[2]), '!!!'
                            total_amount += one[2]
                            assert not pd.isnull(one[3]), '!!!'
                            share_increased += one[3]
                            cash_flow_amount_list.append({'datetime': one[1], 'event_type': FOFStatementStatus.IN_INVESTOR, 'amount': one[2]})
                            deposit_done.append(deposit_in_transit.index(one))
                    other_debt_list.loc[date] = round(other_debt_sum, 2)
                for one in deposit_done:
                    del deposit_in_transit[one]

                total_cash += total_amount
                total_cash = round(total_cash, 2)
                share_increased = round(share_increased, 2)

                try:
                    # 看看当天有没有卖出FOF
                    redemp_data = self._fof_redemp.loc[[date], :]
                except KeyError:
                    # 处理没有赎回的情况
                    total_amount_redemp = 0
                else:
                    # 后边都是汇总信息了 所以在这里先加一下记录
                    investor_pos_list.append(redemp_data.loc[:, ['fof_id', 'investor_id', 'amount', 'share', 'event_type']])

                    # TODO 处理水位线
                    # 汇总今天所有的赎回资金
                    total_amount_redemp = redemp_data.amount.sum()
                    share_increased -= redemp_data.share.sum()
                    total_cash -= total_amount_redemp
                    cash_flow_amount_list.append({'datetime': date, 'event_type': FOFStatementStatus.OUT_INVESTOR, 'amount': total_amount_redemp})
                finally:
                    share_increased = round(share_increased, 2)
                    total_cash = round(total_cash, 2)

                if not math.isclose(total_amount, 0) or not math.isclose(total_amount_redemp, 0):
                    if debug_mode:
                        print(f'{self._FOF_ID} share changed (date){date} (amount){total_amount} (redemp_amount){total_amount_redemp} (share){share_increased}')

                # 这个日期之后才正式成立，所以在此之前都不需要处理后续步骤
                if date < self._ESTABLISHED_DATE:
                    cash_list.loc[date] = total_cash
                    if share_increased > 0:
                        shares_list.loc[date] = share_increased
                    continue

                try:
                    # 看看当天有没有投出去，继而产生在途资金
                    cash_in_transit = 0
                    today_asset_alloc = asset_alloc.loc[[date], :]
                    for row in today_asset_alloc.itertuples():
                        if row.event_type in (FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE):
                            assert not pd.isnull(row.amount), '!!!'
                            cash_in_transit += row.amount
                            cash_flow_amount_list.append({'datetime': date, 'event_type': FOFStatementStatus.OUT_HEDGE, 'amount': row.amount})
                            if row.confirmed_date != row.Index or row.status == FundStatus.IN_TRANSIT:
                                # 如果没有到 confirmed_date 或状态是仍然在途，需要把它们记下来
                                trades_in_transit[row.id] = (row.Index, row.confirmed_date, row.amount, row.fund_id)
                        if row.event_type in (FOFTradeStatus.DEDUCT_REWARD, FOFTradeStatus.DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME):
                            assert not pd.isnull(row.share), '!!!'
                            # 业绩报酬计提扣除份额完成
                            if row.status == FundStatus.DONE:
                                if row.event_type in (FOFTradeStatus.DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME):
                                    self._hedge_pos.loc[self._hedge_pos.index >= date, row.fund_id] += row.share
                                else:
                                    self._hedge_pos.loc[self._hedge_pos.index >= date, row.fund_id] -= row.share
                                # 重刷hedge_fund_mv
                                hedge_fund_mv = self._get_hedge_mv()
                        if row.event_type == FOFTradeStatus.DIVIDEND_CASH:
                            total_cash += row.amount
                            cash_flow_amount_list.append({'datetime': date, 'event_type': FOFStatementStatus.IN_HEDGE_DIVIDEND, 'amount': row.amount})
                    assert total_cash >= cash_in_transit, f'no enough cash to buy asset!! (date){date} (total cash){total_cash} (cash in transit){cash_in_transit}'
                    total_cash -= cash_in_transit
                except KeyError:
                    cash_in_transit = 0

                # 计算那些仍然在途的资金
                trades_done = []
                for row_id, one in trades_in_transit.items():
                    # 当天就不处理了(在上边处理过了)
                    if one[0] == date:
                        continue
                    if one[1] is not None:
                        if date >= one[1]:
                            # 到confirmed_date了，把这些记录记下来，后续可以删除
                            trades_done.append(row_id)
                            # confirmed当天就不把amount计进来了
                            if date == one[1]:
                                continue
                    cash_in_transit += one[2]
                for one in trades_done:
                    data = trades_in_transit[one]
                    cash_in_transit_part_list.append({'confirmed_datetime': data[1], 'event_type': FOFStatementStatus.OUT_HEDGE, 'amount': data[2], 'fund_id': data[3], 'transit_cash': cash_in_transit})
                    del trades_in_transit[one]

                try:
                    today_asset_redemp = asset_redemp.loc[[date], :]
                    for row in today_asset_redemp.itertuples():
                        if row.event_type in (FOFTradeStatus.REDEEM, ):
                            self._hedge_pos.loc[self._hedge_pos.index >= date, row.fund_id] -= row.share
                            if row.deposited_date != date or row.status == FundStatus.IN_TRANSIT:
                                if not pd.isnull(row.deposited_date):
                                    # 如果没有到 deposited_date 或状态是仍然在途，需要把它们记下来
                                    redemps_in_transit[row.id] = (row.Index, row.deposited_date, row.amount, row.fund_id)
                            else:
                                total_cash += row.amount
                                cash_flow_amount_list.append({'datetime': date, 'event_type': FOFStatementStatus.IN_HEDGE, 'amount': row.amount})
                except KeyError:
                    pass

                # 计算那些仍然在途的资金
                redemps_done = []
                for row_id, one in redemps_in_transit.items():
                    if date >= one[1]:
                        # 到 deposited_date 了，把这些记录记下来，后续可以删除
                        redemps_done.append(row_id)
                        # deposited当天就不把amount计进来了
                        if date == one[1]:
                            total_cash += row.amount
                            cash_flow_amount_list.append({'datetime': date, 'event_type': FOFStatementStatus.IN_HEDGE, 'amount': row.amount})
                            continue
                    cash_in_transit += one[2]
                for one in redemps_done:
                    data = redemps_in_transit[one]
                    cash_in_transit_part_list.append({'confirmed_datetime': data[1], 'event_type': FOFStatementStatus.IN_HEDGE, 'amount': data[2], 'fund_id': data[3], 'transit_cash': cash_in_transit})
                    del redemps_in_transit[one]
                cash_in_transit = round(cash_in_transit, 2)

                # 应收募集期利息 TODO 暂时先hard code了
                if date <= self._LAST_RAISING_PERIOD_INTEREST_DATE:
                    raising_period_interest = 77.78
                else:
                    raising_period_interest = 0
                # 计提管理费, 计提行政服务费, 计提托管费
                if not net_assets_list.empty:
                    fees_in_separate_items = (net_assets_list.iat[-1] * pd.Series([self._MANAGEMENT_FEE_PER_YEAR, self._CUSTODIAN_FEE_PER_YEAR, self._ADMIN_SERVICE_FEE_PER_YEAR]) / self._get_days_this_year_for_fee(date)).round(2)
                    misc_fees = fees_in_separate_items.sum()
                    fee_details_part = fees_in_separate_items.set_axis(['management_fee', 'custodian_fee', 'administrative_fee']).to_dict()
                    fee_details_part['pre_market_value'] = net_assets_list.iat[-1]
                else:
                    misc_fees = 0
                    fee_details_part = {}

                try:
                    incidental_trading = self._incidental_trading.loc[[date], :]
                except KeyError:
                    incidental_trading = None

                # 处理人工手工校正的一些数据
                # try:
                #     fee_transfer = self._manually.at[date, 'fee_transfer']
                #     if not pd.isnull(fee_transfer):
                #         fee_transfer = round(fee_transfer, 2)
                #         # 现金里扣掉的同时 累计计提费用也相应扣掉
                #         total_cash += fee_transfer
                #         misc_fees += fee_transfer
                # except KeyError:
                #     pass
                if incidental_trading is not None:
                    fee_transfer = 0
                    management_fee_transfer = incidental_trading.loc[incidental_trading.event_type.isin([FOFStatementStatus.OUT_MANAGEMENT, ]), 'amount'].sum()
                    fee_transfer += management_fee_transfer.sum()
                    custodian_fee_transfer = incidental_trading.loc[incidental_trading.event_type.isin([FOFStatementStatus.OUT_CUSTODIAN, ]), 'amount'].sum()
                    fee_transfer += custodian_fee_transfer.sum()
                    administrative_fee_transfer = incidental_trading.loc[incidental_trading.event_type.isin([FOFStatementStatus.OUT_ADMINISTRATIVE, ]), 'amount'].sum()
                    fee_transfer += administrative_fee_transfer.sum()

                    fee_transfer = round(fee_transfer, 2)
                    total_cash -= fee_transfer
                    misc_fees -= fee_transfer
                else:
                    management_fee_transfer = 0
                    custodian_fee_transfer = 0
                    administrative_fee_transfer = 0

                # try:
                #     other_fees = self._manually.at[date, 'other_fees']
                #     if not pd.isnull(other_fees):
                #         other_fees = round(other_fees, 2)
                #         # 只在现金里扣掉(或增加)
                #         total_cash += other_fees
                # except KeyError:
                #     pass
                if incidental_trading is not None:
                    cash_interest = incidental_trading.loc[incidental_trading.event_type.isin([FOFStatementStatus.IN_INTEREST, FOFStatementStatus.IN_OTHER_IN]), 'amount']
                    if not cash_interest.empty:
                        cash_interest = round(cash_interest.sum(), 2)
                        total_cash += cash_interest

                    other_fees = incidental_trading.loc[incidental_trading.event_type.isin([FOFStatementStatus.OUT_OTHER_OUT]), 'amount']
                    if not other_fees.empty:
                        other_fees = round(other_fees.sum(), 2)
                        total_cash -= other_fees
                cash_list.loc[date] = total_cash

                # 应收银行存款利息
                deposit_interest = round(cash_list.iat[-1] * self._DEPOSIT_INTEREST_PER_YEAR / self._DAYS_PER_YEAR_FOR_INTEREST, 2)
                pure_deposit_interest = deposit_interest

                # try:
                #     cd_interest_transfer = self._manually.at[date, 'cd_interest_transfer']
                #     if not pd.isnull(cd_interest_transfer):
                #         cd_interest_transfer = round(cd_interest_transfer, 2)
                #         # 应计利息相应扣掉
                #         deposit_interest += cd_interest_transfer
                # except KeyError:
                #     pass
                if incidental_trading is not None:
                    cd_interest_transfer = incidental_trading.loc[incidental_trading.event_type.isin([FOFStatementStatus.IN_INTEREST]), 'amount']
                    if not cd_interest_transfer.empty:
                        cd_interest_transfer = round(cd_interest_transfer.sum(), 2)
                        # 应计利息相应扣掉
                        deposit_interest -= cd_interest_transfer

                # 记录一些信息
                if deposit_interest_list.empty:
                    deposit_interest_list.loc[date] = deposit_interest
                else:
                    deposit_interest_list.loc[date] = deposit_interest_list.iat[-1] + deposit_interest
                cash_details_part_list.append({'date': date, 'remain_cash': total_cash, 'interest': pure_deposit_interest, 'total_interest': deposit_interest_list.iat[-1]})

                if misc_fees_list.empty:
                    misc_fees_list.loc[date] = misc_fees
                else:
                    misc_fees_list.loc[date] = misc_fees_list.iat[-1] + misc_fees
                misc_amount = total_cash + cash_in_transit + deposit_amount_in_transit + deposit_interest_list.iat[-1] + raising_period_interest - misc_fees_list.iat[-1]
                misc_amount_list.loc[date] = misc_amount
                if fee_details_part:
                    if len(fee_details_part_list) == 0:
                        fee_details_part['total_management_fee'] = fee_details_part['management_fee']
                        fee_details_part['total_custodian_fee'] = fee_details_part['custodian_fee']
                        fee_details_part['total_administrative_fee'] = fee_details_part['administrative_fee']
                    else:
                        last_day_data = fee_details_part_list[-1]
                        fee_details_part['total_management_fee'] = last_day_data['total_management_fee'] + fee_details_part['management_fee']
                        fee_details_part['total_custodian_fee'] = last_day_data['total_custodian_fee'] + fee_details_part['custodian_fee']
                        fee_details_part['total_administrative_fee'] = last_day_data['total_administrative_fee'] + fee_details_part['administrative_fee']

                    fee_details_part['total_management_fee'] -= management_fee_transfer
                    fee_details_part['total_custodian_fee'] -= custodian_fee_transfer
                    fee_details_part['total_administrative_fee'] -= administrative_fee_transfer
                    fee_details_part['date'] = pd.to_datetime(date, infer_datetime_format=True).date()
                    fee_details_part_list.append(fee_details_part)

                # 获取持仓中当日公募、私募基金的MV
                try:
                    today_fund_mv = fund_mv.loc[date]
                except KeyError:
                    today_fund_mv = 0
                today_fund_mv_list.loc[date] = today_fund_mv
                try:
                    today_hedge_mv = hedge_fund_mv.loc[date]
                except KeyError:
                    today_hedge_mv = 0
                today_hedge_mv_list.loc[date] = today_hedge_mv

                # other_debt_sum = 0
                # if incidental_trading is not None:
                #     other_debt = incidental_trading.loc[incidental_trading.event_type.isin([FOFStatementStatus.OUT_OTHER_DEBT]), 'amount']
                #     if not other_debt.empty:
                #         other_debt = round(other_debt.sum(), 2)
                #         other_debt_sum += other_debt
                #     other_debt_offset = incidental_trading.loc[incidental_trading.event_type.isin([FOFStatementStatus.IN_OTHER_DEBT_OFFSET]), 'amount']
                #     if not other_debt_offset.empty:
                #         other_debt_offset = round(other_debt_offset.sum(), 2)
                #         other_debt_sum -= other_debt_offset
                # other_debt_list.loc[date] = other_debt_sum

                # 计算净资产
                today_net_assets = today_fund_mv + today_hedge_mv + misc_amount - other_debt_list.sum()
                net_assets_list.loc[date] = today_net_assets

                try:
                    fund_pos_info = pd.concat([self._fund_pos.loc[date, :].rename('share'), fund_nav.loc[date, :].rename('nav')], axis=1)
                    fund_pos_info = fund_pos_info[fund_pos_info.share.notna()]
                    fund_pos_info['asset_type'] = HoldingAssetType.MUTUAL
                except KeyError:
                    fund_pos_info = None
                try:
                    hedge_pos_info = pd.concat([self._hedge_pos.loc[date, :].rename('share'), self._hedge_nav.loc[date, :].rename('nav')], axis=1)
                    hedge_pos_info = hedge_pos_info[hedge_pos_info.share.notna()]
                    hedge_pos_info['asset_type'] = HoldingAssetType.HEDGE
                except KeyError:
                    hedge_pos_info = None
                if fund_pos_info is not None or hedge_pos_info is not None:
                    position = pd.concat([fund_pos_info, hedge_pos_info], axis=0).rename_axis(index='fund_id').reset_index()
                    positions_list.loc[date] = json.dumps(position.to_dict(orient='records'))

                # 计算修正净资产
                try:
                    errors_to_be_fixed = self._manually.loc[self._manually.index <= date, ['admin_service_fee_error', 'custodian_fee_error', 'management_fee_error']].round(2).sum(axis=1).sum()
                except KeyError:
                    errors_to_be_fixed = 0
                today_net_assets_fixed = today_net_assets + errors_to_be_fixed
                net_assets_fixed_list.loc[date] = today_net_assets_fixed

                # 如果今日有投资人申购fof 记录下来
                if share_increased > 0:
                    shares_list.loc[date] = share_increased
                # 计算fof的nav
                if shares_list.sum() != 0:
                    fof_nav = today_net_assets_fixed / shares_list.sum()
                else:
                    fof_nav = 1
                fof_nav_list.loc[date] = round(fof_nav, 4)
            # 汇总所有信息
            if debug_mode:
                total_info = pd.concat([shares_list, cash_list, fof_nav_list, today_fund_mv_list, today_hedge_mv_list, net_assets_list, net_assets_fixed_list, misc_amount_list, misc_fees_list, deposit_interest_list, positions_list], axis=1).sort_index()
                print(total_info)
            self._fof_nav = pd.concat([fof_nav_list, net_assets_list, shares_list.cumsum()], axis=1).sort_index().rename_axis('datetime').reset_index()
            self._fof_nav['share'] = self._fof_nav.share.ffill()
            self._fof_nav = self._fof_nav[self._fof_nav.datetime >= self._ESTABLISHED_DATE]
            self._fof_nav['fof_id'] = FOFDataManager._FOF_ID
            # TODO: 暂时先直接用 nav 给 acc_net_value 和 adjusted_nav 赋值
            self._fof_nav['acc_net_value'] = self._fof_nav.nav
            self._fof_nav['adjusted_nav'] = self._fof_nav.nav
            self._fof_nav['ret'] = self._fof_nav.adjusted_nav / self._fof_nav.adjusted_nav.array[0] - 1

            self._fof_position = positions_list.rename_axis('datetime').to_frame(name='position').reset_index()
            self._fof_position['fof_id'] = FOFDataManager._FOF_ID

            self._fof_investor_pos = pd.concat(investor_pos_list).rename(columns={'share': 'shares'}).reset_index(drop=True)
            self._fof_investor_pos = self._fof_investor_pos.groupby(by=['fof_id', 'investor_id'], sort=False).sum().reset_index()
            self._fof_investor_pos['datetime'] = date

            self._fof_fee_details = pd.DataFrame(fee_details_part_list)
            self._fof_fee_details['fof_id'] = FOFDataManager._FOF_ID

            self._fof_cash_details = pd.DataFrame(cash_details_part_list)
            self._fof_cash_details['fof_id'] = FOFDataManager._FOF_ID

            self._fof_cash_in_transit = pd.DataFrame(cash_in_transit_part_list)
            self._fof_cash_in_transit['fof_id'] = FOFDataManager._FOF_ID

            self._fof_cash_flow_amount = pd.DataFrame(cash_flow_amount_list)
            self._fof_cash_flow_amount['fof_id'] = FOFDataManager._FOF_ID

            self._total_net_assets = net_assets_list.array[-1]
            self._total_shares = shares_list.sum()

            asset_type = pd.Series(HoldingAssetType.HEDGE, index=self._hedge_pos.columns, name='asset_type')
            asset_type = asset_type.append(pd.Series(HoldingAssetType.MUTUAL, index=self._fund_pos.columns, name='asset_type'))
            all_pos = self._hedge_pos.iloc[-1, :].append(self._fund_pos.iloc[-1, :]).rename('total_shares')
            latest_mv = all_pos * self._all_latest_nav
            dividend = self._asset_allocation.loc[self._asset_allocation.event_type.isin([FOFTradeStatus.DIVIDEND_CASH, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_CASH]), :].pivot(index='confirmed_date', columns='fund_id', values='amount').sum()
            redemptions = self._asset_allocation.loc[self._asset_allocation.event_type == FOFTradeStatus.REDEEM, :].pivot(index='confirmed_date', columns='fund_id', values='share').sum()
            total_ret = latest_mv.add(dividend, fill_value=0).add(redemptions, fill_value=0).sub(self._total_cost)
            total_rr = total_ret / self._total_cost
            fof_position_details_list = [self._latest_nav_date.rename('datetime'), asset_type, all_pos, total_ret.rename('total_ret'), total_rr.rename('total_rr'), self._total_cost.rename('total_cost'), self._all_latest_nav.rename('nav'),
                                         self._all_latest_acc_nav.rename('acc_nav'), self._hedge_latest_v_nav.rename('v_nav'), latest_mv.rename('latest_mv')]
            self._fof_position_details = self._water_line_and_confirmed_nav.join(fof_position_details_list, how='outer')
            self._fof_position_details = self._fof_position_details.rename_axis(index='fund_id').reset_index()
            self._fof_position_details['fof_id'] = FOFDataManager._FOF_ID

        if dump_to_db:
            self.dump_fof_nav_and_pos_to_db(debug_mode)
        else:
            print(self._fof_nav)

    def dump_fof_nav_and_pos_to_db(self, debug_mode=False) -> bool:
        ret = False
        if self._fof_nav is not None:
            renamed_fof_nav = self._fof_nav.rename(columns={'net_asset': 'mv', 'share': 'volume'})
            now_df = DerivedDataApi().get_fof_nav([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted']).astype(renamed_fof_nav.dtypes.to_dict())
                # merge on all columns
                df = renamed_fof_nav.round(6).merge(now_df.round(6), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = renamed_fof_nav
            if debug_mode:
                print(df)
            if not df.empty:
                for date in df.datetime.unique():
                    DerivedDataApi().delete_fof_nav(date_to_delete=date, fof_id_list=df[df.datetime == date].fof_id.to_list())
                df.to_sql(FOFNav.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
                # self._wechat_bot.send_fof_nav_update(df)
                ret = True
            print('[dump_fof_nav_and_pos_to_db] dump nav done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no nav, should calc it first')
        fof_nav = FOFDataManager.get_fof_nav(FOFDataManager._FOF_ID)
        fof_nav = fof_nav.set_index('datetime').sort_index()
        fof_latest_acc_nav = fof_nav.acc_net_value.array[-1]
        fof_latest_adjusted_nav = fof_nav.adjusted_nav.array[-1]
        fof_nav = fof_nav.nav
        nav = fof_nav.array[-1]
        mv = (self._fof_scale.share.sum() - self._fof_redemp.share.sum()) * nav
        total_ret = fof_nav.array[-1] / fof_nav.array[0] - 1
        if ret:
            Session = sessionmaker(BasicDatabaseConnector().get_engine())
            db_session = Session()
            fof_info_to_set = db_session.query(FOFInfo).filter(FOFInfo.fof_id == self._FOF_ID).one_or_none()
            fof_info_to_set.net_asset_value = float(nav) if not pd.isnull(nav) else None
            fof_info_to_set.acc_unit_value = float(fof_latest_acc_nav) if not pd.isnull(fof_latest_acc_nav) else None
            fof_info_to_set.adjusted_net_value = float(fof_latest_adjusted_nav) if not pd.isnull(fof_latest_adjusted_nav) else None
            fof_info_to_set.total_volume = float(self._total_shares) if not pd.isnull(self._total_shares) else None
            fof_info_to_set.total_amount = float(self._total_net_assets) if not pd.isnull(self._total_net_assets) else None
            fof_info_to_set.latest_cal_date = fof_nav.index.array[-1]
            db_session.commit()
            db_session.close()

        if self._fof_position is not None:
            now_df = DerivedDataApi().get_fof_position([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted'])
                # merge on all columns
                df = self._fof_position.merge(now_df, how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_position
            if debug_mode:
                print(df)
            if not df.empty:
                for date in df.datetime.unique():
                    DerivedDataApi().delete_fof_position(date_to_delete=date, fof_id_list=df[df.datetime == date].fof_id.to_list())
                df.to_sql(FOFPosition.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump position done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no position, should calc it first')

        if self._fof_position_details is not None:
            now_df = DerivedDataApi().get_fof_position_detail([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted']).astype(self._fof_position_details.dtypes.to_dict())
                # merge on all columns
                df = self._fof_position_details.round(4).merge(now_df.round(4), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_position_details
            if debug_mode:
                print(df)
            if not df.empty:
                for fof_id in df.fof_id.unique():
                    DerivedDataApi().delete_fof_position_detail(fof_id_to_delete=fof_id, fund_id_list=df[df.fof_id == fof_id].fund_id.to_list())
                df.to_sql(FOFPositionDetail.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump position detail done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no position detail, should calc it first')

        investor_return_df = FOFDataManager().get_investor_return(fof_id=FOFDataManager._FOF_ID)
        if investor_return_df is not None:
            investor_return_df = investor_return_df.drop(columns=['total_rr']).rename(columns={'latest_mv': 'mv'})
            now_df = FOFDataManager().get_fof_investor_position([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted'])
                now_df = now_df.astype(investor_return_df.dtypes.to_dict())
                # merge on all columns
                df = investor_return_df.reset_index().round(4).merge(now_df.round(4), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = investor_return_df
            if debug_mode:
                print(df)
            if not df.empty:
                for fof_id in df.fof_id.unique():
                    BasicDataApi().delete_fof_investor_position(fof_id_to_delete=fof_id, investor_id_list=df[df.fof_id == fof_id].investor_id.to_list())
                df.to_sql(FOFInvestorPosition.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump investor position done')

            now_df = FOFDataManager().get_fof_investor_data([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'is_deleted'])
                # merge on all columns
                df = investor_return_df[['fof_id', 'amount']].rename(columns={'amount': 'total_investment'}).reset_index().round(4).merge(now_df.round(4), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = investor_return_df[['fof_id', 'amount']]
            if debug_mode:
                print(df)
            if not df.empty:
                for fof_id in df.fof_id.unique():
                    DerivedDataApi().delete_fof_investor_data(fof_id_to_delete=fof_id, investor_id_list=df[df.fof_id == fof_id].investor_id.to_list())
                df.to_sql(FOFInvestorData.__table__.name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump investor data done')
        else:
            print('[dump_fof_nav_and_pos_to_db] get investor position failed')

        if self._fof_fee_details is not None:
            now_df = FOFDataManager().get_fof_estimate_fee([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['id', 'is_down', 'remark', 'update_time', 'create_time', 'is_deleted'])
                now_df = now_df.astype(self._fof_fee_details.dtypes.to_dict())
                # merge on all columns
                df = self._fof_fee_details.round(6).merge(now_df.round(6), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_fee_details
            if debug_mode:
                print(df)
            if not df.empty:
                for date in df.date.unique():
                    BasicDataApi().delete_fof_estimate_fee(date_to_delete=date, fof_id_list=df[df.date == date].fof_id.to_list())
                df.to_sql(FOFEstimateFee.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump fee details done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no fee details data, should calc it first')

        if self._fof_cash_details is not None:
            now_df = FOFDataManager().get_fof_estimate_interest([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['id', 'remark', 'update_time', 'create_time', 'is_deleted'])
                now_df = now_df.astype(self._fof_cash_details.dtypes.to_dict())
                # merge on all columns
                df = self._fof_cash_details.round(6).merge(now_df.round(6), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_cash_details
            if debug_mode:
                print(df)
            if not df.empty:
                for date in df.date.unique():
                    BasicDataApi().delete_fof_estimate_interest(date_to_delete=date, fof_id_list=df[df.date == date].fof_id.to_list())
                df.to_sql(FOFEstimateInterest.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump cash details done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no cash details data, should calc it first')

        if self._fof_cash_in_transit is not None:
            now_df = FOFDataManager().get_fof_transit_money([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['id', 'remark', 'update_time', 'create_time', 'is_deleted'])
                now_df = now_df.astype(self._fof_cash_in_transit.dtypes.to_dict())
                # merge on all columns
                df = self._fof_cash_in_transit.round(6).merge(now_df.round(6), how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_cash_in_transit
            if debug_mode:
                print(df)
            if not df.empty:
                for date in df.confirmed_datetime.unique():
                    BasicDataApi().delete_fof_transit_money(date_to_delete=date, fof_id_list=df[df.confirmed_datetime == date].fof_id.to_list())
                df.to_sql(FOFTransitMoney.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump cash in transit done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no cash in transit data, should calc it first')

        if self._fof_cash_flow_amount is not None:
            self._fof_cash_flow_amount = self._fof_cash_flow_amount.append(self._incidental_trading.drop(columns=['id', 'trade_num', 'remark', 'create_time', 'update_time', 'is_deleted']).reset_index())
            self._fof_cash_flow_amount['remain_cash'] = self._fof_cash_flow_amount.apply(lambda x: self._fof_cash_details.loc[(self._fof_cash_details.fof_id == x.fof_id) & (self._fof_cash_details.date == x.datetime), 'remain_cash'].array[0], axis=1)
            now_df = FOFDataManager().get_fof_account_statement([FOFDataManager._FOF_ID])
            if now_df is not None:
                now_df = now_df.drop(columns=['id', 'trade_num', 'remark', 'update_time', 'create_time', 'is_deleted'])
                now_df = now_df.astype(self._fof_cash_flow_amount.dtypes.to_dict())
                # merge on all columns
                df = self._fof_cash_flow_amount.round(6).merge(now_df.round(6), how='left', indicator=True, validate='many_to_many')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            else:
                df = self._fof_cash_flow_amount
            if debug_mode:
                print(df)
            if not df.empty:
                for date in df.datetime.unique():
                    BasicDataApi().delete_fof_account_statement(date_to_delete=date, fof_id_list=df[df.datetime == date].fof_id.to_list())
                df.to_sql(FOFAccountStatement.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            print('[dump_fof_nav_and_pos_to_db] dump cash flow amount done')
        else:
            print('[dump_fof_nav_and_pos_to_db] no cash flow amount data, should calc it first')

        if ret:
            try:
                # fof_info = FOFDataManager.get_fof_info([FOFDataManager._FOF_ID]).set_index('fof_id')
                res_status = Calculator.get_stat_result(fof_nav.index, fof_nav.array)
                fof_data = {
                    'start_date': res_status.start_date.isoformat(),
                    'days': (fof_nav.index.array[-1] - res_status.start_date).days,
                    'mv': mv,
                    'nav': round(nav, 4),
                    'total_ret': f'{round(total_ret * 100, 2)}%',
                    'sharpe': round(res_status.sharpe, 6),
                    'annualized_ret': f'{round(res_status.annualized_ret * 100, 2)}%',
                    'mdd': f'{round(res_status.mdd * 100, 2)}%',
                    'annualized_vol': round(res_status.annualized_vol, 6),
                }
                self._wechat_bot.send_fof_info(FOFDataManager._FOF_ID, fof_nav.index.array[-1], fof_data)
            except Exception as e:
                traceback.print_exc()
                self._wechat_bot.send_fof_info_failed(self._FOF_ID, e)

        # 把is_calculating的标记置为false
        Session = sessionmaker(BasicDatabaseConnector().get_engine())
        db_session = Session()
        fof_info_to_set = db_session.query(FOFInfo).filter(FOFInfo.fof_id == self._FOF_ID).one_or_none()
        fof_info_to_set.is_calculating = False
        db_session.commit()
        db_session.close()

    def _gather_asset_info_of_fof(self, fund_list: List[str], v_nav: pd.DataFrame):
        fof_aa = FOFDataManager.get_fof_asset_allocation([FOFDataManager._FOF_ID])
        hedge_nav = FOFDataManager.get_hedge_fund_nav(fund_list)
        trading_day = BasicDataApi().get_trading_day_list(start_date=hedge_nav.datetime.min(), end_date=hedge_nav.datetime.max())
        hedge_info = FOFDataManager.get_hedge_fund_info(fund_list).set_index('fund_id')
        for fund_id in fund_list:
            try:
                fund_fof_aa = fof_aa.loc[fof_aa.fund_id == fund_id, :]
                pur_sub_aa = fund_fof_aa[fund_fof_aa.event_type.isin([FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE])]
                if pur_sub_aa.empty:
                    continue
                redempt_aa = fund_fof_aa[fund_fof_aa.event_type.isin([FOFTradeStatus.REDEEM, ])]
                aa_insentive_info = fund_fof_aa[fund_fof_aa.event_type.isin([FOFTradeStatus.DEDUCT_REWARD, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_CASH])]
                aa_dividend_reinvestment = fund_fof_aa[fund_fof_aa.event_type.isin([FOFTradeStatus.DIVIDEND_VOLUME, FOFTradeStatus.DEDUCT_REWARD_AND_DIVIDEND_VOLUME])]
                fund_nav = hedge_nav[hedge_nav.fund_id == fund_id]
                # TODO 这里最好应该用复权净值
                fund_auv = fund_nav.set_index('datetime')['acc_unit_value']
                fund_auv = fund_auv.reindex(trading_day[trading_day.datetime.between(fund_auv.index.min(), fund_auv.index.max())].datetime).ffill()
                res_status = Calculator.get_stat_result(fund_auv.index, fund_auv.array)
                total_ret = fund_auv.array[-1] / fund_auv.array[0] - 1
                fund_data = {
                    'start_date': res_status.start_date.isoformat(),
                    'days': (fund_auv.index.array[-1] - res_status.start_date).days,
                    'nav': round(fund_nav.net_asset_value.array[-1], 4),
                    'total_ret': f'{round(total_ret * 100, 2)}%',
                    'sharpe': round(res_status.sharpe, 6),
                    'annualized_ret': f'{round(res_status.annualized_ret * 100, 2)}%',
                    'mdd': f'{round(res_status.mdd * 100, 2)}%',
                    'annualized_vol': round(res_status.annualized_vol, 6),
                }

                latest_nav_date = fund_nav.loc[:, 'datetime'].iat[-1]
                Session = sessionmaker(BasicDatabaseConnector().get_engine())
                db_session = Session()
                fof_info_to_set = db_session.query(HedgeFundInfo).filter(HedgeFundInfo.fund_id == fund_id).one_or_none()
                fof_info_to_set.latest_cal_date = latest_nav_date
                fof_info_to_set.net_asset_value = float(fund_nav.net_asset_value.array[-1]) if not pd.isnull(fund_nav.net_asset_value.array[-1]) else None
                fof_info_to_set.acc_unit_value = float(fund_nav.acc_unit_value.array[-1]) if not pd.isnull(fund_nav.acc_unit_value.array[-1]) else None
                fof_info_to_set.adjusted_net_value = float(fund_nav.adjusted_net_value.array[-1]) if not pd.isnull(fund_nav.adjusted_net_value.array[-1]) else None
                fof_info_to_set.mdd = float(res_status.mdd) if not pd.isnull(res_status.mdd) else None
                fof_info_to_set.ret = float(total_ret) if not pd.isnull(total_ret) else None
                fof_info_to_set.ann_ret = float(res_status.annualized_ret) if not pd.isnull(res_status.annualized_ret) else None
                db_session.commit()
                db_session.close()

                ret_data_with_last_date = {}
                last_date: datetime.date = fund_auv.index.array[-1]
                while last_date == fund_auv.index.array[-1] or last_date.isoweekday() != 5:
                    last_date -= datetime.timedelta(days=1)
                last_date_data = fund_auv[fund_auv.index <= last_date]
                if not last_date_data.empty:
                    last_date_data = last_date_data.iloc[[-1]]
                    ret_data_with_last_date['date'] = last_date_data.index.array[0]
                    ret_data_with_last_date['rr'] = f'{round(((fund_auv.array[-1] / last_date_data.array[0]) - 1) * 100, 2)}%'

                fund_auv = fund_auv[fund_auv.index >= pur_sub_aa.sort_values(by='confirmed_date').confirmed_date.array[0]]
                if not fund_auv.empty:
                    res_status = Calculator.get_stat_result(fund_auv.index, fund_auv.array)
                    mv = (pur_sub_aa.share.sum() - aa_insentive_info.share.sum() + aa_dividend_reinvestment.share.sum()) * fund_nav.net_asset_value.array[-1]
                    real_mv = mv - redempt_aa.share.sum() * fund_nav.net_asset_value.array[-1]
                    total_cost = pur_sub_aa.amount.sum()
                    v_net_value = fund_nav.v_net_value.array[-1]
                    if not pd.isnull(v_net_value):
                        v_net_value = round(float(v_net_value), 4)
                    else:
                        try:
                            v_net_value = f'{round(v_nav[fund_id].iat[-1], 4)}(计算值)'
                        except KeyError:
                            v_net_value = '/'
                    holding_data = {
                        'start_date': res_status.start_date.isoformat(),
                        'days': (fund_auv.index.array[-1] - res_status.start_date).days,
                        'mv': real_mv,
                        'total_ret': f'{round((mv / total_cost - 1) * 100, 2)}%',
                        'v_nav': v_net_value,
                        'avg_cost': round(total_cost / (pur_sub_aa.share.sum() - aa_insentive_info.share.sum()), 4),
                        'sharpe': round(res_status.sharpe, 6),
                        'annualized_ret': f'{round(xirr(pur_sub_aa.amount.to_list() + [-mv], pur_sub_aa.confirmed_date.to_list() + [fund_nav.datetime.array[-1]]) * 100, 2)}%',
                        'mdd': f'{round(res_status.mdd * 100, 2)}%',
                        'annualized_vol': round(res_status.annualized_vol, 6),
                    }
                    self._wechat_bot.send_hedge_fund_info(self._FOF_ID, fund_id, hedge_info.at[fund_id, 'brief_name'], latest_nav_date, fund_data, holding_data, ret_data_with_last_date)
            except Exception as e:
                traceback.print_exc()
                self._wechat_bot.send_hedge_fund_info_failed(self._FOF_ID, fund_id, e)

    def pull_hedge_fund_nav(self):
        import os
        from ..nav_reader.hedge_fund_nav_reader import HedgeFundNAVReader

        try:
            email_data_dir = os.environ['SURFING_EMAIL_DATA_DIR']
            user_name = os.environ['SURFING_EMAIL_USER_NAME']
            password = os.environ['SURFING_EMAIL_PASSWORD']
        except KeyError as e:
            print(f'[calc_all] can not found enough params in env (e){e}')
            return False

        hf_nav_r = HedgeFundNAVReader(email_data_dir, user_name, password)
        nav_df: Optional[pd.DataFrame] = hf_nav_r.read_navs_and_dump_to_db()
        if nav_df is not None:
            fund_list = list(nav_df.index.unique())
            v_nav = FOFDataManager._calc_virtual_net_value(fund_list)
            self._gather_asset_info_of_fof(fund_list, v_nav)
        return True

    def calc_all(self):
        if not self.pull_hedge_fund_nav():
            return
        try:
            self.calc_fof_nav()
        except Exception as e:
            traceback.print_exc()
            self._wechat_bot.send_fof_nav_update_failed(self._FOF_ID, f'calc fof nav failed (e){e}')

    @staticmethod
    def _concat_assets_price(main_asset: pd.DataFrame, secondary_asset: pd.Series) -> pd.DataFrame:
        # FIXME 理论上任意资产在任意交易日应该都是有price的 所以这里的判断应该是可以确保之后可以将N种资产的price接起来
        secondary_asset = secondary_asset[secondary_asset.index <= main_asset.datetime.array[0]]
        # 将price对齐
        secondary_asset /= (secondary_asset.array[-1] / main_asset.nav.array[0])
        # 最后一个数据是对齐用的 这里就不需要了
        return pd.concat([main_asset.set_index('datetime'), secondary_asset.iloc[:-1].to_frame('nav')], verify_integrity=True).sort_index().reset_index()

    # 以下是一些获取数据的接口
    @staticmethod
    def get_fof_info(fof_id: Tuple[str] = ()):
        fof_info = BasicDataApi().get_fof_info(fof_id)
        if fof_id is None:
            return
        return fof_info.sort_values(by=['fof_id', 'datetime']).iloc[-1]

    @staticmethod
    def get_fof_investor_position(fof_id: Tuple[str] = ()):
        df = BasicDataApi().get_fof_investor_position(fof_id)
        if df is None:
            return
        return df.sort_values(by=['fof_id', 'investor_id', 'datetime']).drop_duplicates(subset=['fof_id', 'investor_id'], keep='last')

    @staticmethod
    def get_fof_investor_data(fof_id: Tuple[str] = ()):
        return DerivedDataApi().get_fof_investor_data(fof_id)

    @staticmethod
    def get_fof_asset_allocation(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_asset_allocation(fof_id)

    @staticmethod
    def get_fof_scale_alteration(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_scale_alteration(fof_id)

    @staticmethod
    def get_fof_estimate_fee(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_estimate_fee(fof_id)

    @staticmethod
    def get_fof_estimate_interest(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_estimate_interest(fof_id)

    @staticmethod
    def get_fof_transit_money(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_transit_money(fof_id)

    @staticmethod
    def get_fof_account_statement(fof_id: Tuple[str] = ()):
        return BasicDataApi().get_fof_account_statement(fof_id)

    @staticmethod
    def get_fof_nav(fof_id: str, *, ref_index_id: str = '', ref_fund_id: str = '') -> Optional[pd.DataFrame]:
        fof_nav = DerivedDataApi().get_fof_nav([fof_id])
        if fof_nav is None or fof_nav.empty:
            return
        fof_nav = fof_nav.drop(columns=['update_time', 'fof_id', 'create_time', 'is_deleted'])
        if ref_index_id:
            index_price = BasicDataApi().get_index_price(index_list=[ref_index_id])
            if index_price is None or index_price.empty:
                print(f'[get_fof_nav] get price of index {ref_index_id} failed (fof_id){fof_id}')
                return fof_nav
            return FOFDataManager._concat_assets_price(fof_nav, index_price.drop(columns=['_update_time', 'index_id']).set_index('datetime')['close'])
        elif ref_fund_id:
            fund_nav = BasicDataApi().get_fund_nav_with_date(fund_list=[ref_fund_id])
            if fund_nav is None or fund_nav.empty:
                print(f'[get_fof_nav] get nav of fund {ref_fund_id} failed (fof_id){fof_id}')
                return fof_nav
            return FOFDataManager._concat_assets_price(fof_nav, fund_nav.drop(columns='fund_id').set_index('datetime')['adjusted_net_value'])
        else:
            return fof_nav

    @staticmethod
    def get_hedge_fund_info(fund_id: Tuple[str] = ()):
        return BasicDataApi().get_hedge_fund_info(fund_id)

    @staticmethod
    def get_hedge_fund_nav(fund_id: Tuple[str] = ()):
        df = BasicDataApi().get_hedge_fund_nav(fund_id)
        if df is None:
            return
        return df.sort_values(by=['fund_id', 'datetime', 'insert_time']).drop_duplicates(subset=['fund_id', 'datetime'], keep='last')

    @staticmethod
    def get_investor_return(fof_id: str, *, investor_id_list: Tuple[str] = (), start_date: Optional[datetime.date] = None, end_date: Optional[datetime.date] = None) -> Optional[pd.DataFrame]:
        '''计算投资者收益'''
        fof_nav = FOFDataManager().get_fof_nav(fof_id)
        if fof_nav is None:
            return
        fof_scale_info = FOFDataManager().get_fof_scale_alteration([fof_id])
        if fof_scale_info is None:
            return

        fof_nav = fof_nav.set_index('datetime')
        if start_date:
            fof_nav = fof_nav[fof_nav.index >= start_date]
        if end_date:
            fof_nav = fof_nav[fof_nav.index <= end_date]
        investor_mvs = defaultdict(list)
        for row in fof_scale_info.itertuples(index=False):
            if investor_id_list and row.investor_id not in investor_id_list:
                continue
            if row.event_type in (FOFTradeStatus.PURCHASE, FOFTradeStatus.SUBSCRIBE):
                if start_date is not None:
                    actual_start_date = max(row.applied_date, start_date)
                else:
                    actual_start_date = row.applied_date
                try:
                    init_mv = fof_nav.at[actual_start_date, 'nav'] * row.share
                except KeyError:
                    init_mv = row.share
                try:
                    init_water_line = fof_nav.at[row.applied_date, 'nav']
                except KeyError:
                    init_water_line = 1
                investor_mvs[row.investor_id].append({'trade_ids': [row.id], 'start_date': actual_start_date, 'amount': row.amount, 'left_amount': row.amount, 'share': row.share, 'left_share': row.share, 'init_mv': init_mv, 'water_line': init_water_line})
            elif row.event_type in (FOFTradeStatus.REDEEM, ):
                share_redemp = row.share
                for one in investor_mvs[row.investor_id]:
                    if one['left_share'] >= share_redemp:
                        one['left_share'] -= share_redemp
                        one['trade_ids'].append(row.id)
                        break
                    else:
                        share_redemp -= one['left_share']
                        one['left_share'] = 0
                        one['left_amount'] = 0
                        one['trade_ids'].append(row.id)
                for one in investor_mvs[row.investor_id]:
                    one['water_line'] = row.nav

        investor_returns = {}
        latest_nav = fof_nav.nav.array[-1]
        for investor_id, datas in investor_mvs.items():
            datas = pd.DataFrame(datas)
            # TODO: hard code 0.2 and 4 and the second param should be acc nav
            v_nav = FOFDataManager._do_calc_v_net_value(latest_nav, datas.left_share, latest_nav, datas.water_line, 0.2, 4)
            # 这里确保单取的几个Series的顺序不会发生任何变化 这样直接运算才是OK的
            mv = v_nav * datas.left_share
            latest_mv = mv.sum()
            total_mv = (v_nav * datas.share).sum()
            total_share = datas.left_share.sum()
            avg_v_nav = latest_mv / total_share
            amount_sum = datas.amount.sum()
            if not math.isclose(amount_sum, 0):
                total_ret = total_mv - amount_sum
                total_rr = total_ret / amount_sum
            else:
                total_ret = np.nan
                total_rr = np.nan
            if not math.isclose(total_share, 0):
                avg_nav_cost = datas.left_amount.sum() / total_share
            else:
                avg_nav_cost = np.nan
            investor_returns[investor_id] = {
                'datetime': datas.start_date.array[-1], 'fof_id': fof_id, 'v_nav': avg_v_nav, 'cost_nav': avg_nav_cost, 'total_ret': total_ret, 'total_rr': total_rr, 'amount': amount_sum, 'shares': total_share, 'latest_mv': latest_mv,
                'details': datas[['trade_ids', 'amount', 'left_share', 'water_line']].rename(columns={'left_share': 'share'}).join(mv.rename('mv')).to_json(orient='records')
            }
            # print(json.dumps([{'fof_id': FOFDataManager._FOF_ID, 'v_nav': avg_v_nav, 'amount': datas.amount.sum(), 'shares': total_share}]))
        return pd.DataFrame.from_dict(investor_returns, orient='index').rename_axis(index='investor_id')

    @staticmethod
    def calc_share_by_subscription_amount(fof_id: str, amount: float, confirmed_date: datetime.date) -> Optional[float]:
        '''根据金额和日期计算申购fof产品的确认份额'''

        fof_info: Optional[pd.DataFrame] = FOFDataManager.get_fof_info([fof_id])
        if fof_info is None:
            return
        fof_nav = FOFDataManager().get_fof_nav(fof_id)
        if fof_nav is None:
            return
        try:
            # 用申购金额除以确认日的净值以得到份额
            return amount / (1 + fof_info.subscription_fee) / fof_nav.loc[fof_nav.datetime == confirmed_date, 'nav'].array[-1]
        except KeyError:
            return

    @staticmethod
    def remove_hedge_nav_data(fund_id: str, start_date: str = '', end_date: str = ''):
        BasicDataApi().delete_hedge_fund_nav(fund_id_to_delete=fund_id, start_date=start_date, end_date=end_date)

    @staticmethod
    def upload_hedge_nav_data(datas: bytes, file_name: str, hedge_fund_id: str) -> bool:
        '''上传单个私募基金净值数据'''
        '''目前支持：私募排排网 朝阳永续'''

        if not datas:
            return True

        try:
            # 下边这个分支是从私募排排网上多只私募基金净值数据的文件中读取数据
            # if file_type == 'csv':
            #     hedge_fund_info = BasicDataApi().get_hedge_fund_info()
            #     if hedge_fund_info is None:
            #         return
            #     fund_name_map = hedge_fund_info.set_index('brief_name')['fund_id'].to_dict()
            #     fund_name_map['日期'] = 'datetime'
            #     df = pd.read_csv(io.BytesIO(datas), encoding='gbk')
            #     lacked_map = set(df.columns.array) - set(fund_name_map.keys())
            #     assert not lacked_map, f'lacked hedge fund name map {lacked_map}'
            #     df = df.rename(columns=fund_name_map).set_index('datetime').rename_axis(columns='fund_id')
            #     df = df.stack().to_frame('adjusted_net_value').reset_index()
            #     # validate = 'many_to_many'
            try:
                if '产品详情-历史净值' in file_name:
                    df = pd.read_excel(io.BytesIO(datas), usecols=['净值日期', '单位净值', '累计净值', '复权累计净值'], na_values='--')
                    df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
                    df['fund_id'] = hedge_fund_id
                elif '业绩走势' in file_name:
                    df = pd.read_excel(io.BytesIO(datas), usecols=['净值日期', '净值(分红再投)'], na_values='--')
                    df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
                    df['fund_id'] = hedge_fund_id
                else:
                    assert False
            except Exception:
                try:
                    try:
                        df = pd.read_excel(io.BytesIO(datas), na_values='--')
                    except Exception:
                        df = pd.read_csv(io.BytesIO(datas), na_values='--')
                except Exception:
                    print(f'[upload_hedge_nav_data] can not read data from this file (file name){file_name} (fund_id){hedge_fund_id}')
                    return False
                else:
                    df = df.rename(columns=HedgeFundNAVReader.COLUMNS_DICT)
                    df['fund_id'] = hedge_fund_id

            df = df[df.drop(columns=['fund_id', 'datetime']).notna().any(axis=1)]
            now_df = BasicDataApi().get_hedge_fund_nav([hedge_fund_id])
            if now_df is not None:
                now_df = now_df.drop(columns=['update_time', 'create_time', 'insert_time', 'is_deleted', 'calc_date']).astype({'net_asset_value': 'float64', 'acc_unit_value': 'float64', 'v_net_value': 'float64', 'adjusted_net_value': 'float64'})
                df = df.reindex(columns=now_df.columns).astype(now_df.dtypes.to_dict())
                df['datetime'] = pd.to_datetime(df.datetime, infer_datetime_format=True).dt.date
                # merge on all columns
                df = df.round(6).merge(now_df, how='left', indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge'])
            if not df.empty:
                df['insert_time'] = datetime.datetime.now()
                print(f'[upload_hedge_nav_data] try to insert data to db (df){df}')
                df.to_sql(HedgeFundNAV.__table__.name, BasicDatabaseConnector().get_engine(), index=False, if_exists='append')
            else:
                print(f'[upload_hedge_nav_data] empty df, nothing to do')
            return True
        except Exception as e:
            print(f'[upload_hedge_nav_data] failed, got exception {e} (file_name){file_name} (hedge_fund_id){hedge_fund_id}')
            return False

    @staticmethod
    def _do_backtest(fund_nav_ffilled, wgts):
        INITIAL_CASH = 10000000
        INIT_NAV = 1
        UNIT_TOTAL = INITIAL_CASH / INIT_NAV

        positions = []
        mvs = []
        navs = []
        # 初始市值
        mv = INITIAL_CASH
        for index, s in fund_nav_ffilled.iterrows():
            s = s[s.notna()]
            if positions:
                # 最新市值
                mv = (positions[-1][1] * s).sum()

            if not positions or (s.size != positions[-1][1].size):
                # 调仓
                new_wgts = wgts.loc[s.index]
                # 各标的目标权重
                new_wgts /= new_wgts.sum()
                # 新的各标的持仓份数
                shares = (mv * new_wgts) / s
                # shares = (mv / s.size) / s
                positions.append((index, shares))

            nav = mv / UNIT_TOTAL
            mvs.append(mv)
            navs.append(nav)
        return positions, mvs, navs

    @staticmethod
    def virtual_backtest(hedge_fund_ids: Dict[str, float], ref_fund_ids: Dict[str, str], start_date: datetime.date, end_date: Optional[datetime.date] = None, benchmark_ids: Tuple[str] = ()) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]]:
        '''
        对私募基金做虚拟回测

        Parameters
        ----------
        hedge_fund_ids : Dict[str, float]
            私募基金ID列表
        ref_fund_ids : Dict[str, str]
            ref基金ID列表
        start_date: datetime.date
            回测起始日期
        end_date: datetime.date
            回测终止日期
        benchmark_ids : Tuple[str]
            指数ID列表

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]
        '''

        DEFAULT_INCENTIVE_RATIO = 0.2
        DEFAULT_DECIMAL = 4

        try:
            if end_date is None:
                end_date = datetime.date.today()
            # 获取必要的私募基金信息
            fund_info = BasicDataApi().get_hedge_fund_info(list(hedge_fund_ids.keys()))
            if fund_info is None:
                return
            fund_info = fund_info.set_index('fund_id')

            # 统计一下需要替代的基金的ref ids
            funds_added = [ref for fund, ref in ref_fund_ids.items() if fund in hedge_fund_ids.keys()]
            # 获取私募基金净值数据
            fund_nav = FOFDataManager.get_hedge_fund_nav(list(hedge_fund_ids.keys()) + funds_added)
            if fund_nav is None:
                return

            # 这里首选复权净值
            fund_nav = fund_nav[(fund_nav.fund_id != 'SR9762') | (fund_nav.datetime >= pd.to_datetime('2020-07-01', infer_datetime_format=True).date())]
            adj_nav = fund_nav.pivot(index='datetime', columns='fund_id', values='adjusted_net_value')
            # 处理ref fund
            for fund, ref in ref_fund_ids.items():
                org_nav = adj_nav[fund]
                org_nav = org_nav.ffill().dropna().sort_index()

                # 取出来ref nav在org fund成立之前的净值
                ref_nav = adj_nav.sort_index().loc[adj_nav.index <= org_nav.index.array[0], ref].ffill()
                org_nav *= ref_nav.array[-1]
                adj_nav[fund] = pd.concat([ref_nav.iloc[:-1], org_nav])
            # 最后再删掉所有的ref fund列
            adj_nav = adj_nav.loc[:, set(adj_nav.columns.array) - set(ref_fund_ids.values())]

            # 去掉全是nan的列
            valid_adj_nav = adj_nav.loc[:, adj_nav.notna().any(axis=0)]
            # 计算缺少的列
            adj_nav_lacked = set(adj_nav.columns.array) - set(valid_adj_nav.columns.array)
            if adj_nav_lacked:
                # TODO 如果某只基金完全没有复权净值 需要用累计净值来计算
                # FIXME 这里不能直接用数据库里存的虚拟净值 因为这个是邮件里发过来的单位净值虚拟后净值 而上边算出来的是复权净值虚拟后净值
                acc_nav = fund_nav[fund_nav.fund_id.isin(adj_nav_lacked)].pivot(index='datetime', columns='fund_id', values='acc_unit_value')
                adj_nav = adj_nav.drop(columns=adj_nav_lacked).join(acc_nav, how='outer')
            fund_info = fund_info.reindex(adj_nav.columns)
            lacked_funds = list(set(hedge_fund_ids.keys()) - set(adj_nav.columns.array))
            for one in lacked_funds:
                del hedge_fund_ids[one]

            # 计算虚拟净值
            FOFDataManager._adj_nav = adj_nav
            fund_nav = FOFDataManager._do_calc_v_net_value_by_nav(adj_nav, adj_nav, adj_nav.loc[adj_nav.index >= start_date, :].bfill().iloc[0, :], fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals.fillna(DEFAULT_DECIMAL))
            # water_line = pd.Series({'SGM473': 1, 'SGM992': 1, 'SJE335': 1, 'SLC213': 1, 'SNG191': 1, 'SNH765': 1, 'SR9762': 1.1146})
            # fund_nav = FOFDataManager._do_calc_v_net_value_by_nav(adj_nav, adj_nav, water_line, fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals.fillna(DEFAULT_DECIMAL))
            # fund_nav = FOFDataManager._do_calc_v_net_value_by_nav(adj_nav, adj_nav, fund_info.water_line.fillna(INIT_NAV), fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals.fillna(DEFAULT_DECIMAL))
            FOFDataManager._v_nav = fund_nav

            trading_day = BasicDataApi().get_trading_day_list(start_date=fund_nav.index.array[0], end_date=fund_nav.index.array[-1])
            trading_day = trading_day[trading_day.datetime.between(start_date, end_date)]
            fund_nav_ffilled = fund_nav.reindex(trading_day.datetime).ffill()
            fund_nav_ffilled = fund_nav_ffilled.loc[:, fund_nav_ffilled.notna().any(axis=0)].loc[fund_nav_ffilled.notna().any(axis=1), :]
            FOFDataManager._nav_filled = fund_nav_ffilled

            adj_nav_ffilled = adj_nav.reindex(trading_day.datetime).ffill()
            adj_nav_ffilled = adj_nav_ffilled.loc[:, adj_nav_ffilled.notna().any(axis=0)].loc[adj_nav_ffilled.notna().any(axis=1), :]
            FOFDataManager._adj_nav_filled = adj_nav_ffilled

            wgts = pd.Series(hedge_fund_ids)
            positions, mvs, navs = FOFDataManager._do_backtest(fund_nav_ffilled, wgts)
            FOFDataManager._positions = positions
            fof_nav = pd.Series(navs, index=fund_nav_ffilled.index, name='fof_nav')

            positions_not_v, mvs_not_v, navs_not_v = FOFDataManager._do_backtest(adj_nav_ffilled, wgts)
            FOFDataManager._positions_not_v = positions_not_v
            fof_nav_not_v = pd.Series(navs_not_v, index=adj_nav_ffilled.index, name='fof_nav_no_v')
            FOFDataManager._fof_nav_not_v = fof_nav_not_v

            indicators = []
            if benchmark_ids:
                benchmarks = BasicDataApi().get_index_price(index_list=benchmark_ids)
                benchmarks = benchmarks.pivot(index='datetime', columns='index_id', values='close')
                benchmarks = benchmarks.loc[start_date:end_date, :]
                fof_with_benchmark = [benchmarks[one] for one in benchmarks.columns.array]
            else:
                fof_with_benchmark = []
            fof_with_benchmark.extend([fof_nav, fof_nav_not_v])
            for data in fof_with_benchmark:
                data = data[data.notna()]
                # data.index = pd.to_datetime(data.index).date
                res_status = Calculator.get_stat_result(data.index, data.array)
                data.index = pd.to_datetime(data.index)
                to_calc_win_rate = data.resample(rule='1W').last().diff()
                weekly_win_rate = (to_calc_win_rate > 0).astype('int').sum() / to_calc_win_rate.size
                indicators.append({
                    'name': data.name,
                    'days': (data.index.array[-1] - data.index.array[0]).days,
                    'total_ret': (data[-1] / data[0]) - 1,
                    'annualized_ret': res_status.annualized_ret,
                    'annualized_vol': res_status.annualized_vol,
                    'weekly_win_rate': weekly_win_rate,
                    'mdd': res_status.mdd,
                    'sharpe': res_status.sharpe,
                })
            fof_indicators = pd.DataFrame(indicators)
            if len(fof_with_benchmark) > 1:
                fof_with_benchmarks = pd.concat(fof_with_benchmark, axis=1)
                fof_with_benchmarks = fof_with_benchmarks[fof_with_benchmarks.fof_nav.notna() & fof_with_benchmarks.fof_nav_no_v.notna()]
                fof_with_benchmarks = fof_with_benchmarks.set_index(pd.to_datetime(fof_with_benchmarks.index, infer_datetime_format=True))
                fof_with_benchmarks = fof_with_benchmarks.resample('1W').last().ffill()
                fof_with_benchmarks = fof_with_benchmarks / fof_with_benchmarks.iloc[0, :]
                fof_with_benchmarks = fof_with_benchmarks.set_axis(fof_with_benchmarks.index.date, axis=0)
            else:
                fof_with_benchmarks = None
            return fof_nav, fof_indicators, fof_with_benchmarks, lacked_funds
        except Exception as e:
            print(f'[virtual_backtest] failed, got exception {e} (hedge_fund_ids){hedge_fund_ids} (start_date){start_date} (end_date){end_date} (benchmark_ids){benchmark_ids}')
            traceback.print_exc()
            return

    @staticmethod
    def virtual_backtest_sub(hedge_fund_ids: Dict[str, str], start_date: datetime.date, end_date: Optional[datetime.date] = None) -> Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, List[str]]]:
        DEFAULT_INCENTIVE_RATIO = 0.2
        DEFAULT_DECIMAL = 4
        INIT_NAV = 1

        try:
            if end_date is None:
                end_date = datetime.date.today()
            # 获取必要的私募基金信息
            fund_info = BasicDataApi().get_hedge_fund_info(list(hedge_fund_ids.keys()))
            if fund_info is None:
                return
            fund_info = fund_info.set_index('fund_id')

            # 获取私募基金净值数据
            fund_nav = FOFDataManager.get_hedge_fund_nav(list(hedge_fund_ids.keys()))
            if fund_nav is None:
                return
            # 这里首选复权净值
            adj_nav = fund_nav.pivot(index='datetime', columns='fund_id', values='adjusted_net_value')
            # 去掉全是nan的列
            valid_adj_nav = adj_nav.loc[:, adj_nav.notna().any(axis=0)]
            # 计算缺少的列
            adj_nav_lacked = set(adj_nav.columns.array) - set(valid_adj_nav.columns.array)
            if adj_nav_lacked:
                # TODO 如果某只基金完全没有复权净值 需要用累计净值来计算
                # FIXME 这里不能直接用数据库里存的虚拟净值 因为这个是邮件里发过来的单位净值虚拟后净值 而上边算出来的是复权净值虚拟后净值
                acc_nav = fund_nav[fund_nav.fund_id.isin(adj_nav_lacked)].pivot(index='datetime', columns='fund_id', values='acc_unit_value')
                adj_nav = adj_nav.join(acc_nav, how='outer')
            fund_info = fund_info.reindex(adj_nav.columns)
            lacked_funds = list(set(hedge_fund_ids.keys()) - set(adj_nav.columns.array))
            for one in lacked_funds:
                del hedge_fund_ids[one]

            # 计算虚拟净值
            fund_nav = FOFDataManager._do_calc_v_net_value_by_nav(adj_nav, adj_nav, fund_info.water_line.fillna(INIT_NAV), fund_info.incentive_fee_ratio.fillna(DEFAULT_INCENTIVE_RATIO), fund_info.v_nav_decimals.fillna(DEFAULT_DECIMAL))

            trading_day = BasicDataApi().get_trading_day_list(start_date=fund_nav.index.array[0], end_date=fund_nav.index.array[-1])
            trading_day = trading_day[trading_day.datetime.between(start_date, end_date)]
            fund_nav_ffilled = fund_nav.reindex(trading_day.datetime).ffill()
            fund_nav_ffilled = fund_nav_ffilled.loc[:, fund_nav_ffilled.notna().any(axis=0)].loc[fund_nav_ffilled.notna().any(axis=1), :]

            benchmarks = BasicDataApi().get_index_price(index_list=list(set(hedge_fund_ids.values())))
            benchmarks = benchmarks.pivot(index='datetime', columns='index_id', values='close')
            benchmarks = benchmarks.loc[start_date:end_date, :]

            indicators = []
            for col in fund_nav_ffilled.columns.array:
                temp_nav = fund_nav_ffilled[col].dropna()
                the_benchmark = benchmarks[hedge_fund_ids[col]]
                the_benchmark = the_benchmark.reindex(temp_nav.index).ffill()
                res_status = Calculator.get_benchmark_stat_result(dates=temp_nav.index, values=temp_nav.array, benchmark_values=the_benchmark)
                indicators.append({
                    'fund_name': temp_nav.name,
                    'days': (temp_nav.index.array[-1] - temp_nav.index.array[0]).days,
                    'total_ret': (temp_nav[-1] / temp_nav[0]) - 1,
                    'annualized_ret': res_status.annualized_ret,
                    'annualized_vol': res_status.annualized_vol,
                    'mdd': res_status.mdd,
                    'sharpe': res_status.sharpe,
                    'ir': res_status.ir,
                })
            fund_nav_ffilled = fund_nav_ffilled.set_index(pd.to_datetime(fund_nav_ffilled.index, infer_datetime_format=True))
            fund_nav_ffilled = fund_nav_ffilled.resample('1W').last().ffill()
            fund_nav_ffilled = fund_nav_ffilled / fund_nav_ffilled.iloc[0, :]
            fund_nav_ffilled = fund_nav_ffilled.set_axis(fund_nav_ffilled.index.date, axis=0)
            return pd.DataFrame(indicators), fund_nav_ffilled
        except KeyError as e:
            print(f'[virtual_backtest] failed, got exception {e} (hedge_fund_ids){hedge_fund_ids} (start_date){start_date} (end_date){end_date}')
            return


if __name__ == "__main__":
    fof_dm = FOFDataManager()
    # fof_dm.pull_hedge_fund_nav()
    fof_dm.calc_fof_nav(dump_to_db=True, debug_mode=True)
    # fof_dm.calc_all()
