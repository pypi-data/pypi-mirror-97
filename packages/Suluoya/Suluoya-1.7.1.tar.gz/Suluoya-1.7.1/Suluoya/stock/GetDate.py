from lunar_python.util import HolidayUtil
import pandas as pd
import time


class GetDate(object):
    def __init__(self, start='20000101',end=None):
        if end == None:
            end = time.strftime("%Y%m%d", time.localtime())
        self.end = end
        self.start= start
        date = pd.Series(pd.date_range(start=start, end=end, freq='D'))
        self.date = date

    @property
    def holiday(self):
        series = pd.Series(
            [HolidayUtil.getHoliday(str(i)[0:10]) for i in self.date])

        def func1(x):
            if x != None:
                name=str(x)[11:-11]
                if '调休' in name:
                    return None
                if name == '国庆中秋':
                    name='国庆节'
                if str(x)[-10:]=='2009-10-03':
                    name='国庆节'
                return name
        holiday = series.map(func1)
        def func2(x):
            if x != None:
                return str(x)[-11:]
        holidaystart = series.map(func2) 
        return (holiday,holidaystart)

    
    @property
    def day(self):
        return pd.Series([i.day for i in self.date])

    @property
    def week(self):
        return pd.Series([i.week for i in self.date])

    @property
    def month(self):
        return pd.Series([i.month for i in self.date])

    @property
    def year(self):
        return pd.Series([i.year for i in self.date])

    @property
    def weekofyear(self):
        return pd.Series([i.weekofyear for i in self.date])

    @property
    def dayofyear(self):
        return pd.Series([i.dayofyear for i in self.date])

    @property
    def Date(self):
        Date = pd.DataFrame()
        Date['date'] = self.date
        Date['holiday'] = self.holiday[0]
        Date['holidaystart'] = self.holiday[1]
        Date['day'] = self.day
        Date['week'] = self.week
        Date['month'] = self.month
        Date['year'] = self.year
        Date['dayofyear'] = self.dayofyear
        Date['weekofyear'] = self.weekofyear
        return Date

