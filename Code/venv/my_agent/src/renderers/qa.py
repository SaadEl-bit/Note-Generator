"""Renderer for Q&A-type notes."""

from docx import Document
from docx.shared import RGBColor, Pt
from pathlib import Path
from src.renderers.base import add_title, add_meta_line, add_section_heading, add_bullet_list


CONFIDENCE_COLORS = {
    "high": RGBColor(0, 128, 0),    # green
    "medium": RGBColor(255, 165, 0), # orange
    "low": RGBColor(255, 0, 0),      # red
}


def render_qa(data: dict, output_path: str):
    """Convert a Q&A dict into a formatted .docx."""
    doc = Document()

    # Title
    add_title(doc, data.get("title", "Q&A Document"))

    # Date
    add_meta_line(doc, "Date", data.get("date", "N/A"))

    # Confidence badge
    confidence = data.get("confidence", "medium").lower()
    p = doc.add_paragraph()
    p.add_run("Confidence: ").bold = True
    run = p.add_run(confidence.upper())
    run.bold = True
    if confidence in CONFIDENCE_COLORS:
        run.font.color.rgb = CONFIDENCE_COLORS[confidence]

    doc.add_paragraph()  # spacer

    # Question (highlighted box feel)
    add_section_heading(doc, "Question")
    p = doc.add_paragraph(data.get("question", "No question provided."))
    p.runs[0].font.size = Pt(12)
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(0, 100, 200)

    # Answer
    add_section_heading(doc, "Answer")
    doc.add_paragraph(data.get("answer", "No answer provided."))

    # Sources
    if data.get("sources"):
        add_section_heading(doc, "Sources")
        add_bullet_list(doc, data["sources"])

    # Follow-up Questions
    if data.get("follow_up_questions"):
        add_section_heading(doc, "Follow-up Questions")
        add_bullet_list(doc, data["follow_up_questions"], color=RGBColor(100, 100, 100))

    # Tags
    if data.get("tags"):
        add_section_heading(doc, "Tags")
        doc.add_paragraph(", ".join(str(t) for t in data["tags"]))

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"  Saved: {output_path}")