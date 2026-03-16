# src/utils/ollama_llm.py
# Helper to create the Ollama LLM instance for CrewAI agents

import os
from dotenv import load_dotenv

# Load .env BEFORE anything else
load_dotenv()

# Set a dummy OPENAI_API_KEY so CrewAI doesn't complain during init
# (We're using Ollama, not OpenAI)
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-no-openai-key-needed-using-ollama"

from crewai import LLM


def get_ollama_llm():
    """Returns a CrewAI LLM instance configured for Ollama with qwen2.5-coder:7b.
    Uses CrewAI's native LLM class with the 'ollama/' prefix."""
    model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    return LLM(
        model=f"ollama/{model}",
        base_url=base_url,
        temperature=0.1,
    )
