# test_apis.py
# Updated for google-genai (new Gemini SDK) and current Groq models

import os
from dotenv import load_dotenv

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
# TEST 1: GEMINI (new SDK: google-genai)
# ============================================================
print("-" * 50)
print("TESTING GEMINI API...")
print("-" * 50)

try:
    from google import genai
    from google.genai import types
    
    client = genai.Client(api_key=GEMINI_KEY)
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",           # current model name
        contents="Say 'Gemini is working' and nothing else."    )
    
    print(f"Status: SUCCESS")
    print(f"Response: {response.text.strip()}")
    
except Exception as e:
    print(f"Status: FAILED")
    print(f"Error: {type(e).__name__}: {e}")

print()


# ============================================================
# TEST 2: GROQ (updated model)
# ============================================================
# print("-" * 50)
# print("TESTING GROQ API...")
# print("-" * 50)

# try:
#     from groq import Groq
    
#     client = Groq(api_key=GROQ_KEY)
    
#     completion = client.chat.completions.create(
#         model="llama-3.1-8b-instant",        # current replacement model
#         messages=[
#             {"role": "user", "content": "Say 'Groq is working' and nothing else."}
#         ],
#         temperature=0.0,
#         max_tokens=50
#     )
    
#     print(f"Status: SUCCESS")
#     print(f"Response: {completion.choices[0].message.content.strip()}")
    
# except Exception as e:
#     print(f"Status: FAILED")
#     print(f"Error: {type(e).__name__}: {e}")

# print()
# print("=" * 50)
# print("TEST COMPLETE")
# print("=" * 50)