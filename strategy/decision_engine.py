from signals.signal_engine import generate_signal
from ai.ai_decisions import get_ai_decision
from forecasting.forecast import analyze_with_forecast

def combine_decision(rule_score, ai_decision, ai_confidence):
    # Normalize rule score
    if rule_score >= 1:
        rule = "BUY"
    elif rule_score <= -1:
        rule = "SELL"
    else:
        rule = "HOLD"

    # 🔥 Weighted decision logic
    if ai_confidence > 0.7:
        return ai_decision

    if ai_confidence > 0.4:
        # AI influences but doesn't dominate
        if rule == ai_decision:
            return rule
        else:
            return "HOLD"

    # Low confidence → trust rules
    return rule

def decide_action(coin, row, df, future_days=7):
    """
    Unified decision engine combining:
    - Technical signals
    - AI decision
    - Forecast trend
    """

    reasons = []

    # 🔥 1. Technical signal
    signal, score, signal_reasons = generate_signal(row)
    reasons.extend(signal_reasons)

    # 🔥 2. AI decision
    ai_result = get_ai_decision(row)
    ai_decision = ai_result.get("decision", "HOLD")
    ai_confidence = ai_result.get("confidence", 0.5)

    # 🔥 3. Forecast trend
    try:
        _, future, _ = analyze_with_forecast(coin, len(df), future_days)

        future_prices = [f["price"] for f in future]

        if future_prices[-1] > future_prices[0]:
            forecast_trend = "UP"
        else:
            forecast_trend = "DOWN"

    except Exception:
        forecast_trend = "UNKNOWN"

    # 🧠 Combine logic (weighted decision)

    score_total = 0

    # Technical signal weight
    if signal == "BUY":
        score_total += 1
    elif signal == "SELL":
        score_total -= 1

    # AI weight
    if ai_decision == "BUY":
        score_total += ai_confidence
    elif ai_decision == "SELL":
        score_total -= ai_confidence

    # Forecast weight
    if forecast_trend == "UP":
        score_total += 0.5
    elif forecast_trend == "DOWN":
        score_total -= 0.5

    # 🎯 Final decision
    if score_total > 0.5:
        final_decision = "BUY"
    elif score_total < -0.5:
        final_decision = "SELL"
    else:
        final_decision = "HOLD"

    return {
        "decision": final_decision,
        "confidence": round(min(abs(score_total) / 2, 1), 2),
        "reasons": reasons,
        "components": {
            "signal": signal,
            "ai": ai_decision,
            "forecast": forecast_trend
        }
    }