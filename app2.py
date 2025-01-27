import streamlit as st

st.set_page_config(
    page_title="My Great ChatGPT",
    page_icon="🤗"
)
st.header("My Great ChatGPT🤗")

container = st.container() 
with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area(label='Message: ', key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input: 
        # 何か入力されて Submit ボタンが押されたら実行される
        st.write(f"入力されたメッセージ: {user_input}")
