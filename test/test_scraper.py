from unittest import TestCase

import numpy as np

from scraper import Scraper, Data, Result
import pandas as pd


class TestScraper(TestCase):
    def test_daily_report(self):
        self.fail()

    def test_calculate_SMA(self):
        data_file = "test_data/Output-daily-data-tlt2.csv"

        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")

        returned_data = Scraper().calc_sma(daily_data, 200)

        self.assertEqual(returned_data.iloc[-1], np.float64(19471.174765625))

    def test_calculator(self):
        data_file = "test_data/Output-daily-data-tlt2.csv"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test_data/Output-intraday-data-tlt2.csv"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper().calculator(data, 200)

        expected = Result(np.float64(22425.19921875), np.float64(22576.119140625), np.float64(19471.174765625),
                          np.float64(19451.473115234374))

        self.assertEqual(result, expected)

    def test_generate_signal_hold(self):
        data_file = "test_data/daily-hold.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test_data/intraday-hold.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper().calculator(data, 200)

        expected = "hold"

        self.assertEqual(expected, Scraper().generate_signal(result))

    def test_generate_signal_buy(self):
        data_file = "test_data/daily-buy.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test_data/intraday-buy.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper().calculator(data, 200)

        expected = "buy"

        self.assertEqual(expected, Scraper().generate_signal(result))

    def test_generate_signal_sell(self):
        data_file = "test_data/daily-sell.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test_data/intraday-sell.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper().calculator(data, 200)

        expected = "sell"

        self.assertEqual(expected, Scraper().generate_signal(result))

    def test_generate_signal_hold_offset(self):
        data_file = "test_data/daily-hold-offset.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test_data/intraday-hold-offset.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper().calculator(data, 200)

        expected = "hold"

        self.assertEqual(expected, Scraper().generate_signal(result, 0.025))

    def test_generate_signal_buy_offset(self):
        data_file = "test_data/daily-buy-offset.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test_data/intraday-buy-offset.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper().calculator(data, 200)

        expected = "buy"

        self.assertEqual(expected, Scraper().generate_signal(result,0.025))

    def test_generate_signal_sell_offset(self):
        data_file = "test_data/daily-sell-offset.txt"
        daily_data = pd.read_csv(data_file, parse_dates=["Date"], index_col="Date")
        intraday_file = "test_data/intraday-sell-offset.txt"  # Heutige 15-Minuten-Kerzen
        intraday = pd.read_csv(intraday_file, parse_dates=["Datetime"], index_col="Datetime")

        data = Data(daily_data, intraday)
        result = Scraper().calculator(data, 200)

        expected = "sell"

        self.assertEqual(expected, Scraper().generate_signal(result, 0.025))