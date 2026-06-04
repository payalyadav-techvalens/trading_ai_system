# def rule_based_signal(latest_price, previous_price, avg_price, latest_volume, avg_volume):
#     """
#     Current signal logic.
#     Later this can be replaced or compared with ML model prediction.
#     """

#     price_change = latest_price - previous_price
#     price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0

#     if latest_price > avg_price and latest_volume > avg_volume:
#         signal = "BUY"
#         reason = "Latest price is above average price and volume is above average volume."

#     elif latest_price < avg_price and latest_volume > avg_volume:
#         signal = "SELL"
#         reason = "Latest price is below average price while volume is above average volume."

#     else:
#         signal = "HOLD"
#         reason = "Price and volume conditions are not strong enough for buy or sell."

#     return {
#         "signal": signal,
#         "reason": reason,
#         "price_change": float(price_change),
#         "price_change_pct": round(float(price_change_pct), 2),
#     }


# def ml_signal_placeholder(features):
#     """
#     Placeholder for future ML model prediction.

#     Later this function can load a trained model and return:
#     BUY / SELL / HOLD with confidence score.
#     """

#     return {
#         "signal": "ML_NOT_IMPLEMENTED",
#         "confidence": 0.0,
#         "reason": "ML model is not added yet. Currently using rule-based signal.",
#     }


import os
import joblib
import pandas as pd


MODEL_PATH = "models/signal_model.pkl"


def rule_based_signal(latest_price, previous_price, avg_price, latest_volume, avg_volume):
    """
    Current fallback signal logic.
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
        "signal_type": "RULE_BASED",
        "confidence": None,
    }


def load_ml_model():
    """
    Load trained ML signal model.
    """

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        model_package = joblib.load(MODEL_PATH)
        return model_package

    except Exception as e:
        print(f"Error loading ML model: {str(e)}")
        return None


def create_features_from_price_data(symbol_df):
    """
    Create latest feature row for ML prediction.

    Features must match training feature columns:
    daily_return, price_range, close_open_diff, price_vs_ma_5, volume_vs_ma_5
    """

    df = symbol_df.copy()

    if "close_price" in df.columns:
        df = df.rename(columns={"close_price": "close"})

    if "open_price" in df.columns:
        df = df.rename(columns={"open_price": "open"})

    required_columns = ["open", "high", "low", "close", "volume"]

    for col in required_columns:
        if col not in df.columns:
            return None, f"Missing column for ML feature generation: {col}"

    df = df.sort_values(by="date")

    df["daily_return"] = df["close"].pct_change()
    df["price_range"] = (df["high"] - df["low"]) / df["close"]
    df["close_open_diff"] = (df["close"] - df["open"]) / df["open"]

    df["ma_5"] = df["close"].rolling(window=5).mean()
    df["volume_ma_5"] = df["volume"].rolling(window=5).mean()

    df["price_vs_ma_5"] = (df["close"] - df["ma_5"]) / df["ma_5"]
    df["volume_vs_ma_5"] = (df["volume"] - df["volume_ma_5"]) / df["volume_ma_5"]

    df = df.dropna()

    if df.empty:
        return None, "Not enough price history to create ML features."

    latest_row = df.iloc[-1]

    features = latest_row[
        [
            "daily_return",
            "price_range",
            "close_open_diff",
            "price_vs_ma_5",
            "volume_vs_ma_5",
        ]
    ]

    return features, None


def ml_signal_prediction(symbol_df):
    """
    Predict BUY / SELL / HOLD using trained ML model.
    """

    model_package = load_ml_model()

    if model_package is None:
        return {
            "signal": "ML_NOT_AVAILABLE",
            "confidence": 0.0,
            "reason": "ML model file is not available. Falling back to rule-based signal.",
            "signal_type": "ML_FALLBACK",
        }

    model = model_package["model"]
    feature_columns = model_package["feature_columns"]

    features, error = create_features_from_price_data(symbol_df)

    if error:
        return {
            "signal": "ML_FEATURE_ERROR",
            "confidence": 0.0,
            "reason": error,
            "signal_type": "ML_FALLBACK",
        }

    input_df = pd.DataFrame([features])
    input_df = input_df[feature_columns]

    prediction = model.predict(input_df)[0]

    confidence = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        confidence = max(probabilities)

    return {
        "signal": prediction,
        "confidence": round(float(confidence), 2) if confidence is not None else None,
        "reason": "Signal generated using trained ML model.",
        "signal_type": "ML_MODEL",
    }