"""
Streamlit Web UI for the Groq-powered Chatbot
Run with: streamlit run app.py
"""

import streamlit as st
from chatbot import get_groq_client, chat, build_messages

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# ── Hide Streamlit default menu & footer for a cleaner look ─────────────────
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        max-width: 800px;
    }
    div[data-testid="stChatMessage"] {
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Initialize Groq client (loads API key from .env automatically) ──────────
@st.cache_resource
def load_client():
    return get_groq_client()

client = load_client()

# ── Main Chat Area ──────────────────────────────────────────────────────────
st.title("🤖 AI Chatbot")
st.caption("Ask me anything!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
if user_input := st.chat_input("Type your message here..."):
    # Display user message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_input)

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                full_messages = build_messages(st.session_state.messages)
                response = chat(client=client, messages=full_messages)
                st.markdown(response)
            except Exception as e:
                response = f"❌ Something went wrong. Please try again."
                st.error(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
