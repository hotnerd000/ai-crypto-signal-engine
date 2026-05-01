from fastapi import APIRouter
from pydantic import BaseModel

from core.data.data_fetch import get_historical_prices
from core.indicators.indicators import compute_indicators
from core.strategy.trade_decision import generate_trade_decision

router = APIRouter()


class PortfolioRequest(BaseModel):
    coins: list[str]
    days: int = 30


@router.post("/portfolio")
def analyze_multiple_coins(req: PortfolioRequest):
    results = []

    for coin in req.coins:
        try:
            # 🔥 Fetch + indicators
            df = get_historical_prices(coin, req.days)
            df = compute_indicators(df)

            latest = df.iloc[-1]

            # 🔥 Decision engine
            decision = generate_trade_decision(coin, latest, df)

            # 🔥 Score for ranking
            score = compute_score(decision)

            results.append({
                "coin": coin,
                "price": float(latest["price"]),
                "decision": decision["decision"],
                "confidence": decision["confidence"],
                "score": score
            })

        except Exception as e:
            results.append({
                "coin": coin,
                "error": str(e)
            })

    # 🔥 Sort by best opportunities
    ranked = sorted(
        results,
        key=lambda x: x.get("score", -999),
        reverse=True
    )

    return {
        "results": ranked
    }


# 🔥 Simple scoring logic
def compute_score(decision):
    score = 0

    if decision["decision"] == "BUY":
        score += 1
    elif decision["decision"] == "SELL":
        score -= 1

    score += decision["confidence"]

    return round(score, 3)