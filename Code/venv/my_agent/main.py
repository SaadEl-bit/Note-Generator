import json
from pathlib import Path
from src.apis.groq import call_groq
from src.extractors.prompt_builder import build_prompt
from src.renderers.meeting import render_meeting


def main():
    # Paths
    notes_dir = Path("notes")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Find all .txt files
    note_files = [f for f in notes_dir.iterdir() if f.suffix == ".txt"]
    print(f"Found {len(note_files)} note(s) to process.\n")

    for note_file in note_files:
        print(f"Processing: {note_file.name}")

        # 1. READ raw note
        raw_note = note_file.read_text(encoding="utf-8")

        # 2. BUILD prompt from template
        # here we just test with meetings notes
        prompt, required_fields = build_prompt("meeting", raw_note)

        # 3. CALL API
        response_text = call_groq(prompt)
        if not response_text:
            print(f"  FAILED: API did not return a response.\n")
            continue

        # 4. PARSE JSON (clean markdown fences if present)
        try:
            text = response_text
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]

            data = json.loads(text.strip())

        except json.JSONDecodeError as e:
            print(f"  FAILED: JSON parse error — {e}")
            print(f"  Raw response preview: {response_text[:200]}...\n")
            continue

        # 5. VALIDATE required fields (fill missing with defaults)
        for field in required_fields:
            if field not in data:
                data[field] = "N/A"

        # 6. RENDER docx
        output_path = output_dir / f"{note_file.stem}.docx"
        render_meeting(data, str(output_path))

        print(f"  Done.\n")

    print("=" * 40)
    print("Batch processing complete.")
    print("=" * 40)


if __name__ == "__main__":
    main()