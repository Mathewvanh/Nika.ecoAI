from sentence_transformers import SentenceTransformer
import os
import numpy as np

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')

chunk_directory = "chunks"
embeddings = []

def get_embedding(text):
    return model.encode(text)

# Process each text chunk
for category in os.listdir(chunk_directory):
    category_dir = os.path.join(chunk_directory, category)
    if os.path.isdir(category_dir):
        for chunk_file in os.listdir(category_dir):
            if chunk_file.endswith(".txt"):
                chunk_path = os.path.join(category_dir, chunk_file)
                with open(chunk_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    embedding = get_embedding(text)
                    embeddings.append(embedding)

import faiss

dimension = embeddings[0].shape[0]  # Dimension of embeddings
faiss_index = faiss.IndexFlatL2(dimension)

# Convert embeddings list to a numpy array
embeddings_matrix = np.array(embeddings)

# Add embeddings to the index
faiss_index.add(embeddings_matrix)

faiss.write_index(faiss_index, 'faiss_index.bin')

# To load the index
# faiss_index = faiss.read_index('faiss_index.bin')

def search_similar_chunks(query_embedding, k=5):
    distances, indices = faiss_index.search(np.array([query_embedding]), k)
    return indices

# Example usage
query_text = "tell me about a summary"
query_embedding = get_embedding(query_text)
similar_chunks_indices = search_similar_chunks(query_embedding)
