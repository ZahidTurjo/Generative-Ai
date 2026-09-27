from backend import chatbot
import streamlit as st 
from langchain_core.messages import HumanMessage
import uuid

#==========utility function ===========
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    st.session_state['chat_history']=[]
    add_thread(st.session_state['thread_id'])
    
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])



# st.text(st.session_state['thread_id'])

# ================session state============
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

add_thread(st.session_state['thread_id'])
#=============slidebar=======================
st.sidebar.title("Basic Chatbot")
if st.sidebar.button("New chat"):
    reset_chat()
st.sidebar.header("My conversation")

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages=load_conversation(thread_id)

        temp_messages=[]

        for msg in messages:
            if isinstance(msg,HumanMessage):
                role='user'
            else :
                role='assistant'
            temp_messages.append({"role":role,'content':msg.content})
        st.session_state['chat_history']=temp_messages






# ================Main UI============

#loading chat conversation
for message in st.session_state['chat_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])




user_input=st.chat_input("type here")
CONFIG={'configurable': {'thread_id': st.session_state['thread_id']}}
if user_input:
    st.session_state['chat_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

  
    with st.chat_message('assistant'):
        assistant_message=st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )

    st.session_state['chat_history'].append({"role":'assistant','content':assistant_message})