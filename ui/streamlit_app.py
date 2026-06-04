import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/chat-graph"


st.set_page_config(
    page_title="Trading AI Assistant",
    page_icon="📈",
    layout="wide",
)

st.title("Trading AI Assistant")
st.caption("Multi-agent trading assistant using Ollama, LangGraph, LangChain tools, memory, live market data, and ML signals.")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "streamlit_user"


with st.sidebar:
    st.header("Settings")

    thread_id = st.text_input(
        "Thread ID",
        value=st.session_state.thread_id,
    )

    st.session_state.thread_id = thread_id

    date = st.text_input(
        "Trading Date",
        value="2026-06-04",
    )

    st.markdown("---")

    st.subheader("Example Questions")

    st.markdown(
        """
        - Generate trading signal for TCS
        - Show latest price of INFY
        - Show price trend for HDFCBANK
        - Give me portfolio summary for 2026-06-04
        - Show risk alerts for 2026-06-04
        - Show symbol concentration risk
        """
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("tool_calls"):
            with st.expander("Tool Calls"):
                st.json(message["tool_calls"])


user_question = st.chat_input("Ask your trading question...")

if user_question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    payload = {
        "question": user_question,
        "date": date,
        "thread_id": st.session_state.thread_id,
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()

                data = response.json()

                answer = data.get("answer", "No answer received.")
                tool_calls = data.get("tool_calls", [])

                st.markdown(answer)

                if tool_calls:
                    with st.expander("Tool Calls"):
                        st.json(tool_calls)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "tool_calls": tool_calls,
                    }
                )

            except requests.exceptions.ConnectionError:
                error_message = "FastAPI backend is not running. Please start it using: uvicorn app:app --reload"
                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )

            except Exception as e:
                error_message = f"Error: {str(e)}"
                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )