"""Shared utilities for all docx renderers."""
#Theme of the document word to export as output

from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_title(doc, text: str):
    """Add a centered title heading."""
    title = doc.add_heading(text, level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_meta_line(doc, label: str, value: str):
    """Add a bold label + value paragraph."""
    p = doc.add_paragraph()
    p.add_run(f"{label}: ").bold = True
    p.add_run(value or "N/A")


def add_section_heading(doc, text: str):
    """Add a level-2 heading."""
    doc.add_heading(text, level=2)


def add_bullet_list(doc, items: list, color: RGBColor = None):
    """Add items as bullet points. Optional text color."""
    for item in items:
        if not item:
            continue
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(str(item))
        if color:
            run.font.color.rgb = color


def add_numbered_list(doc, items: list):
    """Add items as numbered list."""
    for item in items:
        if not item:
            continue
        doc.add_paragraph(str(item), style='List Number')