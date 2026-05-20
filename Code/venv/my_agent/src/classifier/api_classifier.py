"""AI-powered classification fallback when heuristic is unsure."""

#If the first manual test did not work , we turn to groq using API token

import json
from src.apis.groq import call_groq


# OLD:
# "type" must be one of: "meeting", "idea", "todo", "qa"

# NEW — replace the entire CLASSIFIER_PROMPT string:
CLASSIFIER_PROMPT = """You are a note classifier. Read the note below and return ONLY a JSON object.

Rules:
- "type" must be one of: "meeting", "idea", "todo", "qa", "question_only", "default"
- "confidence" is 0.0 to 1.0
- "question_only": use when the text is JUST a question seeking an answer
- "default": use when the text is mixed, unclear, or doesn't fit other categories
- Be decisive. If unsure, use "default".

Return ONLY valid JSON like: {{"type": "meeting", "confidence": 0.95}}

Note:
{raw_note}
"""


def classify_api(raw_note: str) -> tuple[str, float]:
    """
    Ask Groq to classify the note.
    Returns: (type, confidence)
    """
    prompt = CLASSIFIER_PROMPT.format(raw_note=raw_note)
    response = call_groq(prompt)

    # if not response:
    #     return "meeting", 0.0  # fallback default

    # NEW (temporary):
    # FORCE DEFAULT FOR TESTING:
    return "default", 1.0
    
    # ORIGINAL CODE (restore after test):
    # try:
    #     data = json.loads(text.strip())
    #     note_type = data.get("type", "meeting")
    #     confidence = float(data.get("confidence", 0.5))
    #     return note_type, confidence
    # except (json.JSONDecodeError, ValueError):
    #     return "meeting", 0.5

    # Clean markdown fences if present
    text = response
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    # try:
    #     data = json.loads(text.strip())
    #     note_type = data.get("type", "meeting")
    #     confidence = float(data.get("confidence", 0.5))
    #     return note_type, confidence
    # except (json.JSONDecodeError, ValueError):
    #     return "meeting", 0.5  # fallback