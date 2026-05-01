from core.data.data_fetch import get_historical_prices
from core.indicators.indicators import compute_indicators
from core.signals.rule_signals import generate_rule_signal
from core.forecasting.price_forecast import forecast_prices
from core.strategy.strategy import find_best_trade


def analyze_coin(coin="bitcoin", days=30):
    df = get_historical_prices(coin, days)
    df = compute_indicators(df)

    results = []

    for _, row in df.iterrows():
        signal, score, reasons = generate_rule_signal(row)

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

def run_market_analysis(coin="bitcoin", days=30, future_days=7):
    df = get_historical_prices(coin, days)
    df = compute_indicators(df)

    historical = []

    for _, row in df.iterrows():
        signal, score, reasons = generate_rule_signal(row)

        historical.append({
            "date": row["timestamp"].strftime("%Y-%m-%d"),
            "price": float(row["price"]),
            "signal": signal
        })

    
    future = forecast_prices(coin, df, future_days)
    print(f"\nFind Beset Trade\n")
    trade = find_best_trade(future)

    return historical, future, trade