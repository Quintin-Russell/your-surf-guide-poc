def chunk_text(text, chunk_on="\n\n"):
    # Split into chunks by paragraph - each blank line becomes a split point.
    # strip() removes extra whitespace, and the if-check skips empty chunks.
    return [chunk.strip() for chunk in text.split(chunk_on) if chunk.strip()]
