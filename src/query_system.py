import faiss
import numpy as np
import ollama

from .embedding import (
    generate_embeddings,
    generate_query_embedding
)
from .config import OLLAMA_MODEL

class PDFQA:
    def __init__(self):
        self.index = None
        self.chunks = None

    def create_index(self, chunks):
        """
        Creates a FAISS index from the generated text chunk embeddings.
        """
        self.chunks = chunks
        embeddings = generate_embeddings(chunks)
        embeddings = np.array(embeddings).astype("float32")
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def retrieve_context(self, question):
        """
        Retrieves the most semantically relevant chunk based on FAISS index search.
        """
        query_vector = generate_query_embedding(question)
        query_vector = np.array([query_vector]).astype("float32")
        
        # Search the index for top 1 nearest neighbor
        distances, indices = self.index.search(query_vector, 1)
        
        context = []
        for idx in indices[0]:
            if idx != -1:
                context.append(self.chunks[idx])
        return "\n".join(context)

    def ask(self, question):
        """
        Formulates a prompt with context and asks the Ollama model for an answer.
        """
        context = self.retrieve_context(question)
        
        prompt = f"""Context:
{context}

Question:
{question}

Answer the question only using the context provided above. If the context does not contain the answer, state that the answer is not available in the document."""

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response["message"]["content"]
