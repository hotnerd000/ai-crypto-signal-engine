from analyzer import analyze_with_forecast
from multi_coin import analyze_multiple
from ranking import rank_coins
from ai_explainer import explain_coin

PREDEFINED_COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "ripple": "XRP",
    "cardano": "ADA",
    "dogecoin": "DOGE",
    "polkadot": "DOT",
    "tron": "TRX"
}

def multi_coin_mode():
    coins = list(PREDEFINED_COINS.keys())

    print("\nAnalyzing multiple coins...\n")

    results = analyze_multiple(coins, days=30, future_days=7)
    ranked = rank_coins(results)

    print("\n=== COIN RANKING ===\n")

    for i, r in enumerate(ranked, start=1):
        print(f"{i}. {r['coin'].upper()}")
        print(f"   Score: {r['avg_score']:.2f}")
        print(f"   Expected Profit: {r['expected_profit']:.2f}%")

        # 🔥 AI explanation
        explanation = explain_coin(r)
        print(f"   AI Insight: {explanation[:200]}...\n")

def main():
    print("=== AI Crypto Signal + Forecast ===\n")

    print("1. Single Coin Analysis")
    print("2. Multi-Coin Ranking")

    choice = input("Select mode: ").strip()

    if choice == "2":
        multi_coin_mode()
        return

    # 🔥 Show available coins
    print("Available Coins:")
    for i, (coin_id, symbol) in enumerate(PREDEFINED_COINS.items(), start=1):
        print(f"{i}. {coin_id} ({symbol})")

    print("\nYou can type coin name (e.g., bitcoin) or number (e.g., 1)\n")

    # 🔥 User input
    user_input = input("Select coin: ").strip().lower()

    # Handle number input
    if user_input.isdigit():
        index = int(user_input) - 1
        coin_list = list(PREDEFINED_COINS.keys())

        if 0 <= index < len(coin_list):
            coin = coin_list[index]
        else:
            print("Invalid selection. Defaulting to bitcoin.")
            coin = "bitcoin"
    else:
        coin = user_input if user_input in PREDEFINED_COINS else "bitcoin"

    # Other inputs
    try:
        days = int(input("Past days: ") or 30)
    except:
        days = 30

    try:
        future_days = int(input("Future days: ") or 7)
    except:
        future_days = 7

    print(f"\nAnalyzing {coin.upper()}...\n")

    historical, future, trade = analyze_with_forecast(
        coin, days, future_days
    )

    print("\n--- FUTURE SIGNALS ---\n")

    for f in future:
        print(f"Day {f['day']}")
        print(f"Price: {f['price']:.2f}")
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