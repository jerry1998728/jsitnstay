# app.py — Full Agentic Concierge App with Pinecone Retrieval
import streamlit as st
import time
import os
from pinecone import Pinecone
from router import route_message

# -------- CONFIG --------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "petsittingknowledge"

# ✅ Initialize Pinecone client (Modern way)
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(PINECONE_INDEX_NAME)

# -------- STREAMLIT SETTINGS --------
st.set_page_config(
    page_title="J.Sit & Stay Concierge",
    page_icon="🐾",
    layout="wide"
)

# ✅ Custom styling
st.markdown("""
<style>
    html, body, [class*="css"] {
        background-color: #FFFFFF;
        color: #FFFFFF;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, serif;
        font-size: 18px;
    }

    .chat-container {
        padding: 0.5rem 1rem;
        border-radius: 1.5rem;
        margin-bottom: 1rem;
        max-width: 100%;
        word-wrap: break-word;
        line-height: 1.6;
    }

    .chat-assistant {
        background-color: #262730;
        color: white;
        align-self: flex-start;
    }

    .chat-user {
        background-color: #f0f0f0;
        color: #1d1d1f;
        align-self: flex-end;
        margin-left: auto;
    }

    .chat-row {
        display: flex;
        flex-direction: row;
        margin-bottom: 1rem;
    }
    
    .block-container {
        padding-top: 1rem !important;
    }

    .side-img {
        position: fixed;
        z-index: 1;
        opacity: 0.92;
        animation: float 5s ease-in-out infinite;
    }

    .left-img {
        left: 1rem;
        bottom: 4rem;
        width: 140px;
    }

    .right-img {
        right: 1rem;
        top: 6rem;
        width: 160px;
    }

    .side-img img {
        width: 100%;
        height: auto;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    @keyframes float {
        0%   { transform: translateY(0px); }
        50%  { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
with st.container():
    st.markdown("""
        <div style='text-align: center; margin-top: 0rem; margin-bottom: 0rem;'>
            <h0 style='font-family: -apple-system, BlinkMacSystemFont, serif; font-size: 4rem;'>🐶🐱</h0>
            <h1 style='font-family: -apple-system, BlinkMacSystemFont, serif; font-size: 4rem;'>🐾 J.Sit & Stay 🐾</h1>
            <p style='font-family: -apple-system, BlinkMacSystemFont, serif; font-size: 2.5rem; margin-top: -0.5rem;'>🏠 Your Pet’s Home Away From Home 🏠</p>
            <hr style='margin-top: 1rem; margin-bottom: 1rem;'/>
        </div>
    """, unsafe_allow_html=True)

# -------- CHAT --------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.chat_history:
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "👋 Hello there! I’m the assistant for Jerry at J.Sit & Stay!<br>"
    })
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "Feel free to let me know if I can help you with anything! 😊<br><br>"
                   "You can say things like:<br>"
                   "- Tell me more about Jerry<br>"
                   "- How does Jerry manage conflicts<br>"
                   "- Help me book a stay<br>"
                   "- Ask any general questions about J.Sit & Stay!"
    })

# Chat bubble renderer
def render_bubble(message, sender="assistant"):
    css_class = "chat-assistant" if sender == "assistant" else "chat-user"
    st.markdown(
        f"<div class='chat-row'><div class='chat-container {css_class}'>{message}</div></div>",
        unsafe_allow_html=True
    )

# Render chat history
for msg in st.session_state.chat_history:
    render_bubble(msg["content"], sender=msg["role"])

# Input + reply handling
user_input = st.chat_input(
    "Ask your question here...",
    disabled=st.session_state.get("waiting_for_reply", False)
)

if user_input and not st.session_state.get("waiting_for_reply"):
    # Save user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    render_bubble(user_input, sender="user")
    st.session_state.waiting_for_reply = True

    # Process message
    with st.spinner("Just a second..."):
        reply = route_message(user_input)

    # Stream assistant reply with 🐶
    placeholder = st.empty()
    streamed_text = ""
    for i, token in enumerate(reply):
        streamed_text += token
        display_text = streamed_text + " 🐶" if i < len(reply) - 1 else streamed_text
        placeholder.markdown(
            f"<div class='chat-row'><div class='chat-container chat-assistant'>{display_text}</div></div>",
            unsafe_allow_html=True
        )
        time.sleep(0.025)

    # Save full reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.waiting_for_reply = False
