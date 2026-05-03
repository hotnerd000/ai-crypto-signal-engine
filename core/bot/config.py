# core/bot/config.py

class TradeConfig:
    def __init__(
        self,
        coin_pair,
        initial_balance=1000,
        risk_per_trade=0.1,
        min_confidence=0.6,
        trade_cooldown=60,
        stop_loss_pct=0.03,
        take_profit_pct=0.05,
        use_ai=True,
        use_forecast=True,
    ):
        self.coin_pair = coin_pair
        self.initial_balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.min_confidence = min_confidence
        self.trade_cooldown = trade_cooldown
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.use_ai = use_ai
        self.use_forecast = use_forecast