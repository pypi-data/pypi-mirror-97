import pandas as pd
import numpy as np
import os
import datetime
import traceback
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from ...api.raw import RawDataApi
from ...view.raw_models import YahooIndexPrice
from .raw_data_helper import RawDataHelper


class WebRawDataDownloader(object):

    def __init__(self, data_helper):
        self._data_helper = data_helper
        self._session = Session()
        self._session.mount('https://', HTTPAdapter(
            max_retries=Retry(total=10, backoff_factor=0.02),
        ))
        self._session.mount('http://', HTTPAdapter(
            max_retries=Retry(total=10, backoff_factor=0.02),
        ))

    def read_csv(self, csv_path):
        return pd.read_csv(csv_path, index_col=1)

    def fund_fee(self):
        pass

    def wind_fund_info(self, csv_path):
        # Update manually
        # Default file in company wechat is 'fundlist_wind_20202015.xlsx'
        df = pd.read_excel(csv_path)
        df.columns = ['wind_id', 'desc_name', 'full_name', 'start_date', 'end_date', 'benchmark', 'wind_class_1',
            'wind_class_2', 'currency', 'base_fund_id', 'is_structured', 'is_open', 'manager_id', 'company_id']
        df['start_date'] = df['start_date'].map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
        df['end_date'] = df['end_date'].map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
            if isinstance(x, str) else datetime.datetime.strptime('2040-12-31', '%Y-%m-%d'))
        df['is_structured'] = df['is_structured'].map(lambda x: False if x == '否' else True)
        df['is_open'] = df['is_open'].map(lambda x: False if x == '否' else True)
        self._data_helper._upload_raw(df, 'wind_fund_info')

    def cm_index_price(self, start_date, end_date):
        try:
            # history
            # default file in company wechat is 汇率数据.xls
            # df = pd.read_excel(csv_path)
            # df = df[['日期','美元中间价','欧元中间价','日元中间价','美元CFETS','欧元CFETS','日元CFETS']]
            # df.columns = ['datetime','usd_central_parity_rate','eur_central_parity_rate','jpy_central_parity_rate',
            #               'usd_cfets','eur_cfets','jpy_cfets']

            # auto update
            # data from http://www.chinamoney.com.cn/chinese/bkccpr
            start_date = datetime.datetime.strptime(start_date, '%Y%m%d').strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y%m%d').strftime('%Y-%m-%d')
            url = ('http://www.chinamoney.com.cn/dqs/rest/cm-u-bk-ccpr/CcprHisExcelNew'
                f'?startDate={start_date}&endDate={end_date}&currency=USD/CNY,EUR/CNY,100JPY/CNY')
            headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 '
                                      '(KHTML, like Gecko) Version/13.0.5 Safari/605.1.15')}
            filename = ''
            try:
                r = self._session.get(url, headers=headers, timeout=(15, 60))
                filename = os.path.join('/tmp', 'cm.xlsx')
                with open(filename, 'wb') as f:
                    f.write(r.content)
            except Exception as e:
                print(f'[cm_index_price] got error {e}')
                return False
            df = pd.read_excel(filename)
            # Drop last 2 lines in excel, which are
            #   数据来源：	中国货币网
            #   www.chinamoney.com.cn
            df.drop(df.index[-2:], inplace=True)
            df = df[['日期', 'USD/CNY', 'EUR/CNY', '100JPY/CNY']]
            df.columns = ['datetime', 'usd_central_parity_rate', 'eur_central_parity_rate', 'jpy_central_parity_rate']
            df['jpy_central_parity_rate'] = df['jpy_central_parity_rate'] / 100
            df = df.sort_values('datetime')
            self._data_helper._upload_raw(df, 'cm_index_price')
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def cxindex_index_price(self, start_date, end_date):
        try:
            # history
            # default file in company wechat is 中证信用债指数历史数据.xls
            # df = pd.read_excel(csv_path)
            # df.columns = ['index_id', 'symbol', 'datetime', 'open', 'high', 'low', 'close', 'total_turnover', 'volume']
            # df['ret'] = df['close'] / df['close'].shift(1) - 1
            # df['index_id'] = 'credit_debt'
            # df = df.drop(['symbol'], axis=1)[:-2]

            # auto update
            # data from http://www.csindex.com.cn/zh-CN/indices/index-detail/H11073
            # File download url
            url = 'http://www.csindex.com.cn/uploads/file/autofile/perf/H11073perf.xls'
            filename = ''
            try:
                r = self._session.get(url, timeout=(15, 60))
                filename = os.path.join('/tmp', 'H11073perf.xls')
                with open(filename, 'wb') as f:
                    f.write(r.content)
            except Exception as e:
                print(f'[cxindex_index_price] got error {e}')
                return False
            df = pd.read_excel(filename)
            df = df[['日期Date', '收盘Close', '涨跌幅(%)Change(%)', '成交量（万元）Volume(10 thousand CNY)',
                '成交金额（元）Turnover']]
            df.columns = ['datetime', 'close', 'ret', 'volume', 'total_turnover']
            df['volume'] = df['volume'].values * 10000
            df['ret'] = df['ret'] / 100
            df = df[(df['datetime']>=start_date) & (df['datetime']<=end_date)].sort_values('datetime')
            df['open'] = float('Nan')
            df['high'] = float('Nan')
            df['low'] = float('Nan')
            df['index_id'] = 'credit_debt'
            self._data_helper._upload_raw(df, 'cxindex_index_price')
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def yahoo_index_price(self, start_date, end_date):
        try:
            # history
            # default file in company wechat is 大类资产指数据.xlsx
            # df = pd.read_excel(csv_path)
            # df['datetime'] = df['date']
            # for c in ['sp500', 'dax30', 'n225']:
            #     df_i = df[['datetime']].copy()
            #     df_i['close'] = df[c].copy()
            #     df_i['ret'] = df_i['close'] / df_i['close'].shift(1) - 1
            #     df_i['open'] = float('Nan')
            #     df_i['high'] = float('Nan')
            #     df_i['low'] = float('Nan')
            #     df_i['volume'] = float('Nan')
            #     df_i['total_turnover'] = float('Nan')
            #     df_i['index_id'] = c
            #     self._data_helper._upload_raw(df_i, 'yahoo_index_price')

            # auto update
            # data from
            # sp500 https://finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC
            # n225 https://finance.yahoo.com/quote/%5EN225/history?p=%5EN225
            # dax30 https://finance.yahoo.com/quote/%5EGDAXI/history/
            # File download url:
            # https://query1.finance.yahoo.com/v7/finance/download/%5EGSPC?period1=1553667756&period2=1585290156&interval=1d&events=history
            # https://query1.finance.yahoo.com/v7/finance/download/%5EN225?period1=1553673330&period2=1585295730&interval=1d&events=history
            # https://query1.finance.yahoo.com/v7/finance/download/%5EGDAXI?period1=1553673346&period2=1585295746&interval=1d&events=history

            url_prefix = 'https://query1.finance.yahoo.com/v7/finance/download/'

            trading_day = RawDataApi().get_em_tradedates().set_index('TRADEDATES')
            start_date_loc = trading_day.index.get_loc(pd.to_datetime(start_date).date(), method='ffill')
            end_date_loc = trading_day.index.get_loc(pd.to_datetime(end_date).date(), method='ffill')

            assert isinstance(start_date_loc, int), 'start date is not a valid trading day'
            assert isinstance(end_date_loc, int), 'end date is not a valid trading day'

            # TODO: (deprecated)由于我们目前更新的时间（次日0点），美股还没收盘，所以这里只能更新前一天的数据；之后再看看可能需要分批做自动更新
            # TODO: 更新时间暂时统一挪到美股收盘后了，这里直接更新当天数据
            extra_days = 0
            assert start_date_loc >= extra_days, 'there is no enough extra days before start date'
            start_date_with_extra_days = trading_day.index.array[start_date_loc - extra_days]
            print(f'start date with extra days: {start_date_with_extra_days}')

            assert end_date_loc >= extra_days, 'there is no enough extra days before end date'
            end_date_with_extra_days = trading_day.index.array[end_date_loc - extra_days]
            print(f'end date with extra days: {end_date_with_extra_days}')

            start_date = min(pd.to_datetime(start_date, infer_datetime_format=True) - datetime.timedelta(days=7), start_date_with_extra_days)
            start_timestamp = str(int((start_date).timestamp()))
            end_timestamp = str(int((datetime.datetime.strptime(end_date, '%Y%m%d') + datetime.timedelta(days=1)).timestamp()))
            url_postfix = f'?period1={start_timestamp}&period2={end_timestamp}&interval=1d&events=history'
            url_type_list = ['%5EGSPC', '%5EN225', '%5EGDAXI', '%5EFTSE', '%5EDJI', '%5Eixic']
            csv_list = ['^GSPC.csv', '^N225.csv', '^GDAXI.csv', '^FTSE.csv', '^DJI.csv', '^IXIC.csv']
            index_list = ['sp500', 'n225', 'dax30', 'ftse100', 'dji', 'ixic']
            df_list = []
            for url_type, csv_i, index_i in zip(url_type_list, csv_list, index_list):
                url = url_prefix + url_type + url_postfix
                filename = ''
                try:
                    r = self._session.get(url, timeout=(15, 60))
                    filename = os.path.join('/tmp', csv_i)
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                except Exception as e:
                    print(f'[yahoo_index_price] got error {e}')
                    continue
                df = pd.read_csv(filename)
                df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
                df.columns = ['datetime', 'open', 'high', 'low', 'close', 'adjclose', 'volume']
                df['datetime'] = df['datetime'].map(lambda x: pd.to_datetime(x, infer_datetime_format=True).date())
                df['index_id'] = index_i
                df['total_turnover'] = float('Nan')
                df['ret'] = df['adjclose'] / df['adjclose'].shift(1) - 1
                df = df.drop(['adjclose'], axis=1)
                df = df[df['datetime'].between(start_date_with_extra_days, end_date_with_extra_days)].sort_values('datetime')
                if not df.empty:
                    df_list.append(df)
            if df_list:
                df_all = pd.concat(df_list)
                self._data_helper._upload_raw(df_all, YahooIndexPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def download_all(self, start_date, end_date):
        failed_tasks = []
        if not self.cm_index_price(start_date, end_date):
            failed_tasks.append('cm_index_price')

        if not self.cxindex_index_price(start_date, end_date):
            failed_tasks.append('cxindex_index_price')

        if not self.yahoo_index_price(start_date, end_date):
            failed_tasks.append('yahoo_index_price')

        return failed_tasks


if __name__ == "__main__":
    data_helper = RawDataHelper()
    web_downloader = WebRawDataDownloader(data_helper)
    # web_downloader.cm_index_price('20200408', '20200508')
    # web_downloader.yahoo_index_price('20200427', '20200710')
