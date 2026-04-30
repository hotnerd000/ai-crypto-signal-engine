from signals.signal_engine import generate_signal


def project_future(df, days_ahead=7):
    last_row = df.iloc[-1]

    price = float(last_row["price"])
    rsi = float(last_row["rsi"])
    ma = float(last_row["ma"])

    results = []

    for i in range(1, days_ahead + 1):
        # 🔥 Simple trend simulation
        trend = (price - ma) / ma

        # simulate price movement
        price = price * (1 + trend * 0.2)

        # simulate RSI drift
        if trend > 0:
            rsi = min(100, rsi + 2)
        else:
            rsi = max(0, rsi - 2)

        simulated_row = {
            "price": price,
            "rsi": rsi,
            "ma": ma
        }

        signal, score, reasons = generate_signal(simulated_row)

        results.append({
            "day": i,
            "price": price,
            "rsi": rsi,
            "signal": signal,
            "score": score,
            "reasons": reasons
        })

    return results