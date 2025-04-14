import streamlit as st
import datetime
import json
import os
from chatbot_logic import get_response

HISTORY_FILE = "chat_history.json"

# --- Load chat history if exists ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# --- Save chat history ---
def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)

# Page config
st.set_page_config(page_title="🤖 AI Chatbot", layout="centered")
st.title("🤖 AI Chatbot")
st.markdown("Welcome to your AI-powered chatbot! Just type a message below to start chatting.")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = load_history()

# Handle input submission and clearing
def submit_input():
    st.session_state.submitted_input = st.session_state.input
    st.session_state.input = ""

st.text_input("You:", key="input", on_change=submit_input)

# Bot logic
if "submitted_input" in st.session_state:
    user_input = st.session_state.submitted_input
    user_input_lower = user_input.lower()

    # Rule-based responses
    if "day" in user_input_lower and "today" in user_input_lower:
        response = f"📅 Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
    elif "time" in user_input_lower:
        response = f"⏰ The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    else:
        with st.spinner("🤖 Bot is typing..."):
            response = get_response(user_input)

    # Update history
    st.session_state.history.append({"user": user_input, "bot": response})
    save_history(st.session_state.history)  # Save after each message
    del st.session_state.submitted_input

# Stylish chat
if st.session_state.history:
    for msg in st.session_state.history:
        st.markdown(f"""
        <div style="background-color:#f0f0f5;padding:10px;border-radius:10px;margin-bottom:5px;">
            <b>🙂 You:</b> {msg['user']}
        </div>
        <div style="background-color:#e8f4fd;padding:10px;border-radius:10px;margin-bottom:10px;">
            <b>🤖 Bot:</b> {msg['bot']}
        </div>
        """, unsafe_allow_html=True)

# Scrollable chat history
with st.container():
    st.markdown("""
    <style>
    .scrollable-chat {
        max-height: 400px;
        overflow-y: auto;
        padding-right: 15px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("### Chat History")
        chat_html = '<div class="scrollable-chat">'
        for msg in st.session_state.history:
            chat_html += f"<p><strong>You:</strong> {msg['user']}</p>"
            chat_html += f"<p><strong>Bot:</strong> {msg['bot']}</p><hr>"
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

# Download button
if st.session_state.history:
    chat_history_text = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in st.session_state.history])
    st.download_button(
        label="📄 Download Conversation",
        data=chat_history_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# Clear Chat Button
if st.session_state.history:
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []  # clear in-memory history

        # Also clear JSON file if it exists
        if os.path.exists("chat_history.json"):
            with open("chat_history.json", "w") as f:
                f.write("[]")  # write empty JSON array

        st.rerun()  # refresh UI