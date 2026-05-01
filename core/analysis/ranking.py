def rank_coins(results):
    return sorted(
        results,
        key=lambda x: (x["avg_score"], x["expected_profit"]),
        reverse=True
    )