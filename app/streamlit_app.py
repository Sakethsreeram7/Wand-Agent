import streamlit as st
import requests
import datetime

# from exception.exceptions import TradingBotException
import sys

BASE_URL = "http://localhost:8000"  # Backend endpoint

st.set_page_config(
    page_title="🌍 Travel Planner Agentic Application",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🌍 Travel Planner Agentic Application")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat history as a chat conversation
st.header("How can I help you in planning a trip? Let me know where do you want to visit.")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Chat input box at bottom

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("User Input", placeholder="e.g. Plan a trip to Goa for 5 days")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    try:
        # Add user message to conversation history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Prepare payload with full conversation
        payload = {"messages": st.session_state.messages}

        # Show thinking spinner while backend processes
        with st.spinner("Bot is thinking..."):
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            # Add assistant message to conversation history
            st.session_state.messages.append({"role": "assistant", "content": answer})
            # Rerun to show updated chat
            st.rerun()
        else:
            st.error(" Bot failed to respond: " + response.text)

    except Exception as e:
        st.error(f"The response failed due to {e}")