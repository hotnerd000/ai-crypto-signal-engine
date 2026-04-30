def generate_signal(row):
    score = 0
    reasons = []

    # RSI
    if row["rsi"] < 30:
        score += 1
        reasons.append("RSI oversold (BUY)")
    elif row["rsi"] > 70:
        score -= 1
        reasons.append("RSI overbought (SELL)")

    # MA
    if row["price"] > row["ma"]:
        score += 1
        reasons.append("Price above MA (bullish)")
    else:
        score -= 1
        reasons.append("Price below MA (bearish)")

    # 🔥 Strong SELL override
    if row["rsi"] > 75 and row["price"] < row["ma"]:
        return "SELL", -2, ["Strong reversal signal"]

    # Final
    if score >= 1:
        return "BUY", score, reasons
    elif score <= -1:
        return "SELL", score, reasons
    else:
        return "HOLD", score, reasons