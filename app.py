"""
Streamlit Web UI for the Multi-Mode Chatbot:
Tab 1: ⚡ AI Chatbot (Groq API) - Fast LLM Powered
Tab 2: 🐍 Python Native Chatbot - Wikipedia & Knowledge Powered (No API key needed)
Run with: streamlit run app.py
"""

import streamlit as st
from chatbot import get_groq_client, chat, build_messages
from python_bot import get_smart_python_response

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Modern, Clean, Professional UI Styling ──────────────────────────────────
st.markdown(
    """
    <style>
    /* Global & background polish */
    #MainMenu, footer, header {visibility: hidden;}
    
    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 7rem;
        margin: 0 auto;
    }

    /* Top banner */
    .app-header {
        text-align: center;
        padding: 1rem 0 1.5rem 0;
    }
    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .app-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        background-color: #1E293B;
        padding: 0.35rem;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 8px;
        padding: 0 1.5rem;
        color: #94A3B8;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
    }

    /* Chat Messages styling */
    div[data-testid="stChatMessage"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Empty state welcome card */
    .welcome-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px dashed #475569;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 2rem 0;
    }
    .welcome-card h3 {
        color: #F1F5F9;
        margin-bottom: 0.5rem;
    }
    .welcome-card p {
        color: #94A3B8;
        font-size: 0.95rem;
    }

    /* Pin chat input cleanly to the bottom */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 1.5rem;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 860px;
        z-index: 999;
        background: transparent;
        padding: 0 1rem;
    }
    div[data-testid="stChatInput"] > div {
        background-color: #0F172A;
        border: 1.5px solid #3B82F6;
        border-radius: 14px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Initialize Groq Client ──────────────────────────────────────────────────
@st.cache_resource
def load_client():
    try:
        return get_groq_client()
    except Exception:
        return None

client = load_client()

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">🤖 AI Chatbot Suite</div>
        <div class="app-subtitle">Built for Agentic AI • Dual Engine: Groq LLM & Pure Python</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Navigation Tabs ─────────────────────────────────────────────────────────
tab_groq, tab_python = st.tabs(["⚡ AI Chatbot (Groq API)", "🐍 Python Native Chatbot"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1: Groq API Chatbot
# ════════════════════════════════════════════════════════════════════════════
with tab_groq:
    if "groq_messages" not in st.session_state:
        st.session_state.groq_messages = []

    # Display welcome card when chat is empty
    if not st.session_state.groq_messages:
        st.markdown(
            """
            <div class="welcome-card">
                <h3>⚡ Cloud LLM Engine</h3>
                <p>Powered by Groq's high-speed LPU inference engine. Ask coding, reasoning, or open-ended questions.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Render conversation history
    for msg in st.session_state.groq_messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Clear chat button
    if st.session_state.groq_messages:
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("🗑️ Clear", key="clear_groq", use_container_width=True):
                st.session_state.groq_messages = []
                st.rerun()

    # Chat Input (Pinned to bottom)
    if groq_user_input := st.chat_input("Ask the Groq AI anything...", key="groq_input"):
        st.session_state.groq_messages.append({"role": "user", "content": groq_user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(groq_user_input)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Generating answer..."):
                try:
                    if not client:
                        client = load_client()
                    full_messages = build_messages(st.session_state.groq_messages)
                    response = chat(client=client, messages=full_messages)
                    st.markdown(response)
                except Exception:
                    response = "❌ Groq API error. Please verify your internet connection or API key."
                    st.error(response)

        st.session_state.groq_messages.append({"role": "assistant", "content": response})
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# TAB 2: Python Native Chatbot (Zero API Key, Wikipedia & Knowledge)
# ════════════════════════════════════════════════════════════════════════════
with tab_python:
    if "python_messages" not in st.session_state:
        st.session_state.python_messages = []

    # Display welcome card when chat is empty
    if not st.session_state.python_messages:
        st.markdown(
            """
            <div class="welcome-card">
                <h3>🐍 Python Native Engine</h3>
                <p>Runs locally in Python with live Wikipedia search and built-in knowledge. <b>No API key required!</b></p>
                <p style="font-size:0.85rem; color:#64748B;">Try: <i>"PM of India"</i> • <i>"What is India"</i> • <i>"Who is Elon Musk"</i> • <i>"calc 75 * 12"</i></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Render conversation history
    for msg in st.session_state.python_messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🐍"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Clear chat button
    if st.session_state.python_messages:
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("🗑️ Clear", key="clear_python", use_container_width=True):
                st.session_state.python_messages = []
                st.rerun()

    # Chat Input (Pinned to bottom)
    if python_user_input := st.chat_input("Ask Python Bot (e.g. 'PM of India', 'Who is Elon Musk', 'What is Python')...", key="python_input"):
        st.session_state.python_messages.append({"role": "user", "content": python_user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(python_user_input)

        with st.chat_message("assistant", avatar="🐍"):
            with st.spinner("Searching knowledge base & Wikipedia..."):
                response = get_smart_python_response(python_user_input)
                st.markdown(response)

        st.session_state.python_messages.append({"role": "assistant", "content": response})
        st.rerun()
