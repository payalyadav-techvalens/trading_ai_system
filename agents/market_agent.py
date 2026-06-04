from llm.ollama_client import ask_ollama
from tools.tool_registry import execute_tool


def extract_symbol(question: str):
    """
    Basic symbol extraction.
    Later this can be replaced with LLM-based entity extraction.
    """

    known_symbols = ["TCS", "INFY", "HDFCBANK", "RELIANCE", "SBIN", "WIPRO", "LT"]

    question_upper = question.upper()

    for symbol in known_symbols:
        if symbol in question_upper:
            return symbol

    return None


def select_market_tool(question: str):
    """
    Select market data tool based on user question.
    """

    q = question.lower()

    if "latest price" in q or "current price" in q or "last price" in q:
        return "get_latest_price"

    if "volume" in q:
        return "get_volume_trend"

    if "trend" in q or "price movement" in q:
        return "get_price_trend"

    return "get_market_summary"


def handle_market_question(question: str, recent_memory=None):
    """
    Market Agent:
    Handles price, trend, volume and market-data related questions.
    """

    symbol = extract_symbol(question)

    if not symbol:
        return {
            "agent_used": "market_agent",
            "tool_used": "no_tool",
            "tool_result": None,
            "answer": "Please provide a valid symbol like TCS, INFY, or HDFCBANK for market data.",
        }

    tool_used = select_market_tool(question)

    tool_result = execute_tool(
        tool_name=tool_used,
        symbol=symbol,
    )

    prompt = f"""
You are a Market Agent in a Trading AI Assistant.

User question:
{question}

Recent memory:
{recent_memory}

Tool used:
{tool_used}

Tool result:
{tool_result}

Answer the user in simple professional English.
Use only the given tool result.
Do not make up live market data.
Clearly mention that this is based on available price data.
"""

    answer = ask_ollama(prompt)

    return {
        "agent_used": "market_agent",
        "tool_used": tool_used,
        "tool_result": tool_result,
        "answer": answer,
    }