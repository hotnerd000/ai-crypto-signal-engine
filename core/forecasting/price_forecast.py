from strategy.trade_decision import generate_trade_decision

def forecast_prices(coin, df, days_ahead=7):
    print(f"\nProject Future\n")
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

        print(f"\nCalling Decide Action----\n")
        decision = generate_trade_decision(coin, simulated_row, df.iloc[:])

        results.append({
            "day": i,
            "price": price,
            "rsi": rsi,
            "signal": decision["decision"],
            "score": decision["confidence"],
            "reasons": decision["reasons"]
        })

    return results