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