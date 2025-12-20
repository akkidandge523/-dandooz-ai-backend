print("🔥 RUNNING DANDOOZ BACKEND v2 — SAFE MODE ENABLED 🔥")

import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "answer": "AI service is not configured yet.",
            "sources": []
        }

    prompt = f"""
Answer clearly and in detail.

Question:
{question}
"""

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
            return {
                "answer": "AI service temporarily unavailable.",
                "sources": []
            }

        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        return {
            "answer": answer.strip(),
            "sources": []
        }

    except Exception as e:
        print("OPENAI FAILED:", e)
        return {
            "answer": "AI service temporarily unavailable.",
            "sources": []
        }
