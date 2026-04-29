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

    # Moving Average
    if row["price"] > row["ma"]:
        score += 1
        reasons.append("Price above MA (bullish)")
    else:
        score -= 1
        reasons.append("Price below MA (bearish)")

    # Final decision
    if score >= 1:
        signal = "BUY"
    elif score <= -1:
        signal = "SELL"
    else:
        signal = "HOLD"

    return signal, score, reasons