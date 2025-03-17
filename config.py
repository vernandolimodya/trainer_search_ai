import os
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")

# Model Name for Sentence Embeddings
MODEL_NAME = "all-MiniLM-L6-v2"