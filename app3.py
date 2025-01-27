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

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
result = llm.invoke("こんにちは!ChayGPT!") # invoke:呼ぶ、引き起こす
print(result)
# -> content='こんにちは！お元気ですか？何かお手伝いできますか？'

#必要なライブラリの呼び出し
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#あなたの質問をここに書く
user_input = "こんにちは!ChatGPT!"

#ChatGPTに質問を与えて回答を取り出す（パースする）処理を作成
# 1. ChatGPTのモデルを呼び出すように設定（デフォルトではGPT-3.5 Turboが呼ばれる）
llm = ChatOpenAI()

#2. ユーザーの質問を受け取り、ChatGPTに渡すためのテンプレートを作成 
prompt = ChatPromptTemplate.from_messages([ 
     ("system", "You are a helpful assistant."), # System Message の設定 
     ("user", "(input)")
])

#3. ChatGPTの返答をパースするための処理を呼び出し
output_parser = StrOutputParser()

#4. ユーザーの質問をChatGPTに渡し、返答を取り出す連続的な処理(chain)を作成 
# # 各要素を | (パイプ)でつなげて連続的な処理を作成するのがLCELの特徴 
chain = prompt | llm | output_parser

#chainの処理をinvoke(呼び出し)してChatGPTに質問を投げる
response = chain.invoke({"input": user_input})

# ChatGPTの返答を表示 
print (response) # -> こんにちは! どのようにお手伝いできますか?