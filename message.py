from src.dataclasses.result import Result


class Message:
    index_dict = {
        'sp500': ['S&P500', 'https://finance.yahoo.com/quote/%5EGSPC/chart/'],
        'nasdaq': ['NASDAQ-100', 'https://finance.yahoo.com/quote/%5ENDX/chart/'],
        'dax' : ['DAX', 'https://de.finance.yahoo.com/quote/%5EGDAXI/chart/'],
        'tlt' : ['TLT', 'https://finance.yahoo.com/quote/TLT/chart/']
    }

    def alarm_message(self, index, signal):
        message = '@everyone \n'
        if signal == 'hold':
            message = 'hold' + " " + self.index_dict[index][0]
        elif signal == 'buy' or signal == 'sell':
            message = signal + " " + self.index_dict[index][0] + " " + message + self.index_dict[index][1]
        else:
            message = f"No valid signal, possibly no trading today for {self.index_dict[index][0]}?"
        return message

    def report_message(self, index, signal):
        return ''

    @staticmethod
    def get_position(result: Result)-> str:

        position = "over" if result.current_price > result.current_sma else "under"
        return f"Price is {result.current_price} and **{position}** {result.sma}-SMA of {result.current_sma}.\n"

    @staticmethod
    def get_distances(result: Result)->str:

        current_distance = "{:.2f}".format(result.current_distance)
        yesterday_distance = "{:.2f}".format(result.yesterday_distance)

        return f"Difference between today's closing price and {result.sma}-day SMA: {result.current_diff:.2f}\t**{current_distance}%**\nDifference between yesterday's closing price and {result.sma}-day SMA: {result.yesterday_diff:.2f}\t{yesterday_distance}%\n"

    @staticmethod
    def get_direction(result: Result):
        gap_change_direction = "Increased" if abs(result.current_diff) > abs(result.yesterday_diff) else "Decreased"

        return f"Gap between price and SMA since yesterday: **{gap_change_direction}**\n"

    @staticmethod
    def get_distances_with_offset(result: Result, offset: float)->str:

        current_sma_high = result.current_sma*(1+offset)
        current_sma_low = result.current_sma*(1-offset)
        yesterday_sma_high = result.yesterday_sma*(1+offset)
        yesterday_sma_low = result.yesterday_sma*(1-offset)

        current_distance_high = result.current_price - current_sma_high
        current_distance_low = result.current_price - current_sma_low
        yesterday_distance_high = result.current_price - yesterday_sma_high
        yesterday_distance_low = result.current_price - yesterday_sma_low

        current_diff_high = abs(((result.current_price / current_sma_high) - 1) * 100)
        current_diff_low = abs(((result.current_price / current_sma_low) - 1) * 100)
        yesterday_diff_high = abs(((result.current_price / yesterday_sma_high) - 1) * 100)
        yesterday_diff_low = abs(((result.current_price / yesterday_sma_low) - 1) * 100)

        if current_distance_low <= 0.0 and current_distance_high <=0.0:

            position_text = "Price is **under** both SMAs\n"
        elif current_distance_low >= 0.0 and current_distance_high >= 0.0:
            position_text = "Price is **above** both SMAs\n"
        else:
            position_text = "Price is **between** high and low SMA\n"

        text = f"""Differences between today's closing price and {result.sma}-day SMAs with {offset}% offset: 
        Current SMA without offset: {result.current_sma}
        SMA, distance in points, distance in percentage
        Current high sma: {current_sma_high}, {current_distance_high:.2f}, **{current_diff_high:.2f}%**
        Current low sma: {current_sma_low}, {current_distance_low:.2f}\t**{current_diff_low:.2f}%**
        Yesterday high sma: {yesterday_sma_high}, {yesterday_distance_high:.2f}\t{yesterday_diff_high:.2f}%
        Yesterday low sma: {yesterday_sma_low}, {yesterday_distance_low:.2f}\t{yesterday_diff_low:.2f}%\n"""

        return position_text+text