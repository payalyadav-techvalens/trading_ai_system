import json
import os
from datetime import datetime


MEMORY_FILE = "memory/conversation_history.json"


def load_memory():
    """
    Load previous conversation memory from JSON file.
    """

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_memory(memory_data):
    """
    Save conversation memory into JSON file.
    """

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory_data, file, indent=4)


def add_to_memory(question: str, answer: str, agent_used: str, tool_used: str):
    """
    Store user question, assistant answer, agent and tool information.
    """

    memory_data = load_memory()

    memory_data.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "answer": answer,
            "agent_used": agent_used,
            "tool_used": tool_used,
        }
    )

    save_memory(memory_data)


def get_recent_memory(limit: int = 5):
    """
    Return recent conversation history.
    """

    memory_data = load_memory()

    return memory_data[-limit:]