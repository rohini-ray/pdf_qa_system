import faiss
import numpy as np

from pdf_loader import extract_text
from chunker import create_chunks
from embedding import generate_embedding
from config import *

pdf_text = extract_text(
    "data/sample.pdf"
)

chunks = create_chunks(
    pdf_text
)

embeddings = []

for chunk in chunks:

    vector = generate_embedding(
        chunk
    )

    embeddings.append(vector)

embeddings = np.array(
    embeddings
).astype("float32")

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(
    embeddings
)

faiss.write_index(
    index,
    FAISS_INDEX
)

np.save(
    CHUNKS_FILE,
    np.array(chunks)
)

print("PDF Indexed Successfully")