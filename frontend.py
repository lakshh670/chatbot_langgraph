import streamlit as st
from langchain_core.messages import HumanMessage
import uuid
from backend import chatbot

# ********************************* utility_functions *****************************************
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id =generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(thread_id)
    st.session_state['chat_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state=chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages',[])


# ********************************** session_setup *********************************************


if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []
add_thread(st.session_state['thread_id'])


# *********************************** sidebar_ui ***************************************************

st.sidebar.title('Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My Conversations')
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages=load_conversation(thread_id)
        # messages=  [BaseMessage] ->[{'role':...,'content':...},{}..]
        temp_history=[]
        for message in messages:
            role=''
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_history.append({'role':role,'content':message.content})
        st.session_state['chat_history']=temp_history


# ********************************** main_ui *******************************************************
# loading the conversation history:
for message in st.session_state['chat_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
user_input=st.text_input("Type here")
if user_input:
    st.session_state['chat_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    CONFIG={'configurable': {'thread_id': st.session_state['thread_id']}}
    with st.chat_message('assistant'):
        ai_message=st.write_stream(message_chunk.content for message_chunk,meta_data in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages' # Stream mode message doesn't loads the whole state dictionary it just loads the the ai messages step by step
        ))
        st.session_state['chat_history'].append({'role':'assistant','content':ai_message})




