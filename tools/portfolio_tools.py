import pandas as pd


POSITIONS_FILE = "data\\positions.csv"


def load_positions():
    """
    Load position data from CSV.
    """
    df = pd.read_csv(POSITIONS_FILE)

    df["market_value"] = df["quantity"] * df["current_price"]
    df["cost_value"] = df["quantity"] * df["avg_price"]
    df["pnl"] = df["market_value"] - df["cost_value"]

    return df


def get_positions(date: str):
    """
    Return all positions for a given date.
    """
    df = load_positions()
    result = df[df["date"] == date]

    if result.empty:
        return f"No positions found for date {date}"

    return result.to_dict(orient="records")


def get_position_by_symbol(symbol: str, date: str):
    """
    Return position details for one symbol.
    """
    df = load_positions()

    result = df[
        (df["symbol"].str.upper() == symbol.upper())
        & (df["date"] == date)
    ]

    if result.empty:
        return f"No position found for symbol {symbol} on {date}"

    return result.to_dict(orient="records")


def get_top_pnl(date: str, limit: int = 5):
    """
    Return top profit-making positions.
    """
    df = load_positions()
    result = df[df["date"] == date]

    if result.empty:
        return f"No positions found for date {date}"

    result = result.sort_values(by="pnl", ascending=False).head(limit)

    return result[["symbol", "fund", "quantity", "market_value", "pnl"]].to_dict(
        orient="records"
    )


def get_top_loss(date: str, limit: int = 5):
    """
    Return top loss-making positions.
    """
    df = load_positions()
    result = df[df["date"] == date]

    if result.empty:
        return f"No positions found for date {date}"

    result = result.sort_values(by="pnl", ascending=True).head(limit)

    return result[["symbol", "fund", "quantity", "market_value", "pnl"]].to_dict(
        orient="records"
    )


def calculate_gross_exposure(date: str):
    """
    Gross exposure = sum of absolute market values.
    """
    df = load_positions()
    result = df[df["date"] == date]

    if result.empty:
        return f"No positions found for date {date}"

    gross_exposure = result["market_value"].abs().sum()

    return {
        "date": date,
        "gross_exposure": float(gross_exposure),
    }


def calculate_net_exposure(date: str):
    """
    Net exposure = sum of market values.
    """
    df = load_positions()
    result = df[df["date"] == date]

    if result.empty:
        return f"No positions found for date {date}"

    net_exposure = result["market_value"].sum()

    return {
        "date": date,
        "net_exposure": float(net_exposure),
    }


def get_portfolio_summary(date: str):
    """
    Return portfolio level summary.
    """
    df = load_positions()
    result = df[df["date"] == date]

    if result.empty:
        return f"No positions found for date {date}"

    total_market_value = result["market_value"].sum()
    total_cost_value = result["cost_value"].sum()
    total_pnl = result["pnl"].sum()
    total_positions = len(result)

    return {
        "date": date,
        "total_positions": int(total_positions),
        "total_market_value": float(total_market_value),
        "total_cost_value": float(total_cost_value),
        "total_pnl": float(total_pnl),
    }