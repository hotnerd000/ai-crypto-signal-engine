# core/bot/auto_trader.py

import time
from datetime import datetime
from core.data.data_adapter import fetch_price_data
import asyncio
from backend.ws_manager import manager, send_ws_message

class AutoTraderBot:
    def __init__(self, config, portfolio, execution_engine, strategy_engine):
        self.config = config
        self.portfolio = portfolio
        self.execution = execution_engine
        self.strategy = strategy_engine

        self.running = False

    def start(self):
        self.running = True
        self.run_loop()

    def stop(self):
        self.running = False

    def run_loop(self):
        coin_A, coin_B = self.config.coin_pair

        while self.running:
            try:
                # 1. Fetch data
                df_A = fetch_price_data(coin_A)
                df_B = fetch_price_data(coin_B)

                # 2. Analyze
                decision_A = self.strategy.analyze(coin_A, df_A)
                decision_B = self.strategy.analyze(coin_B, df_B)

                # 3. Decide switching
                self._handle_switch(
                    coin_A, coin_B,
                    decision_A, decision_B,
                    df_A, df_B
                )

                # 4. Log
                prices = {
                    coin_A: df_A.iloc[-1]["price"],
                    coin_B: df_B.iloc[-1]["price"]
                }

                value = self.portfolio.get_value(prices)

                send_ws_message({
                    "type": "portfolio_update",
                    "value": value,
                    "asset": self.portfolio.current_asset,
                    "timestamp": str(datetime.now())
                })
                self.portfolio.log_state(datetime.now(), value)

                print(f"[BOT] Value: {value:.2f}, Asset: {self.portfolio.current_asset}")

                time.sleep(self.config.trade_cooldown)

            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(5)

    def _handle_switch(self, coin_A, coin_B, dA, dB, df_A, df_B):

        # Confidence filter
        if dA.get("confidence", 1) < self.config.min_confidence:
            return
        if dB.get("confidence", 1) < self.config.min_confidence:
            return

        price_A = df_A.iloc[-1]["price"]
        price_B = df_B.iloc[-1]["price"]

        current = self.portfolio.current_asset

        # Switch logic
        if dA["action"] == "BUY" and current != coin_A:
            self.execution.execute_trade(
                self.portfolio,
                current,
                coin_A,
                price_A
            )

        elif dB["action"] == "BUY" and current != coin_B:
            self.execution.execute_trade(
                self.portfolio,
                current,
                coin_B,
                price_B
            )