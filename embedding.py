from sentence_transformers import SentenceTransformer
from config import *

model = SentenceTransformer(
    EMBEDDING_MODEL
)

def generate_embedding(text):

    return model.encode(text)
