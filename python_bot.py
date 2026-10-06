"""
Pure Python Knowledge, RAG, and Wikipedia-Augmented Chatbot.
Zero external API key required!

Features:
1. Local Document RAG (Retrieval-Augmented Generation):
   - Users can load text documents or course notes
   - Splits into chunks, vectors them with TF-IDF, finds top relevant paragraphs using Cosine Similarity
2. Live Wikipedia Search:
   - Fetches real-time summaries for any person, country, event, concept, science, history
3. Safe math calculation & greeting handling
"""

import re
import datetime
import wikipedia
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Default local knowledge base for RAG (Course / AI concepts)
DEFAULT_LOCAL_DOCS = [
    "Agentic AI is an autonomous paradigm in artificial intelligence where agents perceive environments, formulate multi-step plans, invoke tools and APIs, reflect on outputs, and execute actions to reach specified goals.",
    "A typical AI Agent architecture consists of four primary components: Profile (agent persona/role), Memory (short-term conversation history and long-term vector storage), Planning (task decomposition and reasoning), and Actions (calling external tools, APIs, and calculators).",
    "Retrieval-Augmented Generation (RAG) is an AI framework that retrieves relevant documents from a private knowledge base and provides them as grounding context to answer queries accurately without hallucination.",
    "Large Language Models (LLMs) are trained on massive text corpora to predict next tokens. When equipped with tool-use, they transition from passive text generators to active reasoning engines.",
    "Python is the dominant programming language for Artificial Intelligence, Data Science, and Machine Learning due to extensive libraries like NumPy, PyTorch, Scikit-Learn, and Streamlit.",
    "Streamlit is a Python-based open-source framework used by AI researchers to rapidly build reactive, beautiful web interfaces directly from Python scripts without writing HTML, CSS, or JavaScript.",
    "Groq is an AI acceleration platform utilizing custom Language Processing Units (LPUs) that run inference at deterministic, high throughput speeds exceeding hundreds of tokens per second."
]


class LocalRAGIndex:
    """
    Local TF-IDF & Cosine Similarity vector retriever for private documents.
    Implements the Retrieval stage of RAG completely in Python!
    """
    def __init__(self, documents: list[str] = None):
        self.documents: list[str] = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.doc_vectors = None
        if documents:
            self.add_documents(documents)

    def add_documents(self, docs: list[str]):
        # Filter empty docs
        cleaned_docs = [d.strip() for d in docs if d.strip()]
        if not cleaned_docs:
            return
        self.documents.extend(cleaned_docs)
        self.doc_vectors = self.vectorizer.fit_transform(self.documents)

    def query(self, user_query: str, top_k: int = 1, threshold: float = 0.18) -> list[tuple[str, float]]:
        """Returns the most relevant chunks with similarity score."""
        if not self.documents or self.doc_vectors is None:
            return []
        
        query_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(query_vec, self.doc_vectors).flatten()
        
        ranked_indices = similarities.argsort()[::-1]
        results = []
        for idx in ranked_indices[:top_k]:
            score = float(similarities[idx])
            if score >= threshold:
                results.append((self.documents[idx], score))
        return results


# Global singleton instance of local RAG
rag_system = LocalRAGIndex(DEFAULT_LOCAL_DOCS)


def search_wikipedia(query: str, sentences: int = 3) -> str | None:
    """Queries live Wikipedia for any real-world knowledge topic."""
    try:
        wikipedia.set_lang("en")
        # Search for page title
        search_results = wikipedia.search(query)
        if not search_results:
            return None
        
        # Get page summary of best match
        best_title = search_results[0]
        summary = wikipedia.summary(best_title, sentences=sentences, auto_suggest=False)
        return f"🌐 **Wikipedia ({best_title})**:\n\n{summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            # Pick first option if disambiguation
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


def get_smart_python_response(user_input: str, custom_rag: LocalRAGIndex = None) -> str:
    """
    Intelligent Python-only reasoning workflow:
    1. Check for greetings / meta-queries
    2. Check for arithmetic calculation
    3. Check Local RAG index (Retrieval from local course notes/docs)
    4. Fallback to live Wikipedia lookup for global knowledge
    5. Final fallback with helpful prompts
    """
    text = user_input.strip()
    lower_text = text.lower()

    # 1. Greetings & Meta questions
    if re.search(r"\b(hi|hello|hey|greetings|howdy|vanakkam|namaste)\b", lower_text):
        return (
            "👋 **Hello!** I am your smart Python assistant with:\n"
            "- 📚 **Local RAG Retrieval** (Search notes on Agentic AI, components, memory, tools)\n"
            "- 🌐 **Live Wikipedia Search** (Ask about any country, historical event, celebrity, science concept)\n"
            "- 🔢 **Math Solver** (e.g. `calc 45 * 12`)\n\n"
            "What would you like to explore?"
        )

    if re.search(r"\b(who are you|what is your name)\b", lower_text):
        return (
            "🤖 I am **PyBot-RAG**, a pure Python agent equipped with local TF-IDF semantic document search "
            "and Wikipedia knowledge integration. No cloud API key required!"
        )

    if re.search(r"\b(time|date|what day is it)\b", lower_text):
        return f"🕒 Current local date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 2. Math evaluation
    calc_match = re.search(r"\b(?:calc|calculate|what is|compute)\s+([0-9\.\s\+\-\*\/\(\)]+)\b", lower_text)
    if calc_match:
        math_res = evaluate_math(calc_match.group(1))
        if math_res:
            return math_res

    # 3. Clean query for information retrieval
    search_query = re.sub(r"^(what is|who is|tell me about|explain|describe|search for|define)\s+", "", lower_text).strip()
    search_query = search_query.rstrip("?.!")

    # 4. Check Local RAG first (High priority for course materials)
    active_rag = custom_rag or rag_system
    rag_matches = active_rag.query(search_query or text, top_k=1)
    if rag_matches:
        doc, score = rag_matches[0]
        return f"📚 **Retrieved from Local Knowledge Base (RAG)**:\n\n{doc}"

    # 5. Live Wikipedia Lookup (Answers ANY real-world topic: countries, India, personalities, science, etc.)
    wiki_topic = search_query if search_query else text
    wiki_result = search_wikipedia(wiki_topic)
    if wiki_result:
        return wiki_result

    # 6. Fallback if nothing found
    return (
        f"🤔 I searched both the local knowledge base and Wikipedia for **'{text}'** but couldn't find a direct result.\n\n"
        "Try asking:\n"
        "- 📚 Local Notes: *'What is Agentic AI?'*, *'Explain agent memory'*, *'What is RAG?'*\n"
        "- 🌐 Wikipedia: *'What is India?'*, *'Who is Alan Turing?'*, *'Photosynthesis'*\n"
        "- 🔢 Math: *'calc 128 * 4'*"
    )
