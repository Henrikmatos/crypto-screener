class RatingService:

    @staticmethod
    def calculate_moving_averages_rating(asset):
        last_price = asset["LastPrice"]
        sma_20 = asset["SMA_20"]
        sma_50 = asset["SMA_50"]
        sma_200 = asset["SMA_200"]

        # [Python - List Comprehension](https://www.w3schools.com/python/python_lists_comprehension.asp)
        count_up = len([x for x in [sma_20, sma_50, sma_200] if x is not None and x < last_price])
        count_down = len([x for x in [sma_20, sma_50, sma_200] if x is not None and x > last_price])

        if count_up == 3:
            return "STRONG_UP_TREND"

        if count_up == 2:
            return "UP_TREND"

        if count_down == 3:
            return "STRONG_DOWN_TREND"

        if count_down == 2:
            return "DOWN_TREND"

        return None

    @staticmethod
    def calculate_oscillators_rating(asset):
        rsi = asset["RSI_14"]

        if rsi is None:
            return None

        if rsi > 70:
            return "OVERBOUGHT"
        if 50 <= rsi <= 70:
            return "BULLISH"
        if 30 <= rsi < 50:
            return "BEARISH"
        if rsi < 30:
            return "OVERSOLD"

    @staticmethod
    def calculate_volatility_rating(asset):
        volatility = asset["ATR%_W"]

        if volatility is None:
            return None

        if volatility > 0.3:
            return "HIGH"
        elif volatility > 0.1:
            return "MEDIUM"
        else:
            return "LOW"
