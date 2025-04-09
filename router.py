from agents.concierge_agent import concierge_agent
from agents.booking_manager import booking_manager
from agents.public_relations import public_relations
import streamlit as st

def route_message(message: str) -> str:
    message_lower = message.lower()

    # Initialize agent and lock state
    if "active_agent" not in st.session_state:
        st.session_state.active_agent = None
    if "waiting_for_reply" not in st.session_state:
        st.session_state.waiting_for_reply = False

    # ----------------------- Booking Agent Logic -----------------------
    if any(keyword in message_lower for keyword in ["book", "schedule", "appointment"]) or st.session_state.active_agent == "booking":
        st.session_state.active_agent = "booking"
        st.session_state.waiting_for_reply = True
        reply = booking_manager(message)

        # Release booking agent if booking is completed
        if "booking_state" in st.session_state and st.session_state.booking_state.get("completed"):
            st.session_state.active_agent = None

        st.session_state.waiting_for_reply = False
        return reply

    # ----------------------- Public Relations Logic -----------------------
    elif any(keyword in message_lower for keyword in ["payment", "discount", "cheaper", "venmo", "zelle", "pay"]):
        st.session_state.active_agent = "public_relations"
        st.session_state.waiting_for_reply = True
        reply = public_relations(message)
        st.session_state.waiting_for_reply = False
        return reply

    # ----------------------- Concierge Fallback -----------------------
    else:
        st.session_state.active_agent = "concierge"
        st.session_state.waiting_for_reply = True
        reply = concierge_agent(message)
        st.session_state.waiting_for_reply = False
        return reply
