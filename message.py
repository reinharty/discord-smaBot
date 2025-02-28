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
        return f"Price is {result.current_price} and **{position}** SMA of {result.current_sma}.\n"

    @staticmethod
    def get_distances(result: Result)->str:

        current_distance = "{:.2f}".format(result.current_distance)
        yesterday_distance = "{:.2f}".format(result.yesterday_distance)

        return f"Difference between today's closing price and {result.sma}-day SMA: {result.current_diff:.2f}\t**{current_distance}%**\nDifference between yesterday's closing price and {result.sma}-day SMA: {result.yesterday_diff:.2f}\t{yesterday_distance}%\n"

    @staticmethod
    def get_direction(result: Result):
        gap_change_direction = "Increased" if abs(result.current_diff) > abs(result.yesterday_diff) else "Decreased"

        return f"Gap between price and SMA since yesterday: **{gap_change_direction}**\n"