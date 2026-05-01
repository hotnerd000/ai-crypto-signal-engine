from analysis.market_analysis import run_market_analysis
from ai.ai_decisions import get_ai_portfolio_signal
from strategy.trade_engine import combine_decision
from data.data_fetch import get_price_series
from portfolio.risk import calculate_volatility

def run_multi_coin_analysis(coins, days=30, future_days=7):
    results = []

    for coin in coins:
        try:
            _, future, trade = run_market_analysis(coin, days, future_days)

            avg_score = sum([f["score"] for f in future]) / len(future)

            # 🔥 AI decision
            ai = get_ai_portfolio_signal({
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
                "best_buy": trade["best_buy"],
                "best_sell": trade["best_sell"],
                "final_decision": final_decision,
                "ai_confidence": ai["confidence"],
                "volatility": volatility
            })

        except Exception as e:
            print(f"Error: {coin} → {e}")

    return results