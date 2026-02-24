"""
chatbot.py — VAYU AI
Session-state conversation management for VAYU AI chatbot.
Uses NVIDIA Kimi K2 AI via gemini_explainer.py
"""

import streamlit as st
from gemini_explainer import chat_with_vayu


def init_chat_session():
    """Initialize chat history in Streamlit session state."""
    if "vayu_chat_history" not in st.session_state:
        st.session_state.vayu_chat_history = []


def add_user_message(text: str):
    st.session_state.vayu_chat_history.append({"role": "user", "content": text})


def add_bot_message(text: str):
    st.session_state.vayu_chat_history.append({"role": "assistant", "content": text})


def get_chat_response(question: str, city: str, aqi_data: dict) -> str:
    """Get chatbot response using NVIDIA Kimi K2 and update session history."""
    response = chat_with_vayu(
        history=st.session_state.vayu_chat_history,
        question=question,
        city=city,
        aqi_data=aqi_data,
    )
    return response


def clear_chat():
    st.session_state.vayu_chat_history = []


def render_chat_messages():
    """Render all chat messages with custom styling."""
    for msg in st.session_state.vayu_chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
