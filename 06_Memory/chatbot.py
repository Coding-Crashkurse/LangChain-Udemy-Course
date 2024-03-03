"""Python file to serve as the frontend"""

import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv, find_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.globals import get_verbose

get_verbose()

load_dotenv(find_dotenv())

template = """You are an AI chatbot having a conversation with a human.

{history}
Human: {human_input}
AI: """

# TODO: Add prompt

msgs = StreamlitChatMessageHistory(key="special_app_key")

# TODO: Add Memory


def load_chain():
    # Add an LLMChain with memory and a prompt
    return llm_chain


def initialize_session_state():
    if "chain" not in st.session_state:
        st.session_state.chain = load_chain()

    if "generated" not in st.session_state:
        st.session_state.generated = []

    if "past" not in st.session_state:
        st.session_state.past = []

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    if "widget_input" not in st.session_state:
        st.session_state.widget_input = ""


initialize_session_state()

st.set_page_config(page_title="LangChain ChatBot Demo", page_icon=":robot:")
st.header("LangChain ChatBot Demo")


def submit():
    st.session_state.user_input = st.session_state.widget_input
    st.session_state.widget_input = ""


st.text_input("You:", key="widget_input", on_change=submit)

if st.session_state.user_input:
    output = st.session_state.chain.run(st.session_state.user_input)
    st.session_state.past.append(st.session_state.user_input)
    st.session_state.generated.append(output)

    st.session_state.user_input = ""

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
