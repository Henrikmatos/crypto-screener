import logging
import logging.config

import pandas as pd

from crypto_screener import __version__
from crypto_screener.crypto_screener_service import CryptoScreenerService

# Constants
__logo__ = """
---------------------------------------------------------------------
crypto-screener {}
---------------------------------------------------------------------
""".format(__version__.__version__)

from crypto_screener.data_downloader import DataDownloader

from crypto_screener.utils import load_config

CONFIG_FILE_PATH = "config.yaml"
LOGGER_CONFIG_FILE_PATH = "logger.conf"
INPUT_EXCEL_PATH = "data/CryptoScreener.xlsx"
OUTPUT_CSV_PATH = "data/CryptoScreenerWithValues.csv"

logging.config.fileConfig(fname=LOGGER_CONFIG_FILE_PATH, disable_existing_loggers=False)
logging.info(__logo__)
config = load_config(CONFIG_FILE_PATH)

if __name__ == "__main__":
    data_downloader = DataDownloader(config["RateExceedDelaySeconds"])
    crypto_screener_service = CryptoScreenerService(data_downloader)

    assets = pd.read_excel(INPUT_EXCEL_PATH, sheet_name="CryptoScreener")
    assets_with_values = crypto_screener_service.download_and_calculate_values(assets)
    assets_with_values.to_csv(OUTPUT_CSV_PATH, index=False)
