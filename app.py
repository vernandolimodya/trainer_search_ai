from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from handlers.db_connector import fetch_trainers
from handlers.embeddings import generate_embeddings
from handlers.faiss_indexer import FaissIndexer
from fastapi.responses import HTMLResponse

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Setup Jinja2 for HTML templates
templates = Jinja2Templates(directory="templates")

# Load data & FAISS index
df = fetch_trainers()
bio_embeddings = generate_embeddings(df["bio"].tolist())

embedding_dim = bio_embeddings.shape[1]
indexer = FaissIndexer(embedding_dim)
indexer.add_to_index(bio_embeddings)

# Define request model
class QueryRequest(BaseModel):
    query: str

@app.get("/results/{query}", response_class=HTMLResponse)
async def show_results(request: Request, query: str):
    """Render the results page based on the query."""
    similar_trainer_ids = indexer.search_similar(query, df["id"].values)
    trainer_results = indexer.get_trainer_details(similar_trainer_ids)

    # Select top 5 trainers only
    top_trainers = trainer_results.head(5).to_dict(orient="records")

    return templates.TemplateResponse(
        "results.html",
        {"request": request, "query": query, "trainers": top_trainers},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)