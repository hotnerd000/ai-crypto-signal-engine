import pandas as pd
from indicators.indicators import apply_indicators
from signals.signal_engine import generate_signal


class Backtester:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.positions = {}  # coin → {entry_price, quantity}
        self.history = []

    def run(self, df, coin):
        df = apply_indicators(df)

        for _, row in df.iterrows():
            price = float(row["price"])
            date = row["timestamp"]

            signal, score, _ = generate_signal(row)

            # 🔥 BUY logic
            if signal == "BUY" and coin not in self.positions:
                allocation = self.balance * 0.2  # 20% per trade
                quantity = allocation / price

                self.positions[coin] = {
                    "entry_price": price,
                    "quantity": quantity
                }

                self.balance -= allocation

            # 🔥 SELL logic
            elif signal == "SELL" and coin in self.positions:
                position = self.positions[coin]
                value = position["quantity"] * price

                self.balance += value
                del self.positions[coin]

            # 🔥 Track portfolio value
            portfolio_value = self.balance

            for c, pos in self.positions.items():
                portfolio_value += pos["quantity"] * price

            self.history.append({
                "date": date,
                "price": price,
                "signal": signal,
                "balance": self.balance,
                "portfolio_value": portfolio_value
            })

        return pd.DataFrame(self.history)
    
def calculate_metrics(df):
    returns = df["portfolio_value"].pct_change().dropna()

    total_return = (df["portfolio_value"].iloc[-1] / df["portfolio_value"].iloc[0]) - 1
    win_rate = (returns > 0).mean()

    # max drawdown
    cumulative = df["portfolio_value"]
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_dd = drawdown.min()

    return {
        "total_return_pct": total_return * 100,
        "win_rate": win_rate * 100,
        "max_drawdown_pct": max_dd * 100
    }