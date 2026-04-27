"""Renderer for todo-type notes."""

from docx import Document
from docx.shared import RGBColor
from pathlib import Path
from src.renderers.base import add_title, add_meta_line, add_section_heading


PRIORITY_COLORS = {
    "high": RGBColor(255, 0, 0),      # red
    "medium": RGBColor(255, 165, 0),  # orange
    "low": RGBColor(0, 128, 0),       # green
}


STATUS_COLORS = {
    "pending": RGBColor(128, 128, 128),     # gray
    "in_progress": RGBColor(0, 100, 200),   # blue
    "done": RGBColor(0, 128, 0),            # green
}


def render_todo(data: dict, output_path: str):
    """Convert a todo dict into a formatted .docx with table."""
    doc = Document()

    # Title
    add_title(doc, data.get("title", "Task List"))

    # Date
    add_meta_line(doc, "Date", data.get("date", "N/A"))

    # Categories
    if data.get("categories"):
        add_meta_line(doc, "Categories", ", ".join(str(c) for c in data["categories"]))

    doc.add_paragraph()  # spacer

    # Tasks Table
    add_section_heading(doc, "Tasks")

    table = doc.add_table(rows=1, cols=4)
    table.style = 'Light Grid Accent 1'

    # Header
    hdr_cells = table.rows[0].cells
    headers = ["Task", "Priority", "Due Date", "Status"]
    for i, header in enumerate(headers):
        hdr_cells[i].text = header
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True

    # Rows
    for task in data.get("tasks", []):
        if isinstance(task, dict):
            desc = str(task.get("description") or "—")
            priority = str(task.get("priority") or "medium").lower()
            due = str(task.get("due_date") or "—")
            status = str(task.get("status") or "pending").lower().replace(" ", "_")
        else:
            desc = str(task)
            priority = "medium"
            due = "—"
            status = "pending"

        row_cells = table.add_row().cells
        row_cells[0].text = desc
        row_cells[1].text = priority.capitalize()
        row_cells[2].text = due
        row_cells[3].text = status.replace("_", " ").capitalize()

        # Color priority
        if priority in PRIORITY_COLORS:
            row_cells[1].paragraphs[0].runs[0].font.color.rgb = PRIORITY_COLORS[priority]

        # Color status
        if status in STATUS_COLORS:
            row_cells[3].paragraphs[0].runs[0].font.color.rgb = STATUS_COLORS[status]

    # Tags
    if data.get("tags"):
        doc.add_paragraph()
        add_section_heading(doc, "Tags")
        doc.add_paragraph(", ".join(str(t) for t in data["tags"]))

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"  Saved: {output_path}")