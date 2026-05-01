from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException

from core.data.data_fetch import get_historical_prices
from core.backtest.backtest import Backtester, compute_performance_metrics

router = APIRouter()


class BacktestRequest(BaseModel):
    coin: str
    days: int = 90
    balance: float = 1000


@router.post("/backtest")
def run_backtest(req: BacktestRequest):
    try:
        df = get_historical_prices(req.coin, req.days)

        bt = Backtester(initial_balance=req.balance)
        result = bt.run_backtest(df, req.coin)

        metrics = compute_performance_metrics(result)

        return {
            "history": result.to_dict(orient="records"),
            "metrics": metrics,
            "trades": bt.trades
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Backtest failed: {str(e)}"
        )