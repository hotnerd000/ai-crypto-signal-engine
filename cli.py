from analyzer import analyze_coin


def main():
    print("=== AI Crypto Signal Analyzer ===\n")

    # 🔥 Ask user input instead of argparse
    coin = input("Enter coin (e.g., bitcoin, ethereum, solana): ").strip().lower()
    days_input = input("Enter number of past days (e.g., 30): ").strip()

    # Default fallback
    if not coin:
        coin = "bitcoin"

    try:
        days = int(days_input)
    except:
        days = 30

    print(f"\nAnalyzing {coin.upper()} for last {days} days...\n")

    results = analyze_coin(coin, days)

    for r in results[-5:]:  # last 5 days
        print(f"Date: {r['date']}")
        print(f"Price: {r['price']:.2f}")
        print(f"RSI: {r['rsi']:.2f}")
        print(f"MA: {r['ma']:.2f}")
        print(f"Signal: {r['signal']} (Score: {r['score']})")
        print(f"Reasons: {', '.join(r['reasons'])}")
        print("-" * 40)


if __name__ == "__main__":
    main()