import logging
import time

import ccxt
import pandas as pd
from ccxt import RateLimitExceeded


class DataDownloader:

    def __init__(self, rate_exceed_delay_seconds):
        self.phemex_client = ccxt.phemex()
        self.kucoin_client = ccxt.kucoin()
        self.rate_exceed_delay_seconds = rate_exceed_delay_seconds

    def download_daily_ohlc(self, exchange, ticker):
        logging.debug("Start downloading daily OHLC for {} on exchange {}".format(ticker, exchange))
        if exchange == "Phemex":
            return self.__download_daily_ohlc_from_ccxt("Phemex", ticker.replace("PERP", "").replace("100", "u100"))
        else:
            return self.__download_daily_ohlc_from_ccxt("Kucoin", ticker.replace("USDT", "-USDT"))

    def __download_daily_ohlc_from_crypto_data_download(self, exchange, ticker):
        ohlc_daily = pd.read_csv(self.CRYPTO_DATA_DOWNLOADER_URL.format(exchange, ticker),
                                 skiprows=1)
        ohlc_daily["date"] = pd.to_datetime(ohlc_daily["date"])
        ohlc_daily.set_index(["date"], inplace=True)
        ohlc_daily.sort_values(["date"], ascending=True, inplace=True)
        return ohlc_daily[["open", "high", "low", "close"]]

    def __download_daily_ohlc_from_ccxt(self, exchange, ticker):
        while True:
            try:
                exchange_client = self.phemex_client if exchange == "Phemex" else self.kucoin_client
                ohlc_daily_raw = exchange_client.fetch_ohlcv(ticker, timeframe="1d", limit=200)
                ohlc_daily = pd.DataFrame(ohlc_daily_raw, columns=["date", "open", "high", "low", "close", "volume"])
                ohlc_daily["date"] = pd.to_datetime(ohlc_daily["date"], unit='ms')
                ohlc_daily.set_index(["date"], inplace=True)
                ohlc_daily.sort_values(["date"], ascending=True, inplace=True)
                return ohlc_daily
            except RateLimitExceeded:
                logging.warning(
                    "RateLimitExceeded: Too Many Requests on exchange api, app will be sleep {} seconds before recall api."
                    .format(self.rate_exceed_delay_seconds))
                time.sleep(self.rate_exceed_delay_seconds)
