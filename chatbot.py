"""
Groq-powered AI Chatbot - Core logic
Uses Groq's blazing-fast LLM inference to power conversations.
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_groq_client(api_key: str | None = None) -> Groq:
    """Create and return a Groq client.

    Args:
        api_key: Groq API key. If None, reads from GROQ_API_KEY env var.

    Returns:
        Configured Groq client.

    Raises:
        ValueError: If no API key is provided or found in environment.
    """
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        try:
            import streamlit as st
            if "GROQ_API_KEY" in st.secrets:
                key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass

    if not key or key == "your_groq_api_key_here":
        raise ValueError(
            "Groq API key not found. Please set GROQ_API_KEY in your .env file or Streamlit Cloud Secrets."
        )
    return Groq(api_key=key)


# System prompt that defines the chatbot's personality and behavior
SYSTEM_PROMPT = (
    "You are a friendly and helpful AI assistant. "
    "You give concise, accurate answers. "
    "If you don't know something, you say so honestly. "
    "You can help with coding, general knowledge, math, creative writing, and more."
)

# Available Groq models (fast & free-tier friendly)
AVAILABLE_MODELS = {
    "Qwen 3.8 27B (Best Quality)": "qwen/qwen3.8-27b",
    "GPT-OSS 20B (Fast)": "openai/gpt-oss-20b",
    "GPT-OSS 120B (Largest)": "openai/gpt-oss-120b",
}

# Default model used by the chatbot
DEFAULT_MODEL = "qwen/qwen3.8-27b"


def chat(
    client: Groq,
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """Send a chat request to Groq and return the assistant's response.

    Args:
        client: Groq client instance.
        messages: Conversation history as a list of {"role": ..., "content": ...} dicts.
        model: Model identifier to use.
        temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative).
        max_tokens: Maximum tokens in the response.

    Returns:
        The assistant's response text.
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def build_messages(
    conversation_history: list[dict],
    system_prompt: str = SYSTEM_PROMPT,
) -> list[dict]:
    """Build the full messages list including the system prompt.

    Args:
        conversation_history: List of user/assistant message dicts.
        system_prompt: The system instruction for the chatbot.

    Returns:
        Complete messages list with system prompt prepended.
    """
    return [{"role": "system", "content": system_prompt}] + conversation_history
