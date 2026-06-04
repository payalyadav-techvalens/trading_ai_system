from llm.ollama_client import ask_ollama
from tools.portfolio_tools import (
    calculate_gross_exposure,
    calculate_net_exposure,
    get_portfolio_summary,
)


def handle_risk_question(question: str, date: str, recent_memory=None):
    """
    Risk Agent:
    Handles exposure and portfolio risk-related questions.
    """

    q = question.lower()

    tool_used = None
    tool_result = None

    if "gross exposure" in q:
        tool_used = "calculate_gross_exposure"
        tool_result = calculate_gross_exposure(date)

    elif "net exposure" in q:
        tool_used = "calculate_net_exposure"
        tool_result = calculate_net_exposure(date)

    elif "risk" in q or "exposure" in q:
        tool_used = "risk_summary"

        gross_exposure = calculate_gross_exposure(date)
        net_exposure = calculate_net_exposure(date)
        portfolio_summary = get_portfolio_summary(date)

        tool_result = {
            "gross_exposure": gross_exposure,
            "net_exposure": net_exposure,
            "portfolio_summary": portfolio_summary,
        }

    else:
        tool_used = "risk_summary"

        tool_result = {
            "gross_exposure": calculate_gross_exposure(date),
            "net_exposure": calculate_net_exposure(date),
            "portfolio_summary": get_portfolio_summary(date),
        }

    prompt = f"""
You are a Risk Agent in a Trading AI Assistant.

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

Explain the risk or exposure in simple professional English.
Do not make up numbers.
Use only the tool result.
"""

    answer = ask_ollama(prompt)

    return {
        "agent_used": "risk_agent",
        "tool_used": tool_used,
        "tool_result": tool_result,
        "answer": answer,
    }