from data.data_fetch import fetch_price_data
from indicators.indicators import apply_indicators
from signals.signal_engine import generate_signal
from forecasting.forecast import project_future
from strategy.strategy import find_best_trade


def analyze_coin(coin="bitcoin", days=30):
    df = fetch_price_data(coin, days)
    df = apply_indicators(df)

    results = []

    for _, row in df.iterrows():
        signal, score, reasons = generate_signal(row)

        results.append({
            "date": row["timestamp"].strftime("%Y-%m-%d"),
            "price": float(row["price"]),
            "rsi": float(row["rsi"]),
            "ma": float(row["ma"]),
            "signal": signal,
            "score": score,
            "reasons": reasons
        })

    return results

def analyze_with_forecast(coin="bitcoin", days=30, future_days=7):
    df = fetch_price_data(coin, days)
    df = apply_indicators(df)

    historical = []

    for _, row in df.iterrows():
        signal, score, reasons = generate_signal(row)

        historical.append({
            "date": row["timestamp"].strftime("%Y-%m-%d"),
            "price": float(row["price"]),
            "signal": signal
        })

    
    future = project_future(coin, df, future_days)
    print(f"\nFind Beset Trade\n")
    trade = find_best_trade(future)

    return historical, future, trade