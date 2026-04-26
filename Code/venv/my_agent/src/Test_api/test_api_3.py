import os
from dotenv import load_dotenv
from google import genai

# Load the .env file from the same folder as this script
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
print(f"Key loaded: {'YES' if GEMINI_KEY else 'NO'}")

# Pass the key explicitly to the client
client = genai.Client(api_key=GEMINI_KEY)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works in a few words"
)
print(response.text)