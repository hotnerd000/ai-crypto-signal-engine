from analyzer import analyze_coin
from analyzer import analyze_with_forecast


def main():
    print("=== AI Crypto Signal + Forecast ===\n")

    coin = input("Enter coin: ").strip().lower() or "bitcoin"
    days = int(input("Past days: ") or 30)
    future_days = int(input("Future days: ") or 7)

    historical, future, trade = analyze_with_forecast(
        coin, days, future_days
    )

    print("\n--- FUTURE SIGNALS ---\n")

    for f in future:
        print(f"Day {f['day']}")
        print(f"Price: {f['price']:.2f}")
        print(f"RSI: {f['rsi']:.2f}")
        print(f"Signal: {f['signal']} (Score: {f['score']})")
        print("-" * 30)

    print("\n--- BEST TRADE ---\n")

    if trade["best_buy"]:
        print(f"Best BUY → Day {trade['best_buy']['day']} @ {trade['best_buy']['price']:.2f}")

    if trade["best_sell"]:
        print(f"Best SELL → Day {trade['best_sell']['day']} @ {trade['best_sell']['price']:.2f}")

    print(f"Expected Profit: {trade['expected_profit_pct']:.2f}%")


if __name__ == "__main__":
    main()