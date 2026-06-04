from fastapi import FastAPI
from pydantic import BaseModel

from llm.ollama_client import ask_ollama
from agents.llm_router_agent import route_question_with_llm
from agents.portfolio_agent import handle_portfolio_question
from agents.risk_agent import handle_risk_question
from memory.conversation_memory import add_to_memory, get_recent_memory
from agents.signal_agent import handle_signal_question
from agents.market_agent import handle_market_question
from graph.trading_graph import run_trading_graph

app = FastAPI(title="Trading AI Assistant")


class ChatRequest(BaseModel):
    question: str
    date: str = "2026-06-04"
    thread_id: str = "default_thread"


def extract_final_graph_answer(graph_result):
    """
    Extract final assistant response from LangGraph result.
    """

    messages = graph_result.get("messages", [])

    if not messages:
        return "No response generated from LangGraph."

    final_message = messages[-1]

    return final_message.content


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

    router_response = route_question_with_llm(question)
    selected_agent = router_response["agent"]
    router_reason = router_response["reason"]

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
    
    elif selected_agent == "signal_agent":
        response = handle_signal_question(
            question=question,
            recent_memory=recent_memory,
        )
    
    elif selected_agent == "market_agent":
        response = handle_market_question(
            question=question,
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
        "router_reason": router_reason,
        "tool_used": response["tool_used"],
        "tool_result": response["tool_result"],
        "answer": response["answer"],
        # "recent_memory": get_recent_memory(limit=5),
    }

@app.post("/chat-graph")
def chat_graph(request: ChatRequest):
    """
    LangGraph-based chat endpoint.

    This uses:
    ChatOllama + LangChain tools + LangGraph workflow.
    """

    question = request.question

    graph_result = run_trading_graph(
        question=question,
        thread_id=request.thread_id,
    )

    final_answer = extract_final_graph_answer(graph_result)

    messages = graph_result.get("messages", [])

    tool_calls = []

    for message in messages:
        if hasattr(message, "tool_calls") and message.tool_calls:
            tool_calls.extend(message.tool_calls)

    return {
    "question": question,
    "answer": final_answer,
    "tool_calls": tool_calls,
    "mode": "langgraph",
    "thread_id": request.thread_id,
    }
