import streamlit as st
import streamlit as st

st.set_page_config(
    page_title="ChatGPT Chat Input",
    page_icon="🤗"
)

st.header("ChatGPT Chat Input Example 🤗")

# チャット入力欄
if user_input := st.chat_input("聞きたいことを入力してね！"):
    # 入力があれば表示
    st.write(f"あなたの質問: {user_input}")
