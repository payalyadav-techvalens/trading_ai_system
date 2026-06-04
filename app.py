from fastapi import FastAPI
from pydantic import BaseModel

from llm.ollama_client import ask_ollama
from tools.portfolio_tools import (
    get_positions,
    get_position_by_symbol,
    get_top_pnl,
    get_top_loss,
    calculate_gross_exposure,
    calculate_net_exposure,
    get_portfolio_summary,
)


app = FastAPI(title="Trading AI Assistant")


class ChatRequest(BaseModel):
    question: str
    date: str = "2026-06-04"


def detect_tool(question: str):
    """
    Simple rule-based tool selection for Level 1.
    Later we will replace this with proper tool calling.
    """

    q = question.lower()

    if "summary" in q or "portfolio" in q:
        return "portfolio_summary"

    if "top profit" in q or "profit" in q or "highest pnl" in q:
        return "top_pnl"

    if "loss" in q or "negative pnl" in q:
        return "top_loss"

    if "gross exposure" in q:
        return "gross_exposure"

    if "net exposure" in q:
        return "net_exposure"

    if "position" in q and "symbol" in q:
        return "positions"

    return "general"


def extract_symbol(question: str):
    """
    Basic symbol extraction for Level 1.
    Later we will improve this using LLM/tool calling.
    """

    known_symbols = ["TCS", "INFY", "HDFCBANK", "RELIANCE", "SBIN", "WIPRO", "LT"]

    question_upper = question.upper()

    for symbol in known_symbols:
        if symbol in question_upper:
            return symbol

    return None


@app.get("/")
def home():
    return {
        "message": "Trading AI Assistant is running",
        "level": "Level 1",
    }


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question
    date = request.date

    tool_name = detect_tool(question)
    tool_result = None

    if tool_name == "portfolio_summary":
        tool_result = get_portfolio_summary(date)

    elif tool_name == "top_pnl":
        tool_result = get_top_pnl(date)

    elif tool_name == "top_loss":
        tool_result = get_top_loss(date)

    elif tool_name == "gross_exposure":
        tool_result = calculate_gross_exposure(date)

    elif tool_name == "net_exposure":
        tool_result = calculate_net_exposure(date)

    elif tool_name == "positions":
        symbol = extract_symbol(question)

        if symbol:
            tool_result = get_position_by_symbol(symbol, date)
        else:
            tool_result = get_positions(date)

    else:
        tool_result = "No specific trading tool matched. Answer generally."

    prompt = f"""
You are a Trading AI Assistant.

User question:
{question}

Tool selected:
{tool_name}

Tool result:
{tool_result}

Now answer the user in simple professional English.
Do not make up numbers.
Use only the tool result when financial data is required.
"""

    answer = ask_ollama(prompt)

    return {
        "question": question,
        "tool_used": tool_name,
        "tool_result": tool_result,
        "answer": answer,
    }