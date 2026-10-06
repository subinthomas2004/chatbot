"""
Pure Python Knowledge & Wikipedia-Powered Chatbot.
Zero external API key required!

Features:
1. Live Wikipedia Search:
   - Fetches real-time summaries for countries, people, science, concepts, history
2. Built-in Core Knowledge Base:
   - Covers Agentic AI, AI Agents, Python, Machine Learning, Groq, etc.
3. Safe math calculation & friendly greeting rules
"""

import re
import datetime
import wikipedia

# Core local knowledge base for quick, instant answers
KNOWLEDGE_BASE = {
    "agentic ai": (
        "🤖 **Agentic AI** refers to autonomous artificial intelligence systems designed to perceive their environment, "
        "reason, formulate multi-step plans, use tools and APIs, and execute actions independently to achieve goals."
    ),
    "ai agent": (
        "An **AI Agent** is an autonomous entity that perceives inputs from its environment, maintains memory/state, "
        "decides on sequential actions, and executes them using tools or code."
    ),
    "python": (
        "🐍 **Python** is a popular high-level programming language created by Guido van Rossum, famous for clean syntax "
        "and extensive libraries powering AI, Machine Learning, and Web Development."
    ),
    "machine learning": (
        "📊 **Machine Learning (ML)** is a branch of AI where algorithms learn patterns from data and improve their performance "
        "without being explicitly hardcoded."
    ),
    "groq": (
        "⚡ **Groq** is an AI hardware company known for LPUs (Language Processing Units) that run open-source LLMs at lightning-fast speeds."
    ),
    "streamlit": (
        "🎈 **Streamlit** is an open-source Python framework that allows developers to create interactive web applications "
        "directly from Python scripts without HTML, CSS, or JavaScript."
    ),
}

# Conversational rules for greetings, meta queries, etc.
GREETING_PATTERNS = r"\b(hi|hello|hey|greetings|howdy|vanakkam|namaste)\b"


def search_wikipedia(query: str, sentences: int = 3) -> str | None:
    """Queries live Wikipedia for real-world knowledge topics."""
    try:
        wikipedia.set_lang("en")
        search_results = wikipedia.search(query)
        if not search_results:
            return None
        best_title = search_results[0]
        summary = wikipedia.summary(best_title, sentences=sentences, auto_suggest=False)
        return f"🌐 **Wikipedia ({best_title})**:\n\n{summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            first_opt = e.options[0]
            summary = wikipedia.summary(first_opt, sentences=sentences, auto_suggest=False)
            return f"🌐 **Wikipedia ({first_opt})**:\n\n{summary}"
        except Exception:
            return None
    except Exception:
        return None


def evaluate_math(expression: str) -> str | None:
    """Safely evaluates basic arithmetic expressions."""
    cleaned = expression.strip()
    if re.fullmatch(r"^[0-9\.\s\+\-\*\/\(\)]+$", cleaned):
        try:
            result = eval(cleaned, {"__builtins__": None}, {})
            return f"🔢 **Calculation**: `{cleaned}` = **{result}**"
        except Exception:
            return None
    return None


def get_smart_python_response(user_input: str) -> str:
    """
    Evaluates user input through greetings, calculations,
    built-in knowledge base, and live Wikipedia search.
    """
    text = user_input.strip()
    lower_text = text.lower()

    # 1. Greetings
    if re.search(GREETING_PATTERNS, lower_text):
        return (
            "👋 **Hello!** I am your pure Python chatbot.\n\n"
            "You can ask me about:\n"
            "- 🌐 **General Knowledge via Wikipedia** (e.g. *'What is India?'*, *'Who is Elon Musk?'*)\n"
            "- 🤖 **AI Concepts** (e.g. *'What is Agentic AI?'*, *'What is Python?'*)\n"
            "- 🔢 **Calculations** (e.g. *'calc 45 * 12'*)"
        )

    if re.search(r"\b(who are you|what is your name)\b", lower_text):
        return "🤖 I am **PyBot**, a Python-native chatbot powered by built-in knowledge and live Wikipedia search. No external API key required!"

    if re.search(r"\b(time|date|what day is it)\b", lower_text):
        return f"🕒 Current local date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 2. Math evaluation
    calc_match = re.search(r"\b(?:calc|calculate|what is|compute)\s+([0-9\.\s\+\-\*\/\(\)]+)\b", lower_text)
    if calc_match:
        math_res = evaluate_math(calc_match.group(1))
        if math_res:
            return math_res

    # 3. Clean search query
    cleaned_query = re.sub(r"^(what is|who is|tell me about|explain|describe|search for|define)\s+", "", lower_text).strip()
    cleaned_query = cleaned_query.rstrip("?.!")

    # 4. Check Built-in Knowledge Base
    if cleaned_query in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[cleaned_query]

    for key, answer in KNOWLEDGE_BASE.items():
        if key in lower_text:
            return answer

    # 5. Live Wikipedia Search (fetches countries, personalities, science, etc.)
    wiki_query = cleaned_query if cleaned_query else text
    wiki_result = search_wikipedia(wiki_query)
    if wiki_result:
        return wiki_result

    # 6. Fallback
    return (
        f"🤔 I couldn't find a direct match for **'{text}'**.\n\n"
        "Try asking:\n"
        "- 🌐 *'What is India?'*\n"
        "- 🤖 *'What is Agentic AI?'*\n"
        "- 👤 *'Who is Alan Turing?'*\n"
        "- 🔢 *'calc 25 * 4'*"
    )
