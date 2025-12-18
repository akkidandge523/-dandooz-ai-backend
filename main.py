from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import web_search

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "DanDooz AI backend running"}

@app.get("/search")
def search(query: str):
    results = web_search(query)
    return {
        "query": query,
        "results": results
    }
