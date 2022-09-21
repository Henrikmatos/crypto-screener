import logging

import pandas as pd

from crypto_screener.rating_service import RatingService
from crypto_screener.statistics_service import StatisticService


class CryptoScreenerService:

    def __init__(self, data_downloader):
        self.data_downloader = data_downloader

    def download_and_calculate_values(self, assets: pd.DataFrame):
        result = pd.DataFrame()

        logging.info("Start download and calculate values")

        count_assets = assets.shape[0]
        for index, asset in assets.iterrows():
            logging.info("Process asset - {} ({}/{})".format(asset["Asset"], index + 1, count_assets))
            try:
                exchange = "Phemex" if asset["PhemexFutures"] else "Kucoin"
                ohlc_daily = self.data_downloader.download_daily_ohlc(exchange, asset["Asset"])
                ohlc_weekly = self.__resample_to_weekly_ohlc(ohlc_daily)
                last_price = self.__parse_last_price(ohlc_daily)

                asset["LastPrice"] = last_price
                asset["RSI_14"] = StatisticService.calculate_actual_rsi(ohlc_daily, 14)
                asset["SMA_20"] = StatisticService.calculate_actual_sma(ohlc_daily, 20)
                asset["SMA_50"] = StatisticService.calculate_actual_sma(ohlc_daily, 50)
                asset["SMA_200"] = StatisticService.calculate_actual_sma(ohlc_daily, 200)
                asset["ATR%_W"] = StatisticService.calculate_actual_atr_percentage(ohlc_weekly,
                                                                                   ohlc_weekly.shape[0] - 1,
                                                                                   last_price)

                asset["MovingAveragesRating"] = RatingService.calculate_moving_averages_rating(asset)
                asset["OscillatorsRating"] = RatingService.calculate_oscillators_rating(asset)
                asset["VolatilityRating"] = RatingService.calculate_volatility_rating(asset)
                asset["LastDate"] = self.__parse_last_date(ohlc_daily)
                result = pd.concat([result, pd.DataFrame([asset])])
            except:
                logging.exception("Problem with compute statistic or rating on coin {}".format(asset["Asset"]))
                result = pd.concat([result, pd.DataFrame([asset])])

        logging.info("Finished download and calculate values")

        return result

    @staticmethod
    def __parse_last_price(ohlc_daily):
        return ohlc_daily.tail(1)["close"].values[0]

    @staticmethod
    def __parse_last_date(ohlc_daily):
        return ohlc_daily.tail(1).index.date[0].strftime("%d.%m.%Y")

    @staticmethod
    def __resample_to_weekly_ohlc(ohlc_daily):
        return ohlc_daily.resample("W").aggregate({'open': 'first',
                                                   'high': 'max',
                                                   'low': 'min',
                                                   'close': 'last'})
