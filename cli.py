from analyzer import analyze_with_forecast
from multi_coin import analyze_multiple
from ranking import rank_coins
from ai_explainer import explain_coin
from portfolio import allocate_portfolio, apply_risk_management, generate_orders
from data_fetch import get_current_prices

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
        print(f"   Rule Score: {r['avg_score']:.2f}")
        print(f"   Expected Profit: {r['expected_profit']:.2f}%")
        print(f"   Final Decision: {r['final_decision']}")
        print(f"   AI Confidence: {r['ai_confidence']:.2f}")
        print("-" * 40)

    print("\n=== PORTFOLIO ALLOCATION ===\n")

    portfolio = allocate_portfolio(ranked, total_balance=1000)
    portfolio = apply_risk_management(portfolio)

    coins = [p["coin"] for p in portfolio]
    prices = get_current_prices(coins)

    orders = generate_orders(portfolio, prices)

    if not portfolio:
        print("No BUY signals. No trades executed.")
        return

    # 🔥 Show portfolio
    for p in portfolio:
        print(f"{p['coin'].upper()}")
        print(f"  Allocation: {p['allocation_pct']*100:.2f}%")
        print(f"  USD: ${p['allocation_usd']:.2f}")
        print(f"  Stop Loss: {p['stop_loss_pct']*100:.1f}%")
        print(f"  Take Profit: {p['take_profit_pct']:.1f}%")
        print("-" * 40)

    # 🔥 Show orders (optional but very useful)
    print("\n=== EXECUTION PLAN ===\n")

    for o in orders:
        print(f"BUY {o['coin'].upper()}")
        print(f"  Amount: ${o['usd']:.2f}")
        print(f"  Quantity: {o['quantity']:.6f}")
        print(f"  Stop Loss: {o['stop_loss']*100:.1f}%")
        print(f"  Take Profit: {o['take_profit']*100:.1f}%")
        print("-" * 40)

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