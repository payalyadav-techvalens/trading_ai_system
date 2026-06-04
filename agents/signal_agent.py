from llm.ollama_client import ask_ollama
from tools.tool_registry import execute_tool


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


def handle_signal_question(question: str, recent_memory=None):
    """
    Signal Agent:
    Handles trading signal related questions.
    """

    symbol = extract_symbol(question)

    if not symbol:
        return {
            "agent_used": "signal_agent",
            "tool_used": "no_tool",
            "tool_result": None,
            "answer": "Please provide a valid symbol like TCS, INFY, or HDFCBANK for signal generation.",
        }

    tool_used = "get_signal_explanation"

    tool_result = execute_tool(
        tool_name=tool_used,
        symbol=symbol,
    )

    prompt = f"""
You are a Signal Agent in a Trading AI Assistant.

User question:
{question}

Recent memory:
{recent_memory}

Tool used:
{tool_used}

Tool result:
{tool_result}

Explain the trading signal in simple professional English.

Important rules:
- Do not say this is guaranteed.
- Do not give financial advice.
- Mention that this is based on rule-based logic.
- Use only the given tool result.
"""

    answer = ask_ollama(prompt)

    return {
        "agent_used": "signal_agent",
        "tool_used": tool_used,
        "tool_result": tool_result,
        "answer": answer,
    }