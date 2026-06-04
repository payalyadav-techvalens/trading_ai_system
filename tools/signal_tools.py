import pandas as pd
from services.signal_service import rule_based_signal
from services.market_data_service import fetch_market_data

PRICES_FILE = "data/prices.csv"


# def load_prices():
#     """
#     Load historical price data.
#     """

#     df = pd.read_csv(PRICES_FILE)
#     df["date"] = pd.to_datetime(df["date"])
#     return df

def load_prices(symbol: str):
    """
    Load price data.

    First try live yfinance data.
    If live data fails, fallback to prices.csv.
    """

    if symbol:
        live_df = fetch_market_data(symbol=symbol)

        if not live_df.empty:
            live_df["date"] = pd.to_datetime(live_df["date"])
            return live_df

    df = pd.read_csv(PRICES_FILE)
    df["date"] = pd.to_datetime(df["date"])
    return df


def generate_signal(symbol: str):
    """
    Generate a simple rule-based trading signal.

    Later this function can be replaced with ML model prediction.
    """

    df = load_prices(symbol)

    symbol_df = df[df["symbol"].str.upper() == symbol.upper()].copy()

    if symbol_df.empty:
        return {
            "symbol": symbol.upper(),
            "signal": "NO_DATA",
            "reason": f"No price data found for {symbol}",
        }

    symbol_df = symbol_df.sort_values(by="date")

    latest_row = symbol_df.iloc[-1]
    previous_row = symbol_df.iloc[-2] if len(symbol_df) > 1 else latest_row

    avg_price = symbol_df["close_price"].mean()
    avg_volume = symbol_df["volume"].mean()

    latest_price = latest_row["close_price"]
    latest_volume = latest_row["volume"]
    previous_price = previous_row["close_price"]

    price_change = latest_price - previous_price
    price_change_pct = (price_change / previous_price) * 100 if previous_price != 0 else 0

    signal_output = rule_based_signal(
        latest_price=latest_price,
        previous_price=previous_price,
        avg_price=avg_price,
        latest_volume=latest_volume,
        avg_volume=avg_volume,
    )

    signal = signal_output["signal"]
    reason = signal_output["reason"]
    price_change = signal_output["price_change"]
    price_change_pct = signal_output["price_change_pct"]

    return {
    "symbol": symbol.upper(),
    "latest_date": latest_row["date"].strftime("%Y-%m-%d"),
    "latest_price": float(latest_price),
    "previous_price": float(previous_price),
    "price_change": float(price_change),
    "price_change_pct": round(float(price_change_pct), 2),
    "average_price": round(float(avg_price), 2),
    "latest_volume": int(latest_volume),
    "average_volume": round(float(avg_volume), 2),
    "signal": signal,
    "reason": reason,
    "signal_type": "RULE_BASED",
    }


def get_signal_explanation(symbol: str):
    """
    Return signal with explanation.
    """

    signal_data = generate_signal(symbol)

    return {
        "symbol": symbol.upper(),
        "signal_data": signal_data,
        "note": "This is a rule-based signal. In future, this can be replaced with an ML model.",
    }