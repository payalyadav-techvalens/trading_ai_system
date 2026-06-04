from langchain_ollama import ChatOllama

from tools.langchain_tools import get_langchain_tools


def run_tool_calling_test():
    tools = get_langchain_tools()

    tool_map = {tool.name: tool for tool in tools}

    llm = ChatOllama(
        model="llama3.1",
        temperature=0,
    )

    llm_with_tools = llm.bind_tools(tools)

    user_question = "Generate trading signal for TCS"

    response = llm_with_tools.invoke(user_question)

    print("\nLLM Response:")
    print(response)

    print("\nTool Calls:")
    print(response.tool_calls)

    if not response.tool_calls:
        print("\nNo tool call returned by LLM.")
        return

    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print("\nSelected tool:", tool_name)
        print("Tool args:", tool_args)

        selected_tool = tool_map.get(tool_name)

        if selected_tool is None:
            print(f"Tool not found: {tool_name}")
            continue

        tool_result = selected_tool.invoke(tool_args)

        print("\nTool Result:")
        print(tool_result)


if __name__ == "__main__":
    run_tool_calling_test()