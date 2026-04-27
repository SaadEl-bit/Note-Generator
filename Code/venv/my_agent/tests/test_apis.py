# test_apis.py
# Updated for google-genai (new Gemini SDK) and current Groq models

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")

print("=" * 50)
print("API KEY CHECK")
print("=" * 50)
print(f"Groq key found:   {'YES' if GROQ_KEY else 'NO'}")
print()

# ============================================================
# TEST: GROQ (updated model)
# ============================================================
print("-" * 50)
print("TESTING GROQ API...")
print("-" * 50)

try:
    from groq import Groq
    
    client = Groq(api_key=GROQ_KEY)
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",        # current replacement model
        messages=[
            {"role": "user", "content": "Say 'Groq is working' and nothing else."}
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