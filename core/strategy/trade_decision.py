from core.signals.rule_signals import generate_rule_signal
from core.ai.ai_decisions import get_ai_signal
from core.forecasting.price_forecast import forecast_prices


def generate_trade_decision(coin, row, df, future_days=7):
    """
    Generate final trade decision using:
    - Rule-based signals
    - AI signal

    Returns:
        {
            decision: BUY / SELL / HOLD
            confidence: 0-1
            components: {...}
            reasons: [...]
        }
    """
    reasons = []

    print(f"\nGenerate Signals----\n")
    # 🔥 1. Rule-based signal
    signal, score, signal_reasons = generate_rule_signal(row)
    reasons.extend(signal_reasons)

    print(f"\nAI Signaling...----\n")
    # 🔥 2. AI signal
    ai_result = get_ai_signal(coin, row)
    ai_decision = ai_result.get("decision", "HOLD")
    ai_confidence = ai_result.get("confidence", 0.5)

    future = forecast_prices(df, future_days)
    
    future_score = sum(f["score"] for f in future)

    print(f"\nAI Signaling Finished...----\n")
    # 🔥 3. Combine logic (weighted)
    score_total = 0

    # Rule signal weight
    if signal == "BUY":
        score_total += 1
    elif signal == "SELL":
        score_total -= 1

    # AI weight (scaled by confidence)
    if ai_decision == "BUY":
        score_total += ai_confidence
    elif ai_decision == "SELL":
        score_total -= ai_confidence

    # 🔹 Consider future score
    score_total += future_score * 0.1

    # 🔥 4. Final decision thresholds
    if score_total > 0.5:
        final_decision = "BUY"
    elif score_total < -0.5:
        final_decision = "SELL"
    else:
        final_decision = "HOLD"

    # 🔥 5. Confidence calculation
    confidence = round(min(abs(score_total) / 2, 1), 2)

    return {
        "decision": final_decision,
        "confidence": confidence,
        "reasons": reasons,
        "future_bias": future_score,
        "components": {
            "rule_signal": signal,
            "ai_signal": ai_decision,
            "ai_confidence": round(ai_confidence, 2)
        }
    }