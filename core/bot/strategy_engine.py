# core/bot/strategy_engine.py

from core.strategy.trade_decision import generate_trade_decision
from core.indicators.indicators import compute_indicators
from core.forecasting.price_forecast import forecast_prices


class StrategyEngine:
    def __init__(self, config):
        self.config = config

    def analyze(self, coin, df):
        df = compute_indicators(df)

        forecast = None
        if self.config.use_forecast:
            forecast = forecast_prices(df)

        decision = generate_trade_decision(
            coin=coin,
            row=df.iloc[-1],
            df=df,
            future_days=7
        )

        return decision