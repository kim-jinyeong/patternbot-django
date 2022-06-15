from context.domains import File, Reader
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import platform
from matplotlib import font_manager, rc
from fbprophet import Prophet
from datetime import datetime
from icecream import ic
from pandas_datareader import data
import yfinance as yf


class Solution(Reader):
    def __init__(self):
        self.file = File(context='./data/')
        self.pinkwink_web = pd.DataFrame()
    def hook(self):
        path = "c:/Windows/Fonts/malgun.ttf"

        if platform.system() == 'Darwin':
            rc('font', family='AppleGothic')
        elif platform.system() == 'Windows':
            font_name = font_manager.FontProperties(fname=path).get_name()
            rc('font', family=font_name)
        else:
            print('Unknown system... sorry~~~~')
        plt.rcParams['axes.unicode_minus'] = False
        def print_menu():
            print('0. Exit\n'
                  '1. Numpy의 polyfit으로 회귀(regression) 분석하기\n'
                  '2. Prophet 모듈을 이용한 forecast\n'
                  '3. Seasonal\n'
                  '4. grow_model\n'
                  '5. holiday')
            return input('메뉴 선택 \n')

        while 1:
            menu = print_menu()
            if menu == '0':
                break
            elif menu == '1':
                self.analysis()
            elif menu == '2':
                self.forecast()
            elif menu == '3':
                self.Seasonal()
            elif menu == '4':
                self.grow_model()
            elif menu == '5':
                self.holiday()

    def analysis(self):
        file = self.file
        file.fname = '08. PinkWink Web Traffic'
        pinkwink_web = self.re_csv(file, ['date', 'hit'], 0)
        pinkwink_web = pinkwink_web[pinkwink_web['hit'].notnull()]
        pinkwink_web.head()
        pinkwink_web['hit'].plot(figsize=(12, 4), grid=True)
        time = np.arange(0, len(pinkwink_web))
        traffic = pinkwink_web['hit'].values

        fx = np.linspace(0, time[-1], 1000)
        fp1 = np.polyfit(time, traffic, 1)
        f1 = np.poly1d(fp1)

        f2p = np.polyfit(time, traffic, 2)
        f2 = np.poly1d(f2p)

        f3p = np.polyfit(time, traffic, 3)
        f3 = np.poly1d(f3p)

        f15p = np.polyfit(time, traffic, 15)
        f15 = np.poly1d(f15p)

        print(self.error(f1, time, traffic))
        print(self.error(f2, time, traffic))
        print(self.error(f3, time, traffic))
        print(self.error(f15, time, traffic))

        plt.figure(figsize=(10, 6))
        plt.scatter(time, traffic, s=10)

        plt.plot(fx, f1(fx), lw=4, label='f1')
        plt.plot(fx, f2(fx), lw=4, label='f2')
        plt.plot(fx, f3(fx), lw=4, label='f3')
        plt.plot(fx, f15(fx), lw=4, label='f15')

        plt.grid(True, linestyle='-', color='0.75')

        plt.legend(loc=2)
        #plt.show()
        return pinkwink_web
    def forecast(self):
        pinkwink_web = self.analysis()
        df = pd.DataFrame({'ds': pinkwink_web.index, 'y': pinkwink_web['hit']})
        df.reset_index(inplace=True)
        df['ds'] = pd.to_datetime(df['ds'], format="%y. %m. %d.")
        del df['date']

        m = Prophet(yearly_seasonality=True, daily_seasonality=True)
        m.fit(df)

        future = m.make_future_dataframe(periods=60)
        #ic(future.tail())

        forecast = m.predict(future)
        #ic(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        #m.plot(forecast).show()
        #m.plot_components(forecast).show()
        return forecast
    def Seasonal(self):
        yf.pdr_override()

        start_date = '1990-1-1'
        end_date = '2017-6-30'
        KIA = data.get_data_yahoo('000270.KS', start_date, end_date)

        # KIA = web.DataReader('KRX:000270','google',start,end) # 구글용... 동작이 안됨
        # KIA = web.DataReader('000270.KS','yahoo',start,end) # 구글용... 동작이 안됨
        #ic(KIA.head())


        KIA_trunc = KIA[:'2016-12-31']
        #ic(KIA_trunc)

        df = pd.DataFrame({'ds': KIA_trunc.index, 'y': KIA_trunc['Close']})
        df.reset_index(inplace=True)
        del df['Date']
        ic(df.head())

        m = Prophet(daily_seasonality=True)
        m.fit(df)

        future = m.make_future_dataframe(periods=365)
        future.tail()

        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

        m.plot(forecast)
        m.plot_components(forecast)


        start_date = '2014-1-1'
        end_date = '2017-7-31'
        KIA = data.get_data_yahoo('000270.KS', start_date, end_date)
        KIA['Close'].plot(figsize=(12, 6), grid=True)

        KIA_trunc = KIA[:'2017-05-31']
        KIA_trunc['Close'].plot(figsize=(12, 6), grid=True);

        df = pd.DataFrame({'ds': KIA_trunc.index, 'y': KIA_trunc['Close']})
        df.reset_index(inplace=True)
        del df['Date']

        m = Prophet(daily_seasonality=True)
        m.fit(df)

        future = m.make_future_dataframe(periods=61)
        #ic(future.tail())

        forecast = m.predict(future)
        m.plot(forecast)

        plt.figure(figsize=(12, 6))
        plt.plot(KIA.index, KIA['Close'], label='real')
        plt.plot(forecast['ds'], forecast['yhat'], label='forecast')
        plt.grid()
        plt.legend()

        plt.show()

    def grow_model(self):
        file = self.file
        file.fname = '08. example_wp_R'
        df = self.csv(file)
        df['y'] = np.log(df['y'])

        df['cap'] = 8.5

        m = Prophet(growth='logistic', daily_seasonality=True)
        m.fit(df)

        future = m.make_future_dataframe(periods=1826)
        future['cap'] = 8.5
        fcst = m.predict(future)
        m.plot(fcst)

        forecast = m.predict(future)
        m.plot_components(forecast)

        plt.show()

    def error(self, f, x, y):
        return np.sqrt(np.mean((f(x) - y) ** 2))

    def holiday(self):
        file = self.file
        file.fname = '08. example_wp_peyton_manning'
        df = self.csv(file)
        df['y'] = np.log(df['y'])
        m = Prophet(daily_seasonality=True)
        m.fit(df)
        future = m.make_future_dataframe(periods=366)
        df.y.plot(figsize=(12, 6), grid=True);
        playoffs = pd.DataFrame({
            'holiday': 'playoff',
            'ds': pd.to_datetime(['2008-01-13', '2009-01-03', '2010-01-16',
                                  '2010-01-24', '2010-02-07', '2011-01-08',
                                  '2013-01-12', '2014-01-12', '2014-01-19',
                                  '2014-02-02', '2015-01-11', '2016-01-17',
                                  '2016-01-24', '2016-02-07']),
            'lower_window': 0,
            'upper_window': 1,
        })
        superbowls = pd.DataFrame({
            'holiday': 'superbowl',
            'ds': pd.to_datetime(['2010-02-07', '2014-02-02', '2016-02-07']),
            'lower_window': 0,
            'upper_window': 1,
        })
        holidays = pd.concat((playoffs, superbowls))
        m = Prophet(holidays=holidays, daily_seasonality=True)
        forecast = m.fit(df).predict(future)
        id(forecast[(forecast['playoff'] + forecast['superbowl']).abs() > 0][
            ['ds', 'playoff', 'superbowl']][-10:])
        m.plot(forecast)
        m.plot_components(forecast)
        plt.show()

if __name__ == '__main__':
    Solution().hook()