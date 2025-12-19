import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import web_search
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USE_LOCAL_AI = os.getenv("USE_LOCAL_AI", "false").lower() == "true"

@app.get("/")
def root():
    return {"status": "DanDooz AI running"}

@app.get("/ask")
def ask(question: str):
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

    if USE_LOCAL_AI:
        # 🔵 LOCAL ONLY (Ollama)
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        ).json()
        answer = res.get("response", "")

    else:
        # 🟢 PRODUCTION (OpenAI / Mistral API)
        headers = {
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        ).json()

        answer = res["choices"][0]["message"]["content"]

    return {
        "answer": answer.strip(),
        "sources": results
    }
