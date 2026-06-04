from graph.trading_graph import run_trading_graph

def print_final_answer(result):
    """
    Print final assistant response from graph result.
    """

    messages = result["messages"]

    print("\nAll Messages:")
    for msg in messages:
        print(type(msg).__name__, ":", msg.content)

        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print("Tool calls:", msg.tool_calls)

    print("\nFinal Answer:")
    print(messages[-1].content)


if __name__ == "__main__":
    questions = [
        "Generate trading signal for TCS",
        "Show latest price of INFY",
        "Give me portfolio summary for 2026-06-04",
        "Show risk alerts for 2026-06-04",
    ]

    for question in questions:
        print("\n====================================")
        print("Question:", question)

        result = run_trading_graph(question)

        print_final_answer(result)