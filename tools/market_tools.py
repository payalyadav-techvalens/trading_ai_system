import pandas as pd
from services.market_data_service import fetch_market_data


PRICES_FILE = "data/prices.csv"


# def load_market_prices():
#     """
#     Load market price data.
#     Later this can be replaced with live API data.
#     """

#     df = pd.read_csv(PRICES_FILE)
#     df["date"] = pd.to_datetime(df["date"])
#     return df

def load_market_prices(symbol: str):
    """
    Load market price data.

    First try live yfinance data.
    If live data fails, fallback to local prices.csv.
    """

    if symbol:
        live_df = fetch_market_data(symbol=symbol)

        if not live_df.empty:
            live_df["date"] = pd.to_datetime(live_df["date"])
            return live_df

    df = pd.read_csv(PRICES_FILE)
    df["date"] = pd.to_datetime(df["date"])
    return df


def get_latest_price(symbol: str):
    """
    Return latest price and volume for a symbol.
    """

    df = load_market_prices(symbol)

    symbol_df = df[df["symbol"].str.upper() == symbol.upper()].copy()

    if symbol_df.empty:
        return {
            "symbol": symbol.upper(),
            "message": f"No market price data found for {symbol}",
        }

    symbol_df = symbol_df.sort_values(by="date")
    latest_row = symbol_df.iloc[-1]

    return {
        "symbol": symbol.upper(),
        "latest_date": latest_row["date"].strftime("%Y-%m-%d"),
        "close_price": float(latest_row["close_price"]),
        "volume": int(latest_row["volume"]),
    }


def get_price_trend(symbol: str):
    """
    Return price trend summary for a symbol.
    """

    df = load_market_prices(symbol)

    symbol_df = df[df["symbol"].str.upper() == symbol.upper()].copy()

    if symbol_df.empty:
        return {
            "symbol": symbol.upper(),
            "message": f"No market price data found for {symbol}",
        }

    symbol_df = symbol_df.sort_values(by="date")

    first_row = symbol_df.iloc[0]
    latest_row = symbol_df.iloc[-1]

    start_price = first_row["close_price"]
    latest_price = latest_row["close_price"]

    price_change = latest_price - start_price
    price_change_pct = (price_change / start_price) * 100 if start_price != 0 else 0

    if price_change > 0:
        trend = "UPTREND"
    elif price_change < 0:
        trend = "DOWNTREND"
    else:
        trend = "SIDEWAYS"

    return {
        "symbol": symbol.upper(),
        "start_date": first_row["date"].strftime("%Y-%m-%d"),
        "latest_date": latest_row["date"].strftime("%Y-%m-%d"),
        "start_price": float(start_price),
        "latest_price": float(latest_price),
        "price_change": float(price_change),
        "price_change_pct": round(float(price_change_pct), 2),
        "trend": trend,
    }


def get_volume_trend(symbol: str):
    """
    Return latest volume compared with average volume.
    """

    df = load_market_prices(symbol)

    symbol_df = df[df["symbol"].str.upper() == symbol.upper()].copy()

    if symbol_df.empty:
        return {
            "symbol": symbol.upper(),
            "message": f"No market price data found for {symbol}",
        }

    symbol_df = symbol_df.sort_values(by="date")

    latest_row = symbol_df.iloc[-1]
    avg_volume = symbol_df["volume"].mean()

    latest_volume = latest_row["volume"]

    if latest_volume > avg_volume:
        volume_status = "ABOVE_AVERAGE"
    elif latest_volume < avg_volume:
        volume_status = "BELOW_AVERAGE"
    else:
        volume_status = "AVERAGE"

    return {
        "symbol": symbol.upper(),
        "latest_date": latest_row["date"].strftime("%Y-%m-%d"),
        "latest_volume": int(latest_volume),
        "average_volume": round(float(avg_volume), 2),
        "volume_status": volume_status,
    }


def get_market_summary(symbol: str):
    """
    Return combined market summary for a symbol.
    """

    return {
        "latest_price": get_latest_price(symbol),
        "price_trend": get_price_trend(symbol),
        "volume_trend": get_volume_trend(symbol),
    }