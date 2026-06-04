import pandas as pd


PRICES_FILE = "data/prices.csv"


def load_prices():
    """
    Load historical price data.
    """

    df = pd.read_csv(PRICES_FILE)
    df["date"] = pd.to_datetime(df["date"])
    return df


def generate_signal(symbol: str):
    """
    Generate a simple rule-based trading signal.

    Later this function can be replaced with ML model prediction.
    """

    df = load_prices()

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