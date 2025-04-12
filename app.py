import streamlit as st
import datetime
from chatbot_logic import get_response

# Page config
st.set_page_config(page_title="🤖 AI Chatbot", layout="centered")
st.title("🤖 AI Chatbot")
st.markdown("Welcome to your AI-powered chatbot! Just type a message below to start chatting.")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", key="input")

# Bot logic
if user_input:
    user_input_lower = user_input.lower()

    # Handle real-world questions manually
    if "day" in user_input_lower and "today" in user_input_lower:
        response = f"📅 Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
    elif "time" in user_input_lower:
        response = f"⏰ The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    else:
        response = get_response(user_input)

    # Add to chat history
    st.session_state.history.append({"user": user_input, "bot": response})

# Show chat history
if st.session_state.history:
    st.write("### Chat History")
    for msg in st.session_state.history:
        st.markdown(f"**You:** {msg['user']}")
        st.markdown(f"**Bot:** {msg['bot']}")

# Add Download Button for Conversation History
if st.session_state.history:
    chat_history_text = "\n".join([f"You: {msg['user']}\nBot: {msg['bot']}" for msg in st.session_state.history])
    
    st.download_button(
        label="Download Conversation",
        data=chat_history_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )
