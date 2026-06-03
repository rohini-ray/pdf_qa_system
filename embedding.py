from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

def generate_embeddings(chunks):

    return model.encode(
        chunks,
        show_progress_bar=True
    )

def generate_query_embedding(query):

    return model.encode(query)
