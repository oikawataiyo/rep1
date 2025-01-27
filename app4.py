import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Streamlitのページ設定
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
        # 送信ボタンが押され、ユーザー入力があれば実行
        st.write(f"入力されたメッセージ: {user_input}")
        
        # ChatGPTの回答を取得する処理
        llm = ChatOpenAI()

        # ChatGPTへの質問を処理するテンプレートを作成
        prompt = ChatPromptTemplate.from_messages([ 
            ("system", "You are a helpful assistant."),  # システムメッセージ
            ("user", user_input)  # ユーザー入力
        ])

        # 出力をパースするための処理を作成
        output_parser = StrOutputParser()

        # 連続的な処理を作成
        chain = prompt | llm | output_parser

        # 質問をChatGPTに渡して回答を取得
        response = chain.invoke({"input": user_input})

        # ChatGPTの返答を表示
        st.write(f"ChatGPTの返答: {response}")
