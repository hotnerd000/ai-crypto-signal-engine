from backend.ws_manager import send_ws_message
from datetime import datetime

class ExecutionEngine:
    def __init__(self, fee=0.001):
        self.fee = fee

    def execute_trade(self, bot_portfolio, from_asset, to_asset, price):
        amount = bot_portfolio.balances.get(from_asset, 0)

        if amount == 0:
            return False

        fee = self.fee
        net_amount = amount * (1 - fee)

        converted = net_amount / price

        # ✅ update balances
        bot_portfolio.balances[from_asset] = 0
        bot_portfolio.balances[to_asset] = converted
        bot_portfolio.current_asset = to_asset

        # ✅ 🔥 PUT IT RIGHT HERE
        send_ws_message({
            "type": "trade",
            "from": from_asset,
            "to": to_asset,
            "price": price,
            "timestamp": str(datetime.now())
        })


        return True