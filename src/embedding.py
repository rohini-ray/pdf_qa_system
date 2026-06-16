from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL

# Load the local sentence-transformer model
model = SentenceTransformer(EMBEDDING_MODEL)

def generate_embeddings(chunks):
    """
    Generates embeddings for a list of text chunks.
    """
    return model.encode(
        chunks,
        show_progress_bar=True
    )

def generate_query_embedding(query):
    """
    Generates embedding for a single text query.
    """
    return model.encode(query)
