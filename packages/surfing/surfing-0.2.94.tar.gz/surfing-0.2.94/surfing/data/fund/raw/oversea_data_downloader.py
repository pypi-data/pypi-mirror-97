import requests
import traceback
import time
from ...api.raw import *
from .raw_data_helper import RawDataHelper
from ...view.raw_models import OSFundNav
from ...api.raw import RawDataApi
class OverseaDataUpdate:

    def __init__(self, update_period:int=35, data_per_page:int=20, data_helper=RawDataHelper()):
        self.update_period = update_period
        self.data_per_page = data_per_page
        self.data_helper = data_helper
        self.raw_data_api = RawDataApi()
        self.today = datetime.datetime.now().date()

    def update_unit(self, fund_id, exsited_price, fund_id_list):
        nav_dic = {
                'navDate':'datetime',
                'price':'nav',
            }
        url = 'https://fund.bluestonehk.com/fund/ifast/info/getHistoryNavs?productId={}&pageSize={}&pageNo={}'.format(
            fund_id, self.data_per_page, 1
        )
        response = requests.get(url)
        datas = response.json()
        if datas['message'] != '请求成功' or datas['body']['data'] == []:
            return None
        new_nav = pd.DataFrame(datas['body']['data'])[nav_dic.keys()].rename(columns=nav_dic)
        td = pd.to_datetime(new_nav.datetime)
        td = [_.date() for _ in td]
        new_nav.datetime = td
        exsited_date = exsited_price[exsited_price['codes'] == fund_id].datetime.max()
        new_df = new_nav[new_nav.datetime > exsited_date].copy()
        if new_df.empty:
            idx = fund_id_list.index(fund_id)
            if idx % 10 == 0:
                time.sleep(0.5)
                print(f'finish fund nav {idx}')
            return None
        new_df.loc[:,'codes'] = fund_id
        idx = fund_id_list.index(fund_id)
        if idx % 10 == 0:
            time.sleep(0.5)
            print(f'finish fund nav {idx}')
        return new_df

    def update_fund_nav(self):
        failed_tasks = []
        try:
            fund_info = self.raw_data_api.get_over_sea_fund_info()
            fund_id_list = fund_info.codes.tolist()
            update_period_dates = self.today - datetime.timedelta(days=self.update_period)
            exsited_price = self.raw_data_api.get_oversea_fund_nav(start_date = update_period_dates).drop(columns=['_update_time'], errors='ignore')
            result = []
            for fund_id in fund_id_list:
                _count = 0
                while True:
                    try:
                        if _count == 5:
                            break                        
                        new_df = self.update_unit(fund_id, exsited_price, fund_id_list)
                        #print(f'    fund_id {fund_id}')
                        if new_df is not None:
                            result.append(new_df)
                    except Exception as e:
                        _count += 1
                        print(e)
                        time.sleep(1)
                    else:
                        break

            nav_result = pd.concat(result)
            self.data_helper._upload_raw(nav_result, OSFundNav.__table__.name)
            

        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append(f'oversea_fund_nav')
        return failed_tasks
    
    def update_index_price(self):
        # todo change file location here
        folder = '/Users/huangkejia/Downloads/Data/'
        excel_name = '8.0_海外基金基准_210220_回溯2000版本_unlink.xlsx'
        sheet_name = 'Benchmark dailydata'
        df = pd.read_excel(folder+excel_name,sheet_name=sheet_name).replace(dic)
        with RawDatabaseConnector().managed_session() as db_session:        
            query = db_session.query(
                OSIndexPrice
            )
            index_price_exsited = pd.read_sql(query.statement, query.session.bind)
        index_price_exsited = index_price_exsited.drop(columns=['_update_time'], errors='ignore')
        dic = {'VNIndex':'VNINDEX','dax':'DAX'}
        fund_cols = df.columns.tolist()
        fund_col_len = len(fund_cols)
        result = []
        for i in range(fund_col_len):
            if i % 2 == 0:
                _fund_cols = fund_cols[i:i+2]
                _df = df[_fund_cols]
                _index_id = _df[_fund_cols[0]].values[0].replace(' Index', '').replace(' index', '')
                _df = _df.iloc[3:].dropna()
                if _df.empty:
                    continue
                _df.columns = ['datetime','close']
                con = [ not isinstance(_, int) for _ in _df.datetime]
                _df = _df[con]
                td = pd.to_datetime(_df.datetime)
                td = [i.date() for i in td]
                _df.datetime = td
                if _index_id in dic.keys():
                    _index_id = dic[_index_id]
                _df.loc[:,'codes'] = _index_id
                _df_exsited = index_price_exsited[index_price_exsited.codes == _index_id]
                _df_new = _df[~_df.datetime.isin(_df_exsited.datetime)]
                result.append(_df_new)
        df_result = pd.concat(result).drop_duplicates(subset=['datetime','codes'])
        df_result.to_sql('oversea_index_price', RawDatabaseConnector().get_engine(), index=False, if_exists='append')
