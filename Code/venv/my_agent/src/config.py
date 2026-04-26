import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GROQ_KEY   = os.getenv("GROQ_API_KEY")

if not GEMINI_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")