from typing import Annotated, TypedDict

from langchain_ollama import ChatOllama
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from tools.langchain_tools import get_langchain_tools


class TradingGraphState(TypedDict):
    """
    LangGraph state.
    messages stores conversation messages and tool messages.
    """
    messages: Annotated[list[AnyMessage], add_messages]


tools = get_langchain_tools()

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)


def assistant_node(state: TradingGraphState):
    """
    Main assistant node.
    It receives messages and decides whether to answer directly
    or call a tool.
    """

    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)


def build_trading_graph():
    """
    Build LangGraph workflow.

    Flow:
    START -> assistant
    assistant -> tools if tool call exists
    tools -> assistant
    assistant -> END if no tool call exists
    """

    graph_builder = StateGraph(TradingGraphState)

    graph_builder.add_node("assistant", assistant_node)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_edge(START, "assistant")

    graph_builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )

    graph_builder.add_edge("tools", "assistant")

    memory = MemorySaver()

    graph = graph_builder.compile(checkpointer=memory)

    return graph


def run_trading_graph(question: str, thread_id: str = "default_thread"):
    """
    Run graph for a user question with memory support.
    """

    result = trading_graph_app.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return result

trading_graph_app = build_trading_graph()