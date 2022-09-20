import math

import pandas as pd
import pandas_ta as ta


class StatisticService:

    @staticmethod
    def calculate_actual_rsi(ohlc: pd.DataFrame, length: int = 14):
        if length > ohlc.shape[0]:
            return None

        rsi = ohlc.ta.rsi(length=length)
        actual_rsi = rsi.tail(1).values[0]

        if math.isnan(actual_rsi):
            return None
        return round(actual_rsi, 6)

    @staticmethod
    def calculate_actual_sma(ohlc: pd.DataFrame, length: int = 20):
        if length > ohlc.shape[0]:
            return None

        sma = ohlc.ta.sma(length=length)
        actual_sma = sma.tail(1).values[0]

        if math.isnan(actual_sma):
            return None
        return round(actual_sma, 6)

    @staticmethod
    def calculate_actual_atr_percentage(ohlc: pd.DataFrame, length: int, last_price: int):
        if length > ohlc.shape[0]:
            return None

        atr = ohlc.ta.atr(length=length)
        actual_atr = atr.tail(1).values[0]

        if math.isnan(actual_atr):
            return None
        return round(actual_atr / last_price, 6)
