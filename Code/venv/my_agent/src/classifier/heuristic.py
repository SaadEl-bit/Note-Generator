"""Rule-based note classification. Zero API cost, instant."""

#The role of this step is to identify the type of the notes without API cost
KEYWORDS = {
    "meeting": ["meeting", "meet", "attendees", "agenda", "discussed", "participants", "action items" , "reunion" , "conference", "seance"],
    "idea": ["idea", "concept", "brainstorm", "what if", "proposal", "innovation", "think about", "think", "reflechire"],
    "todo": ["todo", "task", "checklist", "due", "priority", "deadline", "complete", "finish", "tache", "a faire", "priorite"],
    "qa": ["question", "answer", "q&a", "how to", "why does", "what is", "explain", "faq", "question", "reponse", "proposition"],
    "question_only": ["?", "how do i", "how to", "why is", "what are", "can you explain", "help me understand", "quand" , "est ce que" , "pourquoi" , "comment"],
    "default": ["note", "research", "learn about", "find out", "mixed", "random", "draft", "tell me", "explain me", "resume" , "synthese", "rappelle moi" , "résumé" , "synthèse" , "rappelle"],

}


def classify_heuristic(raw_note: str) -> tuple[str, float]:
    """
    Classify note based on keyword matching.
    Returns: (type, confidence)
    Confidence: 0.0 to 1.0 based on keyword density
    """
    #confidence is the probability that the note is of the identified or correct type
    text = raw_note.lower()
    words = text.split()
    total_words = len(words) if words else 1 #if the note is empty, the confidence is 0

    scores = {}
    for note_type, keywords in KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in text)
        # Score = matches weighted by keyword length (longer = more specific)
        weighted_score = sum(len(kw) for kw in keywords if kw in text)
        scores[note_type] = weighted_score

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    # Calculate confidence: best score vs total possible
    max_possible = sum(len(kw) for kw in KEYWORDS[best_type])
    ## if i get only 30% of the keywords, the confidence is 100% sure that the prompt type is correct
    confidence = min(best_score / max(max_possible * 0.3, 1), 1.0) if max_possible else 0.0

    # If no keywords matched at all, return unknown
    # if best_score == 0:
    #     return "unknown", 0.0

    # return best_type, round(confidence, 2)

    # NEW (temporary):
    # FORCE DEFAULT FOR TESTING — comment out the lines above and use this:
    return "default", 1.0
    
    # ORIGINAL CODE (restore after test):
    # if best_score == 0:
    #     return "unknown", 0.0
    # return best_type, round(confidence, 2)