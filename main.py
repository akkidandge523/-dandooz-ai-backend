from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI
import requests
from search import web_search

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "DanDooz AI Search running"}

@app.get("/ask")
def ask(question: str):
    # 1️⃣ Get fresh search results
    results = web_search(question)

    # Prepare context for AI
    context = ""
    for r in results:
        context += f"- {r['title']}: {r['snippet']}\n"

    # 2️⃣ AI prompt with search context
    prompt = f"""
You are DanDooz AI, a smart search assistant.

Use the information below to answer accurately.
If information is missing, say so clearly.
Do NOT guess facts.

Search results:
{context}

Question:
{question}

Answer in clear, professional language.
"""

    # 3️⃣ Send to local AI (Ollama)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return {
        "answer": data.get("response", "").strip(),
        "sources": results
    }
