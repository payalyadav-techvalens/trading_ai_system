from llm.ollama_client import ask_ollama
from tools.tool_registry import execute_tool


def select_risk_tool(question: str):
    """
    Select risk tool based on question.
    """

    q = question.lower()

    if "gross exposure" in q:
        return "calculate_gross_exposure"

    if "net exposure" in q:
        return "calculate_net_exposure"
    
    if "alert" in q or "warning" in q or "breach" in q:
        return "generate_risk_alerts"

    if "concentration" in q:
        return "calculate_symbol_concentration"

    return "risk_summary"


def handle_risk_question(question: str, date: str, recent_memory=None):
    """
    Risk Agent:
    Handles exposure and portfolio risk-related questions.
    """

    tool_used = select_risk_tool(question)

    if tool_used == "calculate_gross_exposure":
        tool_result = execute_tool(
            tool_name="calculate_gross_exposure",
            date=date,
        )

    elif tool_used == "calculate_net_exposure":
        tool_result = execute_tool(
            tool_name="calculate_net_exposure",
            date=date,
        )

    elif tool_used == "generate_risk_alerts":
        tool_result = execute_tool(
            tool_name="generate_risk_alerts",
            date=date,
        )

    elif tool_used == "calculate_symbol_concentration":
        tool_result = execute_tool(
            tool_name="calculate_symbol_concentration",
            date=date,
        )

    else:
        tool_result = {
            "gross_exposure": execute_tool(
                tool_name="calculate_gross_exposure",
                date=date,
            ),
            "net_exposure": execute_tool(
                tool_name="calculate_net_exposure",
                date=date,
            ),
            "portfolio_summary": execute_tool(
                tool_name="get_portfolio_summary",
                date=date,
            ),
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