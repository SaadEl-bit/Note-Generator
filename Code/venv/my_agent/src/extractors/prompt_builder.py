import json
import os
from pathlib import Path

# Base directory = my_agent/ (two levels up from extractors/)
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent


def load_template(template_name: str) -> dict:
    """Load a JSON template from the templates/ folder."""
    #Creating the path of the template
    template_path = BASE_DIR / "templates" / f"{template_name}.json"
    #Opening the template .json file 
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_prompt(template_name: str, raw_note: str) -> tuple[str, list]:
    """
    Load template and inject the raw note.
    Returns: (complete_prompt_string, list_of_required_fields)
    """
    template = load_template(template_name)
    prompt = template["prompt"].replace("{raw_note}", raw_note)
    required_fields = template.get("required_fields", [])
    return prompt, required_fields

def list_available_templates() -> list[str]:
    """Return list of available template names."""
    templates_dir = BASE_DIR / "templates"
    return [f.stem for f in templates_dir.glob("*.json")]