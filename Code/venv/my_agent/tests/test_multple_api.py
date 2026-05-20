# test_openrouter.py
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

# Free models to test
MODELS = {
    "Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct",
    "Llama 3.1 8B": "meta-llama/llama-3.1-8b-instruct",
    "Gemini Flash 1.5": "google/gemini-flash-1.5",
    "Gemini 2.0 Flash": "google/gemini-2.0-flash-exp",
    "Mistral 7B": "mistralai/mistral-7b-instruct",
}

TEST_PROMPT = """Convert this messy note into structured JSON.
Return ONLY valid JSON with: title, date, developpement, action_items (list).

Note: Dans chapitre 5 de gestion d'entreprise, on a parler sur les types et les methodoligies des strategies choisies par l'entreprise et le diagnostique fait par les entreprises dans les 2 parties internes et externes avec leurs branches"""


def test_model(name: str, model_id: str):
    """Test a single model and return results."""
    print(f"\n{'-' * 50}")
    print(f"Testing: {name}")
    print(f"Model ID: {model_id}")
    print("-" * 50)

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://localhost",
                "X-Title": "AI Note Agent"
            },
            json={
                "model": model_id,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a note structuring assistant. Always respond with valid JSON only. No markdown, no explanation."
                    },
                    {"role": "user", "content": TEST_PROMPT}
                ],
                "temperature": 0.2,
                "max_tokens": 512
            },
            timeout=60
        )

        if response.status_code != 200:
            print(f"  ❌ HTTP {response.status_code}: {response.text[:150]}")
            return None

        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()

        # Try to parse JSON
        text = content
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        parsed = json.loads(text.strip())

        # Validate structure
        has_title = "title" in parsed
        has_date = "date" in parsed
        has_summary = "summary" in parsed
        has_actions = "action_items" in parsed and isinstance(parsed["action_items"], list)

        score = sum([has_title, has_date, has_summary, has_actions])

        print(f"  ✅ SUCCESS")
        print(f"  Response time: {response.elapsed.total_seconds():.2f}s")
        print(f"  Tokens: {data.get('usage', {}).get('total_tokens', 'N/A')}")
        print(f"  JSON score: {score}/4 (title:{has_title}, date:{has_date}, summary:{has_summary}, actions:{has_actions})")
        print(f"  Preview: {json.dumps(parsed, indent=2)[:200]}...")

        return {
            "name": name,
            "model": model_id,
            "score": score,
            "time": response.elapsed.total_seconds(),
            "tokens": data.get('usage', {}).get('total_tokens', 0)
        }

    except json.JSONDecodeError as e:
        print(f"  ⚠️  JSON parse failed: {e}")
        print(f"  Raw: {content[:150]}...")
        return {"name": name, "model": model_id, "score": 0, "time": 0, "tokens": 0}

    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {e}")
        return {"name": name, "model": model_id, "score": 0, "time": 0, "tokens": 0}


def main():
    print("=" * 60)
    print("OPENROUTER FREE MODELS COMPARISON")
    print("=" * 60)
    print(f"Testing {len(MODELS)} models with identical prompt...")

    results = []
    for name, model_id in MODELS.items():
        result = test_model(name, model_id)
        if result:
            results.append(result)

    # Summary
    print(f"\n{'=' * 60}")
    print("SUMMARY RANKING")
    print("=" * 60)

    if results:
        results.sort(key=lambda x: (-x["score"], x["time"]))
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['name']} | Score: {r['score']}/4 | Time: {r['time']:.2f}s | Tokens: {r['tokens']}")
    else:
        print("No successful results.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()