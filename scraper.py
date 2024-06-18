import yfinance as yf
from datetime import datetime, timedelta

class Scraper:

    # Geht nur wenn Handelstag in USA begonnen hat
    # creates a report of some different data
    def daily_report(self, ticker, sma_days):
        # Define the ticker symbol for the S&P 500 index
        #ticker = "^GSPC"

        # Set today's date
        today = (datetime.today()).strftime("%Y-%m-%d")
        #today = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")

        # Fetch the daily historical data for the last 365 days to calculate the 200-day SMA
        start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        daily_data = yf.download(ticker, start=start_date, end=today)

        # Calculate the 200-day Simple Moving Average (SMA)
        daily_data['200SMA'] = daily_data['Close'].rolling(window=sma_days).mean()

        # Fetch intraday data for today (1-minute interval)
        intraday_data = yf.download(ticker, start=today, interval="1m")

        if intraday_data.empty is True:
            return "No data today"

        # Convert the index to the EST timezone if necessary
        intraday_data.index = intraday_data.index.tz_convert('US/Eastern')

        # Use the last available 200-day SMA value from the daily data for comparison
        current_200SMA = daily_data['200SMA'].iloc[-1]

        # Check if the intraday price has crossed the 200-day SMA at any point
        cross_above = (intraday_data['Close'] > current_200SMA)
        cross_below = (intraday_data['Close'] < current_200SMA)

        # Identify if there was a crossover from below to above or above to below during the day
        crossed_above_anytime = cross_above.any() and cross_below.any() and (cross_above.idxmax() < cross_below.idxmax())
        crossed_below_anytime = cross_below.any() and cross_above.any() and (cross_below.idxmax() < cross_above.idxmax())

        # Determine the latest available price
        latest_price = intraday_data['Close'].iloc[-1] if not intraday_data.empty else None

        # Output the results
        formatted_time = datetime.now().strftime('%H:%M')

        # Calculate the difference between today's closing price and the 200-day SMA
        today_diff = latest_price - current_200SMA

        # Calculate yesterday's closing price
        yesterday_close = daily_data['Close'].iloc[-2]

        # Calculate yesterday's gap between closing price and SMA
        yesterday_diff = yesterday_close - daily_data['200SMA'].iloc[-2]

        # Determine if the gap between SMA and price has increased or decreased since yesterday
        gap_change_direction = "Increased" if abs(today_diff) > abs(yesterday_diff) else "Decreased"

        # Output the results
        s1 = f"Crossed above {sma_days}-day SMA anytime today: {crossed_above_anytime}\n"
        s2 = f"Crossed below {sma_days}-day SMA anytime today: {crossed_below_anytime}\n"
        s3 = f"Latest price at {formatted_time}: {latest_price:.2f}\n" if latest_price is not None else "No data available for the latest price\n"
        #s4 = f"Signal at {formatted_time}: {signal}\n" if latest_price is not None else "Signal: No data available\n"
        s5 = f"Current {sma_days}-day SMA: {current_200SMA:.2f}\n"
        s6 = f"Difference between today's closing price and {sma_days}-day SMA: {today_diff:.2f}\n"
        s7 = f"Difference between yesterday's closing price and {sma_days}-day SMA: {yesterday_diff:.2f}\n"
        s8 = f"Gap between price and SMA since yesterday: {gap_change_direction}\n"

        return "".join([s1, s2, s3, s5, s6, s7, s8])


    # generates hold, buy or sell signal
    def get_signal(self, ticker, sma_days):

        # Set today's date
        today = datetime.today().strftime("%Y-%m-%d")
        #today = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")

        # Fetch the daily historical data for the last 365 days to calculate the 200-day SMA
        start_date = (datetime.today() - timedelta(days=365)).strftime("%Y-%m-%d")
        daily_data = yf.download(ticker, start=start_date, end=today)

        # Calculate the 200-day Simple Moving Average (SMA)
        daily_data['SMA'] = daily_data['Close'].rolling(window=sma_days).mean()

        # Fetch intraday data for today (1-minute interval)
        intraday_data = yf.download(ticker, start=today, interval="1m")

        if intraday_data.empty is True:
            return "No data today"

        # Convert the index to the EST timezone if necessary
        intraday_data.index = intraday_data.index.tz_convert('US/Eastern')

        # Use the last available 200-day SMA value from the daily data for comparison
        current_200SMA = daily_data['SMA'].iloc[-1]

        # Determine the latest available price for today
        latest_price = intraday_data['Close'].iloc[-1] if not intraday_data.empty else None

        # Determine yesterday's closing price
        yesterday_close = daily_data['Close'].iloc[-2]

        # Initialize signal
        signal = "hold"

        # Generate the signal based on the latest price and yesterday's close
        if latest_price is not None:
            if yesterday_close < current_200SMA and latest_price > current_200SMA:
                signal = 'buy'
            elif yesterday_close > current_200SMA and latest_price < current_200SMA:
                signal = 'sell'
            else:
                signal = 'hold'

        return signal