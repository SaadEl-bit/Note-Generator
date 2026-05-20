from docx import Document
from docx.shared import RGBColor, Pt
from pathlib import Path
from src.renderers.base import add_title, add_meta_line, add_section_heading, add_bullet_list


def render_default(data: dict, output_path: str):
    """Convert a default/research dict into a formatted .docx — study notes version."""
    doc = Document()

    # Title
    add_title(doc, data.get("title", "Research Notes"))

    # Subject & Date
    add_meta_line(doc, "Subject", data.get("subject", "N/A"))
    add_meta_line(doc, "Date", data.get("date", "N/A"))

    doc.add_paragraph()

    # Summary box
    add_section_heading(doc, "Summary")
    p = doc.add_paragraph(data.get("summary", "No summary."))
    p.runs[0].italic = True
    p.runs[0].font.color.rgb = RGBColor(80, 80, 80)

    doc.add_paragraph()

    # Sections (the main content)
    for section in data.get("sections", []):
        add_section_heading(doc, section.get("heading", "Section"))

        # Main paragraph
        if section.get("content"):
            doc.add_paragraph(section["content"])

        # Sub-points with explanations
        if section.get("sub_points"):
            doc.add_paragraph("Key Points:").runs[0].bold = True
            for point in section["sub_points"]:
                p = doc.add_paragraph(style='List Bullet')
                p.add_run(point)

        # Examples
        if section.get("examples"):
            doc.add_paragraph("Examples:").runs[0].bold = True
            for ex in section["examples"]:
                p = doc.add_paragraph(style='List Bullet')
                p.add_run(ex).italic = True
                p.runs[0].font.color.rgb = RGBColor(0, 100, 200)

        doc.add_paragraph()  # spacer between sections

    # Key Definitions
    if data.get("key_definitions"):
        add_section_heading(doc, "Key Definitions")
        for item in data["key_definitions"]:
            term = item.get("term", "")
            definition = item.get("definition", "")
            p = doc.add_paragraph()
            p.add_run(f"{term}: ").bold = True
            p.add_run(definition)

    # Q&A
    if data.get("questions_answered"):
        add_section_heading(doc, "Questions & Answers")
        for qa in data["questions_answered"]:
            q = qa.get("question", "")
            a = qa.get("answer", "")
            p = doc.add_paragraph()
            p.add_run(f"Q: {q}").bold = True
            p.runs[0].font.color.rgb = RGBColor(0, 100, 200)
            doc.add_paragraph(f"A: {a}")

    # Key Takeaways
    if data.get("key_takeaways"):
        add_section_heading(doc, "Key Takeaways")
        add_bullet_list(doc, data["key_takeaways"], color=RGBColor(0, 128, 0))

    # Suggested Actions
    if data.get("suggested_actions"):
        add_section_heading(doc, "Suggested Study Actions")
        add_bullet_list(doc, data["suggested_actions"], color=RGBColor(128, 0, 128))

    # Tags
    if data.get("tags"):
        add_section_heading(doc, "Tags")
        doc.add_paragraph(", ".join(str(t) for t in data["tags"]))

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"  Saved: {output_path}")