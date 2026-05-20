# # test_apis.py
# # Tests: Groq API + OpenRouter API

# import os
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_KEY        = os.getenv("GROQ_API_KEY")
# OPENROUTER_KEY  = os.getenv("OPENROUTER_API_KEY")

# print("=" * 50)
# print("API KEY CHECK")
# print("=" * 50)
# print(f"Groq key found:        {'YES' if GROQ_KEY       else 'NO'}")
# print(f"OpenRouter key found:  {'YES' if OPENROUTER_KEY else 'NO'}")
# print()

# # ============================================================
# # TEST: GROQ (updated model)
# # ============================================================
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

# # ============================================================
# # TEST: OpenRouter
# # Uses the openai-compatible endpoint at openrouter.ai
# # Model: mistralai/mistral-7b-instruct  (free tier, no billing required)
# # ============================================================
# print("-" * 50)
# print("TESTING OpenRouter API...")
# print("-" * 50)

# try:
#     from openai import OpenAI

#     client = OpenAI(
#         api_key=OPENROUTER_KEY,
#         base_url="https://openrouter.ai/api/v1",
#     )

#     completion = client.chat.completions.create(
#         model="mistralai/mistral-7b-instruct",   # free model on OpenRouter
#         messages=[
#             {"role": "user", "content": "Say 'OpenRouter is working' and nothing else."}
#         ],
#         temperature=0.0,
#         max_tokens=50,
#         extra_headers={
#             "HTTP-Referer": "http://localhost",   # required by OpenRouter
#             "X-Title": "my_agent test",
#         },
#     )

#     print(f"Status:   SUCCESS")
#     print(f"Model:    {completion.model}")
#     print(f"Response: {completion.choices[0].message.content.strip()}")

# except Exception as e:
#     print(f"Status: FAILED")
#     print(f"Error:  {type(e).__name__}: {e}")

# print()
# print("=" * 50)
# print("ALL TESTS COMPLETE")
# print("=" * 50)

# test_openrouter.py
import os
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

print("=" * 50)
print("OPENROUTER API TEST")
print("=" * 50)
print(f"Key found: {'YES' if OPENROUTER_KEY else 'NO'}")
print()


# ============================================================
# TEST: Using requests (no extra library needed)
# ============================================================
print("-" * 50)
print("TESTING OPENROUTER (via requests)...")
print("-" * 50)

try:
    import requests

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost",  # Required by OpenRouter
            "X-Title": "AI Note Agent"             # Your app name
        },
        json={
            "model": "meta-llama/llama-3.1-8b-instruct",  # Same model as Groq
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": "Say 'OpenRouter is working' and nothing else."
                }
            ],
            "temperature": 0.0,
            "max_tokens": 50
        },
        timeout=30
    )

    if response.status_code == 200:
        data = response.json()
        message = data["choices"][0]["message"]["content"]
        print(f"Status: SUCCESS")
        print(f"Response: {message.strip()}")
        print(f"Model used: {data.get('model', 'unknown')}")
        print(f"Tokens used: {data.get('usage', {}).get('total_tokens', 'N/A')}")
    else:
        print(f"Status: FAILED")
        print(f"HTTP {response.status_code}: {response.text[:200]}")

except Exception as e:
    print(f"Status: FAILED")
    print(f"Error: {type(e).__name__}: {e}")

print()
print("=" * 50)
print("TEST COMPLETE")
print("=" * 50)