import os
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

# PostgreSQL Configuration
DB_CONFIG = {
    "dbname": "trainer_db",
    "user": os.getenv("POSTGRES_USERNAME"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "localhost",
    "port": "5432",
}

# Model Name for Sentence Embeddings
MODEL_NAME = "all-MiniLM-L6-v2"