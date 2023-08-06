import dataclasses
import datetime
import pandas as pd
import numpy as np
import math
import statsmodels.api as sm
from statsmodels import regression
from scipy.stats import gmean
from functools import partial
import statsmodels.api as sm
from statsmodels.tsa.ar_model import AutoReg
from scipy.stats import kurtosis, skew
from decimal import Decimal, ROUND_HALF_UP, Context
from pandas.tseries.offsets import DateOffset

class CalculatorBase:

    TRADING_DAYS_PER_YEAR = 242
    TOTAL_DAYS_PER_YEAR = 365
    TOTAL_WEEKS_PER_YEAR = 52
    TOTAL_MONTHS_PER_YEAR = 12
    STOCK_IPO_NUM_MARKET = {
        '深交所中小板': 500,
        '深交所创业板': 500,
        '上交所主板': 1000,
        '上交所科创板': 500,
        '深交所主板': 500,
    }

    @staticmethod
    def get_begin_date_dic(week_end_date):
        begin_date_period_dic = {
            'w1': DateOffset(weeks=1),
            'm1': DateOffset(months=1),
            'm3': DateOffset(months=3),
            'm6': DateOffset(months=6),
            'y1': DateOffset(years=1),
            'y2': DateOffset(years=2),
            'y3': DateOffset(years=3),
            'y4': DateOffset(years=4),
            'y5': DateOffset(years=5),
        }
        last_date = datetime.datetime.now().date()
        begin_date_dic = {}
        for name, value in begin_date_period_dic.items():
            if name == 'w1':
                bd = (week_end_date - value).date()
            else:
                bd = (week_end_date - value).date()
            begin_date_dic[name] = bd
        return last_date, begin_date_dic

    @staticmethod
    def calc_cl_alpha_beta(total: np.ndarray):
        if total.shape[0] <= 1:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    }
        X = np.array([total[:, 1], total[:, 1]]).T
        X[:, 0][X[:, 0] < 0] = 0
        X[:, 1][X[:, 1] > 0] = 0
        if np.count_nonzero(X[:, 1]) == 0:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    'beta_bull':np.nan,
                    'beta_bear':np.nan,
                    
                    }
        est2 = sm.OLS(total[:, 0], sm.add_constant(X, prepend=False)).fit()
        return {'beta':est2.params[0] - est2.params[1],
                'alpha':est2.params[-1],
                'beta_bull':est2.params[0],
                'beta_bear':-est2.params[1],
                }
    
    @staticmethod
    def calc_hm_alpha_beta(total: np.ndarray):
        # 牛市追踪 市场上涨是alpha
        if total.shape[0] <= 1:
            return {'beta':np.nan,
                    'alpha':np.nan,
                    }
        X = np.array([total[:, 1], total[:, 1]]).T
        X[:, 1][X[:, 1] < 0] = 0
        est2 = sm.OLS(total[:, 0], sm.add_constant(X, prepend=False)).fit()
        return {'beta':est2.params[1],
                'alpha':est2.params[-1],
                }

    @staticmethod
    def stat_round_pct(x):
        s = str(round(100*x,2))
        s = s[::-1].zfill(4)[::-1]
        return s + '%'

    @staticmethod
    def calc_continue_regress_v(monthly_ret, risk_free_rate):
        # 半年周期
        window = 6
        yearly_multiplier = 2
        period_num = 12
        annual_ret = monthly_ret.rolling(window=window).apply(lambda x : x.sum() * yearly_multiplier - risk_free_rate)
        annual_vol = monthly_ret.rolling(window=window).apply(lambda x : x.std(ddof=1) * np.sqrt(period_num))
        sharpe = (annual_ret / annual_vol)
        sharpe = sharpe.replace(np.Inf, np.nan).replace(-np.Inf, sharpe).dropna() # 空值sharpe赋值np.nan
        if sharpe.shape[0] < 6:
            return np.nan
        mod = AutoReg(endog=sharpe.values, lags=1)
        res = mod.fit()
        continue_regress_v = res.params[0]
        return continue_regress_v

    @staticmethod
    def calc_recent_ret(dates:             pd.core.series.Series,
                        values:            pd.core.series.Series,
                        frequency:         str='1D'):
        assert frequency in ['1D'], f'frequency provided: {frequency} is not included, must in 1D'
        dates = pd.to_datetime(dates)
        dates = [i.date() for i in dates]
        _end_dt = dates[-1]
        last_date, begin_date_dic = CalculatorBase.get_begin_date_dic(week_end_date = _end_dt)
        assert len(dates) == len(values), 'date and port_values has different numbers'
        sr = pd.Series(values, index=dates).sort_index().dropna()
        sr = sr.set_axis(pd.to_datetime(sr.index), inplace=False).resample(frequency).last().dropna()
        sr.index = [i.date() for i in sr.index]
        _begin_date = sr.index[0]
        _natural_year_begin_date = datetime.date(last_date.year,1,1)
        recent_natural_year_ret = sr.loc[:last_date][-1] / sr.loc[:max(_natural_year_begin_date,_begin_date)][-1] - 1
        _res = {}
        for _period, _period_begin_date in begin_date_dic.items():
            if _period_begin_date >= _begin_date and sr.index[-1] > _period_begin_date:
                _res[_period] = sr.loc[:last_date][-1] / sr.loc[_period_begin_date:][0] - 1
            else:
                _res[_period] = np.nan
        recent_1w_ret = _res['w1']
        recent_1m_ret = _res['m1']
        recent_3m_ret = _res['m3']
        recent_6m_ret = _res['m6']
        recent_1y_ret = _res['y1']
        recent_2y_ret = _res['y2']
        recent_3y_ret = _res['y3']
        recent_4y_ret = _res['y4']
        recent_5y_ret = _res['y5']
        history_ret = sr.loc[:last_date][-1] / sr[0] - 1
        days = (dates[-1] - dates[0]).days
        history_annual_ret = math.pow(history_ret + 1, CalculatorBase.TOTAL_DAYS_PER_YEAR/days) - 1
        
        return {
            'recent_natural_year_ret':recent_natural_year_ret,
            'recent_1w_ret':recent_1w_ret,
            'recent_1m_ret':recent_1m_ret,
            'recent_3m_ret':recent_3m_ret,
            'recent_6m_ret':recent_6m_ret,
            'recent_1y_ret':recent_1y_ret,
            'recent_2y_ret':recent_2y_ret,
            'recent_3y_ret':recent_3y_ret,
            'recent_4y_ret':recent_4y_ret,
            'recent_5y_ret':recent_5y_ret,
            'history_ret':history_ret,
            'history_annual_ret':history_annual_ret,
        }

    @staticmethod
    def get_period_ret(dates: pd.core.series.Series,
                       values: pd.core.series.Series,
                       frequency: str='3M'):
        assert frequency in ['1D','1W','2W','1M','3M','1Y'], 'frequency provided is not included, must in 1D 1W 2W 1M 3M 1Y'
        if frequency == '1Y':
            sr = pd.Series(values, index=dates).sort_index().dropna()
            year_list = set(sorted([i.year for i in sr.index]))
            _date = []
            for y in year_list:
                for m_d in [[12,31]]:
                    m = m_d[0]
                    d = m_d[1]
                    dt = datetime.date(y,m,d)
                    _date.append(dt)
            sr = sr.reindex(sr.index.union(_date)).sort_index().ffill().bfill()
            sr = sr.reindex([sr.index[0]] + _date).pct_change(1).dropna()
            sr = sr[sr!=0]
            df = pd.DataFrame(sr)
            df.columns = ['ret']
            return df.sort_index()
        if frequency == '3M':
            sr = pd.Series(values, index=dates).sort_index().dropna()
            year_list = set(sorted([i.year for i in sr.index]))
            _date = []
            for y in year_list:
                for m_d in [[3,31],[6,30],[9,30],[12,31]]:
                    m = m_d[0]
                    d = m_d[1]
                    dt = datetime.date(y,m,d)
                    _date.append(dt)
            sr = sr.reindex(sr.index.union(_date)).sort_index().ffill().bfill()
            sr = sr.reindex(_date).pct_change(1).dropna()
            sr = sr[sr!=0]
            df = pd.DataFrame(sr)
            df.columns = ['ret']
            return df.sort_index()
        sr = pd.Series(values, index=dates).sort_index().dropna()
        sr = sr.set_axis(pd.to_datetime(sr.index), inplace=False).resample(frequency,).last().dropna()
        df = pd.DataFrame(sr.pct_change(1).dropna())
        df.columns = ['ret']
        td = df.index
        df.index = [i.date() for i in td]
        return df.sort_index()

    @staticmethod
    def calc_recent_vol(dates:             pd.core.series.Series,
                        values:            pd.core.series.Series,
                        frequency:         str='1D'):
        assert frequency in ['1D','1W'], 'frequency provided is not included, must in 1D 1W 2W 1M'
        dates = pd.to_datetime(dates)
        dates = [i.date() for i in dates]
        _end_dt = dates[-1]
        last_date, begin_date_dic = CalculatorBase.get_begin_date_dic(week_end_date = _end_dt)
        assert len(dates) == len(values), 'date and port_values has different numbers'
        sr = pd.Series(values, index=dates).sort_index().dropna()
        sr = sr.set_axis(pd.to_datetime(sr.index), inplace=False).resample(frequency).last().dropna()
        sr.index = [i.date() for i in sr.index]
        sr_ret = sr.pct_change(1).dropna()
        if frequency == '1D':    
            period_1y = CalculatorBase.TRADING_DAYS_PER_YEAR
        elif frequency == '1W':
            period_1y = CalculatorBase.TOTAL_WEEKS_PER_YEAR
        _begin_date = sr_ret.index[0]
        _natural_year_begin_date = datetime.date(last_date.year,1,1)
        recent_natural_year_vol = sr_ret.loc[_natural_year_begin_date:].std(ddof=1) * np.sqrt(period_1y)
        recent_1w_vol = sr_ret.loc[max(begin_date_dic['w1'],_begin_date):].std(ddof=1) * np.sqrt(period_1y)
        recent_1m_vol = sr_ret.loc[max(begin_date_dic['m1'],_begin_date):].std(ddof=1) * np.sqrt(period_1y)
        recent_3m_vol = sr_ret.loc[max(begin_date_dic['m3'],_begin_date):].std(ddof=1) * np.sqrt(period_1y)
        recent_6m_vol = sr_ret.loc[max(begin_date_dic['m6'],_begin_date):].std(ddof=1) * np.sqrt(period_1y)
        recent_1y_vol = sr_ret.loc[max(begin_date_dic['y1'],_begin_date):].std(ddof=1) * np.sqrt(period_1y)
        recent_3y_vol = sr_ret.loc[max(begin_date_dic['y3'],_begin_date):].std(ddof=1) * np.sqrt(period_1y)
        recent_5y_vol = sr_ret.loc[max(begin_date_dic['y5'],_begin_date):].std(ddof=1) * np.sqrt(period_1y)
        history_vol = sr_ret.std(ddof=1) * np.sqrt(period_1y)
        return {
            'recent_natural_year_vol':recent_natural_year_vol,
            'recent_1w_vol':recent_1w_vol,
            'recent_1m_vol':recent_1m_vol,
            'recent_3m_vol':recent_3m_vol,
            'recent_6m_vol':recent_6m_vol,
            'recent_1y_vol':recent_1y_vol,
            'recent_3y_vol':recent_3y_vol,
            'recent_5y_vol':recent_5y_vol,
            'history_vol':history_vol,
        }

    @staticmethod
    def get_period_vol(dates: pd.core.series.Series,
                       values: pd.core.series.Series,
                       frequency: str='3M'):
        assert frequency in ['1D','1W','2W','1M','3M','1Y'], 'frequency provided is not included, must in 1D 1W 2W 1M 3M 1Y'
        sr = pd.Series(values, index=dates).sort_index().pct_change(1).dropna()
        if frequency == '1D':
            roll_d = CalculatorBase.TRADING_DAYS_PER_YEAR
        elif frequency == '1W':
            roll_d = 5
        elif frequency == '2W':
            roll_d = 10
        elif frequency == '1M':
            roll_d = 20
        elif frequency == '3M':
            roll_d = 60
        elif frequency == '1Y':
            roll_d = CalculatorBase.TRADING_DAYS_PER_YEAR
        if frequency == '1Y':
            sr = pd.Series(values, index=dates).sort_index().dropna()
            year_list = set(sorted([i.year for i in sr.index]))
            _date = []
            for y in year_list:
                for m_d in [[12,31]]:
                    m = m_d[0]
                    d = m_d[1]
                    dt = datetime.date(y,m,d)
                    _date.append(dt)
            sr = sr.reindex(sr.index.union(_date)).sort_index().ffill().pct_change(1)
            sr = sr.rolling(window=roll_d).std(ddof=1) * np.sqrt(CalculatorBase.TRADING_DAYS_PER_YEAR)
            sr = sr.reindex(_date).dropna()
            sr = sr[sr!=0]
            df = pd.DataFrame(sr)
            df.columns = ['vol']
            return df.sort_index()
        if frequency == '3M':
            sr = pd.Series(values, index=dates).sort_index().dropna()
            year_list = set(sorted([i.year for i in sr.index]))
            _date = []
            for y in year_list:
                for m_d in [[3,31],[6,30],[9,30],[12,31]]:
                    m = m_d[0]
                    d = m_d[1]
                    dt = datetime.date(y,m,d)
                    _date.append(dt)
            sr = sr.reindex(sr.index.union(_date)).sort_index().ffill().pct_change(1)
            sr = sr.rolling(window=roll_d).std(ddof=1) * np.sqrt(CalculatorBase.TRADING_DAYS_PER_YEAR)
            sr = sr.reindex(_date).dropna()
            sr = sr[sr!=0]
            df = pd.DataFrame(sr)
            df.columns = ['vol']
            df = df.sort_index()
            today = datetime.datetime.now().date()
            this_year = today.year
            year_list = np.array([datetime.date(this_year, m_d[0], m_d[1]) for m_d in [[3,31],[6,30],[9,30],[12,31]]])
            next_report_date = year_list[year_list>today][0]
            return df.loc[:next_report_date]
        sr = sr.rolling(window=roll_d).std(ddof=1) * np.sqrt(CalculatorBase.TRADING_DAYS_PER_YEAR)
        sr = sr.set_axis(pd.to_datetime(sr.index), inplace=False).resample(frequency).last().dropna()
        df = pd.DataFrame(sr)
        df.columns = ['vol']
        td = df.index
        df.index = [i.date() for i in td]
        return df.sort_index()

    @staticmethod
    def get_fund_correlation_df(df: pd.DataFrame):
        # 列是资产代码 index是日期
        # 求最近一年日度收益相关性
        return df.pct_change(1).corr()

    @staticmethod
    def get_stat_result(dates:             pd.core.series.Series,
                        values:            pd.core.series.Series,
                        benchmark_values:  pd.core.series.Series=None,
                        risk_free_rate:    float=0.025,
                        frequency:         str='1D',
                        ret_method:        str='log_ret',
                        ):# '1W' '1M'
        assert frequency in ['1D','1W','2W','1M'], 'frequency provided is not included, must in 1D 1W 2W 1M'
        assert ret_method in ['log_ret', 'pct_ret'], 'ret_method is not included'
        dates = pd.to_datetime(dates)
        dates = [i.date() for i in dates]
        _end_dt = dates[-1]
        last_date, begin_date_dic = CalculatorBase.get_begin_date_dic(week_end_date = _end_dt)
        assert len(dates) == len(values), 'date and port_values has different numbers'
        if len(dates) > 2:
            sr = pd.Series(values, index=dates).sort_index().dropna()
            sr = sr.set_axis(pd.to_datetime(sr.index), inplace=False).resample(frequency).last().dropna()
            sr.index = [i.date() for i in sr.index]
            if frequency == '1D':            
                period_1m = 20
                period_3m = period_1m * 3
                period_6m = period_1m * 6
                period_1y = CalculatorBase.TRADING_DAYS_PER_YEAR
                risk_free_per_period = risk_free_rate / CalculatorBase.TRADING_DAYS_PER_YEAR
            elif frequency == '1W':
                period_1m = 4
                period_3m = period_1m * 3
                period_6m = period_1m * 6
                period_1y = CalculatorBase.TOTAL_WEEKS_PER_YEAR
                risk_free_per_period = risk_free_rate / 52
            elif frequency == '2W':
                period_1m = 2
                period_3m = period_1m * 3
                period_6m = period_1m * 6
                period_1y = CalculatorBase.TOTAL_WEEKS_PER_YEAR / 2
                risk_free_per_period = risk_free_rate / 26
            elif frequency == '1M':
                period_1m = 1
                period_3m = period_1m * 3
                period_6m = period_1m * 6
                period_1y = CalculatorBase.TOTAL_MONTHS_PER_YEAR
                risk_free_per_period = risk_free_rate / 12
            if ret_method == 'log_ret':
                sr_ret = np.log(sr).diff(1).iloc[1:]
            elif ret_method == 'pct_ret':
                sr_ret = sr.pct_change(1).iloc[1:]
            start_date = sr.index[0] 
            end_date = sr.index[-1]
            days = (dates[-1] - dates[0]).days
            last_unit_nav = sr[-1] / sr[0]
            cumu_ret = last_unit_nav - 1
            trade_year = days / CalculatorBase.TOTAL_DAYS_PER_YEAR
            annual_ret = math.pow(last_unit_nav, CalculatorBase.TOTAL_DAYS_PER_YEAR/days) - 1
            annual_vol = sr_ret.std(ddof=1) * np.sqrt(period_1y)
            _begin_date = sr.index[0]
            recent_ret_res = CalculatorBase.calc_recent_ret(dates=dates,values=values,frequency='1D')
            recent_1w_ret = recent_ret_res['recent_1w_ret']
            recent_1m_ret = recent_ret_res['recent_1m_ret']
            recent_3m_ret = recent_ret_res['recent_3m_ret']
            recent_6m_ret = recent_ret_res['recent_6m_ret']
            recent_1y_ret = recent_ret_res['recent_1y_ret']
            recent_3y_ret = recent_ret_res['recent_3y_ret']
            recent_5y_ret = recent_ret_res['recent_5y_ret']
            worst_3m_ret = sr.pct_change(period_3m).min()
            worst_6m_ret = sr.pct_change(period_6m).min()
            last_mv_diff = sr[-1] - sr[-2]
            last_increase_rate = (sr[-1] - sr[-2])/ sr[-2]
            sharpe = (annual_ret - risk_free_rate) / annual_vol
            recent_drawdown = 1 - (sr[-1] / sr.max())
            if np.isnan(recent_drawdown):
                recent_mdd_date1 = None
                recent_mdd_lens = None
            else:
                recent_mdd_date1 = sr.idxmax()
                recent_mdd_lens = (end_date - recent_mdd_date1).days
            mdd_part =  sr / sr.rolling(window=sr.shape[0], min_periods=1).max()
            mdd = 1 - mdd_part.min()
            if np.isnan(mdd):
                mdd_date2 = None
                mdd_date1 = None
                mdd_lens = None
            else:
                mdd_date2 = mdd_part.idxmin()
                mdd_date1 = sr[:mdd_date2].idxmax()
                mdd_lens = (mdd_date2-mdd_date1).days
            calmar = (annual_ret - risk_free_rate) / mdd if mdd != 0 else 0
            sr_ret_no_risk_free = sr_ret - risk_free_rate / period_1y
            downside_risk = np.minimum(sr_ret_no_risk_free,0).std(ddof=1) * np.sqrt(period_1y)
            sortino = (annual_ret - risk_free_rate) / downside_risk
            var =  np.quantile(sr_ret, 0.05) # 按照最大回撤处理， 损失非负， 计算ervar用
            cvar = max(0, -sr_ret[sr_ret < var].mean())
            var = - var
            ervar = (annual_ret - risk_free_rate) / var
            skew_value = skew(sr_ret)
            kurtosis_value = kurtosis(sr_ret)        
            
            if benchmark_values is not None:
                assert len(dates) == len(benchmark_values), 'date and bench_values has different numbers'
                sr_benchmark = pd.Series(benchmark_values, index=dates).sort_index().dropna()
                sr_benchmark = sr_benchmark.set_axis(pd.to_datetime(sr_benchmark.index), inplace=False).resample(frequency).last().dropna()
                sr_benchmark.index = [i.date() for i in sr_benchmark.index]
                if ret_method == 'log_ret':
                    sr_benchmark_ret = np.log(sr_benchmark).diff(1).iloc[1:]
                elif ret_method == 'pct_ret':
                    sr_benchmark_ret = sr_benchmark.pct_change(1).iloc[1:]
                last_unit_benchmark = sr_benchmark[-1] / sr_benchmark[0]
                annual_ret_benchmark = math.pow(last_unit_benchmark, CalculatorBase.TOTAL_DAYS_PER_YEAR / days) - 1
                df = pd.concat([sr, sr_benchmark],axis=1)
                df.columns= ['fund_ret','index_ret']
                df_monthly = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(rule='1M').last()
                df_monthly.index = df_monthly.index.date
                monthly_ret = df_monthly.pct_change(1).dropna()
                continue_value_m = CalculatorBase.calc_continue_regress_v(monthly_ret.fund_ret,risk_free_rate)
                df_ret_risk_free = (df.pct_change(1) - risk_free_per_period).dropna()
                cl_res = CalculatorBase.calc_cl_alpha_beta(df_ret_risk_free.to_numpy())
                alpha_cl = cl_res['alpha'] * period_1y
                beta_cl = cl_res['beta']
                beta_bear = cl_res['beta_bear']
                beta_bull = cl_res['beta_bull']
                hm_res = CalculatorBase.calc_hm_alpha_beta(df_ret_risk_free.to_numpy())
                alpha_hm = hm_res['alpha'] * period_1y
                beta_hm = hm_res['beta']
                excess_ret = annual_ret - annual_ret_benchmark
                _index = sorted(sr_ret.index.intersection(sr_benchmark_ret.index))
                sr_ret = sr_ret.reindex(_index)
                sr_benchmark_ret = sr_benchmark_ret.reindex(_index)
                win_rate = np.mean((sr_ret > sr_benchmark_ret) * 1)
                corr = sr_ret.corr(sr_benchmark_ret)    
                track_err = (sr_ret - sr_benchmark_ret).std(ddof=1) * np.sqrt(period_1y)
                info = excess_ret / track_err
                x = (sr_benchmark_ret - risk_free_per_period).dropna() .values
                y = (sr_ret - risk_free_per_period).dropna().values
                x = sm.add_constant(x)
                model = regression.linear_model.OLS(y,x).fit()
                alpha = model.params[0]
                beta = model.params[1]
                treynor = (annual_ret - risk_free_rate) / beta
                not_system_risk = sum((sr_ret - risk_free_per_period)**2) \
                                - alpha * sum(sr_ret - risk_free_per_period) \
                                - beta * sum((sr_ret - risk_free_per_period) * (sr_benchmark_ret - risk_free_per_period))
                not_system_risk = np.sqrt(not_system_risk / (len(sr_ret) - 2))
                alpha = alpha * period_1y
                df_ret = np.log(df).diff(1).iloc[1:]
                df_ret_up = df_ret[df_ret.index_ret > 0] + 1 
                up_cap_top = df_ret_up.fund_ret.product() ** (period_1y/len(df_ret_up)) - 1
                up_cap_bot = df_ret_up.index_ret.product() ** (period_1y/len(df_ret_up)) - 1
                up_capture = up_cap_top / up_cap_bot

                df_ret_down = df_ret[df_ret.index_ret < 0] + 1
                df_ret_down_length = max(1,len(df_ret_down))
                down_cap_top = df_ret_down.fund_ret.product() ** (period_1y/df_ret_down_length) - 1
                down_cap_bot = df_ret_down.index_ret.product() ** (period_1y/df_ret_down_length) - 1
                down_capture = down_cap_top / down_cap_bot

                df_ret['excess_ret'] = df_ret.fund_ret - df_ret.index_ret
                df_ret = df_ret.replace(np.Inf,np.nan).replace(-np.Inf,np.nan).dropna()
                if df_ret.shape[0] < 4:
                    excess_ret_cotinue = np.nan
                else:
                    mod = AutoReg(endog=df_ret.excess_ret.values, lags=1)
                    res = mod.fit()
                    excess_ret_cotinue = res.params[0]
                return {
                    'start_date':start_date,
                    'end_date':end_date,
                    'trade_year':trade_year,
                    'last_unit_nav':last_unit_nav,
                    'cumu_ret':cumu_ret,
                    'annual_ret':annual_ret,
                    'annual_vol':annual_vol,
                    'sharpe':sharpe,
                    'recent_1w_ret':recent_1w_ret,
                    'recent_1m_ret':recent_1m_ret,
                    'recent_3m_ret':recent_3m_ret,
                    'recent_6m_ret':recent_6m_ret,
                    'recent_1y_ret':recent_1y_ret,
                    'recent_3y_ret': recent_3y_ret,
                    'recent_5y_ret':recent_5y_ret,
                    'worst_3m_ret':worst_3m_ret,
                    'worst_6m_ret':worst_6m_ret,
                    'last_mv_diff':last_mv_diff,
                    'last_increase_rate':last_increase_rate,
                    'recent_drawdown':recent_drawdown,
                    'recent_mdd_date1':recent_mdd_date1,
                    'recent_mdd_lens':recent_mdd_lens,
                    'mdd':mdd,
                    'mdd_date1':mdd_date1,
                    'mdd_date2':mdd_date2,
                    'mdd_lens':mdd_lens,
                    'calmar':calmar,
                    'downside_risk':downside_risk,
                    'sortino':sortino,
                    'var':var,
                    'ervar':ervar,
                    'skew':skew_value,
                    'kurtosis':kurtosis_value,
                    'alpha_cl':alpha_cl,
                    'beta_cl':beta_cl,
                    'beta_bear':beta_bear,
                    'beta_bull':beta_bull,
                    'alpha_hm':alpha_hm,
                    'beta_hm':beta_hm,
                    'excess_ret':excess_ret,
                    'win_rate':win_rate,
                    'corr':corr,
                    'track_err':track_err,
                    'info':info,
                    'alpha':alpha,
                    'beta':beta,
                    'treynor':treynor,
                    'not_system_risk':not_system_risk,
                    'cvar':cvar,
                    'up_capture':up_capture,
                    'down_capture':down_capture,
                    'excess_ret_cotinue':excess_ret_cotinue,
                    'continue_value_m':continue_value_m,
                }
            else:
                return {
                    'start_date':start_date,
                    'end_date':end_date,
                    'trade_year':trade_year,
                    'last_unit_nav':last_unit_nav,
                    'cumu_ret':cumu_ret,
                    'annual_ret':annual_ret,
                    'annual_vol':annual_vol,
                    'sharpe':sharpe,
                    'recent_1w_ret':recent_1w_ret,
                    'recent_1m_ret':recent_1m_ret,
                    'recent_3m_ret':recent_3m_ret,
                    'recent_6m_ret':recent_6m_ret,
                    'recent_1y_ret':recent_1y_ret,
                    'recent_3y_ret': recent_3y_ret,
                    'recent_5y_ret':recent_5y_ret,
                    'worst_3m_ret':worst_3m_ret,
                    'worst_6m_ret':worst_6m_ret,
                    'last_mv_diff':last_mv_diff,
                    'last_increase_rate':last_increase_rate,
                    'recent_drawdown':recent_drawdown,
                    'recent_mdd_date1':recent_mdd_date1,
                    'recent_mdd_lens':recent_mdd_lens,
                    'mdd':mdd,
                    'mdd_date1':mdd_date1,
                    'mdd_date2':mdd_date2,
                    'mdd_lens':mdd_lens,
                    'calmar':calmar,
                    'downside_risk':downside_risk,
                    'sortino':sortino,
                    'var':var,
                    'cvar':cvar,
                    'ervar':ervar,
                    'skew':skew_value,
                    'kurtosis':kurtosis_value,
                }
        else:
            return {
                    'start_date':dates[0] if len(dates) > 0 else None,
                    'end_date':dates[-1] if len(dates) > 0 else None,
                    'trade_year':0,
                    'last_unit_nav':0,
                    'cumu_ret':0,
                    'annual_ret':0,
                    'annual_vol':0,
                    'sharpe':0,
                    'recent_1w_ret':0,
                    'recent_1m_ret':0,
                    'recent_3m_ret':0,
                    'recent_6m_ret':0,
                    'recent_1y_ret':0,
                    'recent_3y_ret': 0,
                    'recent_5y_ret':0,
                    'worst_3m_ret':0,
                    'worst_6m_ret':0,
                    'last_mv_diff':0,
                    'last_increase_rate':0,
                    'recent_drawdown':0,
                    'recent_mdd_date1':dates[0] if len(dates) > 0 else None,
                    'recent_mdd_lens':0,
                    'mdd':0,
                    'mdd_date1':dates[0] if len(dates) > 0 else None,
                    'mdd_date2':dates[0] if len(dates) > 0 else None,
                    'mdd_lens':0,
                    'calmar':0,
                    'downside_risk':0,
                    'sortino':0,
                    'var':0,
                    'cvar':0,
                    'ervar':0,
                    'skew':0,
                    'kurtosis':0,
                    'alpha_cl':0,
                    'beta_cl':0,
                    'beta_bear':0,
                    'beta_bull':0,
                    'alpha_hm':0,
                    'beta_hm':0,
                    'excess_ret':0,
                    'win_rate':0,
                    'corr':0,
                    'track_err':0,
                    'info':0,
                    'alpha':0,
                    'beta':0,
                    'treynor':0,
                    'not_system_risk':0,
                    'cvar':0,
                    'up_capture':0,
                    'down_capture':0,
                    'excess_ret_cotinue':0,
                    'continue_value_m':0,
                }

    @staticmethod
    def simulated_mv_calc(df,fee_dic,weight_dic):
        '''
        df structure: 
                    index   : datetime
                    column  : different assets mv
        i.g.

                	A	    B	    C	    D	    E
        2020-03-02	1.2047	1.0858	1.4002	1.0482	1.000
        2020-03-06	1.2156	1.0983	1.4211	1.0496	1.005
        
        mng_fee_dic: 
        i.g.            
            fee_dic = {'A':0.2,'B':0.2,'C':0.2,'D':0.2,'E':0.2}
        
        weight_dic: value or weight 
        i.g.
            weight_dic = {'A':1,'B':1,'C':1,'D':1,'E':1}

        '''
        # 归一化
        df_to_1 = df / df.iloc[0]
        # 盈利
        excess_ret = (df_to_1 - 1)
        # 盈 或 亏
        earn_con = (excess_ret > 0) * 1
        # 费
        pay_mng_fee = excess_ret * earn_con * pd.DataFrame([fee_dic]).values
        # 净值
        simu_nav = df_to_1
        simu_nav_vir = df_to_1 - pay_mng_fee
        # 真实总净值
        simu_nav_total = pd.DataFrame((simu_nav*pd.DataFrame([weight_dic]).values).sum(axis=1))
        # 虚拟总净值
        simu_nav_vir_total = pd.DataFrame((simu_nav_vir*pd.DataFrame([weight_dic]).values).sum(axis=1))
        simu_nav_total.columns = ['mv']
        simu_nav_vir_total.columns = ['mv']
        return simu_nav_vir_total, simu_nav_total

    @staticmethod
    def df_data_select(df, start_date, end_date, cols, resample_method, drop_col_title):
        # 组合净值分析时 净值选取
        # 设置 起始日 截止日 选取列名 对列共同名字是否去掉
        if end_date is None:
            end_date = datetime.date(2040,1,1)
        if start_date is None:
            start_date = datetime.date(2010,1,1)
        if cols is not None:
            df = df[cols]
        df = CalculatorBase.data_resample(df.loc[start_date:end_date], resample_method, drop_col_title)
        return df

    @staticmethod
    def data_resample(df, resample_method, drop_col_title=True):
        COL_TITLE = '融智'
        if resample_method == '1D':
            return df 
        if drop_col_title:
            cols = df.columns.tolist()
            cols = [i.replace(COL_TITLE,'') for i in cols]
            df.columns = cols
        df = df.set_axis(pd.to_datetime(df.index), inplace=False).resample(resample_method).last()
        df.index = [i.date() for i in df.index]
        df.index.name = 'datetime'
        return df.ffill()

    @staticmethod
    def proper_round(num, dec=0):
        dec = Decimal(10) ** -dec
        return float(Decimal(str(num)).quantize(dec, context=Context(rounding=ROUND_HALF_UP)))

    @staticmethod
    def stock_ipo_continue_up_limit(    dates:  pd.core.series.Series,
                                        values: pd.core.series.Series,
                                        ipo_price: float,
                                        list_date: datetime.date,
                                        ipo_date: datetime.date,
                                        trade_market: str,
                                        stock_name: str,
                                        stock_code: str):
        dates = pd.to_datetime(dates)
        dates = [i.date() for i in dates]
        assert len(dates) == len(values), 'date and port_values has different numbers'
        df = pd.DataFrame(values, index=dates).sort_index().dropna()
        col = 'price'
        df.columns = [col]
        rate = [1.44] + df.shape[0] * [1.1]
        df.loc[ipo_date,col] = ipo_price
        df = df.sort_index()
        if trade_market in ['上交所主板','深交所中小板']:
            df.loc[:,'limit_price'] = (df.price * rate).map(lambda x: CalculatorBase.proper_round(x,2)).shift(1)
            df.loc[:,'limit_con'] = (df.limit_price == df.price) * 1  
            limit_list = df.limit_con.iloc[1:].tolist()
            if 0 not in limit_list:
                ipo_lens = len(limit_list)
            else:
                ipo_lens = limit_list.index(0)
            num = CalculatorBase.STOCK_IPO_NUM_MARKET[trade_market]
            earning_per_stick = int(round((df.price.values[ipo_lens] - df.price.values[0]) * num))
        else:
            ipo_lens = np.nan
            earning_per_stick = np.nan
        res = {
            'stock_code':stock_code,
            'stock_name':stock_name,
            'trade_market':trade_market,
            'list_date':list_date,
            'ipo_price':ipo_price,
            'latest_price':df.price.values[-1],
            'latest_rate':df.price.pct_change(1).values[-1],
            'cumulate_rate':df.price.values[-1] / df.price.values[0] - 1,
            'first_date_rate':df.price.values[1] / df.price.values[0] - 1,
            'continue_limited_rise':ipo_lens,
            'earn_per_stick':earning_per_stick,
        }
        return res

    @staticmethod
    def conv_bond_ipo_result(   bond_id:str,
                                bond_name:str,
                                list_date:datetime.date,
                                ipo_price:float,
                                dates:pd.core.series.Series,
                                close_values:pd.core.series.Series,
                                open_values:pd.core.series.Series,
                                rate:float,
                                limit_num:str):

        rate = rate / 100
        dates = pd.to_datetime(dates)
        dates = [i.date() for i in dates]
        assert len(dates) == len(close_values), 'date and port_values has different numbers'
        assert len(dates) == len(open_values), 'date and port_values has different numbers'
        df = pd.DataFrame({'close':close_values,'open':open_values}, index=dates).sort_index().dropna()
        limit_num = int(limit_num.split('网上申购数量上限：')[1].split('手')[0])
        trade_market = bond_id.split('.')[1]
        new_price = df.close[-1]
        total_ret = df.close[-1] / ipo_price - 1
        first_open = df.open[0]
        first_date_rate = df.close[0] / 100 - 1
        earn_per_stick = (first_open - ipo_price) * 10
        earn_per_account = earn_per_stick * limit_num * rate
        res = {
            'bond_id':bond_id,
            'bond_name':bond_name,
            'list_date':list_date,
            'ipo_price':ipo_price,
            'trade_market':trade_market,
            'new_price':new_price,
            'total_ret':total_ret,
            'earn_per_account':earn_per_account,
            'earn_per_stick':earn_per_stick,
            'first_date_rate':first_date_rate,
            'first_open':first_open,
            'rate':rate,
            'limit_num':limit_num,
        }
        return res