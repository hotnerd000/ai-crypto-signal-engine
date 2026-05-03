# core/bot/portfolio.py

class BotPortfolio:
    def __init__(self, initial_balance):
        self.balances = {
            "USDT": initial_balance
        }
        self.current_asset = "USDT"
        self.history = []

    def get_value(self, prices):
        total = 0
        for asset, amount in self.balances.items():
            if asset == "USDT":
                total += amount
            else:
                total += amount * prices.get(asset, 0)
        return total

    def update_balance(self, asset, amount):
        self.balances[asset] = amount

    def log_state(self, timestamp, value):
        self.history.append({
            "time": timestamp,
            "value": value,
            "asset": self.current_asset
        })