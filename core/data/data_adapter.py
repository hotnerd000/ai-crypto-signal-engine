# core/data/data_adapter.py

from core.data.data_fetch import get_historical_prices

def fetch_price_data(coin, days=30):
    """
    Standardized data fetch for bot + backtest
    Returns DataFrame with 'price' column
    """
    
    df = get_historical_prices(coin, days)

    
    # Ensure consistent column naming
    if "price" not in df.columns:
        if "close" in df.columns:
            df["price"] = df["close"]

    return df