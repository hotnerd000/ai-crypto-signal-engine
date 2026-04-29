from analyzer import analyze_with_forecast

def analyze_multiple(coins, days=30, future_days=7):
    results = []

    for coin in coins:
        try:
            _, future, trade = analyze_with_forecast(coin, days, future_days)

            score = sum([f["score"] for f in future]) / len(future)

            results.append({
                "coin": coin,
                "avg_score": score,
                "expected_profit": trade["expected_profit_pct"],
                "best_buy": trade["best_buy"],
                "best_sell": trade["best_sell"]
            })

        except Exception as e:
            print(f"Error analyzing {coin}: {e}")

    return results