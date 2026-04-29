import numpy as np

def calculate_volatility(price_series):
    """
    price_series: list or numpy array of prices
    """
    prices = np.array(price_series)

    if len(prices) < 2:
        return 0

    returns = np.diff(prices) / prices[:-1]
    volatility = np.std(returns)

    return float(volatility)