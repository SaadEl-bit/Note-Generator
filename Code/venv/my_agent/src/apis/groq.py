import time
import json
from groq import Groq
from src.config import GROQ_KEY

# Create client once (reused across calls)
client = Groq(api_key=GROQ_KEY)


def call_groq(prompt: str, retries: int = 3) -> str:
    """
    Send prompt to Groq API with retry logic.
    Returns the raw text response (JSON string).
    """
    for attempt in range(retries):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        #Here is the message that i (the system) give to groq API
                        "role": "system",
                        "content": (
                            "You are a note structuring assistant. "
                            "Always respond with valid JSON only. "
                            "No markdown, no explanation, no code fences."
                        )
                    },
                    #Here is the prompt message that the user gave (notes)
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1024
            )
            return completion.choices[0].message.content.strip()

        #Netwrok Error Handling
        except ConnectionError as e:
            print(f"  Network error (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(2 ** attempt)  # 1s, 2s, 4s

        #Other Exception
        except Exception as e:
            print(f"  Error (attempt {attempt + 1}/{retries}): {e}")
            if attempt == retries - 1:
                raise

    return None