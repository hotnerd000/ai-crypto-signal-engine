from analysis.analyzer import analyze_with_forecast
from ai.ai_decision import get_ai_decision
from strategy.decision_engine import combine_decision
from data.data_fetch import get_price_series
from portfolio.risk import calculate_volatility

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


def analyze_multiple(coins, days=30, future_days=7):
    results = []

    for coin in coins:
        try:
            _, future, trade = analyze_with_forecast(coin, days, future_days)

            avg_score = sum([f["score"] for f in future]) / len(future)

            # 🔥 AI decision
            ai = get_ai_decision({
                "coin": coin,
                "score": avg_score,
                "expected_profit": trade["expected_profit_pct"]
            })

            final_decision = combine_decision(
                avg_score,
                ai["decision"],
                ai["confidence"]
            )

            price_series = get_price_series(coin, days)
            volatility = calculate_volatility(price_series)

            results.append({
                "coin": coin,
                "avg_score": avg_score,
                "expected_profit": trade["expected_profit_pct"],
                "final_decision": final_decision,
                "ai_confidence": ai["confidence"],
                "volatility": volatility
            })

        except Exception as e:
            print(f"Error: {coin} → {e}")

    return results