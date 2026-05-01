import pandas as pd
from core.indicators.indicators import compute_indicators
from core.strategy.trade_decision import generate_trade_decision

class Backtester:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.positions = {}  # coin → {entry_price, quantity}
        self.history = []
        self.trades = []

    def run_backtest(self, df, coin):
        df = compute_indicators(df)

        for i, row in df.iterrows():
            price = float(row["price"])
            date = row["timestamp"]

            # 🔥 ONLY past data (no leakage)
            past_df = df.iloc[:i+1]

            decision = generate_trade_decision(
                coin,
                row,
                past_df
            )
            signal = decision["decision"]
            confidence = decision["confidence"]

            # 🔥 BUY logic
            if signal == "BUY" and coin not in self.positions:
                allocation = self.balance * (0.1 + 0.4 * confidence)
                quantity = allocation / price

                self.positions[coin] = {
                    "entry_price": price,
                    "quantity": quantity
                }

                self.balance -= allocation

                self.trades.append({
                    "type": "BUY",
                    "price": price,
                    "date": date,
                    "confidence": confidence
                })

            # 🔥 SELL logic
            elif signal == "SELL" and coin in self.positions:
                position = self.positions[coin]
                entry_price = position["entry_price"]

                pnl_pct = (price - entry_price) / entry_price

                # 🔥 Optional filter (avoid bad sells)
                if pnl_pct > -0.05:  # don’t panic sell too early
                    value = position["quantity"] * price

                    self.balance += value
                    del self.positions[coin]

                    self.trades.append({
                        "type": "SELL",
                        "price": price,
                        "date": date,
                        "pnl_pct": pnl_pct
                    })

            # 🔥 Track portfolio value
            portfolio_value = self.balance
            for pos in self.positions.values():
                portfolio_value += pos["quantity"] * price
            
            self.history.append({
                "date": date,
                "price": price,
                "signal": signal,
                "balance": self.balance,
                "portfolio_value": portfolio_value
            })

        return pd.DataFrame(self.history)
    
def compute_performance_metrics(df):
    print('DF---', df)
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