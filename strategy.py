def find_best_trade(future_data, fee=0.005):
    best_buy = None
    best_sell = None

    min_price = float("inf")
    max_profit = 0

    for i, day in enumerate(future_data):
        price = day["price"]

        # find best buy point
        if day["signal"] == "BUY" and price < min_price:
            min_price = price
            best_buy = day

        # find best sell AFTER buy
        if best_buy:
            profit = (price - min_price) / min_price - fee

            if profit > max_profit:
                max_profit = profit
                best_sell = day

    return {
        "best_buy": best_buy,
        "best_sell": best_sell,
        "expected_profit_pct": max_profit * 100
    }