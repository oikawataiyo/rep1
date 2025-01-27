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

#サイドバーのタイトルを表示
st.sidebar.title("Options")

#サイドバーにオプションボタンを設置
model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))

#サイドバーにボタンを設置
clear_button = st.sidebar.button("Clear Conversation", key="clear")

#サイドバーにスライダーを追加し、temperatureを0から2までの範囲で選択可能にする
#初期値は0.0、刻み幅は0.1とする
temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

# Streamlitはmarkdown を書けばいい感じにHTMLで表示してくれます
#(markdownはもちろんサイドバー以外の箇所でも使えます)
st.sidebar.markdown("## Costs")
st.sidebar.markdown("**Total cost**")
st.sidebar.markdown("- Input cost: $0.001 ") # dummy
st.sidebar.markdown("- Output cost: $0.001 ") # dummy
def select_model():
    #スライダーを追加し、temperatureを0から2までの範囲で選択可能にする
    #初期値は0.0、刻み幅は0.01とする
    temperature = st.sidebar.slider(
        "Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.01)

    models = ("GPT-3.5", "GPT-4")
    model = st.sidebar.radio("Choose a model:", models)
    if model == "GPT-3.5":
        st.session_state.model_name = "gpt-3.5-turbo" 
        return ChatOpenAI (
            temperature=temperature, 
            model_name=st.session_state.model_name
        )
    elif model == "GPT-4":
        st.session_state.model_name = "gpt-40"
        return ChatOpenAI(
            temperature=temperature,
            model_name=st.session_state.model_name
        )

def init_chain():
    llm = select_model()

def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    #clear_button が押された場合や message_history がまだ存在しない場合に初期化
    if clear_button or "message_history" not in st.session_state:
       st.session_state.message_history = [
           ("system", "You are a helpful assistant.")
       ]

def main():
    init_page()
    init_messages()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("user", "{user_input}"), # inputにはあとでuser_inputが代入される
])
llm = ChatOpenAI (temperature=0)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

response = chain.invoke({"user_input": "こんにちは"})
print(response)
#=> こんにちは! 何かお手伝いできますか?!

#一度に複数の入力を処理する場合
responses = chain.batch([
    {"user_input": "こんにちは"},
    {"user_input": "今日の天気は?"},
    {"user_input": "明日の予定は?"}
])

print(responses)
# => [
#     'こんにちは! 何かお手伝いできますか?',
#     '申し訳ありませんが、私は天気情報を提供することができません。',
#     '私はAIですので、明日の予定はありません。',
#]

#max_concurrency パラメータで最大並列数を指定することも可能
responses = chain.batch([
    {"user_input": "こんにちは"},
    {"user_input": "今日の天気は?"},
    {"user_input": "明日の予定は?"},
    {"user_input":"明後日の予定は?"},
    {"user_input":"明々後日の予定は?"}
], config={"max_concurrency": 3}
)

response = st.write_stream(chain.stream({"user_input": user_input}))

import streamlit as st

# セッション状態の初期化
if "message_history" not in st.session_state:
    st.session_state.message_history = []

def main():
    # 1. チャット履歴の表示
    for role, message in st.session_state.get("message_history", []):
        st.chat_message(role).markdown(message)

    # ユーザーの入力を監視
    if user_input := st.chat_input("聞きたいことを入力してね!"):
        st.chat_message("user").markdown(user_input)

        # 2. LLMの返答を Streaming 表示する
        with st.chat_message("ai"):
            # 例として LLM の返答を生成する箇所を擬似的に表現
            response_placeholder = st.empty()  # プレースホルダーを用意
            response = ""
            for chunk in chain.stream({"user_input": user_input}):  # ストリーム処理
                response += chunk  # チャンクを追加
                response_placeholder.markdown(response)  # リアルタイム更新

        # 3. チャット履歴に追加
        st.session_state.message_history.append(("user", user_input))
        st.session_state.message_history.append(("ai", response))

if __name__ == "__main__":
    main()

# models
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic#追加
from langchain_google_genai import ChatGoogleGenerativeAI#追加
import openai
import streamlit as st
from anthropic import ChatAnthropic
from google.generativeai import ChatGoogleGenerativeAI

def select_model(model, temperature):
    if model == "GPT-3.5":
        st.session_state.model_name = "gpt-3.5-turbo"
        return openai.ChatCompletion.create(
            model=st.session_state.model_name,
            temperature=temperature,
            messages=[{"role": "system", "content": "You are a helpful assistant."}]
        )
    elif model == "GPT-4":
        st.session_state.model_name = "gpt-4"
        return openai.ChatCompletion.create(
            model=st.session_state.model_name,
            temperature=temperature,
            messages=[{"role": "system", "content": "You are a helpful assistant."}]
        )
    elif model == "Claude 3.5 Sonnet":
        st.session_state.model_name = "claude-3-5-sonnet-20240620"
        return ChatAnthropic(
            temperature=temperature,
            model_name=st.session_state.model_name
        )
    elif model == "Gemini 1.5 Pro":
        st.session_state.model_name = "gemini-1.5-pro-latest"
        return ChatGoogleGenerativeAI(
            temperature=temperature,
            model=st.session_state.model_name
        )

def init_chain(model, temperature):
    llm = select_model(model, temperature)
    return llm

# サイドバーにモデル選択用のドロップダウンを追加
st.sidebar.title("LLM 切り替え")
model_options = ["GPT-3.5", "GPT-4", "Claude 3.5 Sonnet", "Gemini 1.5 Pro"]
model = st.sidebar.selectbox("モデルを選択", model_options)

# サイドバーに温度設定のスライダーを追加
temperature = st.sidebar.slider("温度", 0.0, 1.0, 0.7)

# モデルと温度に基づいてLLMを選択し、初期化する
llm = init_chain(model, temperature)

# ここで、選択したLLMを使って、他の処理を進めます
st.write(f"選択されたモデル: {model}")

