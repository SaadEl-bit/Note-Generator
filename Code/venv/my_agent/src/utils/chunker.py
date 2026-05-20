"""Split long notes into smaller chunks to fit within API token limits."""


def chunk_text(text: str, max_chars: int = 3000) -> list[str]:
    """
    Split text into chunks of approximately max_chars.
    Splits on paragraph boundaries to avoid breaking sentences.
    Returns list of text chunks.
    """
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current_chunk = []
    current_length = 0

    # Split by double newlines first (paragraphs), then single newlines
    paragraphs = text.split("\n\n")

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        para_len = len(para)

        # If a single paragraph exceeds max_chars, split it by lines
        if para_len > max_chars:
            # Flush current chunk first
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_length = 0

            # Split long paragraph by single newlines
            lines = para.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                line_len = len(line)

                if line_len > max_chars:
                    # Hard split for extremely long lines
                    if current_chunk:
                        chunks.append("\n\n".join(current_chunk))
                        current_chunk = []
                        current_length = 0
                    # Split by words
                    words = line.split()
                    sub_chunk = []
                    sub_length = 0
                    for word in words:
                        if sub_length + len(word) + 1 > max_chars:
                            chunks.append(" ".join(sub_chunk))
                            sub_chunk = [word]
                            sub_length = len(word)
                        else:
                            sub_chunk.append(word)
                            sub_length += len(word) + 1
                    if sub_chunk:
                        chunks.append(" ".join(sub_chunk))
                elif current_length + line_len + 1 > max_chars:
                    # Flush and start new chunk
                    chunks.append("\n\n".join(current_chunk))
                    current_chunk = [line]
                    current_length = line_len
                else:
                    current_chunk.append(line)
                    current_length += line_len + 1
        elif current_length + para_len + 2 > max_chars:
            # Flush current chunk and start new one
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_length = para_len
        else:
            current_chunk.append(para)
            current_length += para_len + 2

    # Don't forget the last chunk
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks
