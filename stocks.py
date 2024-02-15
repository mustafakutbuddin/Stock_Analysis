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

        self.symbol = symbol

        # Get the data for the stock
        self.hist_data = yf.download(
            tickers=symbol, interval='1d', period='1y', rounding=True)  # YYYY-MM-DD

        # print('-'*50)
        # print(self.hist_data.head())
        # print(self.symbol)
        # print(len(self.hist_data))
        # print('-'*50)

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
    # def __init__(self, class_instance):
    #     self.class_instance = class_instance
    #     self.hist_data = class_instance.hist_data
    #     self.todays_date = class_instance.todays_date

    # def ActiveStockSelectionStrategy(self, stock_list):
    #     selected_stocks = []
    #     for stock in stocks:
    #         monthly_return = stock.MonthlyRet(curDate)
    #         if monthly_return > 0:
    #             selected_stocks.append(stock.symbol)
    #     return selected_stocks

    def __init__(self, symbols):
        self.symbols = symbols
        self.stocks = [Stocks(symbol) for symbol in symbols]

    def ActiveStockSelectionStrategy(self):
        active_stocks = {}

        for stock in self.stocks:
            monthly_return = stock.MonthlyRet()

            if monthly_return is not None and monthly_return > 0:
                active_stocks[stock.symbol] = monthly_return

        active_stocks = dict(sorted(active_stocks.items(),
                             key=lambda item: item[1], reverse=True))

        print(str(len(active_stocks)) +
              " Are selected for the active stock strategy")
        top_10_active_stocks = dict(list(active_stocks.items())[:10])

        return active_stocks, top_10_active_stocks


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

# SUMMARY CLASSS
# s1_summary = Summarization(s1)

# print(s1_summary.CAGR(2, '2024-02-14'))
# print(s1_summary.Volatility('2024-02-14', '2024-01-14'))
# print(s1_summary.Volatility())
# print(s1_summary.SharpeRatio('2024-02-14', '2024-01-14'))
# print(s1_summary.SharpeRatio())

# NIFTY50 LIST
nifty50_ticker_list = ['ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'CIPLA.NS',
                       'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GAIL.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS',
                       'ITC.NS', 'ICICIBANK.NS', 'IBULHSGFIN.NS', 'IOC.NS', 'INDUSINDBK.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS',
                       'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TATAMOTORS.NS',
                       'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'VEDL.NS', 'WIPRO.NS', 'YESBANK.NS', 'ZEEL.NS']
failed = ['INFRATEL.NS', 'INF.NS', 'HDFC.NS']

# PORFOLIO CLASS
p1 = Portfolio(nifty50_ticker_list)
AS_list, AST10_list = p1.ActiveStockSelectionStrategy()
print(AS_list)
print('TOP 10 LIST')
print(AST10_list)
