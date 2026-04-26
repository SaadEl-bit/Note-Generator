from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path

#Here i convert the output of API message into .docx file
def render_meeting(data: dict, output_path: str):
    """
    Convert a meeting dict into a formatted .docx file.
    """
    doc = Document()

    # --- TITLE ---
    title = doc.add_heading(data.get("title", "Untitled Meeting"), level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- META INFO ---
    p = doc.add_paragraph()
    p.add_run(f"Date: {data.get('date', 'N/A')}").bold = True
    participants = data.get("participants", [])
    p.add_run(f"\nParticipants: {', '.join(participants) if participants else 'N/A'}")

    doc.add_paragraph()  # spacer

    # --- AGENDA ---
    if data.get("agenda_items"):
        doc.add_heading("Agenda", level=2)
        for item in data["agenda_items"]:
            doc.add_paragraph(str(item), style='List Bullet')

    # --- DECISIONS ---
    if data.get("decisions_made"):
        doc.add_heading("Decisions Made", level=2)
        for dec in data["decisions_made"]:
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(str(dec)).font.color.rgb = RGBColor(0, 128, 0)

    # --- ACTION ITEMS ---
    if data.get("action_items"):
        doc.add_heading("Action Items", level=2)
        for item in data["action_items"]:
            if isinstance(item, dict):
                task = item.get("task", "Unknown task")
                owner = item.get("owner", "Unassigned")
                due = item.get("due_date", "No deadline")
            else:
                task = str(item)
                owner = "—"
                due = "—"

            p = doc.add_paragraph(style='List Number')
            p.add_run(f"{task}").bold = True
            p.add_run(f"\n    Assigned to: {owner}  |  Due: {due}")

    # --- SUMMARY ---
    doc.add_heading("Summary", level=2)
    doc.add_paragraph(data.get("summary", "No summary provided."))

    # --- TAGS ---
    if data.get("tags"):
        doc.add_heading("Tags", level=2)
        doc.add_paragraph(", ".join(str(t) for t in data["tags"]))

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"  Saved: {output_path}")