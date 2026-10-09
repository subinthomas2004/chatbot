"""
Pure Python Knowledge & Wikipedia-Powered Chatbot.
Zero external API key required!

Features:
1. Live Wikipedia Search:
   - Uses reliable Wikipedia REST API with proper User-Agent headers
   - Handles real-world questions, acronyms (e.g. 'pm of india' -> Prime Minister of India)
2. Built-in Core Knowledge Base:
   - Covers Indian Civics (PM, President, Chief Ministers), AI Concepts, Tech Stack
3. Safe math calculation & conversational rules
"""

import re
import datetime
import urllib.parse
import requests

HEADERS = {
    "User-Agent": "StudentAgenticAIChatbot/1.0 (educational-use)"
}

# Core curated knowledge base for instant, accurate answers
KNOWLEDGE_BASE = {
    "pm of india": (
        "🇮🇳 **Prime Minister of India**: The Prime Minister of India is the head of the government of India. "
        "The current Prime Minister is **Narendra Modi** (in office since May 2014)."
    ),
    "prime minister of india": (
        "🇮🇳 **Prime Minister of India**: The Prime Minister of India is the head of the government of India. "
        "The current Prime Minister is **Narendra Modi** (in office since May 2014)."
    ),
    "president of india": (
        "🇮🇳 **President of India**: The President of India is the head of state of the Republic of India. "
        "The current President is **Droupadi Murmu** (in office since July 2022)."
    ),
    "chief minister of india": (
        "🇮🇳 In India, there is no single 'Chief Minister of India'. Instead, each of India's 28 States and 3 Union Territories (with legislatures) has its own **Chief Minister (CM)** who serves as the head of government for that specific state (e.g., CM of Kerala, CM of Tamil Nadu, CM of Maharashtra)."
    ),
    "cheif minister of india": (
        "🇮🇳 In India, there is no single 'Chief Minister of India'. Instead, each of India's 28 States and 3 Union Territories has its own **Chief Minister (CM)** who is the elected head of state government (e.g., CM of Kerala, CM of Karnataka, CM of Delhi). The head of the central national government is the **Prime Minister**."
    ),
    "india": (
        "🇮🇳 **India** (Republic of India) is the world's most populous nation and the largest democracy, located in South Asia. "
        "Capital: New Delhi. Prime Minister: Narendra Modi. President: Droupadi Murmu."
    ),
    "agentic ai": (
        "🤖 **Agentic AI** refers to autonomous artificial intelligence systems designed to perceive their environment, "
        "reason, plan multi-step workflows, use external tools & APIs, and execute actions independently to achieve goals."
    ),
    "ai agent": (
        "An **AI Agent** is an autonomous entity that perceives inputs from its environment, maintains state and memory, "
        "reasons about goals, and executes concrete actions using tools or APIs."
    ),
    "python": (
        "🐍 **Python** is a popular high-level, general-purpose programming language created by Guido van Rossum. "
        "It is famous for readable syntax and vast ecosystems in AI, Machine Learning, Automation, and Web Development."
    ),
    "machine learning": (
        "📊 **Machine Learning (ML)** is a subset of AI where computational models learn patterns from training data "
        "to make predictions without explicit step-by-step programming."
    ),
    "groq": (
        "⚡ **Groq** is an AI hardware company known for LPUs (Language Processing Units) that run open-source LLMs "
        "at ultra-fast speeds exceeding hundreds of tokens per second."
    ),
    "streamlit": (
        "🎈 **Streamlit** is an open-source Python framework that turns data and AI scripts into responsive, "
        "clean web applications without requiring frontend HTML/CSS/JavaScript."
    ),
}

GREETING_PATTERNS = r"\b(hi|hello|hey|greetings|howdy|vanakkam|namaste)\b"


def search_wikipedia(query: str, sentences: int = 3) -> str | None:
    """
    Searches Wikipedia using Wikipedia's robust REST & Query APIs with custom User-Agent.
    """
    try:
        clean_q = query.strip()
        if not clean_q:
            return None

        # Step 1: Query search API to find best matching article title
        encoded_q = urllib.parse.quote(clean_q)
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_q}&utf8=&format=json&srlimit=3"
        resp = requests.get(search_url, headers=HEADERS, timeout=6)
        
        if resp.status_code != 200:
            return None
            
        data = resp.json()
        search_hits = data.get("query", {}).get("search", [])
        if not search_hits:
            return None

        best_title = search_hits[0]["title"]

        # Step 2: Fetch clean summary from Wikipedia REST API
        encoded_title = urllib.parse.quote(best_title.replace(" ", "_"))
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
        summary_resp = requests.get(summary_url, headers=HEADERS, timeout=6)

        if summary_resp.status_code == 200:
            sum_data = summary_resp.json()
            extract = sum_data.get("extract", "")
            if extract:
                # Limit to desired sentences
                sentence_list = re.split(r'(?<=[.!?])\s+', extract)
                shortened = " ".join(sentence_list[:sentences])
                return f"🌐 **Wikipedia ({best_title})**:\n\n{shortened}"

        # Fallback to snippet from search hit if REST summary didn't return
        snippet = re.sub(r'<[^>]+>', '', search_hits[0].get("snippet", ""))
        if snippet:
            return f"🌐 **Wikipedia ({best_title})**:\n\n{snippet}..."

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
    Evaluates user input through:
    1. Greeting rules
    2. Math evaluation
    3. Curated knowledge base (Civics, Tech, AI)
    4. Live Wikipedia REST Search
    5. Fallback guide
    """
    text = user_input.strip()
    lower_text = text.lower()

    # 1. Greetings & Meta
    if re.search(GREETING_PATTERNS, lower_text):
        return (
            "👋 **Hello!** I am your pure Python chatbot.\n\n"
            "Ask me anything:\n"
            "- 🌐 **Current Affairs & General Knowledge** (e.g. *'PM of India'*, *'What is India'*, *'Who is Elon Musk'*)\n"
            "- 🤖 **AI Concepts** (e.g. *'What is Agentic AI'*, *'What is Machine Learning'*)\n"
            "- 🔢 **Calculations** (e.g. *'calc 85 * 12'*)"
        )

    if re.search(r"\b(who are you|what is your name)\b", lower_text):
        return "🤖 I am **PyBot**, an AI chatbot running in pure Python with live Wikipedia and knowledge retrieval!"

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

    # 4. Check Knowledge Base
    if cleaned_query in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[cleaned_query]

    for key, answer in KNOWLEDGE_BASE.items():
        if key in lower_text or lower_text in key:
            return answer

    # 5. Live Wikipedia Search
    wiki_query = cleaned_query if cleaned_query else text
    wiki_result = search_wikipedia(wiki_query)
    if wiki_result:
        return wiki_result

    # 6. Fallback
    return (
        f"🤔 I couldn't find a direct match for **'{text}'**.\n\n"
        "Try asking:\n"
        "- 🌐 *'PM of India'* or *'What is India'* \n"
        "- 👤 *'Who is Elon Musk'* or *'Who is APJ Abdul Kalam'* \n"
        "- 🤖 *'What is Agentic AI'* \n"
        "- 🔢 *'calc 25 * 4'*"
    )
