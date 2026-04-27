"""Validate and sanitize API responses."""
# Here we check that the field that we structred to put in the final output in randers folder , exists in the api respons , if not we cancell them

def validate_response(data: dict, required_fields: list) -> dict:
    """
    Ensure all required fields exist. Fill missing ones with defaults.
    Returns sanitized dict.
    """
    sanitized = dict(data)  # copy

    for field in required_fields:
        if field not in sanitized or sanitized[field] is None:
            if field in ["participants", "action_items", "tags", "tasks",
                         "required_resources", "next_steps", "sources",
                         "follow_up_questions", "categories", "agenda_items",
                         "decisions_made"]:
                sanitized[field] = []
            elif field in ["date", "due_date", "confidence"]:
                sanitized[field] = None
            else:
                sanitized[field] = "N/A"

    # Ensure lists are actually lists
    list_fields = ["participants", "action_items", "tags", "tasks",
                   "required_resources", "next_steps", "sources",
                   "follow_up_questions", "categories", "agenda_items",
                   "decisions_made"]
    for field in list_fields:
        if field in sanitized and not isinstance(sanitized[field], list):
            sanitized[field] = [sanitized[field]] if sanitized[field] else []

    return sanitized