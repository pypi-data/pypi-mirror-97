import pandas as pd
import baostock as bs
from tqdm import tqdm
from itertools import combinations
from .GetDate import GetDate
import datetime


class GetStock(object):
    def __init__(self, names=None,
                 start_date='2020-12-01', end_date='2020-12-31',
                 frequency="w"):
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        if type(names) == str:
            self.names = [names]
        elif type(names) == list:
            self.names = names
        self.bs = bs
        self.bs.login()

    @property
    def stock_pair(self):
        print('getting stock pair...')
        lists = []
        for i in tqdm(self.names):
            rs = self.bs.query_stock_industry()
            rs = self.bs.query_stock_basic(code_name=i)
            industry_list = []
            while (rs.error_code == '0') & rs.next():
                industry_list.append(rs.get_row_data())
            info = pd.DataFrame(industry_list, columns=rs.fields)
            lists.append(info)
        df = pd.concat(lists)
        stocks = {}
        for i, j in df[['code', 'code_name']].iterrows():
            stocks[j[1]] = j[0]
        return stocks

    @property
    def stock_data(self, info="date,code,open,close,volume,amount,adjustflag,turn,pctChg"):

        stock_pair = self.stock_pair
        codes = list(stock_pair.values())
        Name = {}
        for i, j in stock_pair.items():
            Name[j] = i
        lists = []
        print('getting stock data...')
        for i in tqdm(codes):
            rs = bs.query_history_k_data_plus(i, info,
                                              start_date=self.start_date, end_date=self.end_date,
                                              frequency=self.frequency, adjustflag="3")
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            result = pd.DataFrame(data_list, columns=rs.fields)
            result['name'] = Name[i]
            lists.append(result)
        df = pd.concat(lists)
        return codes, stock_pair, df

    @property
    def combine(self):
        print('building a combinations...')
        results = []
        for j in range(1, len(self.names)+1):
            for i in combinations(self.names, j):
                result = []
                result.append(list(i))
                result.append(j)
                results.append(result)
        return pd.DataFrame(results, columns=['group', 'amount'])

    def quit(self):
        self.bs.logout()


class GetHolidayStock(object):
    def __init__(self, names=None,
                 start_date='20000101',
                 end_date='20210101',
                 frequency='d',
                 holiday='国庆节', before=-21, after=21):
        self.holiday = holiday
        self.before = before
        self.after = after
        self.names = names
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency

    @property
    def HolidayDateNearby(self):
        gd = GetDate(start=self.start_date, end=self.end_date)
        Date = gd.Date
        Date = Date[Date['holiday'] == self.holiday]
        start = []
        year = 0
        for i, j in Date.iterrows():
            if j[6] != year:
                start.append(str(j[0])[0:10])
            year = j[6]
        end = []
        year = list(Date['year'])[0]
        lastdate = None  # !!!!!!!!!!!!!!!!!!!!!!!!
        for i, j in Date.iterrows():
            if j[6] != year:
                end.append(str(lastdate)[0:10])
            year = j[6]
            lastdate = j[0]
        end.append(str(list(Date['date'])[-1])[0:10])

        def func(date, num):
            d = datetime.datetime.strptime(date, '%Y-%m-%d')
            delta = datetime.timedelta(days=num)
            d = d+delta
            return d.strftime('%Y-%m-%d')
        startbefore = []
        for i in start:
            startbefore.append(func(i, self.before))
        endafter = []
        for i in end:
            endafter.append(func(i, self.after))
        df = pd.DataFrame([startbefore, start, end, endafter], index=[
            'start before', 'start', 'end', 'end after'])
        df = df.T
        return df

    @property
    def HolidayNearbyData(self):
        date = self.HolidayDateNearby
        lens = date.index.stop
        result = []
        for i in range(0, lens):
            start_date = list(date['start before'])[i]
            end_date = list(date['end after'])[i]
            gs = GetStock(
                names=self.names, start_date=start_date, end_date=end_date, frequency=self.frequency)
            data = gs.stock_data
            result.append(data[2])
        df = pd.concat(result)

        return [data[0], data[1], df]

    @property
    def combine(self):
        print('building a combinations...')
        results = []
        for j in range(1, len(self.names)+1):
            for i in combinations(self.names, j):
                result = []
                result.append(list(i))
                result.append(j)
                results.append(result)
        return pd.DataFrame(results, columns=['group', 'amount'])


class StockAbility(object):
    def __init__(self, names=None,
                 start_year=2018, start_quater=1,
                 end_year=2019, end_quater=4):
        print('Please make sure that all the data has already existed!')
        self.names = names
        self.start_year = start_year
        self.end_year = end_year
        self.start_quater = start_quater
        self.end_quater = end_quater
        Range = []
        if end_year-start_year >= 2:
            for i in range(start_quater, 5):
                Range.append([start_year, i])
            for i in range(start_year+1, end_year):
                for j in range(1, 5):
                    Range.append([i, j])
            for i in range(1, end_quater+1):
                Range.append([end_year, i])
        elif end_year == start_year:
            for i in range(start_quater, end_quater+1):
                Range.append([end_year, i])
        else:
            for i in range(start_quater, 5):
                Range.append([start_year, i])
            for i in range(1, end_quater+1):
                Range.append([end_year, i])
        self.Range = Range
        self.gs = GetStock(names=self.names)
        self.stock_pair = self.gs.stock_pair

    # 盈利能力
    @property
    def profit(self):
        profit = []
        print('getting profit data')
        for i, j in self.stock_pair.items():
            print(i)
            for k in tqdm(self.Range):
                profit_list = []
                profit_list.append(i)
                profit_list.append(k[0])
                profit_list.append(k[1])
                rs_profit = bs.query_profit_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_profit.error_code == '0') & rs_profit.next():
                    profit_list = profit_list+rs_profit.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_profit.fields
                result_profit = pd.DataFrame([profit_list], columns=columns)
                profit.append(result_profit)
        df = pd.concat(profit)
        return df

    # 营运能力
    @property
    def operation(self):
        operation = []
        print('getting operation data')
        for i, j in self.stock_pair.items():
            print(i)
            for k in tqdm(self.Range):
                operation_list = []
                operation_list.append(i)
                operation_list.append(k[0])
                operation_list.append(k[1])
                rs_operation = bs.query_operation_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_operation.error_code == '0') & rs_operation.next():
                    operation_list = operation_list+rs_operation.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_operation.fields
                result_operation = pd.DataFrame(
                    [operation_list], columns=columns)
                operation.append(result_operation)
        df = pd.concat(operation)
        return df

    # 成长能力
    @property
    def growth(self):
        growth = []
        print('getting growth data')
        for i, j in self.stock_pair.items():
            print(i)
            for k in tqdm(self.Range):
                growth_list = []
                growth_list.append(i)
                growth_list.append(k[0])
                growth_list.append(k[1])
                rs_growth = bs.query_growth_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_growth.error_code == '0') & rs_growth.next():
                    growth_list = growth_list+rs_growth.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_growth.fields
                result_growth = pd.DataFrame([growth_list], columns=columns)
                growth.append(result_growth)
        df = pd.concat(growth)
        return df

    # 偿债能力
    @property
    def balance(self):
        balance = []
        print('getting balance data')
        for i, j in self.stock_pair.items():
            print(i)
            for k in tqdm(self.Range):
                balance_list = []
                balance_list.append(i)
                balance_list.append(k[0])
                balance_list.append(k[1])
                rs_balance = bs.query_balance_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_balance.error_code == '0') & rs_balance.next():
                    balance_list = balance_list+rs_balance.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_balance.fields
                result_balance = pd.DataFrame([balance_list], columns=columns)
                balance.append(result_balance)
        df = pd.concat(balance)
        return df

    # 现金流量

    @property
    def cash_flow(self):
        cash_flow = []
        print('getting cash flow data')
        for i, j in self.stock_pair.items():
            print(i)
            for k in tqdm(self.Range):
                cash_flow_list = []
                cash_flow_list.append(i)
                cash_flow_list.append(k[0])
                cash_flow_list.append(k[1])
                rs_cash_flow = bs.query_cash_flow_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
                    cash_flow_list = cash_flow_list+rs_cash_flow.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_cash_flow.fields
                result_cash_flow = pd.DataFrame(
                    [cash_flow_list], columns=columns)
                cash_flow.append(result_cash_flow)
        df = pd.concat(cash_flow)
        return df

    # dupont_data
    # 杜邦指数
    @property
    def dupont_data(self):
        dupont_data = []
        print('getting dupont data')
        for i, j in self.stock_pair.items():
            print(i)
            for k in tqdm(self.Range):
                dupont_data_list = []
                dupont_data_list.append(i)
                dupont_data_list.append(k[0])
                dupont_data_list.append(k[1])
                rs_dupont_data = bs.query_dupont_data(
                    code=j, year=k[0], quarter=k[1])
                while (rs_dupont_data.error_code == '0') & rs_dupont_data.next():
                    dupont_data_list = dupont_data_list+rs_dupont_data.get_row_data()
                columns = ['name', 'year', 'quater']
                columns = columns+rs_dupont_data.fields
                result_dupont_data = pd.DataFrame(
                    [dupont_data_list], columns=columns)
                dupont_data.append(result_dupont_data)
        df = pd.concat(dupont_data)
        return df

    @property
    def AllAbility(self):
        profit = self.profit
        operation = self.operation
        growth = self.growth
        balance = self.balance
        cash_flow = self.cash_flow
        dupont_data = self.dupont_data
        lists = [growth, balance, cash_flow, dupont_data]
        df = pd.merge(profit, operation, how='outer', on=[
                      'code', 'name', 'year', 'quater', 'pubDate', 'statDate'])
        for i in lists:
            df = pd.merge(df, i, how='outer', on=[
                          'code', 'name', 'year', 'quater', 'pubDate', 'statDate'])
        return df

    def save_ability(self):
        self.AllAbility.to_excel('ability.xlsx', encoding='utf8', index=False)

    def quit(self):
        self.gs.quit()


class ConstituentStock(object):
    def __init__(self):
        self.bs = bs
        self.bs.login()

    def StockIndustry(self, names=None):
        if names == None:
            rs = bs.query_stock_industry()
            industry_list = []
            while (rs.error_code == '0') & rs.next():
                industry_list.append(rs.get_row_data())
            result = pd.DataFrame(industry_list, columns=rs.fields)
            return result
        else:
            if type(names) == str:
                names = [names]
            lists = []
            for i in names:
                rs = bs.query_stock_basic(code_name=i)
                industry_list = []
                while (rs.error_code == '0') & rs.next():
                    industry_list.append(rs.get_row_data())
                result = pd.DataFrame(industry_list, columns=rs.fields)
                lists.append(result)
            return pd.concat(lists)
    # 上证50成分股

    @property
    def sz50(self):
        rs = bs.query_sz50_stocks()
        sz50_stocks = []
        while (rs.error_code == '0') & rs.next():
            sz50_stocks.append(rs.get_row_data())
        result = pd.DataFrame(sz50_stocks, columns=rs.fields)
        return result

    # 沪深300成分股
    @property
    def hs300(self):
        rs = bs.query_hs300_stocks()
        hs300_stocks = []
        while (rs.error_code == '0') & rs.next():
            hs300_stocks.append(rs.get_row_data())
        result = pd.DataFrame(hs300_stocks, columns=rs.fields)
        return result

    # 中证500成分股
    @property
    def zz500(self):
        rs = bs.query_zz500_stocks()
        zz500_stocks = []
        while (rs.error_code == '0') & rs.next():
            zz500_stocks.append(rs.get_row_data())
        result = pd.DataFrame(zz500_stocks, columns=rs.fields)
        return result

    def quit(self):
        self.bs.logout()
