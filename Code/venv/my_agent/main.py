import json
import os
from pathlib import Path

# Always resolve paths relative to this file, not the CWD
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
from src.apis.groq import call_groq
from src.extractors.prompt_builder import build_prompt
from src.renderers.meeting import render_meeting
from src.renderers.idea import render_idea
from src.renderers.todo import render_todo
from src.renderers.qa import render_qa
from src.classifier.heuristic import classify_heuristic
from src.classifier.api_classifier import classify_api
from src.validator import validate_response


# Map type → renderer function
RENDERERS = {
    "meeting": render_meeting,
    "idea": render_idea,
    "todo": render_todo,
    "qa": render_qa,
}

# this function is used to classify the note type
def classify_note(raw_note: str) -> str:
    """
    Classify note using heuristic first, API fallback if unsure.
    Returns detected note type.
    """
    note_type, confidence = classify_heuristic(raw_note)

    print(f"  Heuristic: {note_type} (confidence: {confidence})")

    if confidence < 0.3 or note_type == "unknown":
        print(f"  -> Falling back to API classifier...")
        note_type, api_confidence = classify_api(raw_note)
        print(f"  API: {note_type} (confidence: {api_confidence})")

    return note_type


def process_note_file(note_file: Path, output_dir: Path):
    """Process a single note file end-to-end."""
    print(f"Processing: {note_file.name}")

    # 1. READ
    raw_note = note_file.read_text(encoding="utf-8")

    # 2. CLASSIFY
    note_type = classify_note(raw_note)
    print(f"  -> Using template: {note_type}")

    # 3. BUILD prompt
    try:
        prompt, required_fields = build_prompt(note_type, raw_note)
    except FileNotFoundError:
        print(f"  FAILED: Template '{note_type}.json' not found. Using 'meeting' fallback.")
        prompt, required_fields = build_prompt("meeting", raw_note)
        note_type = "meeting"

    # 4. CALL API
    response_text = call_groq(prompt)
    if not response_text:
        print(f"  FAILED: API did not return a response.\n")
        return

    # 5. PARSE JSON
    try:
        text = response_text
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        data = json.loads(text.strip())

    except json.JSONDecodeError as e:
        print(f"  FAILED: JSON parse error — {e}")
        print(f"  Raw preview: {response_text[:200]}...\n")
        return

    # 6. VALIDATE
    data = validate_response(data, required_fields)

    # 7. RENDER
    renderer = RENDERERS.get(note_type, render_meeting)
    output_path = output_dir / f"{note_file.stem}_{note_type}.docx"
    renderer(data, str(output_path))

    print(f"  Done.\n")


def main():
    notes_dir = BASE_DIR / "notes"
    output_dir = BASE_DIR / "output"
    output_dir.mkdir(exist_ok=True)

    note_files = [f for f in notes_dir.iterdir() if f.suffix == ".txt"]
    print(f"Found {len(note_files)} note(s) to process.\n")
    print("=" * 50)

    for note_file in note_files:
        process_note_file(note_file, output_dir)

    print("=" * 50)
    print("Batch processing complete.")
    print("=" * 50)


if __name__ == "__main__":
    main()