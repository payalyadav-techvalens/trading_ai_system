import yfinance as yf
import pandas as pd


def normalize_symbol(symbol: str):
    """
    Convert local symbols into Yahoo Finance format.

    For Indian NSE stocks:
    TCS -> TCS.NS
    INFY -> INFY.NS
    HDFCBANK -> HDFCBANK.NS
    """

    symbol = symbol.upper().strip()

    yahoo_symbol_map = {
        "TCS": "TCS.NS",
        "INFY": "INFY.NS",
        "HDFCBANK": "HDFCBANK.NS",
        "RELIANCE": "RELIANCE.NS",
        "SBIN": "SBIN.NS",
        "WIPRO": "WIPRO.NS",
        "LT": "LT.NS",
    }

    return yahoo_symbol_map.get(symbol, symbol)


def fetch_market_data(symbol: str, period: str = "7d", interval: str = "1d"):
    """
    Fetch market data from Yahoo Finance using yfinance.
    """

    yahoo_symbol = normalize_symbol(symbol)

    try:
        ticker = yf.Ticker(yahoo_symbol)
        df = ticker.history(period=period, interval=interval)

        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()

        df["symbol"] = symbol.upper()
        df = df.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close_price",
                "Volume": "volume",
            }
        )

        return df[["date", "symbol", "open", "high", "low", "close_price", "volume"]]

    except Exception as e:
        print(f"Error while fetching market data for {symbol}: {str(e)}")
        return pd.DataFrame()