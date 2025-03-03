import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Function to call DeepSeek API
def get_deepseek_response(messages):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"model": "deepseek-chat", "messages": messages}
    response = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else f"⚠️ Error: {response.status_code} - {response.text}"

# Streamlit UI
st.set_page_config(page_title="DeepSeek AI Chatbot", page_icon="🤖", layout="wide")

# Initialize session state
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []  # Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today? 😊"}]
if "current_chat_index" not in st.session_state:
    st.session_state.current_chat_index = None  # Track selected chat

# Sidebar for chat history
st.sidebar.title("📜 Chat History")

# New chat button (appears at the top)
if st.sidebar.button("➕ New Chat", use_container_width=True):
    if st.session_state.messages:
        st.session_state.chat_sessions.insert(0, st.session_state.messages.copy())
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today? 😊"}]
    st.session_state.current_chat_index = None

# Display chat history
for i, session in enumerate(st.session_state.chat_sessions):
    chat_summary = session[1]["content"][:30] + "..." if len(session) > 1 else "New Chat"
    cols = st.sidebar.columns([6, 1])  # Increased width of chat titles
    if cols[0].button(chat_summary, key=f"chat_{i}", use_container_width=True):
        st.session_state.messages = session
        st.session_state.current_chat_index = i
    if cols[1].button("🗑", key=f"del_{i}", use_container_width=True):  # Changed to 'Delete' button
        del st.session_state.chat_sessions[i]
        st.rerun()

# Main chat UI
st.title("🤖 Gowtham AI Chatbot")
st.markdown("""
    <style>
        .stChatMessage {border-radius: 10px; padding: 10px; margin: 5px;}
        .stChatMessage[data-role="user"] {background-color: #d1e7fd;}
        .stChatMessage[data-role="assistant"] {background-color: #f1f3f4;}
    </style>
    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        start_time = time.time()
        response = get_deepseek_response(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        response_time = time.time() - start_time

# Display full chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="stChatMessage" data-role="{message["role"]}">{message["content"]}</div>', unsafe_allow_html=True)

# Show response time
if user_input:
    st.caption(f"Response time: {response_time:.2f}s")