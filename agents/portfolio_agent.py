from llm.ollama_client import ask_ollama
from tools.tool_registry import execute_tool


def extract_symbol(question: str):
    """
    Basic symbol extraction.
    Later we can replace this with LLM-based extraction.
    """

    known_symbols = ["TCS", "INFY", "HDFCBANK", "RELIANCE", "SBIN", "WIPRO", "LT"]

    question_upper = question.upper()

    for symbol in known_symbols:
        if symbol in question_upper:
            return symbol

    return None


def select_portfolio_tool(question: str):
    """
    Select portfolio tool based on question.
    """

    q = question.lower()

    if "summary" in q or "portfolio" in q:
        return "get_portfolio_summary"

    if "top profit" in q or "profit" in q or "highest pnl" in q:
        return "get_top_pnl"

    if "loss" in q or "negative pnl" in q:
        return "get_top_loss"

    if "position" in q or "symbol" in q:
        return "get_position_by_symbol"

    return "get_portfolio_summary"


def handle_portfolio_question(question: str, date: str, recent_memory=None):
    """
    Portfolio Agent:
    Handles portfolio, position, PnL and symbol-related questions.
    """

    tool_used = select_portfolio_tool(question)

    if tool_used == "get_position_by_symbol":
        symbol = extract_symbol(question)

        if symbol:
            tool_result = execute_tool(
                tool_name=tool_used,
                symbol=symbol,
                date=date,
            )
        else:
            tool_used = "get_positions"
            tool_result = execute_tool(
                tool_name=tool_used,
                date=date,
            )

    else:
        tool_result = execute_tool(
            tool_name=tool_used,
            date=date,
        )

    prompt = f"""
You are a Portfolio Agent in a Trading AI Assistant.

User question:
{question}

Date:
{date}

Recent memory:
{recent_memory}

Tool used:
{tool_used}

Tool result:
{tool_result}

Answer the user in simple professional English.
Use only the given tool result.
Do not create fake numbers.
"""

    answer = ask_ollama(prompt)

    return {
        "agent_used": "portfolio_agent",
        "tool_used": tool_used,
        "tool_result": tool_result,
        "answer": answer,
    }