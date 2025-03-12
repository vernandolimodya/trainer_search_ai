from handlers.db_connector import fetch_trainers
from handlers.embeddings import generate_embeddings
from handlers.faiss_indexer import FaissIndexer

# Step 1: Fetch trainer data from PostgreSQL
df = fetch_trainers()

# Step 2: Generate embeddings
bio_embeddings = generate_embeddings(df["bio"].tolist())

# Step 3: Initialize FAISS index
embedding_dim = bio_embeddings.shape[1]
indexer = FaissIndexer(embedding_dim)

# Step 4: Add embeddings to FAISS index
indexer.add_to_index(bio_embeddings)

# Step 5: Perform a sample search (get only trainer IDs)
query = "Looking for a trainer with expertise in powerlifting and weight loss"
similar_trainer_ids = indexer.search_similar(query, df["id"].values)

# Step 6: Fetch full trainer details from the database
trainer_results = indexer.get_trainer_details(similar_trainer_ids)

# Step 7: Print Results
print("🔹 Similar Trainers Found:")
print(trainer_results)