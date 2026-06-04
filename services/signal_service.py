def rule_based_signal(latest_price, previous_price, avg_price, latest_volume, avg_volume):
    """
    Current signal logic.
    Later this can be replaced or compared with ML model prediction.
    """

    price_change = latest_price - previous_price
    price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0

    if latest_price > avg_price and latest_volume > avg_volume:
        signal = "BUY"
        reason = "Latest price is above average price and volume is above average volume."

    elif latest_price < avg_price and latest_volume > avg_volume:
        signal = "SELL"
        reason = "Latest price is below average price while volume is above average volume."

    else:
        signal = "HOLD"
        reason = "Price and volume conditions are not strong enough for buy or sell."

    return {
        "signal": signal,
        "reason": reason,
        "price_change": float(price_change),
        "price_change_pct": round(float(price_change_pct), 2),
    }


def ml_signal_placeholder(features):
    """
    Placeholder for future ML model prediction.

    Later this function can load a trained model and return:
    BUY / SELL / HOLD with confidence score.
    """

    return {
        "signal": "ML_NOT_IMPLEMENTED",
        "confidence": 0.0,
        "reason": "ML model is not added yet. Currently using rule-based signal.",
    }