class Message:
    index_dict = {
        'sp500': ['S&P500', 'https://finance.yahoo.com/quote/%5EGSPC/chart/'],
        'nasdaq': ['NASDAQ-100', 'https://finance.yahoo.com/quote/%5ENDX/chart/'],
        'dax' : ['DAX', 'https://de.finance.yahoo.com/quote/%5EGDAXI/chart/'],
        'tyx' : ['TreasuryYield30', 'https://finance.yahoo.com/quote/%5ETYX/chart/']
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
