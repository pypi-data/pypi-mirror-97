
from typing import Tuple, List

import pandas as pd
import datetime
from sqlalchemy import func

from ...util.singleton import Singleton
from ..wrapper.mysql import DerivedDatabaseConnector
from ..view.derived_models import *


class DerivedDataApi(metaclass=Singleton):
    def get_fund_indicator(self, fund_list):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        FundIndicator.fund_id,
                        FundIndicator.datetime,
                        FundIndicator.alpha,
                        FundIndicator.beta,
                        FundIndicator.fee_rate,
                        FundIndicator.track_err,
                    ).filter(
                        FundIndicator.fund_id.in_(fund_list),
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicator.__tablename__}')

    def get_fund_indicator_by_date(self, fund_list, date):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundIndicator
                ).filter(
                    FundIndicator.datetime == date,
                    FundIndicator.fund_id.in_(fund_list),
                )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicator.__tablename__}')

    def get_fund_indicator_monthly(self, start_date, end_date, fund_list, columns: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundIndicatorMonthly.fund_id,
                    FundIndicatorMonthly.datetime,
                )
                if columns:
                    query = query.add_columns(*columns)
                query = query.filter(
                    FundIndicatorMonthly.fund_id.in_(fund_list),
                    FundIndicatorMonthly.datetime >= start_date,
                    FundIndicatorMonthly.datetime <= end_date
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicatorMonthly.__tablename__}')

    def get_fund_indicator_group(self, start_date: str, end_date: str, data_cycle: str = ''):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundIndicatorGroup
                )
                query = query.filter(
                    FundIndicatorGroup.datetime >= start_date,
                    FundIndicatorGroup.datetime <= end_date
                )
                if data_cycle:
                    query = query.filter(
                        FundIndicatorGroup.data_cycle == data_cycle
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicatorGroup.__tablename__}')

    def get_latest_fund_indicator_group(self, data_cycle: str = ''):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                sub_q = quant_session.query(
                    FundIndicatorGroup.datetime.label('latest_time'),
                )
                if data_cycle:
                    sub_q = sub_q.filter(
                        FundIndicatorGroup.data_cycle == data_cycle,
                    )
                sub_q = sub_q.order_by(
                    FundIndicatorGroup.datetime.desc(),
                ).limit(1).subquery()

                query = quant_session.query(FundIndicatorGroup).filter(
                    FundIndicatorGroup.datetime == sub_q.c.latest_time,
                )
                if data_cycle:
                    query = query.filter(
                        FundIndicatorGroup.data_cycle == data_cycle,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicatorGroup.__tablename__}')

    def get_fund_score_extended_by_id(self, fund_id, data_cycle: str = '1Y'):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundScoreExtended,
                ).filter(
                    FundScoreExtended.fund_id == fund_id,
                    FundScoreExtended.data_cycle == data_cycle,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundScoreExtended.__tablename__}')
                return pd.DataFrame([])

    def get_latest_fund_score_new_by_id(self, fund_id, data_cycle: str = '1Y'):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundScoreNew,
                ).filter(
                    FundScoreNew.fund_id == fund_id,
                    FundScoreNew.data_cycle == data_cycle,
                ).order_by(
                    FundScoreNew.datetime.desc()
                ).limit(1)

                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundScoreNew.__tablename__}')
                return pd.DataFrame([])

    def get_fund_score_extended(self, start_date: str, end_date: str, fund_list: Tuple[str] = (), columns: Tuple[str] = (), data_cycle: str = '1Y'):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                if columns:
                    query = quant_session.query(
                        FundScoreExtended.fund_id,
                        FundScoreExtended.datetime,
                    )
                    query = query.add_columns(*columns)
                else:
                    query = quant_session.query(
                        FundScoreExtended,
                    )
                if fund_list:
                    query = query.filter(
                        FundScoreExtended.fund_id.in_(fund_list)
                    )
                query = query.filter(
                    FundScoreExtended.datetime >= start_date,
                    FundScoreExtended.datetime <= end_date,
                    FundScoreExtended.data_cycle == data_cycle,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundScoreExtended.__tablename__}')

    def get_fund_score_extended_for_ranks(self, start_date: str, end_date: str, fund_list: Tuple[str] = ()):
        return self.get_fund_score_extended(start_date, end_date, fund_list=fund_list, columns=['wind_class_1', 'return_score', 'robust_score', 'timing_score', 'return_rank', 'robust_rank', 'timing_rank'])

    def get_index_valuation_develop(self, index_ids, start_date, end_date):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexValuationLongTerm
                ).filter(
                    IndexValuationLongTerm.index_id.in_(index_ids),
                    IndexValuationLongTerm.datetime >= start_date,
                    IndexValuationLongTerm.datetime <= end_date,
                ).order_by(IndexValuationLongTerm.datetime.asc())
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexValuationLongTerm.__tablename__}')
                return pd.DataFrame([])

    def get_index_valuation_develop_without_date(self, index_ids):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexValuationLongTerm
                ).filter(
                    IndexValuationLongTerm.index_id.in_(index_ids),
                ).order_by(IndexValuationLongTerm.datetime.asc())
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexValuationLongTerm.__tablename__}')
                return pd.DataFrame([])

    def get_index_valuation_develop_columns_by_id(self, index_id, columns):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    *columns
                ).filter(
                    IndexValuationLongTerm.index_id == index_id,
                ).order_by(IndexValuationLongTerm.datetime.asc())
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexValuationLongTerm.__tablename__}')
                return pd.DataFrame([])

    def get_asset_allocation_info(self, version:int=2):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    AssetAllocationInfo
                ).filter(
                    AssetAllocationInfo.version == version
                ).order_by(AssetAllocationInfo.allocation_id)
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {AssetAllocationInfo.__tablename__}')
                return pd.DataFrame([])

    def get_style_factor_return(self, start_date: str, end_date: str, index_list: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    StyleAnalysisFactorReturn
                )
                if index_list:
                    query = query.filter(StyleAnalysisFactorReturn.universe_index.in_(index_list))
                query = query.filter(
                    StyleAnalysisFactorReturn.datetime >= start_date,
                    StyleAnalysisFactorReturn.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {StyleAnalysisFactorReturn.__tablename__}')
                return

    def get_barra_cne5_factor_return(self, start_date: str, end_date: str):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    BarraCNE5FactorReturn
                ).filter(
                    BarraCNE5FactorReturn.datetime >= start_date,
                    BarraCNE5FactorReturn.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {BarraCNE5FactorReturn.__tablename__}')
                return

    def get_allocation_distribution(self, version:str=1):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    AllocationDistribution
                ).filter(
                    AllocationDistribution.version == version
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {AllocationDistribution.__tablename__}')
                return

    def get_fund_manager_index(self, manager_id: Tuple[str] = (), start_date: str = '', end_date: str = '', fund_type: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    FundManagerIndex
                )
                if manager_id:
                    query = query.filter(FundManagerIndex.manager_id.in_(manager_id))
                if start_date:
                    query = query.filter(FundManagerIndex.datetime >= start_date)
                if end_date:
                    query = query.filter(FundManagerIndex.datetime <= end_date)
                if fund_type:
                    query = query.filter(FundManagerIndex.fund_type.in_(fund_type))
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundManagerIndex.__tablename__}')

    def get_fund_manager_score(self, manager_id: Tuple[str] = (), start_date: str = '', end_date: str = '', fund_type: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    FundManagerScore
                )
                if manager_id:
                    query = query.filter(FundManagerScore.manager_id.in_(manager_id))
                if start_date:
                    query = query.filter(FundManagerScore.datetime >= start_date)
                if end_date:
                    query = query.filter(FundManagerScore.datetime <= end_date)
                if fund_type:
                    query = query.filter(FundManagerScore.fund_type.in_(fund_type))
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundManagerScore.__tablename__}')

    def get_latest_fund_style_box(self):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                sub_q = mn_session.query(
                    StyleBox.fund_id.label('temp_id'),
                    func.max(StyleBox.datetime).label('temp_date'),
                ).group_by(StyleBox.fund_id).subquery()

                query = mn_session.query(
                    StyleBox.fund_id,
                    StyleBox.x,
                    StyleBox.y,
                    StyleBox.datetime,
                ).filter(
                    StyleBox.fund_id == sub_q.c.temp_id,
                    StyleBox.datetime == sub_q.c.temp_date
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_latest_fund_style_box {e} from {StyleBox.__tablename__}')
                return

    def get_funds_latest_fund_style_box(self, fund_list:Tuple[str]):
        # x： 0 价值型 40 平衡型 60 成长型 100
        # y： 0 小盘 25 中盘 50 大盘 100
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                sub_q = mn_session.query(
                    StyleBox.fund_id.label('temp_id'),
                    func.max(StyleBox.datetime).label('temp_date'),
                ).filter(
                    StyleBox.fund_id.in_(fund_list),
                ).group_by(StyleBox.fund_id).subquery()

                query = mn_session.query(
                    StyleBox.fund_id,
                    StyleBox.x,
                    StyleBox.y,
                    StyleBox.datetime,
                ).filter(
                    StyleBox.fund_id == sub_q.c.temp_id,
                    StyleBox.datetime == sub_q.c.temp_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                df['x'] = df['x'].map(lambda x: 0 if x < 0 else x)
                df['x'] = df['x'].map(lambda x: 300 if x > 300 else x)
                df['y'] = df['y'].map(lambda y: 0 if y < 0 else y)
                df['y'] = df['y'].map(lambda y: 400 if y > 400 else y)
                df['x'] = df['x'] / 3
                df['y'] = df['y'] / 4
                return df
            except Exception as e:
                print(f'Failed to get_latest_fund_style_box {e} from {StyleBox.__tablename__}')
                return

    def get_fund_style_box(self, fund_id: Tuple[str] = (), datetime: str = ''):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    StyleBox
                )
                if fund_id:
                    query = query.filter(
                        StyleBox.fund_id.in_(fund_id),
                    )
                if datetime:
                    query = query.filter(
                        StyleBox.datetime == datetime,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_fund_style_box {e} from {StyleBox.__tablename__}')
                return

    def get_new_share_fund_rank(self):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    NewShareFundRank
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_new_share_fund_rank {e} from {NewShareFundRank.__tablename__}')
                return

    def get_convertible_bond_fund_rank(self):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    ConvertibleBondFundRank
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_convertible_bond_fund_rank {e} from {ConvertibleBondFundRank.__tablename__}')
                return

    def get_abs_return_fund_rank(self):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    AbsReturnFundRank
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_abs_return_fund_rank {e} from {AbsReturnFundRank.__tablename__}')
                return

    def delete_fund_style_box(self, date_to_delete: datetime.date, fund_list: List[str]):
        with DerivedDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    StyleBox
                ).filter(
                    StyleBox.fund_id.in_(fund_list),
                    StyleBox.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {StyleBox.__tablename__}')

    def get_fund_manager_info(self, mng_list: Tuple[str] = (), fund_list: Tuple[str] = (), columns: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                if columns:
                    query = quant_session.query(
                        FundManagerInfo.mng_id,
                        FundManagerInfo.start_date,
                        FundManagerInfo.fund_id,
                    ).add_columns(*columns)
                else:
                    query = quant_session.query(
                        FundManagerInfo,
                    )
                if mng_list:
                    query = query.filter(
                        FundManagerInfo.mng_id.in_(mng_list),
                    )
                if fund_list:
                    query = query.filter(
                        FundManagerInfo.fund_id.in_(fund_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundManagerInfo.__tablename__}')

    def get_market_portfolio_indicator(self):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    ThirdPartyPortfolioIndicator
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_market_portfolio_indicator {e} from {ThirdPartyPortfolioIndicator.__tablename__}')
                return pd.DataFrame([])

    def get_market_portfolio_info(self):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    ThirdPartyPortfolioInfo
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_market_portfolio_info {e} from {ThirdPartyPortfolioInfo.__tablename__}')
                return pd.DataFrame([])

    def get_market_portfolio_trade_dates(self, po_id):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    ThirdPartyPortfolioTrade.datetime
                ).filter(
                    ThirdPartyPortfolioTrade.po_id == po_id,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_market_portfolio_trade_dates {e} from {ThirdPartyPortfolioTrade.__tablename__}')
                return pd.DataFrame([])

    def get_market_portfolio_trade_by_date(self, po_id, date):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    ThirdPartyPortfolioTrade
                ).filter(
                    ThirdPartyPortfolioTrade.po_id == po_id,
                    ThirdPartyPortfolioTrade.datetime == date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_market_portfolio_trade_by_date {e} from {ThirdPartyPortfolioTrade.__tablename__}')
                return pd.DataFrame([])

    def get_market_portfolio_position(self, po_id):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    ThirdPartyPortfolioPositionLatest
                ).filter(
                    ThirdPartyPortfolioPositionLatest.po_id == po_id,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_market_portfolio_position {e} from {ThirdPartyPortfolioPositionLatest.__tablename__}')
                return pd.DataFrame([])

    def get_market_portfolio_position_by_src(self, po_srcs: Tuple[int] = ()):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    ThirdPartyPortfolioPositionLatest
                )
                if po_srcs:
                    query = query.filter(
                        ThirdPartyPortfolioPositionLatest.po_src.in_(po_srcs),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_market_portfolio_position_by_src {e} from {ThirdPartyPortfolioPositionLatest.__tablename__}')
                return

    def get_stock_factor_info(self):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    StockFactorInfo
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_stock_factor_info {e} from {StockFactorInfo.__tablename__}')
                return

    def get_fund_industry_exposure(self, fund_id):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                sub_q = session.query(
                    FundIndicatorGroup.datetime.label('latest_time'),
                ).order_by(
                    FundIndicatorGroup.datetime.desc(),
                ).limit(1).subquery()

                query = session.query(
                    FundIndustryExposure
                ).filter(
                    FundIndustryExposure.fund_id == fund_id,
                    FundIndustryExposure.datetime == sub_q.c.latest_time,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_fund_industry_exposure {e} from {FundIndicatorGroup.__tablename__}')
                return pd.DataFrame([])


    def get_fof_nav(self, fof_id_list: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    FOFNav,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFNav.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_nav <err_msg> {e} from {FOFNav.__tablename__}')

    def delete_fof_nav(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFNav
                ).filter(
                    FOFNav.fof_id.in_(fof_id_list),
                    FOFNav.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFNav.__tablename__}')
                return False

    def get_fof_position(self, fof_id_list: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    FOFPosition,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFPosition.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_position <err_msg> {e} from {FOFPosition.__tablename__}')

    def delete_fof_position(self, date_to_delete: datetime.date, fof_id_list: List[str]) -> bool:
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFPosition
                ).filter(
                    FOFPosition.fof_id.in_(fof_id_list),
                    FOFPosition.datetime == date_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFPosition.__tablename__}')
                return False

    def get_fof_investor_data(self, fof_id_list: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFInvestorData,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFInvestorData.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_investor_data <err_msg> {e} from {FOFInvestorData.__tablename__}')

    def delete_fof_investor_data(self, fof_id_to_delete: datetime.date, investor_id_list: List[str]) -> bool:
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFInvestorData
                ).filter(
                    FOFInvestorData.investor_id.in_(investor_id_list),
                    FOFInvestorData.fof_id == fof_id_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFInvestorData.__tablename__}')
                return False

    def get_fof_position_detail(self, fof_id_list: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FOFPositionDetail,
                )
                if fof_id_list:
                    query = query.filter(
                        FOFPositionDetail.fof_id.in_(fof_id_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'failed to get_fof_position_detail <err_msg> {e} from {FOFPositionDetail.__tablename__}')

    def delete_fof_position_detail(self, fof_id_to_delete: datetime.date, fund_id_list: List[str]) -> bool:
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                session.query(
                    FOFPositionDetail
                ).filter(
                    FOFPositionDetail.fund_id.in_(fund_id_list),
                    FOFPositionDetail.fof_id == fof_id_to_delete,
                ).delete(synchronize_session=False)
                session.commit()
                return True
            except Exception as e:
                print(f'failed to delete data <err_msg> {e} from {FOFPositionDetail.__tablename__}')
                return False