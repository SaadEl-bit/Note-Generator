def clean_note(raw_text: str) -> str:
    """Remove extra whitespace and empty lines."""
    lines = raw_text.strip().split("\n")
    print(lines)
    cleaned = [line.strip() for line in lines if line.strip()]
    print(cleaned)
    return "\n".join(cleaned)

def build_prompt(note: str, style: str = "markdown", max_words: int = 500) -> str:
    return f"""
Convert this note to {style} format in max {max_words} words:
{note}
    """
# print(build_prompt("messy notes to test" , style="pdf" , max_words=100))
# print('-----------------')
# print(build_prompt("messy notes to test"))


# Return multiple values (returns a tuple)
def count_tokens(text: str):
    words = len(text.split())
    chars = len(text)
    hello_words = text.split()
    return hello_words ,words, chars          # returns tuple

# list ,w, c = count_tokens("Hello world")  # unpacking
# print(f"Words: {w}")
# print(f"Characters: {c}")
# print(list)


# model: str = "gemini-1.5-flash"
# model2 = "gemini-1.5-flash"
# print(model)
# print(model2)

def clean_input(text: str) -> str:
    """Private method (convention: prefix with _)"""
    part1 = text.split()
    part2 = [line.strip() for line in part1 if line.strip()]
    return part2
print(clean_input("""   Hello

world   """))

def get_stats(self) -> dict:
    return {"notes_processed": len(self.history),
            "tokens_used": self.token_count}