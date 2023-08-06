import requests
import pandas as pd
import numpy as np
pd.options.display.float_format = '{:,.2f}'.format


def set_terms(start, end):
    '''
    :param start: The first date of period
    :param end: The last date of period
    :return: The array of period in quarters format
    '''
    terms = pd.period_range(start=start, end=end, freq='Q').strftime('%YQ%q')
    return terms


def fn_consolidated(otp, symbol='', term=''):
    '''
    :param otp: One time passcode to access the finterstellar.com api
    :param symbol: Symbol or ticker of equity by finance.yahoo.com
    :param term: Term name in quarters format to retrieve financial data
    :return: The consolidate financial data of whole equities in designated term
    '''
    if term!='' or symbol!='':
        url = 'http://finterstellar.com/api/consolidated?otp={}&symbol={}&term={}'.format(otp, symbol, term)
        r = requests.get(url)
        try:
            df = pd.read_json(r.text, orient='index')
            df.set_index('symbol', inplace=True)
            df = df[~(pd.isna(df['Revenue'])|pd.isna(df['Price']))].fillna(0).copy()
            return df
        except:
            print(r.text)
    else:
        return 'Either symbol or term is required.'


def fn_single(otp, symbol='', window='T'):
    '''
    :param otp: One time passcode to access the finterstellar.com api
    :param symbol: Symbol or ticker of equity by finance.yahoo.com
    :param window: The way how to summarize financial data (Q:Quarterly, Y:Yearly, T:TTM)
    :return: The financial data of a company
    '''
    url = 'http://finterstellar.com/api/single?otp={}&symbol={}&window={}'.format(otp, symbol, window)
    r = requests.get(url)
    try:
        df = pd.read_json(r.text, orient='index')
        if 'Current Debt' in df.columns:
            df['Current Debt'].fillna(0, inplace=True)
        else:
            df['Current Debt'] = 0
        df = df[~(pd.isna(df['Revenue'])|pd.isna(df['Price']))].fillna(0).copy()
        return df
    except:
        print(r.text)


def fn_filter(df, by='PER', floor=-np.inf, cap=np.inf, n=None, asc=True):
    '''
    :param df: Dataframe storing financial data to be filtered
    :param by: Column name to be used a filter
    :param floor: The minimum value of data range to be selected
    :param cap: The maximum value of data range to be selected
    :param n: The size of result data
    :param asc: Sorting order of result data
    :return: The selected data after filtering
    '''
    df[by].replace([-np.inf, np.inf], np.nan, inplace=True)
    rst = df.query(('`{b}`>={f} and `{b}`<={c}').format(b=by,f=floor,c=cap))[['term',by]].sort_values(by=by, ascending=asc)[:n]
    # rst[by].dropna(inplace=True)
    rst.drop(columns='term', inplace=True)
    return rst


def fn_score(df, by='PER', method='relative', floor=None, cap=None, asc=True):
    '''
    :param df: Dataframe storing financial data to be scored
    :param by: Column name to be used to score
    :param method: The way how to score the data. 'relative' scores data according to their rank, 'absolute' scores data according to value
    :param floor: The minimum value of data range to be selected
    :param cap: The maximum value of data range to be selected
    :param asc: Sorting order of result data
    :return: The score data
    '''
    df[by].replace([-np.inf, np.inf], np.nan, inplace=True)
    floor = df[by].min() if floor is None else floor
    cap = df[by].max() if cap is None else cap
    if method == 'absolute':
        rst = df.query(('`{b}`>={f} and `{b}`<={c}').format(b=by,f=floor,c=cap))[['term',by]].sort_values(by=by, ascending=asc)
        if asc is True:
            rst['Score'] = round((1 - (rst[by] - floor) / (cap - floor)), 3) * 100
        else:
            rst['Score'] = round(((rst[by] - floor) / (cap - floor)), 3) * 100
    else:
        rst = df.query(('`{b}`>={f} and `{b}`<={c}').format(b=by,f=floor,c=cap))[['term',by]].sort_values(by=by, ascending=asc)
        rst['Rank'] = rst[by].rank(method='min')
        if asc:
            rst['Score'] = round( ( 1 - (rst['Rank']-1)/rst['Rank'].max() ), 3) * 100
        else:
            rst['Score'] = round(((rst['Rank'] - 1) / rst['Rank'].max()), 3) * 100
        rst.drop(columns=['Rank'], inplace=True)
    rst.drop(columns=['term'], inplace=True)
    return rst


def combine_signal(*signals, how='and', n=None):
    '''
    :param signals: Data set storing trading signal
    :param how: The joining method. Select 'and' for intersection, 'or' for union
    :param n: The size of result data
    :return: Combination of signals
    '''
    how_dict = {'and':'inner', 'or':'outer'}
    signal = signals[0]
    for s in signals[1:]:
        signal = signal.join(s, how=how_dict[how])
    return signal[:n]


def combine_score(*signals, n=None):
    '''

    :param signals: Data set storing trading signal
    :param n: The size of result data
    :return: Sum of scores
    '''
    size = len(signals)
    signal = signals[0].copy()
    signal['Score'] = signal['Score']/size
    for s in signals[1:]:
        signal = signal.join(s['Score']/size, how='outer', rsuffix='_')
        # signal['Score'] = round(signal['Score'].add(s['Score']/size, fill_value=0), 2)
    signal.drop(columns=[list(signal.columns)[0]], inplace=True)
    signal['Sum'] = signal.sum(axis=1)
    return signal.sort_values(by='Sum', ascending=False)[:n]


# def combine_score_(*signals, n=None):
#     '''
#
#     :param signals: Data set storing trading signal
#     :param n: The size of result data
#     :return: Sum of scores
#     '''
#     size = len(signals)
#     signal = signals[0].copy()
#     signal['Score'] = signal['Score']/size
#     for s in signals[1:]:
#         signal['Score'] = round(signal['Score'].add(s['Score']/size, fill_value=0), 2)
#     return signal.sort_values(by='Score', ascending=False)[:n]


def backtest(signal, data, m=3, cost=.001, rf_rate=.01):
    '''

    :param signal: Data set storing trading signal
    :param data: Dataframe storing financial data to be tested
    :param m: Rebalancing date in month unit after the quarter end
    :param cost: Cost of transaction
    :param rf_rate: Risk free rate
    :return: Trading result such as Return, CAGR, Test period, Sharpe ratio, MDD
    '''
    # 포트폴리오 종목 세팅
    stocks = set()
    for k, v in signal.items():
        for s in v:
            stocks.add(s)

    # 트레이딩 포지션 기록
    trades = pd.DataFrame()
    for k, v in signal.items():
        for s in stocks:
            trades.loc[k, s] = 'l' if s in list(v) else 'z'
    prev = trades.shift(periods=1, axis=0)
    prev.fillna('z', inplace=True)
    position = prev + trades

    # 트레이딩 가격 산출
    pm = {0:'Price', 1:'Price_M1', 2:'Price_M2', 3:'Price_M3'}
    prices = pd.DataFrame()
    for t in position.index:
        # prices[t] = data[t][pm[m]][position.columns]
        prices[t] = data[t][pm[m]].reindex(position.columns)
    prices_filtered = prices.T

    # 거래별 수익 계산
    position_cal = position.copy()
    position_cal.replace('zz', 0.0, inplace=True)
    position_cal.replace(['zl', 'll'], 1.0, inplace=True)
    position_cal.replace('lz', 1-cost, inplace=True)
    invest = prices_filtered * position_cal

    # 수익률 계산
    rtn = invest / invest.shift(1, axis=0)
    rtn.replace([np.inf, -np.inf, 0.0], 1, inplace=True)
    rtn.fillna(1, inplace=True)
    rtn[position=='zl'] = 1

    # 기별수익률 계산
    # rtn['term_rtn'] = rtn.replace(1.0, np.nan).mean(axis=1).replace(np.nan, 1.0)
    n = max([len(signal[x]) for x in list(signal.keys())])
    rtn['term_rtn'] = ( rtn.replace(1.0, np.nan).sum(axis=1) + (n - rtn.replace(1.0, np.nan).count(axis=1)) ) / n
    rtn['acc_rtn'] = rtn['term_rtn'].cumprod()
    rtn['dd'] = rtn['acc_rtn'] / rtn['acc_rtn'].cummax()
    rtn['mdd'] = rtn['dd'].cummin()

    tq = []
    for q in rtn.index:
        tq.append((pd.Period(q) + 1).strftime('%YQ%q'))
    rtn.index = tq

    rst = {}
    rst['position'] = position
    rst['rtn'] = rtn

    period = __get_period(rtn)
    rst['period'] = period

    # 포트폴리오전체수익률
    rst['portfolio_rtn'] = rtn['acc_rtn'][-1]
    rst['mdd'] = rtn['mdd'][-1]
    # Sharpe
    rst['sharpe'] = __get_sharpe_ratio(rtn, rf_rate)

    # 연환산
    rst['portfolio_rtn_annual'] = rst['portfolio_rtn'] ** (1/period) if period > 1 \
        else (rst['portfolio_rtn']-1) * (1/period) + 1

    print('Accumulated return: {:.2%}'.format(rst['portfolio_rtn'] - 1))
    print('Annualized return: {:.2%}'.format(rst['portfolio_rtn_annual'] - 1))
    print('Investment period: {:.1f}yrs'.format(rst['period']))
    print('Sharpe ratio: {:.2f}'.format(rst['sharpe']))
    print('MDD: {:.2%}'.format(rst['mdd'] - 1))
    return rtn


def __get_sharpe_ratio(df, rf_rate=.01):
    period = __get_period(df)
    df['sharpe_raw'] = (df['term_rtn']-1) - (rf_rate/4)
    sharpe_ratio = round( ( (df['acc_rtn'][-1] - 1 - rf_rate*period) / (df['sharpe_raw'].std() * np.sqrt(period*4)) ) / period , 2) if df['sharpe_raw'].std()>0 else 0
    return round(sharpe_ratio, 4)


def __get_period(df):
    period = (pd.Period(df.index[-1]).end_time - pd.Period(df.index[0]).start_time).days / 365
    return period


def quarters_before(terms, t, n):
    '''
    Return past quarter value
    :param terms: All terms
    :param current: Current term
    :param n: The value of n quarter before current term
    :return:
    '''
    return terms[list(terms).index(t) - n] if list(terms).index(t) >= n else terms[0]


def sector_info(df):
    '''

    :param df: Dataframe storing sector and industry information
    :return: Sectors and industries
    '''
    sector_info = df.groupby(by='sector', axis=0)['industry'].unique()
    return sector_info


def sector_filter(df, sector=None):
    '''

    :param df: Dataframe storing sector and industry information
    :param sector: Sectors to be selected
    :return: The data of selected sector
    '''
    sectors = sector if isinstance(sector, list) else [sector]
    rst = pd.DataFrame()
    for s in sectors:
        rst = pd.concat((rst, df[(df['sector']==s)]), axis=0)
    return rst


def industry_filter(df, industry=None):
    '''

    :param df: Dataframe storing sector and industry information
    :param industry: Industries to be selected
    :return: The data of selected industries
    '''
    industries = industry if isinstance(industry, list) else [industry]
    rst = pd.DataFrame()
    for s in industries:
        rst = pd.concat((rst, df[(df['industry']==s)]), axis=0)
    return rst


def view_portfolio(data, signal, term=None):
    '''

    :param df: Dataframe storing financial data
    :param signal: The stocks selected according to the trading strategies
    :param term: Term name to retrieve data
    :return: The selected stocks of designated term
    '''
    t = term if term else list(data.keys())[-1]
    return data[t].loc[signal[t]][['name','sector','industry','avg_volume']].sort_values(by=['sector','industry'])


'''
class Financials:
    def __init__(self, start_date=None, end_date=None, country='US'):
        self.end_date = pd.to_datetime(end_date).date() if end_date else Common.last_trade_date()
        self.start_date = pd.to_datetime(start_date).date() if start_date else (pd.to_datetime(self.end_date) - pd.DateOffset(years=1)).date()
        self.period_length = (pd.to_datetime(self.end_date) - pd.to_datetime(self.start_date)).days / 365
        self.month_ends = self.get_month_ends(country)
        self.quarter_ends = self.get_quarter_ends(country)
        self.quarters = self.set_quarters(ttm=False)
        self.quarters_ttm = self.set_quarters(ttm=True)
        self.acct_master = ValueMaster.acct_master

    def get_month_ends(self, country):
        sql = 'SELECT * FROM price_daily WHERE symbol="{}" AND volume>0 '.format('A069500' if country=='KR' else 'SPY')
        sql += 'AND date >= "{}" '.format(self.start_date) if self.start_date else ''
        sql += 'AND date <= "{}" '.format(self.end_date) if self.end_date else ''
        trade_dates = IO.query_df(sql)
        trade_dates.set_index('date', inplace=True)
        month_ends = []
        prev_d = trade_dates.index[0]
        for d in trade_dates.index:
            if d.month != prev_d.month:
                month_ends.append(prev_d.strftime('%Y-%m-%d'))
            prev_d = d
        if month_ends[-1] != trade_dates.index[-1]:
            month_ends.append(trade_dates.index[-1].strftime('%Y-%m-%d'))
        return tuple(month_ends)

    def get_quarter_ends(self, country):
        sql = 'SELECT * FROM price_daily WHERE symbol="{}" AND volume>0 '.format('A069500' if country=='KR' else 'SPY')
        sql += 'AND date >= "{}" '.format(self.start_date) if self.start_date else ''
        sql += 'AND date <= "{}" '.format(self.end_date) if self.end_date else ''
        trade_dates = IO.query_df(sql)
        trade_dates.set_index('date', inplace=True)
        quarter_ends = []
        prev_d = trade_dates.index[0]
        for d in trade_dates.index:
            if pd.to_datetime(d).quarter != pd.to_datetime(prev_d).quarter:
                quarter_ends.append(prev_d.strftime('%Y-%m-%d'))
            prev_d = d
        if quarter_ends[-1] != trade_dates.index[-1]:
            quarter_ends.append(trade_dates.index[-1].strftime('%Y-%m-%d'))
        return tuple(quarter_ends)

    def pickup_rebalance_date(self, d):
        for m in self.month_ends:
            if abs((pd.to_datetime(m).date() - d).days) < 15:
                return m

    def set_quarters(self, ttm=False):
        if ttm:
            year = (pd.to_datetime(self.start_date) - pd.DateOffset(months=9)).year
            quarter = (pd.to_datetime(self.start_date) - pd.DateOffset(months=9)).quarter
        else:
            year = pd.to_datetime(self.start_date).year
            quarter = pd.to_datetime(self.start_date).quarter
        start_term = pd.Period(year=year, quarter=quarter, freq='Q').start_time.date()
        end_term = (pd.to_datetime(self.end_date) - pd.DateOffset(months=2)).date()
        terms = pd.period_range(start=start_term, end=end_term, freq='3M')
        rebalance_dates = []
        if not ttm:
            for t in terms:
                rebalance_dates.append( max([m for m in self.month_ends if pd.to_datetime(m) < (t.end_time.date() + pd.DateOffset(days=70))]))
        quarters = {}
        for i in range(len(terms)):
            if ttm:
                quarters['{}Q{}'.format(terms[i].year, terms[i].quarter)] = [terms[i].start_time.date(), terms[i].end_time.date()]
            else:
                quarters['{}Q{}'.format(terms[i].year, terms[i].quarter)] = [terms[i].start_time.date(), terms[i].end_time.date(), rebalance_dates[i]]
        return quarters


    # column: 기간 / index: 심볼
    def multi_from_raw(self, account, symbol=None, sector=None, country='US'):
        doc = self.acct_master[account][0]
        ttm = self.acct_master[account][1]
        name = self.acct_master[account][7] if country=='KR' else self.acct_master[account][2]
        quarters = self.quarters_ttm if ttm else self.quarters
        query = 'SELECT M.symbol, '
        for k, v in quarters.items():
            if country=='KR':
                query += ' MAX(CASE WHEN term BETWEEN "{}" AND "{}" THEN vlu END) AS `{}`, '.format(v[0].strftime('%Y/%m'), v[1].strftime('%Y/%m'), k)
            else:
                query += ' MAX(CASE WHEN term BETWEEN "{}" AND "{}" THEN vlu END) AS `{}`, '.format(v[0], v[1], k)
        query = query[:-2]
        query += ' FROM _financials F, master M '
        query += 'WHERE M.symbol = F.symbol '
        query += 'AND title="{}" '.format(name) if country=='KR' else 'AND title="{}" AND doc="{}" '.format(name, doc)
        query += 'AND M.country="{}" '.format(country)
        if symbol:
            query += 'AND M.symbol in ('
            for s in symbol:
                query += '"{}", '.format(s)
            query = query[:-2]
            query += ') '
        query += 'AND M.sector="{}" '.format(sector) if sector else ''
        query += 'GROUP BY M.symbol'

        df = IO.query_df(query)
        if isinstance(df, pd.DataFrame):
            df.set_index('symbol', inplace=True)
            if ttm=='ttm':
                df = df.rolling(4, axis=1).sum()
            df.dropna(how='all', axis=1, inplace=True)   # 암것도 없는 기간은 삭제
        return df


    # column: 심볼 / index: 기간
    def multi_from_factor_value(self, acct, symbols):
        query = 'SELECT term, '
        for s in symbols:
            query += 'MAX(CASE WHEN symbol="{s}" THEN `{a}` END) AS "{s}", '.format(a=acct, s=s)
        query = query[:-2]
        query += ' FROM factor_value '
        query += 'WHERE term >= "{}" '.format(list(self.quarters.keys())[0])
        query += 'AND term <= "{}" '.format(list(self.quarters.keys())[-1])
        query += 'GROUP BY term '
        query += 'ORDER BY term'
        rst = IO.query_df(query)
        rst.set_index('term', inplace=True)
        return rst

    # column: 심볼 / index: 기간
    def single_from_factor_value(self, symbol):
        query = 'SELECT * FROM factor_value WHERE symbol="{}" '.format(symbol)
        query += 'AND term >= "{}" '.format(list(self.quarters.keys())[0])
        query += 'AND term <= "{}" '.format(list(self.quarters.keys())[-1])
        rst = IO.query_df(query)
        rst.drop(columns=['symbol'], inplace=True)
        rst.set_index('term', inplace=True)
        rst['Dividend'] = rst['Dividend'] * -1
        return rst

    # column: 기간 / index: 심볼
    def single_from_raw(self, symbol, ttm=False):
        query = 'SELECT term, '
        for k,v in ValueMaster.raw_acct.items():
            query += 'MAX(CASE WHEN title="{}" THEN vlu END) AS "{}", '.format(v[0], k)
        query = query[:-2]
        query += ' FROM _financials '
        query += 'WHERE symbol="{}" '.format(symbol)
        query += 'GROUP BY term'
        df = IO.query_df(query)
        df.set_index('term', inplace=True)
        if ttm:
            df = df.rolling(4, axis=0).sum()
            df.dropna(how='all', axis=0, inplace=True)
            df.fillna(0, inplace=True)
        return df


    def month_end_price(self, symbol, dates=None):
        dates = dates if dates else self.month_ends
        query = 'SELECT date '
        for s in symbol:
            query += ', max(case when symbol="{s}" then close end) as "{s}" '.format(s=s)
        query += 'FROM price_daily '
        query += 'WHERE symbol in ( '
        for s in symbol:
            query += '"{}", '.format(s)
        query = query[:-2]
        query += ') '
        query += 'AND date in {} '.format(dates)
        query += 'GROUP BY date '
        query += 'ORDER BY date ; '
        rows = IO.query_df(query)
        rows.set_index('date', inplace=True)
        rows.index = pd.to_datetime(rows.index)
        self.prices = rows
        return rows


    def quarter_end_price(self, symbol, dates=None):
        dates = dates if dates else self.quarter_ends
        query = 'SELECT date '
        for s in symbol:
            query += ', max(case when symbol="{s}" then close end) as "{s}" '.format(s=s)
        query += 'FROM price_daily '
        query += 'WHERE symbol in ( '
        for s in symbol:
            query += '"{}", '.format(s)
        query = query[:-2]
        query += ') '
        query += 'AND date in {} '.format(dates)
        query += 'GROUP BY date '
        query += 'ORDER BY date ; '
        rows = IO.query_df(query)
        rows.set_index('date', inplace=True)
        rows.index = pd.to_datetime(rows.index)
        self.prices = rows
        return rows


    def signal_by_term(self, constraints, limit=10, country='US', trend=False, liquid=False, profit=False):
        query = ''
        for qk, qv in self.quarters.items():
            query += '( SELECT term, M.symbol FROM factor_value V, master M '
            query += 'WHERE V.symbol=M.symbol AND active="Y" AND country="{}" '.format(country)
            query += 'AND avg_volume>100000 ' if liquid else ''
            query += 'AND eps>0 ' if profit else ''
            query += 'AND term = "{}" '.format(qk)
            for ck, cv in constraints.items():
                query += 'AND `{}` > {} '.format(ck, cv[4]) if cv[4] is not None else ''
                query += 'AND `{}` < {} '.format(ck, cv[5]) if cv[5] is not None else ''
            query += 'ORDER BY ('
            for ck, cv in constraints.items():
                query += 'RANK() OVER(ORDER BY `{}` {}) + '.format(ck, cv[6])
            query = query[:-2]
            query += ') LIMIT {} ) '.format(limit)
            query += 'UNION '
        query = query[:-6]
        # print(query)
        rs = IO.query_df(query)
        signal = {}
        for t in rs.term.drop_duplicates():
            signal[t] = list(rs[rs.term == t]['symbol'])
        return signal


    def backtest(self, signal, limit, cost=0):
        # 포트폴리오 종목 세팅
        stocks = set()
        for k, v in signal.items():
            for s in v:
                stocks.add(s)
        # 트레이딩 포지션 기록
        trades = pd.DataFrame()
        for k, v in signal.items():
            for s in stocks:
                trades.loc[k, s] = 'l' if s in list(v) else 'z'
        prev = trades.shift(periods=1, axis=0)
        prev.fillna('z', inplace=True)
        position = prev + trades
        # 트레이딩 가격 산출
        price_dates = []
        for p in position.index:
            price_dates.append(pd.to_datetime(self.quarters[p][2]))
        prices = self.month_end_price(position.columns)
        prices_filtered = prices[stocks].filter(items=price_dates, axis=0)
        prices_filtered.index = position.index

        # 거래별 수익 계산
        position_cal = position.copy()
        position_cal.replace('zz', 0.0, inplace=True)
        position_cal.replace(['zl', 'll'], 1.0, inplace=True)
        position_cal.replace('lz', 1-cost, inplace=True)
        invest = prices_filtered * position_cal

        # 수익률 계산
        rtn = invest / invest.shift(1, axis=0)
        rtn.replace([np.inf, -np.inf, 0.0], 1, inplace=True)
        rtn.fillna(1, inplace=True)

        # 기별수익률 계산
        # rtn['term_rtn'] = rtn.replace(1.0, np.nan).mean(axis=1).replace(np.nan, 1.0)
        rtn['term_rtn'] = ( rtn.replace(1.0, np.nan).sum(axis=1) + (limit - rtn.replace(1.0, np.nan).count(axis=1)) ) / limit
        rtn['acc_rtn'] = rtn['term_rtn'].cumprod()
        rtn['dd'] = rtn['acc_rtn'] / rtn['acc_rtn'].cummax()
        rtn['mdd'] = rtn['dd'].cummin()

        rst = {}
        rst['position'] = position
        rst['rtn'] = rtn

        period = (pd.to_datetime(rtn.index[-1]) - pd.to_datetime(rtn.index[0])).days / 365
        # 포트폴리오전체수익률
        rst['portfolio_rtn'] = rtn['acc_rtn'][-1]
        rst['mdd'] = rtn['mdd'][-1]
        # Sharpe
        rf_rate = .01
        rtn['sharpe_raw'] = (rtn['term_rtn']-1) - (rf_rate/4)
        rst['sharpe'] = round( ( (rtn['acc_rtn'][-1] - 1 - rf_rate*period) / (rtn['sharpe_raw'].std() * np.sqrt(period)) ) / period , 2)

        # 연환산
        rst['period'] = period
        rst['portfolio_rtn_annual'] = rst['portfolio_rtn'] ** (1/period) if period > 1 \
            else (rst['portfolio_rtn']-1) * (1/period) + 1
        return rst
'''