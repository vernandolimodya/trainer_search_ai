import psycopg2
import pandas as pd
import os
from config import POSTGRES_URL

def connect_db():
    """Establishes a connection to PostgreSQL"""
    return psycopg2.connect(POSTGRES_URL)

def fetch_trainers():
    """Fetch trainer bios from PostgreSQL"""
    conn = connect_db()
    cur = conn.cursor()

    query = "SELECT id, bio FROM users WHERE role = 'Trainer';"
    cur.execute(query)

    # Fetch results & convert to DataFrame
    trainers = cur.fetchall()
    df = pd.DataFrame(trainers, columns=['id', 'bio'])

    # Close connection
    cur.close()
    conn.close()
    
    return df

def fetch_trainers_by_ids(trainer_ids):
    """Fetch trainer details by a list of IDs"""
    if not trainer_ids:
        return pd.DataFrame(columns=['id', 'bio'])  # Return empty DataFrame if no matches

    conn = connect_db()
    cur = conn.cursor()

    # Use SQL's `IN` clause to fetch multiple trainers
    query = f"SELECT name, bio FROM users WHERE id IN ({','.join(map(str, trainer_ids))});"
    cur.execute(query)

    trainers = cur.fetchall()
    df = pd.DataFrame(trainers, columns=['name', 'bio'])

    cur.close()
    conn.close()
    
    return df