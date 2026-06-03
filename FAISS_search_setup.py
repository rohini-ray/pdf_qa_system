import faiss

dimension = 384

index = faiss.IndexFlatL2(
    dimension
)

print("FAISS Index Ready")