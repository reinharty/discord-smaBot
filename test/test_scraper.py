from unittest import TestCase

import numpy as np
import pandas as pd

from src.dataclasses.data import Data
from src.dataclasses.result import Result
from src.logic.scraper import Scraper


class TestScraper(TestCase):
    # def test_daily_report(self):
    #     self.fail()

    def test_calculate_SMA(self):
        data_file = "test-data/Output-daily-data-tlt2.csv"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        returned_data = Scraper.calc_sma(daily_data, 200)
        self.assertEqual(returned_data.iloc[-1], np.float64(19471.174765625))

    def test_calculator(self):
        data_file = "test-data/daily-hold.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test-data/intraday-hold.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper.calculator(data, 200)

        expected = Result(current_price=np.float64(89.19499969482422),
                          yesterday_close=np.float64(89.88999938964844),
                          current_sma=np.float64(92.70424987792968),
                          yesterday_sma=np.float64(92.70074989318847))

        self.assertEqual(expected, result)

    def test_generate_signal_hold(self):
        data_file = "test-data/daily-hold.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test-data/intraday-hold.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper.calculator(data, 200)

        expected = "hold"
        self.assertEqual(expected, Scraper.generate_signal(result))
        self.assertEqual(expected, Scraper.generate_signal(result, 0.025))

    def test_generate_signal_buy(self):
        data_file = "test-data/daily-buy.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test-data/intraday-buy.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper.calculator(data, 200)

        expected = "buy"
        self.assertEqual(expected, Scraper.generate_signal(result))

        # since price is only slightly above sma, hence, with offset it is still 'hold'
        self.assertEqual("hold", Scraper.generate_signal(result,0.025))

    def test_generate_signal_sell(self):
        data_file = "test-data/daily-sell.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test-data/intraday-sell.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper.calculator(data, 200)

        print(result)
        expected = "sell"
        self.assertEqual(expected, Scraper.generate_signal(result))
        self.assertEqual("hold", Scraper.generate_signal(result, 0.025))

    def test_generate_signal_hold_offset(self):
        data_file = "test-data/daily-hold-offset.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test-data/intraday-hold-offset.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper.calculator(data, 200)

        expected = "hold"
        self.assertEqual(expected, Scraper.generate_signal(result, 0.025))

    def test_generate_signal_buy_offset(self):
        data_file = "test-data/daily-buy-offset.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test-data/intraday-buy-offset.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper.calculator(data, 200)

        expected = "buy"
        self.assertEqual(expected, Scraper.generate_signal(result,0.025))

    def test_generate_signal_sell_offset(self):
        data_file = "test-data/daily-sell-offset.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test-data/intraday-sell-offset.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper.calculator(data, 200)

        expected = "sell"
        self.assertEqual(expected, Scraper().generate_signal(result, 0.025))