# Import the yfinance.
import yfinance as yf

import pandas as pd
import numpy as np

import streamlit as st

from datetime import datetime, timedelta

import math
import statistics


class Stocks:
    """
    A class representing stock data and providing methods for initilizing stocks historical data.

    Attributes:
        symbol (str): The symbol representing the stock.
        hist_data (pandas.DataFrame): Historical data for the stock.
        todays_date (datetime.date): The current date.

    Methods:
        __init__(self, symbol):
        CurPrice(self, date):
        DailyReturn(self, date=None):
        MonthlyRet(self, start_date=None):
        Last30Dayprice(self, date=None):
    """

    def __init__(self, symbol):
        """
        Initializes a Stocks object with the provided symbol, downloads historical data,
        and sets the current date.

        Parameters:
            symbol (str): The symbol representing the stock.
        """
        self.symbol = symbol

        # Get the data for the stock
        self.hist_data = yf.download(
            tickers=symbol, interval='1d', period='1y', rounding=True)  # YYYY-MM-DD

        # Get the current date
        self.todays_date = datetime.now().date()

    def CurPrice(self, date):
        """
        Returns the adjusted closing price of the stock on the specified date.

        Parameters:
            date (str or datetime.date): The date for which the adjusted closing price is requested.

        Returns:
            float: The adjusted closing price of the stock on the specified date.
        """
        return (self.hist_data.loc[str(date)]['Adj Close'])

    def DailyReturn(self, date=None):
        """
        Calculates the daily return of the stock. If no date is provided, it calculates the daily return
        from the previous day to the current day. If a date is provided, it calculates the daily return
        from the day before the specified date to the specified date.

        Parameters:
            date (str or datetime.date, optional): The end date for calculating the daily return.
                Defaults to None.

        Returns:
            float: The daily return of the stock.
        """

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
        """
        Calculates the monthly return of the stock. If no start date is provided, it calculates the monthly
        return for the last 30 days from the current date. If a start date is provided, it calculates the
        monthly return for the 30 days leading up to the specified start date.

        Parameters:
            start_date (str or datetime.date, optional): The start date for calculating the monthly return.
                Defaults to None.

        Returns:
            float: The monthly return of the stock.
        """

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

    def Last30Dayprice(self, date=None):
        """
        Retrieves the adjusted closing prices of the stock for the last 30 days. If no date is provided,
        it retrieves the prices for the last 30 days from the current date. If a date is provided, it
        retrieves the prices for the 30 days leading up to the specified date.

        Parameters:
            date (str or datetime.date, optional): The end date for retrieving the prices.
                Defaults to None.

        Returns:
            numpy.ndarray: An array containing the adjusted closing prices for the last 30 days.
        """
        if date is None:
            # print('in if statement of last 30 days')

            prevMonthDate = self.todays_date - timedelta(days=30)
            return (self.hist_data.loc[prevMonthDate:self.todays_date]['Adj Close']).to_numpy()

        else:
            # print('in else statement of las 30 days')

            date = datetime.strptime(date, "%Y-%m-%d")
            prevMonthDate = date - timedelta(days=30)
            return (self.hist_data.loc[prevMonthDate:date]['Adj Close']).to_numpy()

    def DisplayDataframe(self):
        # st.dataframe(self.hist_data.head(10), width=800)
        with st.expander("Stock data"):
            # Display in an expandable section
            st.dataframe(self.hist_data.head(10), width=800)


class Benchmarking:
    def __init__(self, class_instance, symbols):
        self.nifty50_price = yf.download(
            tickers='^NSEI', interval='1d', period='1y', rounding=True)
        self.class_instance = class_instance

        self.symbols = symbols
        self.stocks = [Stocks(symbol) for symbol in symbols]

    def CompairWithBenchmark(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:

            todays_date = datetime.now().date()
            prevMonthDate = todays_date - timedelta(days=30)

            date_range = pd.date_range(
                start=prevMonthDate, end=todays_date)
            # Format dates as "%Y-%m-%d"
            date_range = date_range.strftime('%Y-%m-%d')

            for stock in self.stocks:
                for date in date_range:

                    daily_return_per_stock = stock.DailyReturn()
                    self.nifty50_stocks[stock.symbol] = daily_return_per_stock

                nifty50_stocks = dict(sorted(self.nifty50_stocks.items(),
                                             key=lambda item: item[1], reverse=True))

                return (nifty50_stocks)


class Portfolio:
    """
    A class representing a portfolio of stocks and providing methods for creating a portfolio and analysing it.

    Attributes:
        symbols (list of str): List of symbols representing the stocks in the portfolio.
        stocks (list of Stocks): List of Stocks objects representing the individual stocks in the portfolio.
        nifty50_stocks (dict): Dictionary containing monthly returns of Nifty 50 stocks.
        active_stocks (dict): Dictionary containing monthly returns of actively selected stocks.

    Methods:
        __init__(self, symbols):
        Nifty50_monthlyRet(self):
        ActiveStockSelectionStrategy(self):
        display_stock_selection(self):
    """

    def __init__(self, symbols):
        """
        Initializes a Portfolio object with the provided list of symbols, creates Stocks objects for each symbol,
        and initializes empty dictionaries for Nifty 50 stocks and active stocks.

        Parameters:
            symbols (list of str): List of symbols representing the stocks in the portfolio.
        """

        self.symbols = symbols
        self.stocks = [Stocks(symbol) for symbol in symbols]
        self.nifty50_stocks = {}
        self.active_stocks = {}

    def Nifty50_monthlyRet(self):
        """
        Calculates the monthly returns of Nifty 50 stocks and sorts them in descending order.

        Returns:
            dict: Dictionary containing monthly returns of Nifty 50 stocks sorted in descending order.
        """

        for stock in self.stocks:
            monthly_return = stock.MonthlyRet()
            self.nifty50_stocks[stock.symbol] = monthly_return

        nifty50_stocks = dict(sorted(self.nifty50_stocks.items(),
                                     key=lambda item: item[1], reverse=True))

        return (nifty50_stocks)

    def ActiveStockSelectionStrategy(self):
        """
        Implements an active stock selection strategy based on positive monthly returns of Nifty 50 stocks.
        Selects the top 10 active stocks based on monthly returns.

        Returns:
            tuple: A tuple containing two dictionaries:
                   - Dictionary containing monthly returns of actively selected stocks.
                   - Dictionary containing top 10 actively selected stocks.
        """

        for symbol, value in self.Nifty50_monthlyRet().items():
            if value > 0:
                self.active_stocks[symbol] = value

        active_stocks = dict(sorted(self.active_stocks.items(),
                             key=lambda item: item[1], reverse=True))

        top_10_active_stocks = dict(list(active_stocks.items())[:10])

        return active_stocks, top_10_active_stocks

    def display_stock_selection(self):
        """
        Displays information about the stock selection process including the total number of stocks, the number
        of stocks selected for the active strategy, the number of stocks not selected, and the top 10 active stocks.
        """

        print(
            f"\n{len(self.nifty50_stocks)} Stocks in total.")
        print(
            f"{len(self.active_stocks)} Stocks selected for active strategy (UPWARDS).")
        print(
            f"{len(self.nifty50_stocks) - len(self.active_stocks)} Stocks not selected (DOWNWARDS).")

        print("\nTop 10 Active Stocks[UPWARDS]:")
        st.write("TOP STOCK SELECTED BASED ON MONTHLY RETURNS")
        for symbol, value in list(self.active_stocks.items())[:10]:
            # print(f"{symbol}: {value:.2f}%")
            st.write(f"{symbol}: {value:.2f}%")


class Summarization:
    """
    A class providing methods for summarizing stock data and analyzing stock performance.

    Attributes:
        class_instance: An instance of the class containing stock data.
        hist_data (pandas.DataFrame): Historical data for the stock.
        todays_date (datetime.date): The current date.

    Methods:
        __init__(self, class_instance):
        CAGR(self, numYears, date=None):
        Volatility(self, start_date=None, end_date=None):
        SharpeRatio(self, start_date=None, end_date=None): 
    """

    def __init__(self, class_instance):
        """
        Initializes a Summarization object with the provided instance of a class containing stock data.

        Parameters:
            class_instance: An instance of the class containing stock data.
        """

        self.class_instance = class_instance
        self.hist_data = class_instance.hist_data
        self.todays_date = class_instance.todays_date

    def CAGR(self, numYears, date=None):
        """
        Calculates the Compound Annual Growth Rate (CAGR) of the stock.

        Parameters:
            numYears (int): Number of years for calculating CAGR.
            date (str or datetime.date, optional): The end date for calculating CAGR.
                Defaults to None.

        Returns:
            float: The calculated CAGR.
        """

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
        """
        Calculates the volatility of the stock.

        Parameters:
            start_date (str or datetime.date, optional): The start date for calculating volatility.
                Defaults to None.
            end_date (str or datetime.date, optional): The end date for calculating volatility.
                Defaults to None.

        Returns:
            float: The calculated volatility.
        """
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
            vol = (math.sqrt(252)*(statistics.stdev(DRet)))*100
            st.write('The Sharpe Ratio of the stock selected:- ' +
                     str(round(vol, 2)))
            return (round(vol, 2))

        else:
            # print('in else statement of Volatility')

            DRet = []
            holidays = []
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

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

            vol = (math.sqrt(252)*(statistics.stdev(DRet)))*100
            st.write('The Sharpe Ratio of the stock selected:- ' +
                     str(round(vol, 2)))
            return (round(vol, 2))

    def SharpeRatio(self, start_date=None, end_date=None):
        """
        Calculates the Sharpe Ratio of the stock.

        Parameters:
            start_date (str or datetime.date, optional): The start date for calculating the Sharpe Ratio.
                Defaults to None.
            end_date (str or datetime.date, optional): The end date for calculating the Sharpe Ratio.
                Defaults to None.

        Returns:
            float: The calculated Sharpe Ratio.
        """
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
            spr = math.sqrt(252)*(np.mean(DRet)/statistics.stdev(DRet))
            st.write('The Sharpe Ratio of the stock selected:- ' +
                     str(round(spr, 2)))
            return (round(spr, 2))

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

            spr = math.sqrt(252)*(np.mean(DRet)/statistics.stdev(DRet))
            st.write('The Sharpe Ratio of the stock selected:- ' +
                     str(round(spr, 2)))
            return (round(spr, 2))


# MAIN
# s1 = Stocks('ADANIPORTS.NS')

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
# failed = ['INFRATEL.NS', 'INF.NS', 'HDFC.NS']

# PORFOLIO CLASS
# p1 = Portfolio(nifty50_ticker_list)

# print(p1.Nifty50_monthlyRet())
# AS_list, AST10_list = p1.ActiveStockSelectionStrategy()
# p1.display_stock_selection()

# BENCHMARKIING CLASS
# b1 = Benchmarking(s1)


# App layout and functionality
# Set page layout for better aesthetics
st.set_page_config(page_title='MoneyPeek', page_icon='random')

st.title("STOCK ANALYSIS")
st.markdown("**Select start and end dates to display performance matrices:**")

start_date = str(st.date_input("Start Date"))
end_date = str(st.date_input("End Date"))

# Create the drop-down with a label and default selection
selected_option = st.selectbox("Choose a Stock:", nifty50_ticker_list)

selectedStock = Stocks(selected_option)

st.markdown("## HISTORICAL DATA OF " + str(selected_option))
selectedStock.DisplayDataframe()

selectedStock_summary = Summarization(selectedStock)

st.markdown("## STOCK PERFORMANCE MATRIX")

st.write('The Daily return of the stock selected:- ' +
         str(selectedStock.DailyReturn()))
st.write('The Monthly return of the stock selected:- ' +
         str(selectedStock.MonthlyRet()))

selectedStock_summary.Volatility(start_date, end_date)
selectedStock_summary.SharpeRatio(start_date, end_date)


portfolio = Portfolio(nifty50_ticker_list)
portfolio.Nifty50_monthlyRet()
AS_list, AST10_list = portfolio.ActiveStockSelectionStrategy()

st.markdown("## TOP 10 STOCKS IN PORTFOLIO")
portfolio.display_stock_selection()
