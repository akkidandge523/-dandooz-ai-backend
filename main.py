print("🔥 RUNNING DANDOOZ BACKEND v2 — SAFE MODE ENABLED 🔥")

import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ SAFE import (prevents Render crash)
try:
    from search import web_search
except Exception as e:
    print("⚠️ search.py failed to load:", e)
    web_search = None

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
    return {"status": "DanDooz AI running"}

@app.get("/ask")
def ask(question: str):
    # 🔎 SAFE SEARCH
    results = []
    if web_search:
        try:
            results = web_search(question)
            if not isinstance(results, list):
                results = []
        except Exception as e:
            print("SEARCH FAILED:", e)
            results = []

    # 🧠 BUILD CONTEXT
    context = "\n".join(
        f"- {r.get('title','')}: {r.get('snippet','')}"
        for r in results if isinstance(r, dict)
    )

    prompt = f"""
You are DanDooz AI.

Answer clearly and in detail.
If search data is weak or empty, answer using general knowledge.

Search data:
{context}

Question:
{question}
"""

    # 🔑 OPENAI SAFETY
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": "AI service is not configured yet.",
            "sources": results
        }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            },
            timeout=30
        )

        if response.status_code != 200:
            print("OpenAI HTTP error:", response.text)
            return {
                "answer": "AI service temporarily unavailable.",
                "sources": results
            }

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        return {
            "answer": answer.strip(),
            "sources": results
        }

    except Exception as e:
        print("OPENAI FAILED:", e)
        return {
            "answer": "AI service temporarily unavailable.",
