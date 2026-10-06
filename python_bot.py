"""
Pure Python Knowledge & Rule-Based Chatbot (No external API needed).
Features:
- Typo tolerance (handles typos like 'agnetic ai' -> 'agentic ai')
- Rich built-in knowledge base (Countries, India, AI, Tech, General Knowledge)
- Math expressions & time evaluation
- Pattern and keyword based semantic matching
"""

import re
import random
import datetime
import difflib

# Knowledge Base for direct topic lookups & general knowledge
KNOWLEDGE_BASE = {
    "india": (
        "🇮🇳 **India** (Republic of India) is a country in South Asia. "
        "It is the world's most populous country, the seventh-largest country by area, "
        "and the most populous democracy in the world. Capital: New Delhi. National language/official languages: Hindi and English, alongside 22 scheduled languages."
    ),
    "agentic ai": (
        "🤖 **Agentic AI** refers to advanced artificial intelligence systems designed to act autonomously. "
        "Unlike standard chatbots that only reply with text, an AI Agent can reason, make decisions, plan workflows, use external tools (like search, calculators, databases), and perform tasks step-by-step to achieve a goal."
    ),
    "ai agent": (
        "An **AI Agent** is an autonomous entity that perceives its environment, makes decisions based on goals, maintains memory/state, and takes concrete actions using tools or APIs."
    ),
    "python": (
        "🐍 **Python** is a popular high-level, general-purpose programming language created by Guido van Rossum. "
        "It is renowned for clean syntax, ease of learning, and powerful libraries in AI, Data Science, Web Development, and Automation."
    ),
    "machine learning": (
        "📊 **Machine Learning (ML)** is a subset of AI where algorithms learn patterns from data and improve their performance on tasks without being explicitly hardcoded."
    ),
    "deep learning": (
        "🧠 **Deep Learning** is a branch of machine learning based on multi-layered artificial neural networks, powering image recognition, speech synthesis, and modern LLMs."
    ),
    "groq": (
        "⚡ **Groq** is an AI infrastructure company famous for its LPU (Language Processing Unit), which runs open-source LLMs at blazing-fast speeds (hundreds of tokens per second)."
    ),
    "streamlit": (
        "🎈 **Streamlit** is an open-source Python framework that lets developers turn data scripts and AI models into interactive web applications with zero front-end (HTML/CSS/JS) code needed."
    ),
}

# Conversational & Intent Rules
RULES = [
    (
        [r"\b(hi|hello|hey|greetings|howdy|vanakkam|namaste)\b"],
        [
            "Hello! I am your local Python chatbot. How can I assist you today?",
            "Hey! What would you like to know about? Feel free to ask about Python, AI, India, or test out a calculation!",
            "Greetings! I'm running locally in Python with zero external API dependencies."
        ],
    ),
    (
        [r"\bhow are you\b", r"\bhow('s| is) it going\b"],
        [
            "I'm operating smoothly and ready to assist you! How are you doing?",
            "Doing great! Ready to answer your questions on AI, Python, or anything you'd like to ask."
        ],
    ),
    (
        [r"\b(who are you|what is your name)\b"],
        [
            "I am PyBot, a smart Python-native chatbot built using pattern matching, knowledge retrieval, and rule execution!",
            "You can call me PyBot! I execute fully on Python standard libraries without needing external API keys."
        ],
    ),
    (
        [r"\btime\b", r"\bdate\b", r"\bwhat day is it\b"],
        [
            lambda: f"🕒 Current local date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ],
    ),
    (
        [r"\b(joke|tell me a joke)\b"],
        [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why did the Python programmer get spectacles? Because they couldn't C#! 👓"
        ],
    ),
    (
        [r"\b(thank you|thanks)\b"],
        [
            "You're very welcome! Let me know if there's anything else I can answer.",
            "Glad I could help! 😊"
        ],
    ),
    (
        [r"\b(bye|goodbye|see you|exit)\b"],
        [
            "Goodbye! Best of luck with your Agentic AI course!",
            "Catch you later! Keep building great projects in Python."
        ],
    ),
]

FALLBACKS = [
    "I'm a local Python knowledge bot. Try asking me about: 'What is India?', 'What is Agentic AI?', 'What is Python?', simple math like 'calc 50 * 4', or tell me 'hello'!",
    "I didn't find an exact match for that, but feel free to ask about countries, Agentic AI, Machine Learning, or math operations!",
    "That's outside my current rule set. Try asking: 'What is Agentic AI?', 'Who are you?', 'Tell me a joke', or 'What time is it?'"
]


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


def get_rule_based_response(user_input: str) -> str:
    """
    Evaluates user input through typo correction, knowledge base lookups, 
    regex patterns, and safe mathematical evaluation.
    """
    text = user_input.strip()
    lower_text = text.lower()

    # 1. Math Calculation check
    calc_match = re.search(r"\b(?:calc|calculate|what is|compute)\s+([0-9\.\s\+\-\*\/\(\)]+)\b", lower_text)
    if calc_match:
        res = evaluate_math(calc_match.group(1))
        if res:
            return res

    # 2. Knowledge Base check with typo tolerance (e.g. 'agnetic ai' -> 'agentic ai')
    # Strip common leading question prefixes
    cleaned_query = re.sub(r"^(what is|who is|tell me about|explain|describe)\s+", "", lower_text).strip()
    cleaned_query = cleaned_query.rstrip("?.!")

    # Check exact match in knowledge base
    if cleaned_query in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[cleaned_query]

    # Check fuzzy similarity with knowledge base keys (handles typos like 'agnetic ai')
    best_matches = difflib.get_close_matches(cleaned_query, KNOWLEDGE_BASE.keys(), n=1, cutoff=0.7)
    if best_matches:
        matched_key = best_matches[0]
        return KNOWLEDGE_BASE[matched_key]

    # Keyword search inside knowledge base
    for key, answer in KNOWLEDGE_BASE.items():
        if key in lower_text:
            return answer

    # 3. Conversational Regex Rules
    for patterns, responses in RULES:
        for pattern in patterns:
            if re.search(pattern, lower_text):
                chosen = random.choice(responses)
                if callable(chosen):
                    return chosen()
                return chosen

    # 4. Fallback response
    return random.choice(FALLBACKS)
