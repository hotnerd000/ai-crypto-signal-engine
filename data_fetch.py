import requests
import pandas as pd

def fetch_price_data(coin="bitcoin", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}"
    
    res = requests.get(url)
    data = res.json()

    prices = data["prices"]

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df