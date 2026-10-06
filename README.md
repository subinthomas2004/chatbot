# 🤖 AI Chatbot (Groq-Powered)

A Python chatbot built with **Groq API** and **Streamlit** for an Agentic AI course project.

## Features

- 🚀 **Blazing-fast responses** via Groq's LPU inference engine
- 💬 **Chat memory** — maintains full conversation context
- 🎨 **Clean web UI** with Streamlit
- ⚙️ **Configurable** — choose models, temperature, and system prompt
- 🔑 **Free tier** — Groq offers generous free API access

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Get your Groq API key (free)

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up / log in
3. Create a new API key
4. Copy the key

### 3. Run the chatbot

```bash
streamlit run app.py
```

5. Paste your API key in the sidebar and start chatting!

## Available Models

| Model | Speed | Quality |
|-------|-------|---------|
| LLaMA 3.1 8B | ⚡⚡⚡ Fastest | Good |
| LLaMA 3.3 70B | ⚡⚡ Fast | Best |
| Gemma 2 9B | ⚡⚡⚡ Fast | Good |
| Mixtral 8x7B | ⚡⚡ Fast | Great |

## Project Structure

```
chatbot/
├── app.py              # Streamlit web UI
├── chatbot.py          # Core chatbot logic (Groq client, chat function)
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment file
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## How It Works

1. User types a message in the web UI
2. The message + conversation history is sent to Groq API
3. Groq processes it using the selected LLM at lightning speed
4. The response is displayed in the chat and added to history

## Tech Stack

- **Python 3.10+**
- **Groq SDK** — LLM inference API
- **Streamlit** — Web UI framework
- **python-dotenv** — Environment variable management
