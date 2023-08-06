
from typing import Tuple, List

import datetime
from sqlalchemy import distinct
from sqlalchemy.sql import func
import pandas as pd

from ...util.singleton import Singleton
from ..wrapper.mysql import BasicDatabaseConnector
from ..view.basic_models import *


class BasicDataApi(metaclass=Singleton):
    def get_trading_day_list(self, start_date='', end_date=''):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        TradingDayList
                    )
                if start_date:
                    query = query.filter(
                        TradingDayList.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        TradingDayList.datetime <= end_date,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {TradingDayList.__tablename__}')

    def get_last_week_last_trade_dt(self):
        today = datetime.datetime.today().date()
        start_date = today - datetime.timedelta(days=15)
        df = self.get_trading_day_list(start_date=start_date)
        df.loc[:,'weekday'] = df.datetime.map(lambda x : x.weekday())
        td = pd.to_datetime(df.datetime)
        td = [_.week for _ in td]
        df.loc[:,'week_num'] = td
        last_week_num = df.week_num.values[-1]
        last_week_dt = df[df.week_num != last_week_num].datetime.values[-1]
        return last_week_dt

    def is_today_trading_date(self):
        today = datetime.datetime.now().date()
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        TradingDayList
                    ).filter(
                        TradingDayList.datetime >= today,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                con = today in tag_df.datetime.tolist()
                return con

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {TradingDayList.__tablename__}')

    def get_last_trading_day(self, dt=datetime.datetime.today()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query_result = db_session.query(
                    func.max(TradingDayList.datetime)
                ).filter(
                    TradingDayList.datetime < dt.date(),
                ).one_or_none()
                if query_result:
                    return query_result[0]
                else:
                    return None

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {TradingDayList.__tablename__}')

    def get_sector_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        SectorInfo
                    )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorInfo.__tablename__}')

    def get_sector_index_funds(self, index_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        SectorFunds
                ).filter(
                    SectorFunds.index_id == index_id,
                )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorFunds.__tablename__}')

    def get_sector_index_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        SectorFunds
                )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorFunds.__tablename__}')

    def get_sector_main_index_id(self, sector_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    SectorInfo.main_index_id
                ).filter(
                    SectorInfo.sector_id == sector_id
                )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorInfo.__tablename__}')

    def get_sector_indices(self, sector_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    distinct(SectorFunds.index_id).label("index_id")
                ).filter(
                    SectorFunds.sector_id == sector_id
                )
                ret_df = pd.read_sql(query.statement, query.session.bind)
                return ret_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {SectorFunds.__tablename__}')

    def get_fund_info(self, fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo
                    )
                if fund_list:
                    query = query.filter(
                        FundInfo.fund_id.in_(fund_list),
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundInfo.__tablename__}')

    def get_fund_benchmark(self, fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundBenchmark
                )
                if fund_list:
                    query = query.filter(
                        FundBenchmark.em_id.in_(fund_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundBenchmark.__tablename__}')

    def get_index_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        IndexInfo
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexInfo.__tablename__}')

    def get_index_component(self, index_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    IndexComponent
                )
                if index_list:
                    query = query.filter(
                        IndexComponent.index_id.in_(index_list)
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexComponent.__tablename__}')
                return None

    def get_stock_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        StockInfo
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {StockInfo.__tablename__}')

    def get_fund_nav(self, fund_list=None, dt=None):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundNav
                )
                if fund_list:
                    query = query.filter(
                        FundNav.fund_id.in_(fund_list),
                    )
                if dt:
                    query = query.filter(
                        FundNav.datetime == dt,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundNav.__tablename__}')

    def delete_fund_nav(self, start_date, end_date):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundNav
                ).filter(
                    FundNav.datetime >= start_date,
                    FundNav.datetime <= end_date,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundNav.__tablename__}')
                return None

    def get_fund_nav_with_date(self, start_date='', end_date='', fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundNav.fund_id,
                    FundNav.adjusted_net_value,
                    FundNav.datetime
                )
                if fund_list:
                    query = query.filter(FundNav.fund_id.in_(fund_list))
                if start_date:
                    query = query.filter(
                        FundNav.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        FundNav.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundNav.__tablename__}')

    def get_stock_price(self, stock_list, begin_date: str = '', end_date: str = ''):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        StockPrice
                ).filter(
                    # We could query all fund_ids at one time
                    StockPrice.stock_id.in_(stock_list),
                )
                if begin_date:
                    query = query.filter(StockPrice.datetime >= begin_date)
                if end_date:
                    query = query.filter(StockPrice.datetime <= end_date)

                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {StockPrice.__tablename__}')

    def get_fund_ret(self, fund_list):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundRet
                ).filter(
                        # We could query all fund_ids at one time
                        FundRet.fund_id.in_(fund_list),
                    )

                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundRet.__tablename__}')

    def get_index_price(self, index_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        IndexPrice
                )
                if index_list:
                    query = query.filter(
                        # We could query all fund_ids at one time
                        IndexPrice.index_id.in_(index_list),
                    )

                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexPrice.__tablename__}')

    def get_index_price_dt(self, start_date: str = '', end_date: str = '', index_list: Tuple[str] = (), columns: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                if columns:
                    query = db_session.query(
                        IndexPrice.index_id,
                        IndexPrice.datetime,
                    ).add_columns(*columns)
                else:
                    query = db_session.query(
                        IndexPrice
                    )
                if index_list:
                    query = query.filter(
                        IndexPrice.index_id.in_(index_list),
                    )
                if start_date:
                    query = query.filter(
                        IndexPrice.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        IndexPrice.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexPrice.__tablename__}')

    def delete_index_price(self, index_id_list, start_date, end_date):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    IndexPrice
                ).filter(
                    IndexPrice.index_id.in_(index_id_list),
                    IndexPrice.datetime >= start_date,
                    IndexPrice.datetime <= end_date,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {IndexPrice.__tablename__}')
                return None

    def get_fund_nav_with_date_range(self, fund_list, start_date, end_date):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundNav
                ).filter(
                        FundNav.fund_id.in_(fund_list),
                        FundNav.datetime >= start_date,
                        FundNav.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundNav.__tablename__}')

    def get_fund_list(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundInfo.__tablename__}')

    def get_fund_fee(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.manage_fee,
                        FundInfo.trustee_fee,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundInfo.__tablename__}')

    def get_fund_asset(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.asset_type,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundInfo.__tablename__}')

    def get_fund_id_mapping(self):
        fund_id_mapping = {}
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query_results = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.order_book_id,
                        FundInfo.start_date,
                        FundInfo.end_date
                    ).all()

                for fund_id, order_book_id, start_date, end_date in query_results:
                    if order_book_id not in fund_id_mapping:
                        fund_id_mapping[order_book_id] = []
                    fund_id_mapping[order_book_id].append(
                        {'fund_id': fund_id, 'start_date':start_date, 'end_date': end_date})

            except Exception as e:
                print(f'Failed to get fund id mapping <err_msg> {e} from {FundInfo.__tablename__}')
                return None

        return fund_id_mapping

    def get_fund_size(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundSize,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundSize.__tablename__}')

    def get_fund_open_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundOpenInfo,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundOpenInfo.__tablename__}')


    def get_fund_status(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundStatusLatest,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundStatusLatest.__tablename__}')

    def get_inside_market_funds(self):
        fund_status_latest = self.get_fund_status()
        in_market_fund_list = fund_status_latest[(~fund_status_latest['trade_status'].isnull()) & (fund_status_latest.trade_status != '终止上市')].fund_id.tolist()
        fund_info = self.get_fund_info()
        return fund_info[fund_info.fund_id.isin(in_market_fund_list)]

    def get_outside_market_funds(self):
        fund_status_latest = self.get_fund_status()
        in_market_fund_list = fund_status_latest[(~fund_status_latest['trade_status'].isnull()) & (fund_status_latest.trade_status != '终止上市')].fund_id.tolist()
        fund_info = self.get_fund_info()
        return fund_info[~fund_info.fund_id.isin(in_market_fund_list)]

    def get_fund_conv_stats(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundConvStats,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e}')

    @staticmethod
    def get_history_fund_size(fund_id: str = '', start_date=None, end_date=None):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate,
                )
                if fund_id:
                    query = query.filter(
                        Fund_size_and_hold_rate.fund_id == fund_id
                    )
                if start_date is not None:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime >= start_date,
                    )
                if end_date is not None:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    def delete_fund_size_hold_rate(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    Fund_size_and_hold_rate
                ).filter(
                    Fund_size_and_hold_rate.fund_id.in_(fund_list),
                    Fund_size_and_hold_rate.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return False

    @staticmethod
    def get_fund_size_range(start_date='', end_date='', fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate.fund_id,
                    Fund_size_and_hold_rate.datetime,
                    Fund_size_and_hold_rate.size,
                )
                if fund_list:
                    query = query.filter(
                        Fund_size_and_hold_rate.fund_id.in_(fund_list),
                    )
                if start_date:
                    query = query.filter(
                        # 按报告日多选取3个月，保证初值可以fill出来
                        Fund_size_and_hold_rate.datetime >= (pd.to_datetime(start_date) - datetime.timedelta(days=100)).strftime('%Y%m%d'),
                    )
                if end_date:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_company_hold(start_date='', end_date='', fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate.fund_id,
                    Fund_size_and_hold_rate.datetime,
                    Fund_size_and_hold_rate.institution_holds,
                )
                if fund_list:
                    query = query.filter(
                        Fund_size_and_hold_rate.fund_id.in_(fund_list),
                    )
                if start_date:
                    query = query.filter(
                        # 按报告日多选取3个月，保证初值可以fill出来
                        Fund_size_and_hold_rate.datetime >= (pd.to_datetime(start_date) - datetime.timedelta(days=100)).strftime('%Y%m%d'),
                    )
                if end_date:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_persional_hold(start_date='', end_date='', fund_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate.fund_id,
                    Fund_size_and_hold_rate.datetime,
                    Fund_size_and_hold_rate.personal_holds,
                )
                if fund_list:
                    query = query.filter(
                        Fund_size_and_hold_rate.fund_id.in_(fund_list),
                    )
                if start_date:
                    query = query.filter(
                        # 按报告日多选取3个月，保证初值可以fill出来
                        Fund_size_and_hold_rate.datetime >= (pd.to_datetime(start_date) - datetime.timedelta(days=100)).strftime('%Y%m%d'),
                    )
                if end_date:
                    query = query.filter(
                        Fund_size_and_hold_rate.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_size_all_data():
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    Fund_size_and_hold_rate
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {Fund_size_and_hold_rate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_history_fund_rating(fund_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundRate,
                ).filter(
                    FundRate.fund_id == fund_id
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundRate.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_hold_asset_by_id(fund_id: str = '', start_date=None, end_date=None):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldAsset,
                )
                if fund_id:
                    query = query.filter(
                        FundHoldAsset.fund_id == fund_id,
                    )
                if start_date is not None:
                    query = query.filter(
                        FundHoldAsset.datetime >= start_date,
                    )
                if end_date is not None:
                    query = query.filter(
                        FundHoldAsset.datetime <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundHoldAsset.__tablename__}')
                return pd.DataFrame([])

    def delete_fund_hold_asset(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundHoldAsset
                ).filter(
                    FundHoldAsset.fund_id.in_(fund_list),
                    FundHoldAsset.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundHoldAsset.__tablename__}')
                return False

    @staticmethod
    def get_fund_hold_industry_by_id(fund_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldIndustry,
                ).filter(
                    FundHoldIndustry.fund_id == fund_id,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundHoldIndustry.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_hold_stock_by_id(fund_id: str = ''):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldStock,
                )
                if fund_id:
                    query = query.filter(
                        FundHoldStock.fund_id == fund_id,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundHoldStock.__tablename__}')
                return pd.DataFrame([])

    @staticmethod
    def get_fund_hold_bond_by_id(fund_id):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldBond,
                ).filter(
                    FundHoldBond.fund_id == fund_id,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundHoldBond.__tablename__}')
                return pd.DataFrame([])

    def get_style_analysis_data(self, start_date: str, end_date: str, stock_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    StyleAnalysisStockFactor
                )
                if stock_list:
                    query = query.filter(
                        StyleAnalysisStockFactor.stock_id.in_(stock_list)
                    )
                query = query.filter(
                    StyleAnalysisStockFactor.datetime >= start_date,
                    StyleAnalysisStockFactor.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {StyleAnalysisStockFactor.__tablename__}')
                return

    def get_style_analysis_time_range(self) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    func.max(StyleAnalysisStockFactor.datetime).label('end_date'),
                    func.min(StyleAnalysisStockFactor.datetime).label('start_date'),
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {StyleAnalysisStockFactor.__tablename__}')
                return

    def get_barra_cne5_risk_factor(self, start_date: str, end_date: str, stock_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    BarraCNE5RiskFactor
                )
                if stock_list:
                    query = query.filter(
                        BarraCNE5RiskFactor.stock_id.in_(stock_list)
                    )
                query = query.filter(
                    BarraCNE5RiskFactor.datetime >= start_date,
                    BarraCNE5RiskFactor.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {BarraCNE5RiskFactor.__tablename__}')
                return

    def get_fund_hold_asset(self, dt) -> pd.DataFrame:
       with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundHoldAsset
                        ).filter(
                            FundHoldAsset.datetime == dt
                        )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldAsset.__tablename__}')
                return

    def get_fund_hold_industry(self, dt) -> pd.DataFrame:
       with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundHoldIndustry
                        ).filter(
                            FundHoldIndustry.datetime == dt
                        )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldIndustry.__tablename__}')
                return

    def delete_fund_hold_industry(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundHoldIndustry
                ).filter(
                    FundHoldIndustry.fund_id.in_(fund_list),
                    FundHoldIndustry.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundHoldIndustry.__tablename__}')
                return False

    def get_fund_hold_stock(self, dt=None) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldStock
                )
                if dt:
                    query = query.filter(
                        FundHoldStock.datetime == dt
                    )
                else:
                    query = query.filter(
                        FundHoldStock.datetime > datetime.datetime.now() - datetime.timedelta(days=180)
                    )

                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldStock.__tablename__}')
                return

    def get_fund_hold_stock_latest(self, dt=None, fund_list =[]) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                if not dt:
                    dt = db_session.query(
                        func.max(FundHoldStock.datetime)
                    ).filter(
                    FundHoldStock.fund_id.in_(fund_list),
                ).one_or_none()
                    if dt:
                        dt = dt[0]

                query = db_session.query(
                    FundHoldStock
                ).filter(
                    FundHoldStock.datetime == dt,
                    FundHoldStock.fund_id.in_(fund_list),
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldStock.__tablename__}')
                return

    def get_fund_hold_bond_latest(self, dt=None, fund_list =[]) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                if not dt:
                    dt = db_session.query(
                        func.max(FundHoldBond.datetime)
                    ).filter(
                    FundHoldBond.fund_id.in_(fund_list),
                ).one_or_none()
                    if dt:
                        dt = dt[0]
                query = db_session.query(
                    FundHoldBond
                ).filter(
                    FundHoldBond.datetime == dt,
                    FundHoldBond.fund_id.in_(fund_list),
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldBond.__tablename__}')
                return

    def get_fund_hold_asset_latest(self, dt=None, fund_list = []) -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                if not dt:
                    dt = db_session.query(
                        func.max(FundHoldAsset.datetime)
                    ).filter(
                    FundHoldAsset.fund_id.in_(fund_list),
                ).one_or_none()
                    if dt:
                        dt = dt[0]

                query = db_session.query(
                        FundHoldAsset
                        ).filter(
                            FundHoldAsset.datetime == dt,
                            FundHoldAsset.fund_id.in_(fund_list),
                        )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldAsset.__tablename__}')
                return

    def delete_fund_hold_stock(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundHoldStock
                ).filter(
                    FundHoldStock.fund_id.in_(fund_list),
                    FundHoldStock.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundHoldStock.__tablename__}')
                return False

    def get_fund_hold_bond(self, dt: str = '') -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundHoldBond
                )
                if dt:
                    query = query.filter(
                        FundHoldBond.datetime == dt
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundHoldBond.__tablename__}')
                return

    def get_fund_ipo_stats(self, dt: str = '') -> pd.DataFrame:
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundIPOStats
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundIPOStats.__tablename__}')
                return

    def delete_fund_hold_bond(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundHoldBond
                ).filter(
                    FundHoldBond.fund_id.in_(fund_list),
                    FundHoldBond.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundHoldBond.__tablename__}')
                return False

    def get_fund_stock_portfolio(self, dt: str = ''):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundStockPortfolio
                )
                if dt:
                    query = query.filter(
                        FundStockPortfolio.datetime == dt
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get time range data <err_msg> {e} from {FundStockPortfolio.__tablename__}')
                return

    def get_fund_stock_concept(self, tag_group_id_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    StockTag
                )
                if tag_group_id_list:
                    query = query.filter(
                        StockTag.tag_group_id.in_(tag_group_id_list)
                    )
                return pd.read_sql(query.statement, query.session.bind).drop(columns=['_update_time'])
            except Exception as e:
                print(f'Failed to get_fund_stock_concept <err_msg> {e} from {StockTag.__tablename__}')
                return

    def delete_fund_rate(self, date_to_delete: datetime.date, fund_list: List[str]):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    FundRate
                ).filter(
                    FundRate.fund_id.in_(fund_list),
                    FundRate.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {FundRate.__tablename__}')

    @staticmethod
    def get_model_data(model: Base, *params):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        *(getattr(model, k) for k in params if hasattr(model, k))
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {model.__tablename__}')

    @classmethod
    def get_fund_info_data(cls, *params):
        return cls.get_model_data(FundInfo, *params)


    def get_hedge_fund_info(self, fund_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    HedgeFundInfo,
                )
                if fund_id_list:
                    query = query.filter(
                        HedgeFundInfo.fund_id.in_(fund_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_hedge_fund_info <err_msg> {e} from {HedgeFundInfo.__tablename__}')


    def get_hedge_fund_nav(self, fund_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    HedgeFundNAV,
                )
                if fund_id_list:
                    query = query.filter(
                        HedgeFundNAV.fund_id.in_(fund_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_hedge_fund_nav <err_msg> {e} from {HedgeFundNAV.__tablename__}')


    def delete_hedge_fund_nav(self, fund_id_to_delete: str, *, date_list: Tuple[datetime.date] = (), start_date: str = '', end_date: str = '') -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    HedgeFundNAV
                ).filter(
                    HedgeFundNAV.fund_id == fund_id_to_delete,
                )
                if date_list:
                    query = query.filter(
                        HedgeFundNAV.datetime.in_(date_list),
                    )
                if start_date:
                    query = query.filter(
                        HedgeFundNAV.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        HedgeFundNAV.datetime <= end_date,
                    )
                query.delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {HedgeFundNAV.__tablename__}')
                return False


    def get_fof_info(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFInfo,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFInfo.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_info <err_msg> {e} from {FOFInfo.__tablename__}')


    def get_fof_asset_allocation(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFAssetAllocation,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFAssetAllocation.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_asset_allocation <err_msg> {e} from {FOFAssetAllocation.__tablename__}')


    def get_fof_scale_alteration(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFScaleAlteration,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFScaleAlteration.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_scale_alteration <err_msg> {e} from {FOFScaleAlteration.__tablename__}')


    def get_fof_asset_allocation(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFAssetAllocation,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFAssetAllocation.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_asset_allocation <err_msg> {e} from {FOFAssetAllocation.__tablename__}')


    def get_fof_manually(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFManually,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFManually.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_manually <err_msg> {e} from {FOFManually.__tablename__}')

    def get_fof_other_record(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFOtherRecord,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFOtherRecord.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_manually <err_msg> {e} from {FOFOtherRecord.__tablename__}')

    def get_fof_account_statement(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFAccountStatement,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFAccountStatement.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_account_statement <err_msg> {e} from {FOFAccountStatement.__tablename__}')

    def delete_fof_account_statement(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFAccountStatement
                ).filter(
                    FOFAccountStatement.fof_id.in_(fof_id_list),
                    FOFAccountStatement.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFAccountStatement.__tablename__}')
                return False

    def get_fof_incidental_statement(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFIncidentalStatement,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFIncidentalStatement.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_incidental_statement <err_msg> {e} from {FOFIncidentalStatement.__tablename__}')

    def get_fof_investor_position(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFInvestorPosition,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFInvestorPosition.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_manually <err_msg> {e} from {FOFInvestorPosition.__tablename__}')

    def delete_fof_investor_position(self, fof_id_to_delete: datetime.date, investor_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFInvestorPosition
                ).filter(
                    FOFInvestorPosition.investor_id.in_(investor_id_list),
                    FOFInvestorPosition.fof_id == fof_id_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFInvestorPosition.__tablename__}')
                return False

    def get_fof_estimate_fee(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFEstimateFee,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFEstimateFee.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_estimate_fee <err_msg> {e} from {FOFEstimateFee.__tablename__}')

    def delete_fof_estimate_fee(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFEstimateFee
                ).filter(
                    FOFEstimateFee.fof_id.in_(fof_id_list),
                    FOFEstimateFee.date == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFEstimateFee.__tablename__}')
                return False

    def get_fof_estimate_interest(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFEstimateInterest,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFEstimateInterest.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_estimate_interest <err_msg> {e} from {FOFEstimateInterest.__tablename__}')

    def delete_fof_estimate_interest(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFEstimateInterest
                ).filter(
                    FOFEstimateInterest.fof_id.in_(fof_id_list),
                    FOFEstimateInterest.date == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFEstimateInterest.__tablename__}')
                return False

    def get_fof_transit_money(self, fof_id_list: Tuple[str] = ()):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFTransitMoney,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFTransitMoney.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_transit_money <err_msg> {e} from {FOFTransitMoney.__tablename__}')

    def delete_fof_transit_money(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with BasicDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFTransitMoney
                ).filter(
                    FOFTransitMoney.fof_id.in_(fof_id_list),
                    FOFTransitMoney.confirmed_datetime == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFTransitMoney.__tablename__}')
                return False
