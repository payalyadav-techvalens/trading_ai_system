import json
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"


def route_question_with_llm(question: str):
    """
    LLM Router Agent:
    Uses Ollama to decide which agent should handle the question.
    """

    prompt = f"""
You are a routing agent for a Trading AI Assistant.

Your job is to classify the user question into one agent.

Available agents:

1. portfolio_agent
Use this for:
- portfolio summary
- positions
- symbol details
- PnL
- profit
- loss
- holdings

2. risk_agent
Use this for:
- risk
- exposure
- gross exposure
- net exposure
- concentration
- risk alerts
- warning
- breach
- symbol concentration

3. general_agent
Use this for:
- greetings
- general questions
- questions not related to portfolio or risk

4. signal_agent
Use this for:
- trading signal
- buy signal
- sell signal
- hold signal
- prediction
- price trend
- ML signal

5. market_agent
Use this for:
- latest price
- current price
- market data
- price trend
- price movement
- volume trend
- latest volume

User question:
{question}

Return ONLY valid JSON in this exact format:
{{
  "agent": "portfolio_agent",
  "reason": "short reason"
}}

Allowed values for agent:
portfolio_agent, risk_agent, signal_agent, market_agent, general_agent
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        raw_response = response.json().get("response", "")
        parsed_response = json.loads(raw_response)

        agent = parsed_response.get("agent", "general_agent")
        reason = parsed_response.get("reason", "No reason provided")

        if agent not in ["portfolio_agent", "risk_agent", "signal_agent", "market_agent", "general_agent"]:
            agent = "general_agent"

        return {
            "agent": agent,
            "reason": reason
        }

    except Exception as e:
        return {
            "agent": "general_agent",
            "reason": f"Router failed: {str(e)}"
        }