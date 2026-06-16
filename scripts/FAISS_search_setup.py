import faiss

dimension = 384

# Create a flat L2 index
index = faiss.IndexFlatL2(dimension)

print("FAISS Index Ready")
