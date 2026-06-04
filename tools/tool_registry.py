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
from tools.signal_tools import generate_signal, get_signal_explanation


AVAILABLE_TOOLS = {
    "get_positions": get_positions,
    "get_position_by_symbol": get_position_by_symbol,
    "get_top_pnl": get_top_pnl,
    "get_top_loss": get_top_loss,
    "calculate_gross_exposure": calculate_gross_exposure,
    "calculate_net_exposure": calculate_net_exposure,
    "get_portfolio_summary": get_portfolio_summary,
    "generate_signal": generate_signal,
    "get_signal_explanation": get_signal_explanation,
    "calculate_symbol_concentration": calculate_symbol_concentration,
    "generate_risk_alerts": generate_risk_alerts,
    "get_latest_price": get_latest_price,
    "get_price_trend": get_price_trend,
    "get_volume_trend": get_volume_trend,
    "get_market_summary": get_market_summary,
}


def execute_tool(tool_name: str, **kwargs):
    """
    Execute tool by name using tool registry.
    """

    tool = AVAILABLE_TOOLS.get(tool_name)

    if tool is None:
        return {
            "error": f"Tool '{tool_name}' not found",
            "available_tools": list(AVAILABLE_TOOLS.keys()),
        }

    try:
        return tool(**kwargs)

    except TypeError as e:
        return {
            "error": f"Invalid arguments for tool '{tool_name}'",
            "details": str(e),
        }

    except Exception as e:
        return {
            "error": f"Error while executing tool '{tool_name}'",
            "details": str(e),
        }


def list_available_tools():
    """
    Return available tools.
    """

    return list(AVAILABLE_TOOLS.keys())