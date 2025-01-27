import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# 仮に OutputParser が必要な場合に標準クラスを使用
from langchain_core.output_parsers import OutputParser  # 確認が必要

# Streamlit ページ設定
st.set_page_config(page_title="My Great ChatGPT", page_icon="🤗")
st.header("My Great ChatGPT🤗")

# サイドバー設定
def select_model():
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    model_name = "gpt-3.5-turbo" if model == "GPT-3.5" else "gpt-4"
    return ChatOpenAI(temperature=temperature, model_name=model_name)

# 初期化
if "message_history" not in st.session_state:
    st.session_state.message_history = [("system", "You are a helpful assistant.")]

# メインコンテンツ
with st.container():
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area(label='Message:', key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        # モデル選択とプロンプトの作成
        llm = select_model()
        prompt = ChatPromptTemplate.from_messages(st.session_state.message_history + [("user", user_input)])

        # 出力パーサーの処理 (仮)
        output_parser = OutputParser()  # 代替として標準の OutputParser を使用

        # チェーンを作成して実行
        chain = prompt | llm | output_parser
        response = chain.invoke({"input": user_input})

        # 会話履歴に追加
        st.session_state.message_history.append(("user", user_input))
        st.session_state.message_history.append(("assistant", response))

        # 返答を表示
        st.write(f"ChatGPTの返答: {response}")

# サイドバーオプション
st.sidebar.title("Options")
st.sidebar.markdown("## Costs")
st.sidebar.markdown("**Total cost**")
st.sidebar.markdown("- Input cost: $0.001")  # 仮
st.sidebar.markdown("- Output cost: $0.001")  # 仮
