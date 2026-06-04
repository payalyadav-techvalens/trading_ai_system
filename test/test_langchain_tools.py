from tools.langchain_tools import get_langchain_tools


tools = get_langchain_tools()

print("Total LangChain tools:", len(tools))

for tool in tools:
    print("-", tool.name, ":", tool.description)


portfolio_tool = [tool for tool in tools if tool.name == "get_portfolio_summary"][0]
result = portfolio_tool.invoke({"date": "2026-06-04"})

print("\nPortfolio summary result:")
print(result)


signal_tool = [tool for tool in tools if tool.name == "get_signal_explanation"][0]
signal_result = signal_tool.invoke({"symbol": "TCS"})

print("\nSignal result:")
print(signal_result)