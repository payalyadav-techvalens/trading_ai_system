from llm.ollama_client import ask_ollama
from tools.portfolio_tools import (
    get_positions,
    get_position_by_symbol,
    get_top_pnl,
    get_top_loss,
    get_portfolio_summary,
)


def extract_symbol(question: str):
    """
    Basic symbol extraction.
    Later we can replace this with LLM-based entity extraction.
    """

    known_symbols = ["TCS", "INFY", "HDFCBANK", "RELIANCE", "SBIN", "WIPRO", "LT"]

    question_upper = question.upper()

    for symbol in known_symbols:
        if symbol in question_upper:
            return symbol

    return None


def handle_portfolio_question(question: str, date: str, recent_memory=None):
    """
    Portfolio Agent:
    Handles portfolio, position, PnL and symbol-related questions.
    """

    q = question.lower()

    tool_used = None
    tool_result = None

    if "summary" in q or "portfolio" in q:
        tool_used = "get_portfolio_summary"
        tool_result = get_portfolio_summary(date)

    elif "top profit" in q or "profit" in q or "highest pnl" in q:
        tool_used = "get_top_pnl"
        tool_result = get_top_pnl(date)

    elif "loss" in q or "negative pnl" in q:
        tool_used = "get_top_loss"
        tool_result = get_top_loss(date)

    elif "position" in q or "symbol" in q:
        symbol = extract_symbol(question)

        if symbol:
            tool_used = "get_position_by_symbol"
            tool_result = get_position_by_symbol(symbol, date)
        else:
            tool_used = "get_positions"
            tool_result = get_positions(date)

    else:
        tool_used = "get_portfolio_summary"
        tool_result = get_portfolio_summary(date)

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