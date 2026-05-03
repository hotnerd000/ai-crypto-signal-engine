# core/bot/execution_engine.py

class ExecutionEngine:
    def __init__(self, fee=0.001):
        self.fee = fee

    def execute_trade(self, bot_portfolio, from_asset, to_asset, price):
        amount = bot_portfolio.balances.get(from_asset, 0)

        if amount == 0:
            return False

        # Apply fee
        net_amount = amount * (1 - self.fee)

        # Convert
        converted = net_amount / price

        bot_portfolio.balances[from_asset] = 0
        bot_portfolio.balances[to_asset] = converted
        bot_portfolio.current_asset = to_asset

        return True