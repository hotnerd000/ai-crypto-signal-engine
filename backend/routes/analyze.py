from fastapi import APIRouter
from pydantic import BaseModel

from core.analysis.market_analysis import run_market_analysis
from core.data.data_fetch import get_historical_prices
from core.indicators.indicators import compute_indicators
from core.strategy.trade_decision import generate_trade_decision

router = APIRouter()


class AnalyzeRequest(BaseModel):
    coin: str
    days: int = 30
    future_days: int = 7


@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    coin = req.coin
    days = req.days
    future_days = req.future_days

    # 🔥 Current decision
    df = get_historical_prices(coin, days)
    df = compute_indicators(df)

    latest = df.iloc[-1]

    decision = generate_trade_decision(coin, latest, df)

    # 🔥 Forecast
    historical, future, trade = run_market_analysis(
        coin, days, future_days
    )

    return {
        "coin": coin,
        "decision": decision,
        "future": future,
        "trade": trade,
        "history": df.to_dict(orient="records") 
    }