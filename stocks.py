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

        self.open_month = self.hist_data.loc[:, 'Open']
        self.close_month = self.hist_data.loc[:, 'Adj Close']

        # Get the current date
        self.todays_date = datetime.now().date()

        print('-'*50)
        print(self.hist_data.head())
        print('-'*50)

    def CurPrice(self, date):
        # self.cur_close = self.close_month[-1:]
        return self.hist_data.loc[str(date)]['Adj Close']

    def MonthlyRet(self, start_date=None):
        if start_date is None:
            start_date = self.todays_date
            prevMonthDate = self.todays_date - timedelta(days=30)
            prices = self.hist_data.loc[prevMonthDate:start_date]['Adj Close']

            return (((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100)

        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            prevMonthDate = start_date - timedelta(days=30)
            prices = self.hist_data.loc[prevMonthDate:start_date]['Adj Close']

            return (((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100)

    def DailyReturn(self):
        # self.d_return = ((self.close_month.iloc[-1]/self.close_month.iloc[-2])-1)
        # return (self.curPrice(self.todays_date) - self.curPrice(prevDate)) / self.curPrice(prevDate)
        prevDate = self.todays_date - timedelta(days=1)
        return ((self.CurPrice(self.todays_date)/self.CurPrice(prevDate))-1)

    def Last30Dayprice(self):
        # self.last30dayprice = self.close_full[-30:]
        prevMonthDate = self.todays_date - timedelta(days=30)
        return (self.hist_data.loc[prevMonthDate:self.todays_date]['Adj Close']).to_numpy()


s1 = Stocks('ADANIPORTS.NS')

s1.CurPrice('2024-02-14')
s1.MonthlyRet()  # from to[will be 30 days before the start date]
s1.DailyReturn()  # from to
s1.Last30Dayprice()  # from to


nifty50_ticker_list = ['ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'INFRATEL.NS', 'CIPLA.NS',
                       'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GAIL.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS',
                       'HDFC.NS', 'ITC.NS', 'ICICIBANK.NS', 'IBULHSGFIN.NS', 'IOC.NS', 'INDUSINDBK.NS', 'INF.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS',
                       'M&M', 'MARUTI', 'NTPC', 'ONGC', 'POWERGRID', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TCS', 'TATAMOTORS',
                       'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 'UPL.NS', 'ULTRACEMCO.NS', 'VEDL.NS', 'WIPRO.NS', 'YESBANK.NS', 'ZEEL.NS']
