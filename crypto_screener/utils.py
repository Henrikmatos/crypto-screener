import logging
import pandas as pd

import yaml


def load_config(file_path):
    try:
        with open(file_path, 'r') as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        logging.exception("Problem with loading configuration from file, the application will be terminated.")
        exit(1)
    except yaml.YAMLError:
        logging.exception("Problem with parsing configuration, the application will be terminated.")
        exit(1)


def parse_only_kucoin_coins():
    phemex_futures = pd.read_csv("../data/phemex_futures.csv")
    kucoin_spot = pd.read_csv("../data/kucoin_spot.csv")

    phemex_coins = phemex_futures["Ticker"] \
        .str.replace("USDPERP", "") \
        .str.replace("100", "") \
        .str.replace("1000", "").tolist()

    kucoin_coins = kucoin_spot["Ticker"] \
        .str.replace("USDT", "") \
        .tolist()

    only_kucoin_coins = set(kucoin_coins) - set(phemex_coins)

    result = pd.DataFrame({"Ticker": list(only_kucoin_coins)})
    result["Ticker"] = result["Ticker"] + "USDT"
    result.to_csv("../data/kocoin_only.csv", index=False)
