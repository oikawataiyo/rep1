import tiktoken
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Models
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL_PRICES = {
    "input": {
        "gpt-3.5-turbo": 0.5 / 1_000_000,
        "gpt-4": 5 / 1_000_000,
        "claude-3-5-sonnet-20240620": 3 / 1_000_000,
        "gemini-1.5-pro-latest": 3.5 / 1_000_000,
    },
    "output": {
        "gpt-3.5-turbo": 1.5 / 1_000_000,
        "gpt-4": 15 / 1_000_000,
        "claude-3-5-sonnet-20240620": 15 / 1_000_000,
        "gemini-1.5-pro-latest": 10.5 / 1_000_000,
    }
}

def init_page():
    st.set_page_config(
        page_title="My Great ChatGPT",
        page_icon=""
    )
    st.header("My Great ChatGPT")
    st.sidebar.title("Options")

def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")

    if clear_button or "message_history" not in st.session_state:
        st.session_state.message_history = [("system", "You are a helpful assistant.")]

def select_model():
    temperature = st.sidebar.slider(
        "Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.01
    )
    models = ("GPT-3.5", "GPT-4", "Claude 3.5 Sonnet", "Gemini 1.5 Pro")
    model = st.sidebar.radio("Choose a model:", models)

    if model == "GPT-3.5":
        st.session_state.model_name = "gpt-3.5-turbo"
        return ChatOpenAI(temperature=temperature, model_name=st.session_state.model_name)
    elif model == "GPT-4":
        st.session_state.model_name = "gpt-4"
        return ChatOpenAI(temperature=temperature, model_name=st.session_state.model_name)
    elif model == "Claude 3.5 Sonnet":
        st.session_state.model_name = "claude-3-5-sonnet-20240620"
        return ChatAnthropic(temperature=temperature, model_name=st.session_state.model_name)
    elif model == "Gemini 1.5 Pro":
        st.session_state.model_name = "gemini-1.5-pro-latest"
        return ChatGoogleGenerativeAI(temperature=temperature, model_name=st.session_state.model_name)

def init_chain():
    st.session_state.llm = select_model()
    prompt = ChatPromptTemplate.from_messages([
        *st.session_state.message_history,
        ("user", "{user_input}")
    ])
    output_parser = StrOutputParser()
    return prompt | st.session_state.llm | output_parser

def get_message_counts(text):
    if "gemini" in st.session_state.model_name:
        # Add specific logic for Gemini token counting
        pass
    else:
        encoding = tiktoken.encoding_for_model(st.session_state.model_name)
        return len(encoding.encode(text))

def calc_and_display_costs():
    output_count = 0
    input_count = 0

    for role, message in st.session_state.message_history:
        token_count = get_message_counts(message)

        if role == "ai":
            output_count += token_count
        else:
            input_count += token_count

    if len(st.session_state.message_history) == 1:
        return

    input_cost = MODEL_PRICES['input'][st.session_state.model_name] * input_count
    output_cost = MODEL_PRICES['output'][st.session_state.model_name] * output_count

    if "gemini" in st.session_state.model_name and (input_count + output_count) > 128000:
        input_cost *= 2
        output_cost *= 2

    total_cost = input_cost + output_cost

    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${total_cost:.5f}**")
    st.sidebar.markdown(f"- Input cost: ${input_cost:.5f}")
    st.sidebar.markdown(f"- Output cost: ${output_cost:.5f}")

def main():
    init_page()
    init_messages()
    chain = init_chain()

    for role, message in st.session_state.get("message_history", []):
        st.chat_message(role).markdown(message)

    user_input = st.chat_input("Ask me something!")

    if user_input:
        st.chat_message('user').markdown(user_input)

        with st.chat_message('ai'):
            response = st.write_stream(chain.stream({"user_input": user_input}))

        st.session_state.message_history.append(("user", user_input))
        st.session_state.message_history.append(("ai", response))

        calc_and_display_costs()

if __name__ == '__main__':
    main()
