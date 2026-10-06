"""
Pure Python Rule-Based Chatbot (No API or external models required).
Demonstrates core concepts of NLP, intent recognition, regex pattern matching,
and stateful conversation logic purely in Python standard library.
"""

import re
import random
import datetime

# Pre-defined intent rules: list of (regex_patterns, list_of_responses)
RULES: list[tuple[list[str], list[str]]] = [
    (
        [r"\b(hi|hello|hey|greetings|howdy)\b"],
        [
            "Hello! I am your pure Python rule-based assistant. How can I help you today?",
            "Hey there! What would you like to explore or discuss?",
            "Greetings! I'm running directly in Python without any external API."
        ],
    ),
    (
        [r"\bhow are you\b", r"\bhow('s| is) it going\b"],
        [
            "I'm functioning smoothly and ready to assist you! How are you doing?",
            "All systems operational! How can I assist you with Python or AI topics today?"
        ],
    ),
    (
        [r"\bwhat is your name\b", r"\bwho are you\b"],
        [
            "I am PyBot, a rule-based conversational agent written in pure Python!",
            "You can call me PyBot. I process your text using regular expressions and rule-matching logic."
        ],
    ),
    (
        [r"\b(what is|explain) (agentic ai|agent)\b"],
        [
            "Agentic AI refers to systems where AI agents perceive their environment, reason, plan actions, use tools, and make decisions autonomously to achieve specified goals.",
            "An AI Agent is an autonomous entity that observes inputs, maintains state/memory, decides on a sequence of actions, and executes them to accomplish tasks."
        ],
    ),
    (
        [r"\b(what is|explain) python\b"],
        [
            "Python is a high-level, interpreted programming language famous for its readability, vast library ecosystem, and dominance in AI and data science.",
            "Python is widely used in Machine Learning, Web Development, and Automation due to its simple syntax and strong community."
        ],
    ),
    (
        [r"\btime\b", r"\bdate\b", r"\bwhat day is it\b"],
        [
            lambda: f"Current date and time is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ],
    ),
    (
        [r"\b(calc|calculate|what is)\s+([0-9\.\s\+\-\*\/\(\)]+)\b"],
        [
            # Dynamically handled in rule_based_response
        ],
    ),
    (
        [r"\b(joke|tell me a joke)\b"],
        [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why did the Python developer wear glasses? Because they couldn't C#!"
        ],
    ),
    (
        [r"\b(thank you|thanks)\b"],
        [
            "You're very welcome! Let me know if there's anything else I can do.",
            "Happy to help anytime!"
        ],
    ),
    (
        [r"\b(bye|goodbye|see you|exit)\b"],
        [
            "Goodbye! Have a great time learning Agentic AI!",
            "See you later! Keep coding and exploring."
        ],
    ),
]

FALLBACK_RESPONSES = [
    "That's an interesting question! Since I'm a rule-based Python bot, I match specific patterns. Try asking about Agentic AI, Python, calculations, time, or tell me 'hello'!",
    "I haven't been programmed with a rule for that specific phrasing yet. Try asking 'What is Agentic AI?', 'Tell me a joke', or simple math!",
    "I didn't quite catch that. As a pure Python pattern matcher, I look for key phrases like 'who are you', 'what is python', or 'calculate 15 * 4'."
]


def evaluate_math(expression: str) -> str | None:
    """Safely evaluates basic arithmetic expressions."""
    cleaned = expression.strip()
    if re.fullmatch(r"^[0-9\.\s\+\-\*\/\(\)]+$", cleaned):
        try:
            result = eval(cleaned, {"__builtins__": None}, {})
            return f"Result: {cleaned} = {result}"
        except Exception:
            return None
    return None


def get_rule_based_response(user_input: str) -> str:
    """
    Evaluates user input through regex patterns and returns a suitable response.
    """
    text = user_input.strip()
    lower_text = text.lower()

    # Check for direct calculation
    calc_match = re.search(r"\b(?:calc|calculate|what is)\s+([0-9\.\s\+\-\*\/\(\)]+)\b", lower_text)
    if calc_match:
        expr = calc_match.group(1)
        res = evaluate_math(expr)
        if res:
            return res

    # Check pre-defined pattern rules
    for patterns, responses in RULES:
        for pattern in patterns:
            if re.search(pattern, lower_text):
                chosen = random.choice(responses)
                if callable(chosen):
                    return chosen()
                return chosen

    return random.choice(FALLBACK_RESPONSES)
