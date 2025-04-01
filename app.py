# app_with_rag.py — Full Agentic Concierge App with Pinecone Retrieval (concierge_agent)
import streamlit as st
import time
import json
from openai import OpenAI
from pinecone import Pinecone
import numpy as np
import pinecone as pc
import os


# -------- CONFIG --------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_WQ1Rkuhpgr0HUYNd9SNMVrzs"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "petsittingknowledge"

client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(PINECONE_INDEX_NAME)

import streamlit as st
from router import route_message

st.set_page_config(
    page_title="J.Sit & Stay Concierge",
    page_icon="🐾",
    layout= "centered"
)

# Apple-inspired full white styling and chat bubbles
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
        margin-bottom: 1 rem;
        max-width: %;
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
        margin-bottom: 1rem;  /* Add spacing between messages */
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




</style>
""", unsafe_allow_html=True)



# Apple-style header – adjusted for tighter top margin
with st.container():
    st.markdown("""
        <!-- Header Section -->
        <div style='text-align: center; margin-top: 0rem; margin-bottom: 0rem;'>
            <h0 style='font-family: -apple-system, BlinkMacSystemFont, serif; font-size: 4rem;'>🐶🐱</h1>
            <h1 style='font-family: -apple-system, BlinkMacSystemFont, serif; font-size: 4rem;'>🐾 J.Sit & Stay 🐾</h1>
            <p style='font-family: -apple-system, BlinkMacSystemFont, serif; font-size: 2.5rem; margin-top: -0.5rem;'>🏠 Your Pet’s Home Away From Home 🏠</p>
            <hr style='margin-top: 1rem; margin-bottom: 1rem;'/>
        </div>
    """, unsafe_allow_html=True)



#Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.chat_history:
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "👋 Hello there! I’m the assistant for Jerry at J.Sit & Stay!<br>"
                
            })
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": 
                   "Feel free to let me know if I can help you with anything!😊<br><br>"
                   "You can say things like:<br>"
                   "- Tell me more about Jerry<br>"
                   "- Help me book a stay<br>"
                   "- Ask any general questions about J.Sit & Stay!"

    })



#Chat bubble renderer
def render_bubble(message, sender="assistant"):
    css_class = "chat-assistant" if sender == "assistant" else "chat-user"
    st.markdown(
        f"<div class='chat-row'><div class='chat-container {css_class}'>{message}</div></div>",
        unsafe_allow_html=True
    )

#Render bubbles from chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    render_bubble(msg["content"], sender=msg["role"])

import time

# Input + reply handling
user_input = st.chat_input(
    "Ask your question here...",
    disabled=st.session_state.get("waiting_for_reply", False)
)

# Only process once per turn
if user_input and (not st.session_state.get("waiting_for_reply")):
    # Save user input and render it
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    render_bubble(user_input, sender="user")
    st.session_state.waiting_for_reply = True  # lock reply state

    # Process user message → get assistant reply
    with st.spinner("Just a second..."):
        reply = route_message(user_input)

    # Stream assistant reply token by token with placeholder 🐶
    placeholder = st.empty()
    streamed_text = ""

    for i, token in enumerate(reply):
        streamed_text += token
        # Add 🐶 only while streaming, remove at the last token
        display_text = streamed_text + " 🐶" if i < len(reply) - 1 else streamed_text
        placeholder.markdown(
            f"<div class='chat-row'><div class='chat-container chat-assistant'>{display_text}</div></div>",
            unsafe_allow_html=True
        )
        time.sleep(0.025)  # adjust speed if desired

    # Save full assistant reply to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.waiting_for_reply = False  # unlock
