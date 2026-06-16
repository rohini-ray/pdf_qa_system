def create_chunks(text, chunk_size=1000):
    """
    Splits the input text into chunks of specified size.
    """
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i : i + chunk_size])
    return chunks
