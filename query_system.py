import faiss
import numpy as np
import ollama

from embedding import (
    generate_embeddings,
    generate_query_embedding
)

class PDFQA:

    def __init__(self):

        self.index = None
        self.chunks = None

    def create_index(self, chunks):

        self.chunks = chunks

        embeddings = generate_embeddings(
            chunks
        )

        embeddings = np.array(
            embeddings
        ).astype("float32")

        self.index = faiss.IndexFlatL2(
            embeddings.shape[1]
        )

        self.index.add(
            embeddings
        )

    def retrieve_context(
            self,
            question):

        query_vector = generate_query_embedding(
            question
        )

        query_vector = np.array(
            [query_vector]
        ).astype("float32")

        distances, indices = self.index.search(
            query_vector,
            1
        )

        context = []

        for idx in indices[0]:

            context.append(
                self.chunks[idx]
            )

        return "\n".join(context)

    def ask(self, question):

        context = self.retrieve_context(
            question
        )

        prompt = f"""
        Context:
        {context}

        Question:
        {question}

        Answer only from context.
        """

        response = ollama.chat(
            model="gemma2:2b",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        return response["message"]["content"]