from sentence_transformers import SentenceTransformer
from config import MODEL_NAME

# Load pre-trained SentenceTransformer model
model = SentenceTransformer(MODEL_NAME)

def generate_embeddings(text_list):
    """Convert text data (bios) into embeddings"""
    return model.encode(text_list, convert_to_numpy=True)