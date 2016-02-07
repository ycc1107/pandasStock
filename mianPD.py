import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

BEFORE_MARKET = 'BTO'
AFTER_MARKET = 'AMC'

class PreProcess():
    def __init__(self,epsPath,pricePath,daysNeed = 3):
        self.raw_eps = pd.read_csv(epsPath)
        self.price = pd.read_csv(pricePath)
        self.daysNeed = daysNeed
        self.__getEps()
        minDate = str(min(self.epsBefore['DATE'],self.epsAfter['DATE']))
        maxDate = str(max(self.epsBefore['DATE'],self.epsAfter['DATE']))
        cal = USFederalHolidayCalendar()
        self.holidays = cal.holidays(start=minDate, end=maxDate).to_pydatetime()

    def __getEps(self):
        self.epsBefore = self.raw_eps.loc[ self.raw_eps.loc[:,'ACT_RPT_CODE'] == BEFORE_MARKET, ('Ticker','DATE') ]
        self.epsAfter = self.raw_eps.loc[ self.raw_eps.loc[:,'ACT_RPT_CODE'] == AFTER_MARKET, ('Ticker','DATE') ]
        self.epsBefore['DATE'] = pd.to_datetime(self.epsBefore['DATE'])
        self.epsAfter['DATE'] = pd.to_datetime(self.epsAfter['DATE'])

    def __avoidHoliday(self,date):
        res, dayIndex = date , 0
        while res in self.holidays:
                dayIndex += 1
                addingDate = pd.DatetimeIndex(res) + pd.DateOffset(dayIndex)
        return res

    def __popDateWithDate(self):
        self.epsBefore[ 'DATE' ]  = pd.DatetimeIndex(self.epsAfter['DATE']) + pd.DateOffset(1)
        for i in range(self.daysNeed):
            dayIndex = i + 1
            addingDateBeforeMarket = pd.DatetimeIndex(self.epsBefore['DATE']) + pd.DateOffset(dayIndex)
            addingDateAfterMarket = pd.DatetimeIndex(self.epsBefore['DATE']) + pd.DateOffset(dayIndex)
            addingDateBeforeMarket = self.__avoidHoliday(addingDateBeforeMarket)
            addingDateAfterMarket = self.__avoidHoliday(addingDateAfterMarket)
            self.epsBefore[ 'DATE' + str(i + 1) ] = addingDateBeforeMarket
            self.epsAfter[ 'DATE' + str(i + 1) ] = addingDateAfterMarket

    def __restructPrice(self):
        self.price = self.price.set_index('Date')
        self.price = self.price.stack().reset_index()
        self.price.columns = ['DATE','Ticker','Price']

    def getPreProcessData(self):
        self.__popDateWithDate()
        self.__restructPrice()
        return self.epsBefore, self.epsAfter,self.price


def run():
    epsPath,pricePath = 'eps.csv', 'price.csv'
    generator = PreProcess(epsPath,pricePath)
    epsBefore,epsAfter,price = generator.getPreProcessData()
    priceOnERDay = pd.merge(epsBefore,price,on=['DATE','Ticker'])
    print priceOnERDay



'''
popularedEpsBefore = epsBefore.add()


indexedPrice = price.set_index('Date')
indexedPrice = indexedPrice.stack().reset_index()
indexedPrice.columns = ['DATE','Ticker','Price']


priceOnERDay = pd.merge(indexedPrice,epsBefore,on=['DATE','Ticker'])
'''

