import faiss
from handlers.embeddings import model
from handlers.db_connector import fetch_trainers_by_ids

class FaissIndexer:
    def __init__(self, embedding_dim):
        """Initialize a FAISS index"""
        self.index = faiss.IndexFlatL2(embedding_dim)

    def add_to_index(self, embeddings):
        """Add embeddings to FAISS index"""
        self.index.add(embeddings)

    def search_similar(self, query, trainer_ids, top_k=5):
        """Find top-K similar trainers given a query"""
        query_embedding = model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)

        # Retrieve trainer IDs
        return [trainer_ids[idx] for idx in indices[0]]
    
    def get_trainer_details(self, trainer_ids):
        """Fetch trainer bios from the database based on FAISS results"""
        return fetch_trainers_by_ids(trainer_ids)