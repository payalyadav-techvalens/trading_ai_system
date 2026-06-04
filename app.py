from fastapi import FastAPI
from pydantic import BaseModel

from llm.ollama_client import ask_ollama
from agents.supervisor_agent import route_question
from agents.portfolio_agent import handle_portfolio_question
from agents.risk_agent import handle_risk_question
from memory.conversation_memory import add_to_memory, get_recent_memory


app = FastAPI(title="Trading AI Assistant")


class ChatRequest(BaseModel):
    question: str
    date: str = "2026-06-04"


@app.get("/")
def home():
    return {
        "message": "Trading AI Assistant is running",
        "level": "Level 2",
        "features": [
            "Supervisor Agent",
            "Portfolio Agent",
            "Risk Agent",
            "Conversation Memory",
        ],
    }


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question
    date = request.date

    recent_memory = get_recent_memory(limit=5)

    selected_agent = route_question(question)

    if selected_agent == "portfolio_agent":
        response = handle_portfolio_question(
            question=question,
            date=date,
            recent_memory=recent_memory,
        )

    elif selected_agent == "risk_agent":
        response = handle_risk_question(
            question=question,
            date=date,
            recent_memory=recent_memory,
        )

    else:
        prompt = f"""
You are a Trading AI Assistant.

User question:
{question}

Recent memory:
{recent_memory}

This question does not need a trading data tool.
Answer generally and professionally.
"""

        answer = ask_ollama(prompt)

        response = {
            "agent_used": "general_agent",
            "tool_used": "no_tool",
            "tool_result": None,
            "answer": answer,
        }

    add_to_memory(
        question=question,
        answer=response["answer"],
        agent_used=response["agent_used"],
        tool_used=response["tool_used"],
    )

    return {
        "question": question,
        "date": date,
        "agent_used": response["agent_used"],
        "tool_used": response["tool_used"],
        "tool_result": response["tool_result"],
        "answer": response["answer"],
        "recent_memory": get_recent_memory(limit=5),
    }