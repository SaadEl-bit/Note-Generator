import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from my_agent/ folder (one level up from src/)
env_path = Path(os.path.dirname(os.path.abspath(__file__))).parent / ".env"
load_dotenv(dotenv_path=env_path)

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GROQ_KEY   = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")