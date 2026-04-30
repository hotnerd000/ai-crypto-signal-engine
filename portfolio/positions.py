def evaluate_position(position, current_price, signal=None):
    """
    position = {
        coin, entry_price, stop_loss, take_profit
    }
    """

    entry = position["entry_price"]
    sl = position["stop_loss"]
    tp = position["take_profit"]

    change = (current_price - entry) / entry

    # 🔥 1. Stop loss
    if change <= -sl:
        return "SELL", "Stop loss triggered"

    # 🔥 2. Take profit
    if change >= tp:
        return "SELL", "Take profit reached"

    # 🔥 3. Signal-based SELL (NEW)
    if signal == "SELL":
        return "SELL", "Market signal turned bearish"

    return "HOLD", "Position open"