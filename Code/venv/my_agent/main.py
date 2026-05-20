import json
import os
import time
from pathlib import Path

# Always resolve paths relative to this file, not the CWD
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
from src.apis.groq import call_groq
from src.extractors.prompt_builder import build_prompt
from src.renderers.meeting import render_meeting
from src.renderers.idea import render_idea
from src.renderers.todo import render_todo
from src.renderers.qa import render_qa
from src.renderers.default import render_default
from src.classifier.heuristic import classify_heuristic
from src.classifier.api_classifier import classify_api
from src.validator import validate_response
from src.utils.chunker import chunk_text

# Max characters per chunk (~3000 chars ≈ ~750 tokens, well within 6000 TPM limit)
MAX_CHUNK_CHARS = 3000


# Map type → renderer function
RENDERERS = {
    "meeting": render_meeting,
    "idea": render_idea,
    "todo": render_todo,
    "qa": render_qa,
    "default": render_default,
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
    """Process a single note file end-to-end. Auto-chunks if too large."""
    print(f"Processing: {note_file.name}")

    # 1. READ
    raw_note = note_file.read_text(encoding="utf-8")

    # 2. CLASSIFY
    note_type = "default"
    print(f"  -> FORCED: default (classifier bypassed)")

    # 3. BUILD prompt (to check size)
    try:
        _, required_fields = build_prompt(note_type, "")
    except FileNotFoundError:
        note_type = "default"
        _, required_fields = build_prompt("default", "")

    # 4. CHECK if chunking is needed
    prompt_overhead = len(_)  # template prompt length without note
    estimated_tokens = (len(raw_note) + prompt_overhead) // 4  # rough char→token estimate

    if len(raw_note) > MAX_CHUNK_CHARS:
        chunks = chunk_text(raw_note, MAX_CHUNK_CHARS)
        print(f"  -> Note too large ({len(raw_note)} chars). Splitting into {len(chunks)} chunks.")

        for i, chunk in enumerate(chunks, 1):
            print(f"  Processing chunk {i}/{len(chunks)}...")
            _process_chunk(chunk, note_file.stem, note_type, i, len(chunks), output_dir)
            # Delay between chunks to avoid TPM rate limit
            if i < len(chunks):
                print(f"  Waiting 10s before next chunk (TPM rate limit)...")
                time.sleep(10)
    else:
        _process_chunk(raw_note, note_file.stem, note_type, 1, 1, output_dir)

    print()


def _process_chunk(chunk_text: str, note_stem: str, note_type: str,
                   part_num: int, total_parts: int, output_dir: Path):
    """Process a single chunk of text through the full pipeline."""
    # BUILD prompt
    try:
        prompt, required_fields = build_prompt(note_type, chunk_text)
    except FileNotFoundError:
        prompt, required_fields = build_prompt("default", chunk_text)
        note_type = "default"

    # CALL API
    response_text = call_groq(prompt)
    if not response_text:
        print(f"  FAILED: API did not return a response.")
        return

    # PARSE JSON
    try:
        text = response_text
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        data = json.loads(text.strip())

    except json.JSONDecodeError as e:
        print(f"  FAILED: JSON parse error — {e}")
        print(f"  Raw preview: {response_text[:200]}...")
        return

    # VALIDATE
    data = validate_response(data, required_fields)

    # RENDER
    renderer = RENDERERS.get(note_type, render_meeting)

    # Add part number to filename if multiple chunks
    if total_parts > 1:
        output_name = f"{note_stem}_part{part_num}of{total_parts}_{note_type}.docx"
    else:
        output_name = f"{note_stem}_{note_type}.docx"

    output_path = output_dir / output_name
    renderer(data, str(output_path))

    print(f"  Done.")


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