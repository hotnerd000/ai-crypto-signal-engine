# backend/routes/bot.py

from fastapi import APIRouter

from core.bot.config import TradeConfig
from core.bot.bot_portfolio import BotPortfolio
from core.bot.execution_engine import ExecutionEngine
from core.bot.strategy_engine import StrategyEngine
from core.bot.auto_trader import AutoTraderBot

router = APIRouter()

# Global bot instance (simple version)
bot_instance = None


@router.post("/bot/start")
def start_bot():
    global bot_instance

    config = TradeConfig(
        coin_pair=["bitcoin", "ethereum"]
    )
    print("TradeCONfig----")
    
    portfolio = BotPortfolio(config.initial_balance)
    execution = ExecutionEngine()
    strategy = StrategyEngine(config)
    print("Strategy Engine----")

    bot_instance = AutoTraderBot(
        config, portfolio, execution, strategy
    )
    print("Before Threading----")

    # Run in background (important!)
    import threading
    thread = threading.Thread(target=bot_instance.start)
    thread.start()

    return {"status": "bot started"}


@router.post("/bot/stop")
def stop_bot():
    global bot_instance

    if bot_instance:
        bot_instance.stop()
        return {"status": "bot stopped"}

    return {"status": "no bot running"}


@router.get("/bot/status")
def bot_status():
    if bot_instance and bot_instance.running:
        return {"status": "running"}
    return {"status": "stopped"}