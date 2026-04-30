import requests
import pandas as pd

def fetch_price_data(coin="bitcoin", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}"
    
    print(f"\nFetching price data {coin.upper()}...\n")

    res = requests.get(url, timeout=10)
    data = res.json()

    prices = data["prices"]

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df

def get_current_prices(coins):
    """
    coins: list like ["bitcoin", "ethereum"]
    """
    ids = ",".join(coins)

    print(f"\nFetching price data of {id}...\n")
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"

    res = requests.get(url, timeout=10)
    data = res.json()

    prices = {}
    for coin in coins:
        prices[coin] = data.get(coin, {}).get("usd", 0)

    return prices

def get_price_series(coin, days=30):
    df = fetch_price_data(coin, days)
    return df["price"].tolist()