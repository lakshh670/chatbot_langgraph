import streamlit as st
from langchain_core.messages import HumanMessage

from backend import chatbot

CONFIG={'configurable':{'thread_id':'1'}}

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# loading the conversation history:
for message in st.session_state['chat_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
user_input=st.text_input("Type here")
if user_input:
    st.session_state['chat_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    with st.chat_message('assistant'):
        ai_message=st.write_stream(message_chunk.content for message_chunk,meta_data in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config={'configurable': {'thread_id': '1'}},
            stream_mode='messages' # Stream mode message doesn't loads the whole state dictionary it just loads the the ai messages step by step
        ))
        st.session_state['chat_history'].append({'role':'assistant','content':ai_message})




