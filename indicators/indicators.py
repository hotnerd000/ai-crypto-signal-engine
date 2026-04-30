import ta

def apply_indicators(df):
    df["rsi"] = ta.momentum.RSIIndicator(df["price"], window=14).rsi()
    df["ma"] = ta.trend.SMAIndicator(df["price"], window=50).sma_indicator()

    return df.dropna()