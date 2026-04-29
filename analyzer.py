from data_fetch import fetch_price_data
from indicators import apply_indicators
from signal_engine import generate_signal


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