from analysis.analyzer import analyze_with_forecast
from analysis.multi_coin import analyze_multiple
from analysis.ranking import rank_coins
from ai import explain_coin
from portfolio.portfolio import allocate_portfolio, apply_risk_management, generate_orders
from data.data_fetch import get_current_prices
from data.data_fetch import fetch_price_data
from portfolio.positions import evaluate_position
from backtest.backtest import Backtester, calculate_metrics

from indicators.indicators import apply_indicators
from signals.signal_engine import generate_signal
from strategy.decision_engine import decide_action
from utils.helpers import clear_screen


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


def single_mode():
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
        coin = user_input
        if coin not in PREDEFINED_COINS:
            print("Unknown coin. Defaulting to bitcoin.")
            coin = "bitcoin"

    # 🔥 Other inputs
    try:
        days = int(input("Past days: ") or 30)
    except:
        days = 30

    try:
        future_days = int(input("Future days: ") or 7)
    except:
        future_days = 7

    print(f"\nAnalyzing {coin.upper()}...\n")

     # 🔥 CURRENT DECISION (AI + STRATEGY)
    print("\n--- CURRENT DECISION ---\n")

    df = fetch_price_data(coin, days)
    df = apply_indicators(df)

    latest_row = df.iloc[-1]

    decision = decide_action(
        coin=coin,
        row=latest_row,
        df=df
    )

    print(f"Current Price: {latest_row['price']:.2f}")
    print(f"Decision: {decision['decision']}")
    print(f"Confidence: {decision['confidence']}")

    print("\nComponents:")
    for k, v in decision["components"].items():
        print(f"  {k}: {v}")

    # 🔥 Core analysis
    historical, future, trade = analyze_with_forecast(
        coin, days, future_days
    )

    # 🔥 Future signals
    print("\n--- FUTURE SIGNALS ---\n")

    for f in future:
        print(f"Day {f['day']}")
        print(f"Price: {f['price']:.2f}")
        print(f"Signal: {f['signal']} (Score: {f['score']})")
        print("-" * 30)

    # 🔥 Best trade
    print("\n--- BEST TRADE ---\n")

    if trade["best_buy"]:
        print(f"Best BUY → Day {trade['best_buy']['day']} @ {trade['best_buy']['price']:.2f}")

    if trade["best_sell"]:
        print(f"Best SELL → Day {trade['best_sell']['day']} @ {trade['best_sell']['price']:.2f}")

    print(f"Expected Profit: {trade['expected_profit_pct']:.2f}%")

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

    print("\n=== POSITION MONITOR ===\n")

    for o in orders:
        coin = o["coin"]
        entry_price = o["price"]

        # 🔥 Use REAL current price (replace mock)
        current_prices = get_current_prices([coin])
        current_price = current_prices.get(coin, entry_price)

        # 🔥 get latest signal (simple version)
        signal = "HOLD"
        for r in ranked:
            if r["coin"] == coin:
                signal = r["final_decision"]

        decision, reason = evaluate_position(
            {
                "coin": coin,
                "entry_price": entry_price,
                "stop_loss": o["stop_loss"],
                "take_profit": o["take_profit"]
            },
            current_price,
            signal  # 👈 NEW
        )

        print(f"{coin.upper()}")
        print(f"  Entry: {entry_price:.2f}")
        print(f"  Current: {current_price:.2f}")
        print(f"  Decision: {decision}")
        print(f"  Reason: {reason}")
        print("-" * 40)

def run_backtest():
    coin = input("Enter coin: ") or "bitcoin"
    days = int(input("Days: ") or 90)

    df = fetch_price_data(coin, days)

    bt = Backtester(initial_balance=1000)
    result = bt.run(df, coin)

    metrics = calculate_metrics(result)

    print("\n=== BACKTEST RESULT ===\n")

    print(f"Final Portfolio Value: ${result['portfolio_value'].iloc[-1]:.2f}")
    print(f"Total Return: {metrics['total_return_pct']:.2f}%")
    print(f"Win Rate: {metrics['win_rate']:.2f}%")
    print(f"Max Drawdown: {metrics['max_drawdown_pct']:.2f}%")

def main():
    clear_screen()  # 🔥 add here
    print("\n=== AI Crypto Trading System ===\n")
    print("1. Single Coin Analysis")
    print("2. Multi Coin Analysis")
    print("3. Backtest Strategy")
    print("0. Exit")

    choice = input("Select: ").strip()

    if choice == "1":
        single_mode()

    elif choice == "2":
        multi_coin_mode()

    elif choice == "3":
        run_backtest()

    elif choice == "0":
        return False  # 🔥 signal to stop loop

    else:
        print("Invalid choice")

    return True  # 🔥 keep running

if __name__ == "__main__":
    while True:
        should_continue = main()

        if not should_continue:
            print("\nGoodbye 👋")
            break

        input("\nPress Enter to continue...")