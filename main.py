import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from search import web_search

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ----------------
@app.get("/")
def root():
    return {"status": "DanDooz AI running"}

@app.get("/ask")
def ask(question: str):
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    results = web_search(question)

    context = "\n".join(
        f"- {r['title']}: {r['snippet']}" for r in results
    )

    prompt = f"""
You are DanDooz AI.
Use search results to answer accurately.
Do not guess.

Search:
{context}

Question:
{question}
"""

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    headers = {
        "Authorization": f"Bearer {openai_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI error: {response.text}"
        )

    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    return {
        "answer": answer.strip(),
        "sources": results
    }

# ---------------- RENDER ENTRY ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
