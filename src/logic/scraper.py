import yfinance as yf
from datetime import datetime, timedelta

from message import Message
from src.dataclasses.data import Data
from src.dataclasses.result import Result


class Scraper:

    @staticmethod
    def generate_signal(result: Result, offset: float=0.0)->str:
        if result.yesterday_close > (result.yesterday_sma * (1 - offset)) and result.current_price < (result.current_sma * (1 - offset)):
            return "sell"
        if result.yesterday_close < (result.yesterday_sma * (1 + offset)) and result.current_price > (result.current_sma * (1 + offset)):
            return "buy"
        return "hold"

    @staticmethod
    def calc_sma(daily_data, sma_days):
        #TODO add current price to daily_data but requires knowledge if market is still open for this ticker
        # Calculate the SMA
        return daily_data['Close'].rolling(window=sma_days).mean()

    @staticmethod
    def calc_diff_between_price_and_sma(price, sma)->float:
        return abs(((price / sma) - 1) * 100)

    @staticmethod
    def calculator(data: Data, sma_days: int) -> Result:

        sma_series = Scraper.calc_sma(data.daily, sma_days)

        current_price = data.intraday["Close"].iloc[-1]
        yesterday_price = data.daily["Close"].iloc[-2]
        current_sma = sma_series.iloc[-1]
        yesterday_sma = sma_series.iloc[-2]

        today_diff = current_price - current_sma
        yesterday_diff = yesterday_price - yesterday_sma

        current_distance = Scraper.calc_diff_between_price_and_sma(current_price, current_sma)
        yesterday_distance = Scraper.calc_diff_between_price_and_sma(yesterday_price, yesterday_sma)

        return Result(sma_days,
                      current_price, yesterday_price,
                      current_sma, yesterday_sma,
                      today_diff, yesterday_diff,
                      current_distance, yesterday_distance)

    @staticmethod
    def get_signal(ticker, sma_days=200, offset=0.0):

        ticker_data = yf.Ticker(ticker)
        daily_data = ticker_data.history(period='12mo')
        intraday_data = ticker_data.history(period='1d', interval='1m')

        data = Data(daily_data, intraday_data)
        result = Scraper.calculator(data, sma_days)

        signal = Scraper.generate_signal(result, offset)
        return(signal)

    #TODO handle result object better so that it must not be generated twice
    @staticmethod
    def get_report(ticker, sma_days=200, offset=0.0):

        ticker_data = yf.Ticker(ticker)
        daily_data = ticker_data.history(period='12mo')
        intraday_data = ticker_data.history(period='1d', interval='1m')

        data = Data(daily_data, intraday_data)
        result = Scraper.calculator(data, sma_days)

        if offset == 0.0:
            return Scraper().daily_report3(result)
        else:
            return Scraper().daily_report_with_offset(result, offset)
    # Geht nur wenn Handelstag in USA begonnen hat
    # creates a report of some different data
    def daily_report(self, ticker, sma_days):
        # Set today's date
        today = datetime.today().strftime("%Y-%m-%d")

        # Fetch the daily historical data for the last 365 days
        start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        daily_data = yf.download(ticker, start=start_date, end=today)

        if daily_data.empty or len(daily_data) < 2:
            return "Not enough daily data available"

        # Calculate the SMA
        daily_data['200SMA'] = self.calc_sma(daily_data, sma_days)

        # Fetch intraday data (1-minute interval)
        end_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        # intraday_data = yf.download(ticker, start=today, end=end_time, interval="1m")
        intraday_data = yf.download(ticker, start=today, interval="1m")

        if intraday_data.empty:
            return "No intraday data today"

        # Convert the index to US Eastern Time
        try:
            intraday_data.index = intraday_data.index.tz_convert('US/Eastern')
        except Exception:
            return "Timezone conversion failed"

        # Use the last available 200-day SMA value
        current_200SMA = daily_data['200SMA'].iloc[-1]

        # Check if the intraday price crossed the SMA
        cross_above = (intraday_data['Close'] > current_200SMA)
        cross_below = (intraday_data['Close'] < current_200SMA)

        # crossed_above_anytime = cross_above.any() and cross_below.any() and (cross_above.idxmax() < cross_below.idxmax())
        # crossed_below_anytime = cross_below.any() and cross_above.any() and (cross_below.idxmax() < cross_above.idxmax())

        # Latest price
        latest_price = intraday_data['Close'].iloc[-1] if not intraday_data.empty else None

        # Format the time
        formatted_time = datetime.now().strftime('%H:%M')

        # Differences and positions
        today_diff = latest_price - current_200SMA
        yesterday_close = daily_data['Close'].iloc[-2]
        position = "over" if latest_price > daily_data['200SMA'].iloc[-2] else "under"
        yesterday_diff = yesterday_close - daily_data['200SMA'].iloc[-2]
        gap_change_direction = "Increased" if abs(today_diff) > abs(yesterday_diff) else "Decreased"

        # Distance percentage calculations
        distance_percentage_today = "{:.2f}".format(abs(((latest_price / current_200SMA) - 1) * 100))
        distance_percentage_yesterday = "{:.2f}".format(
            abs(((yesterday_close / daily_data['200SMA'].iloc[-2]) - 1) * 100))

        # Output results
        s0 = f"Price is **{position}** SMA.\n"
        # s1 = f"Crossed above {sma_days}-day SMA anytime today: **{crossed_above_anytime}**\n"
        # s2 = f"Crossed below {sma_days}-day SMA anytime today: **{crossed_below_anytime}**\n"
        s1 = ""
        s2 = ""
        s3 = f"Latest price at {formatted_time}: {latest_price:.2f}\n" if latest_price is not None else "No data available for the latest price\n"
        s5 = f"Current {sma_days}-day SMA: {current_200SMA:.2f}\n"
        s6 = f"Difference between today's closing price and {sma_days}-day SMA: {today_diff:.2f}\t**{distance_percentage_today}%**\n"
        s7 = f"Difference between yesterday's closing price and {sma_days}-day SMA: {yesterday_diff:.2f}\t{distance_percentage_yesterday}%\n"
        s8 = f"Gap between price and SMA since yesterday: **{gap_change_direction}**\n"

        return "".join([s1, s2, s0, s3, s5, s6, s7, s8])

    def daily_report2(self, ticker, sma_days):
        today = (datetime.today()).strftime("%Y-%m-%d")

        # Fetch the daily historical data for the last 365 days to calculate the 200-day SMA
        start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        daily_data = yf.download(ticker, start=start_date, end=today)

        # Calculate the 200-day Simple Moving Average (SMA)
        daily_data['200SMA'] = daily_data['Close'].rolling(window=sma_days).mean()

        # Fetch intraday data for today (1-minute interval)
        intraday_data = yf.download(ticker, start=today, interval="1m")

        if intraday_data.empty is True:
            return "No data today"

    def daily_report3(self, result: Result):
        message = Message.get_position(result)
        message = message + Message.get_distances(result)
        message += Message.get_direction(result)

        return message

    def daily_report_with_offset(self, result: Result, offset):
        message = Message.get_position(result)
        message = message + Message.get_distances_with_offset(result, offset)
        #message += Message.get_direction(result)

        return message

