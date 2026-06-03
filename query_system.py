import faiss
import numpy as np
import ollama

from embedding import generate_embedding
from config import *

# Load FAISS index
index = faiss.read_index(
    FAISS_INDEX
)

# Load stored chunks
chunks = np.load(
    CHUNKS_FILE,
    allow_pickle=True
)

# -------------------------
# Retrieval Function
# -------------------------

def retrieve_context(question):

    query_vector = generate_embedding(
        question
    )

    query_vector = np.array(
        [query_vector]
    ).astype("float32")

    distances, indices = index.search(
        query_vector,
        3
    )

    context = []

    for idx in indices[0]:

        context.append(
            chunks[idx]
        )

    return "\n".join(context)

# -------------------------
# QA Function
# -------------------------

def ask_question(question):

    context = retrieve_context(
        question
    )

    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer using only the context.
    """

    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]

# -------------------------
# Chat Loop
# -------------------------

while True:

    question = input("Ask Question: ")

    if question.lower() == "exit":
        break

    answer = ask_question(question)

    print("\nAnswer:")
    print(answer)