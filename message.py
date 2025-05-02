from src.dataclasses.smametrics import SmaMetrics


class Message:
    index_dict = {
        '^GSPC': ['S&P500', 'https://finance.yahoo.com/quote/%5EGSPC/chart/'],
        '^SP500TR': ['S&P500TR', "https://finance.yahoo.com/quote/%5ESP500TR/chart/"],
        '^NDX': ['NASDAQ-100', 'https://finance.yahoo.com/quote/%5ENDX/chart/'],
        '^GDAXI': ['DAX', 'https://de.finance.yahoo.com/quote/%5EGDAXI/chart/'],
        'TLT': ['TLT', 'https://finance.yahoo.com/quote/TLT/chart/']
    }

    def alarm_message(self, index, signal):
        message = '@everyone \n'
        if signal == 'hold':
            message = 'hold still' + " " + self.index_dict[index][0]
        elif signal == 'buy' or signal == 'sell':
            message = signal + " " + self.index_dict[index][0] + " " + message + self.index_dict[index][1]
        else:
            message = f"No valid signal, possibly no trading today for {self.index_dict[index][0]}?"
        return message

    def report_message(self, index, signal):
        return ''

    @staticmethod
    def get_position(result: SmaMetrics) -> str:

        position = "over" if result.current_price > result.current_sma else "under"
        return f"Price is {result.current_price} and **{position}** {result.sma_days}-SMA of {result.current_sma:.2f}.\n"

    @staticmethod
    def get_distances(result: SmaMetrics) -> str:

        current_distance = "{:.2f}".format(result.current_distance)
        yesterday_distance = "{:.2f}".format(result.yesterday_distance)

        return f"Difference between today's closing price and {result.sma_days}-day SMA: {result.current_diff:.2f}\t**{current_distance}%**\nDifference between yesterday's closing price and {result.sma_days}-day SMA: {result.yesterday_diff:.2f}\t{yesterday_distance}%\n"

    @staticmethod
    def get_direction(result: SmaMetrics):
        gap_change_direction = "Increased" if abs(result.current_diff) > abs(result.yesterday_diff) else "Decreased"

        return f"Gap between price and SMA since yesterday: **{gap_change_direction}**\n"

    @staticmethod
    def get_distances_with_offset(result: SmaMetrics, offset: float) -> str:

        current_sma_high = result.current_sma * (1 + offset)
        current_sma_low = result.current_sma * (1 - offset)
        yesterday_sma_high = result.yesterday_sma * (1 + offset)
        yesterday_sma_low = result.yesterday_sma * (1 - offset)

        current_distance_high = result.current_price - current_sma_high
        current_distance_low = result.current_price - current_sma_low
        yesterday_distance_high = result.current_price - yesterday_sma_high
        yesterday_distance_low = result.current_price - yesterday_sma_low

        current_diff_high = abs(((result.current_price / current_sma_high) - 1) * 100)
        current_diff_low = abs(((result.current_price / current_sma_low) - 1) * 100)
        yesterday_diff_high = abs(((result.current_price / yesterday_sma_high) - 1) * 100)
        yesterday_diff_low = abs(((result.current_price / yesterday_sma_low) - 1) * 100)

        if current_distance_low <= 0.0 and current_distance_high <= 0.0:

            position_text = "Price is **under** both offsets\n"
        elif current_distance_low >= 0.0 and current_distance_high >= 0.0:
            position_text = "Price is **above** both offsets\n"
        else:
            position_text = "Price is **between** high and low offsets\n"

        text = f"""Differences between today's closing price and {result.sma_days}-day SMAs with {offset * 100}% offset: \nCurrent SMA without offset: {result.current_sma:.2f}\nSMA, distance in points, distance in percentage\n\nCurrent high sma: {current_sma_high:.2f}, {current_distance_high:.2f}, **{current_diff_high:.2f}%**\nCurrent low sma: {current_sma_low:.2f}, {current_distance_low:.2f}\t**{current_diff_low:.2f}%**\n\nYesterday high sma: {yesterday_sma_high:.2f}, {yesterday_distance_high:.2f}\t{yesterday_diff_high:.2f}%\nYesterday low sma: {yesterday_sma_low:.2f}, {yesterday_distance_low:.2f}\t{yesterday_diff_low:.2f}%\n\n"""

        return position_text + text

    @staticmethod
    def get_alarms(result: SmaMetrics) -> str:
        message = ""
        if result.nightly_cross_to_above or result.nightly_cross_to_below or result.intraday_to_above or result.intraday_to_below == True:
            message += '@everyone \n'

        if result.nightly_cross_to_above:
            message += 'Price crossed **above SMA** between yesterday Close and todays Open\n'
        if result.nightly_cross_to_below:
            message += 'Price crossed **under SMA** between yesterday Close and todays Open\n'
        if result.intraday_to_above:
            message += 'A cross from below to **above SMA** happened today!\n'
        if result.intraday_to_below:
            message += 'A cross from above to **below SMA** happened today!\n'

        return message
