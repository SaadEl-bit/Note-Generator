# test_apis.py
# Simple script to verify both Gemini and Groq API keys work

import os
import json
from dotenv import load_dotenv

# Load .env file
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

print("=" * 50)
print("API KEY CHECK")
print("=" * 50)
print(f"Gemini key found: {'YES' if GEMINI_KEY else 'NO'}")
print(f"Groq key found:   {'YES' if GROQ_KEY else 'NO'}")
print()


# ============================================================
# TEST 1: GEMINI
# ============================================================
# print("-" * 50)
# print("TESTING GEMINI API...")
# print("-" * 50)

# try:
#     from google import genai

#     client = genai.Client(api_key=GEMINI_KEY)

#     # Try multiple models in case one has quota exhausted
#     models_to_try = ["gemini-1.5-pro", "gemini-2.0-flash-lite", "gemini-2.0-flash"]
#     success = False

#     for model_name in models_to_try:
#         try:
#             response = client.models.generate_content(
#                 model=model_name,
#                 contents="Say 'Gemini is working' and nothing else."
#             )
#             print(f"Status: SUCCESS (model: {model_name})")
#             print(f"Response: {response.text.strip()}")
#             success = True
#             break
#         except Exception as model_err:
#             print(f"  [{model_name}] FAILED: {type(model_err).__name__}: {model_err}")

#     if not success:
#         print("Status: FAILED - all models quota exhausted")
    
# except Exception as e:
#     print(f"Status: FAILED")
#     print(f"Error: {type(e).__name__}: {e}")

# print()


# ============================================================
# TEST 2: GROQ
# ============================================================
print("-" * 50)
print("TESTING GROQ API...")
print("-" * 50)

try:
    from groq import Groq
    
    client = Groq(api_key=GROQ_KEY)
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Say who you are and say how excited to start with us our project"}
        ],
        temperature=0.0,
        max_tokens=50
    )
    
    print(f"Status: SUCCESS")
    print(f"Response: {completion.choices[0].message.content.strip()}")
    
except Exception as e:
    print(f"Status: FAILED")
    print(f"Error: {type(e).__name__}: {e}")

print()
print("=" * 50)
print("TEST COMPLETE")
print("=" * 50)