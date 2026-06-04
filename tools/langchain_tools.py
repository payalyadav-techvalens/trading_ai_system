from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from tools.portfolio_tools import (
    get_positions,
    get_position_by_symbol,
    get_top_pnl,
    get_top_loss,
    calculate_gross_exposure,
    calculate_net_exposure,
    get_portfolio_summary,
    calculate_symbol_concentration,
    generate_risk_alerts,
)

from tools.market_tools import (
    get_latest_price,
    get_price_trend,
    get_volume_trend,
    get_market_summary,
)

from tools.signal_tools import (
    generate_signal,
    get_signal_explanation,
)


class DateInput(BaseModel):
    date: str = Field(description="Trading date in YYYY-MM-DD format")


class SymbolInput(BaseModel):
    symbol: str = Field(description="Stock symbol, for example TCS, INFY, HDFCBANK")


class SymbolDateInput(BaseModel):
    symbol: str = Field(description="Stock symbol, for example TCS, INFY, HDFCBANK")
    date: str = Field(description="Trading date in YYYY-MM-DD format")


portfolio_summary_tool = StructuredTool.from_function(
    func=get_portfolio_summary,
    name="get_portfolio_summary",
    description="Get portfolio summary for a given trading date.",
    args_schema=DateInput,
)

positions_tool = StructuredTool.from_function(
    func=get_positions,
    name="get_positions",
    description="Get all portfolio positions for a given trading date.",
    args_schema=DateInput,
)

position_by_symbol_tool = StructuredTool.from_function(
    func=get_position_by_symbol,
    name="get_position_by_symbol",
    description="Get portfolio position details for a specific symbol and date.",
    args_schema=SymbolDateInput,
)

top_pnl_tool = StructuredTool.from_function(
    func=get_top_pnl,
    name="get_top_pnl",
    description="Get top profit-making positions for a given trading date.",
    args_schema=DateInput,
)

top_loss_tool = StructuredTool.from_function(
    func=get_top_loss,
    name="get_top_loss",
    description="Get top loss-making positions for a given trading date.",
    args_schema=DateInput,
)

gross_exposure_tool = StructuredTool.from_function(
    func=calculate_gross_exposure,
    name="calculate_gross_exposure",
    description="Calculate gross exposure for a given trading date.",
    args_schema=DateInput,
)

net_exposure_tool = StructuredTool.from_function(
    func=calculate_net_exposure,
    name="calculate_net_exposure",
    description="Calculate net exposure for a given trading date.",
    args_schema=DateInput,
)

symbol_concentration_tool = StructuredTool.from_function(
    func=calculate_symbol_concentration,
    name="calculate_symbol_concentration",
    description="Calculate symbol-wise portfolio concentration risk for a given trading date.",
    args_schema=DateInput,
)

risk_alerts_tool = StructuredTool.from_function(
    func=generate_risk_alerts,
    name="generate_risk_alerts",
    description="Generate threshold-based portfolio risk alerts for a given trading date.",
    args_schema=DateInput,
)

latest_price_tool = StructuredTool.from_function(
    func=get_latest_price,
    name="get_latest_price",
    description="Get latest market price and volume for a stock symbol.",
    args_schema=SymbolInput,
)

price_trend_tool = StructuredTool.from_function(
    func=get_price_trend,
    name="get_price_trend",
    description="Get price trend for a stock symbol using available market data.",
    args_schema=SymbolInput,
)

volume_trend_tool = StructuredTool.from_function(
    func=get_volume_trend,
    name="get_volume_trend",
    description="Get volume trend for a stock symbol using available market data.",
    args_schema=SymbolInput,
)

market_summary_tool = StructuredTool.from_function(
    func=get_market_summary,
    name="get_market_summary",
    description="Get latest price, price trend, and volume trend for a stock symbol.",
    args_schema=SymbolInput,
)

signal_tool = StructuredTool.from_function(
    func=generate_signal,
    name="generate_signal",
    description="Generate ML-based trading signal for a stock symbol with rule-based fallback.",
    args_schema=SymbolInput,
)

signal_explanation_tool = StructuredTool.from_function(
    func=get_signal_explanation,
    name="get_signal_explanation",
    description="Generate trading signal with explanation for a stock symbol.",
    args_schema=SymbolInput,
)


LANGCHAIN_TOOLS = [
    portfolio_summary_tool,
    positions_tool,
    position_by_symbol_tool,
    top_pnl_tool,
    top_loss_tool,
    gross_exposure_tool,
    net_exposure_tool,
    symbol_concentration_tool,
    risk_alerts_tool,
    latest_price_tool,
    price_trend_tool,
    volume_trend_tool,
    market_summary_tool,
    signal_tool,
    signal_explanation_tool,
]


def get_langchain_tools():
    """
    Return all LangChain tools.
    """

    return LANGCHAIN_TOOLS