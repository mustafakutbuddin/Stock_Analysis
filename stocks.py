# Import the yfinance. If you get module not found error the run !pip install yfinance from your Jupyter notebook
import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta


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


# MAIN
s1 = Stocks('ADANIPORTS.NS')

print(s1.CurPrice('2024-02-14'))
print(s1.MonthlyRet())  # from to[will be 30 days before the start date]
print(s1.DailyReturn())  # can take any date upto an year
print(s1.Last30Dayprice())  # can take any date of the year


nifty50_ticker_list = ['ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'INFRATEL.NS', 'CIPLA.NS',
                       'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GAIL.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS',
                       'HDFC.NS', 'ITC.NS', 'ICICIBANK.NS', 'IBULHSGFIN.NS', 'IOC.NS', 'INDUSINDBK.NS', 'INF.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS',
                       'M&M', 'MARUTI', 'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TATAMOTORS',
                       'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'VEDL.NS', 'WIPRO.NS', 'YESBANK.NS', 'ZEEL.NS']
