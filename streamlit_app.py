import streamlit as st

from finsight_llm import REFUSAL_MESSAGE, generate_finsight_response


st.set_page_config(
    page_title="FinSight",
    page_icon="💹",
    layout="centered",
)


def initialize_chat() -> None:
    """Create chat history once per browser session."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi, I am FinSight. Ask me finance questions about markets, "
                    "banking, accounting, investing concepts, valuation, risk, or "
                    "personal finance education."
                ),
            }
        ]


initialize_chat()

st.title("FinSight")
st.caption("AI-powered Finance Knowledge Assistant")

with st.sidebar:
    st.header("FinSight")
    st.write(
        "Educational finance insights only. FinSight does not provide personalized "
        "financial advice, buy/sell recommendations, or guaranteed returns."
    )

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_question = st.chat_input("Ask a finance question...")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        with st.spinner("FinSight is thinking..."):
            try:
                answer = generate_finsight_response(user_question)
            except Exception as exc:
                answer = (
                    "Sorry, I could not generate a response right now. Please check "
                    "your API key, internet connection, and model configuration.\n\n"
                    f"Technical detail: {exc}"
                )

        # Preserve the exact refusal phrase for out-of-domain questions.
        if answer.strip() == REFUSAL_MESSAGE:
            st.markdown(REFUSAL_MESSAGE)
            st.session_state.messages.append(
                {"role": "assistant", "content": REFUSAL_MESSAGE}
            )
        else:
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
