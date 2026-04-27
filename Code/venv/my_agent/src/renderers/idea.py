"""Renderer for idea-type notes."""

from docx import Document
from docx.shared import RGBColor
from pathlib import Path
from src.renderers.base import add_title, add_meta_line, add_section_heading, add_bullet_list


def render_idea(data: dict, output_path: str):
    """Convert an idea dict into a formatted .docx."""
    doc = Document()

    # Title
    add_title(doc, data.get("title", "Untitled Idea"))

    # Date
    add_meta_line(doc, "Date", data.get("date", "N/A"))

    doc.add_paragraph()  # spacer

    # Problem
    add_section_heading(doc, "The Problem")
    doc.add_paragraph(data.get("problem_statement", "No problem statement."))

    # Solution (highlighted)
    add_section_heading(doc, "The Solution")
    p = doc.add_paragraph(data.get("proposed_solution", "No solution proposed."))
    p.runs[0].font.color.rgb = RGBColor(0, 100, 200)  # blue
    p.runs[0].bold = True

    # Impact
    add_section_heading(doc, "Potential Impact")
    doc.add_paragraph(data.get("potential_impact", "No impact analysis."))

    # Resources
    if data.get("required_resources"):
        add_section_heading(doc, "Resources Needed")
        add_bullet_list(doc, data["required_resources"])

    # Next Steps
    if data.get("next_steps"):
        add_section_heading(doc, "Next Steps")
        add_bullet_list(doc, data["next_steps"], color=RGBColor(0, 128, 0))

    # Tags
    if data.get("tags"):
        add_section_heading(doc, "Tags")
        doc.add_paragraph(", ".join(str(t) for t in data["tags"]))

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"  Saved: {output_path}")