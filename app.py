"""
Streamlit Web UI for the Multi-Mode Chatbot:
Tab 1: 🤖 AI Chatbot (Groq API) - Fast LLM Powered
Tab 2: 🐍 Python Native Chatbot - Pure Python Rule-Based (No API needed)
Run with: streamlit run app.py
"""

import streamlit as st
from chatbot import get_groq_client, chat, build_messages
from python_bot import get_rule_based_response

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 Multi-Mode AI Chatbot",
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
        padding-top: 1.5rem;
        max-width: 800px;
    }
    div[data-testid="stChatMessage"] {
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        font-weight: 600;
        border-radius: 8px 8px 0px 0px;
        padding: 0 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Initialize Groq client (loads API key from .env automatically) ──────────
@st.cache_resource
def load_client():
    try:
        return get_groq_client()
    except Exception:
        return None

client = load_client()

# ── Top Header ──────────────────────────────────────────────────────────────
st.title("🤖 Chatbot Suite")
st.caption("Select your preferred mode using the tabs below:")

# ── Top Two Tabs: Option 1 (Groq API) vs Option 2 (Python Native) ──────────
tab_groq, tab_python = st.tabs(["⚡ AI Chatbot (Groq API)", "🐍 Python Native Chatbot"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1: Groq API Chatbot
# ════════════════════════════════════════════════════════════════════════════
with tab_groq:
    st.subheader("⚡ Groq LLM Assistant")
    st.caption("Powered by cloud LLM inference using Groq API.")

    # Initialize chat history for Groq bot
    if "groq_messages" not in st.session_state:
        st.session_state.groq_messages = []

    # Display existing messages
    for msg in st.session_state.groq_messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat input for Groq bot
    if groq_user_input := st.chat_input("Ask the Groq AI anything...", key="groq_input"):
        # Display user message
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(groq_user_input)

        st.session_state.groq_messages.append({"role": "user", "content": groq_user_input})

        # Generate assistant response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                try:
                    if not client:
                        client = load_client()
                    full_messages = build_messages(st.session_state.groq_messages)
                    response = chat(client=client, messages=full_messages)
                    st.markdown(response)
                except Exception as e:
                    response = "❌ Something went wrong with the Groq API. Please check your connection or key."
                    st.error(response)

        st.session_state.groq_messages.append({"role": "assistant", "content": response})

    # Clear conversation button for Tab 1
    if st.session_state.groq_messages:
        if st.button("🗑️ Clear Groq Chat", key="clear_groq"):
            st.session_state.groq_messages = []
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# TAB 2: Pure Python Native Chatbot (Rule/Pattern-Based, No API required)
# ════════════════════════════════════════════════════════════════════════════
with tab_python:
    st.subheader("🐍 Pure Python Chatbot")
    st.caption("Runs locally with pure Python standard logic (Regex pattern matching & rule engine). No external API needed.")

    # Initialize chat history for Python bot
    if "python_messages" not in st.session_state:
        st.session_state.python_messages = []

    # Display existing messages
    for msg in st.session_state.python_messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🐍"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat input for Python bot
    if python_user_input := st.chat_input("Type a message for Python Bot (e.g. 'hello', 'what is agentic ai', 'calc 25*4')...", key="python_input"):
        # Display user message
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(python_user_input)

        st.session_state.python_messages.append({"role": "user", "content": python_user_input})

        # Generate rule-based response
        with st.chat_message("assistant", avatar="🐍"):
            response = get_rule_based_response(python_user_input)
            st.markdown(response)

        st.session_state.python_messages.append({"role": "assistant", "content": response})

    # Clear conversation button for Tab 2
    if st.session_state.python_messages:
        if st.button("🗑️ Clear Python Chat", key="clear_python"):
            st.session_state.python_messages = []
            st.rerun()
