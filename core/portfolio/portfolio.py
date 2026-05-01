# portfolio.py

def allocate_portfolio(results, total_balance=1000, max_per_coin=0.3):
    candidates = [r for r in results if r["final_decision"] == "BUY"]

    if not candidates:
        return []

    for r in candidates:
        base_score = (
            r["avg_score"] * 0.4 +
            r["expected_profit"] * 0.4 +
            r["ai_confidence"] * 0.2
        )

        vol = r.get("volatility", 0.01)

        if vol == 0:
            vol = 0.01

        r["weight_score"] = base_score / vol

    # 🔄 normalize
    total_weight = sum(r["weight_score"] for r in candidates)

    for r in candidates:
        r["allocation_pct"] = r["weight_score"] / total_weight

    # 🔄 cap per coin
    for r in candidates:
        r["allocation_pct"] = min(r["allocation_pct"], max_per_coin)

    total_pct = sum(r["allocation_pct"] for r in candidates)

    for r in candidates:
        r["allocation_pct"] /= total_pct

    # 🔄 USD allocation
    for r in candidates:
        r["allocation_usd"] = r["allocation_pct"] * total_balance

    return candidates


# 🔥 ADD THIS RIGHT BELOW
def apply_risk_management(portfolio, stop_loss=0.05):
    for p in portfolio:
        vol = p.get("volatility", 0.02)

        # 🔥 dynamic stop loss based on volatility
        p["stop_loss_pct"] = max(0.03, min(0.15, vol * 3))

        # take profit stays based on expected return
        p["take_profit_pct"] = p["expected_profit"] / 100

    return portfolio


def generate_orders(portfolio, prices):
    orders = []

    for p in portfolio:
        coin = p["coin"]
        usd = p["allocation_usd"]
        price = prices.get(coin, 1)

        quantity = usd / price

        orders.append({
            "coin": coin,
            "action": "BUY",
            "usd": usd,
            "price": price,
            "quantity": quantity,
            "stop_loss": p["stop_loss_pct"],
            "take_profit": p["take_profit_pct"]
        })

    return orders