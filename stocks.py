# Import the yfinance. If you get module not found error the run !pip install yfinance from your Jupyter notebook
import yfinance as yf

import pandas as pd
import numpy as np

import streamlit as st

from datetime import datetime, timedelta

import math
import statistics


class Stocks:

    def __init__(self, symbol):

        # Get the data for the stock
        self.hist_data = yf.download(
            tickers=symbol, interval='1d', period='1y', rounding=True)  # YYYY-MM-DD

        print('-'*50)
        print(self.hist_data.head())
        print('-'*50)

        # Get the current date
        self.todays_date = datetime.now().date()

    def CurPrice(self, date):
        return (self.hist_data.loc[str(date)]['Adj Close'])

    # @staticmethod
    # def CurPriceE(date):
    #     return (Stocks.hist_data.loc[str(date)]['Adj Close'])

    def DailyReturn(self, date=None):
        if date is None:
            # print('in if statement of daily ret')

            prevDate = self.todays_date - timedelta(days=1)
            dailyret = (self.CurPrice(self.todays_date) /
                        self.CurPrice(prevDate))-1

            return (round(dailyret, 4))

        else:
            # print('in else statement of daily ret')

            date = datetime.strptime(date, "%Y-%m-%d")
            prevDate = date - timedelta(days=1)
            dailyret = (self.CurPrice(date)/self.CurPrice(prevDate))-1

            return (round(dailyret, 4))

    def MonthlyRet(self, start_date=None):
        if start_date is None:
            # print('in if statement of monthly ret')

            start_date = self.todays_date
            prevMonthDate = self.todays_date - timedelta(days=30)
            prices = self.hist_data.loc[prevMonthDate:start_date]['Adj Close']
            monthlyret = (
                (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100

            return (round(monthlyret, 2))

        else:
            # print('in else statement of monthly ret')

            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            prevMonthDate = start_date - timedelta(days=30)
            prices = self.hist_data.loc[prevMonthDate:start_date]['Adj Close']
            monthlyret = (
                (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100

            return (round(monthlyret, 2))

    # @staticmethod
    # def DailyReturnS(date=None):
    #     if date is None:
    #         print('in if statement of daily ret')
    #         date = date = datetime.now().date()
    #         prevDate = date - timedelta(days=1)
    #         dailyret = (Stocks.CurPriceE(date) /
    #                     Stocks.CurPriceE(prevDate))-1

    #         return (round(dailyret, 4))

    #     else:
    #         print('in else statement of daily ret')

    #         date = datetime.strptime(date, "%Y-%m-%d")
    #         prevDate = date - timedelta(days=1)
    #         dailyret = (Stocks.CurPriceE(date)/Stocks.CurPriceE(prevDate))-1

    #         return (round(dailyret, 4))

    def Last30Dayprice(self, date=None):
        if date is None:
            # print('in if statement of last 30 days')

            prevMonthDate = self.todays_date - timedelta(days=30)
            return (self.hist_data.loc[prevMonthDate:self.todays_date]['Adj Close']).to_numpy()

        else:
            # print('in else statement of las 30 days')

            date = datetime.strptime(date, "%Y-%m-%d")
            prevMonthDate = date - timedelta(days=30)
            return (self.hist_data.loc[prevMonthDate:date]['Adj Close']).to_numpy()


class Benchmarking:
    pass


class Portfolio:
    def __init__(self):
        # TWO OPTIONS FOR HAVING HIST_DATA INTHIS CLASS
        # 1. EITHER USE @CLASSMETHOD DECORATOR AND CLASS THE STOCK METHOD IN THIS WAY
        # OR
        # 2. CREATE A NEW STOCK CLASS INSTANCE WITH THE INIT OF THIS CLASS
        pass

    def ActiveStockSelectionStrategy(self, stock_list):
        pass


class Summarization:

    def __init__(self, class_instance):
        self.class_instance = class_instance
        self.hist_data = class_instance.hist_data
        self.todays_date = class_instance.todays_date

    def CAGR(self, numYears, date=None):

        if date is None:
            # print('in if statement of CAGR')

            value_cagr = (((self.hist_data.loc[str(
                self.todays_date)]['Close']/self.hist_data.loc[str(self.todays_date)]['Open'])**(1/numYears))-1)*100

            return (round(value_cagr, 2))

        else:
            # print('in else statement of CAGR')

            date = datetime.strptime(date, "%Y-%m-%d")
            value_cagr = (((self.hist_data.loc[str(
                date)]['Close']/self.hist_data.loc[str(date)]['Open'])**(1/numYears))-1)*100

            return (round(value_cagr, 2))

    def Volatility(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
            # print('in if statement of Volatility')

            DRet = []
            holidays = []
            prevMonthDate = self.todays_date - timedelta(days=30)

            date_range = pd.date_range(
                start=prevMonthDate, end=self.todays_date)

            # Format dates as "%Y-%m-%d"
            date_range = date_range.strftime('%Y-%m-%d')

            for date in date_range:
                try:
                    DRet.append(self.class_instance.DailyReturn(date))
                except KeyError:
                    holidays.append(str(date))
                    # pass

            # print(DRet)
            return (round((math.sqrt(252)*(statistics.stdev(DRet)))*100, 2))

        else:
            # print('in else statement of Volatility')

            DRet = []
            holidays = []
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = date = datetime.strptime(end_date, "%Y-%m-%d")

            date_range = pd.date_range(
                start=end_date, end=start_date)
            # Format dates as "%Y-%m-%d"
            date_range = date_range.strftime('%Y-%m-%d')

            for date in date_range:
                try:
                    DRet.append(self.class_instance.DailyReturn(str(date)))
                except KeyError:
                    holidays.append(str(date))
                    # pass
            return (round((math.sqrt(252)*(statistics.stdev(DRet)))*100, 2))

    def SharpeRatio(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
            # print('in if statement of Volatility')

            DRet = []
            holidays = []
            prevMonthDate = self.todays_date - timedelta(days=30)

            date_range = pd.date_range(
                start=prevMonthDate, end=self.todays_date)

            # Format dates as "%Y-%m-%d"
            date_range = date_range.strftime('%Y-%m-%d')

            for date in date_range:
                try:
                    DRet.append(self.class_instance.DailyReturn(date))
                except KeyError:
                    holidays.append(str(date))
                    # pass

            # print(DRet)
            return (round(math.sqrt(252)*(np.mean(DRet)/statistics.stdev(DRet)), 2))

        else:
            # print('in else statement of Volatility')

            DRet = []
            holidays = []
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = date = datetime.strptime(end_date, "%Y-%m-%d")

            date_range = pd.date_range(
                start=end_date, end=start_date)

            # Format dates as "%Y-%m-%d"
            date_range = date_range.strftime('%Y-%m-%d')

            for date in date_range:
                try:
                    DRet.append(self.class_instance.DailyReturn(str(date)))
                except KeyError:
                    holidays.append(str(date))
                    # pass

            return (round(math.sqrt(252)*(np.mean(DRet)/statistics.stdev(DRet)), 2))


# MAIN
s1 = Stocks('ADANIPORTS.NS')

# print(s1.CurPrice('2024-02-14'))
# print(s1.MonthlyRet())  # from to[will be 30 days before the start date]
# print(s1.DailyReturn())  # can take any date upto an year
# print(s1.Last30Dayprice())  # can take any date of the year

# other_object.access_method(my_object)
s1_summary = Summarization(s1)

# print(s1_summary.CAGR(2, '2024-02-14'))
# print(s1_summary.Volatility('2024-02-14', '2024-01-14'))
# print(s1_summary.Volatility())
# print(s1_summary.SharpeRatio('2024-02-14', '2024-01-14'))
# print(s1_summary.SharpeRatio())


nifty50_ticker_list = ['ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'INFRATEL.NS', 'CIPLA.NS',
                       'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GAIL.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS',
                       'HDFC.NS', 'ITC.NS', 'ICICIBANK.NS', 'IBULHSGFIN.NS', 'IOC.NS', 'INDUSINDBK.NS', 'INF.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS',
                       'M&M', 'MARUTI', 'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TATAMOTORS',
                       'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'VEDL.NS', 'WIPRO.NS', 'YESBANK.NS', 'ZEEL.NS']
