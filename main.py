import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    return {"status": "DanDooz AI running"}

@app.get("/ask")
def ask(question: str):
    try:
        # 1️⃣ Get search results
        results = web_search(question)

        context = "\n".join(
            f"- {r.get('title', '')}: {r.get('snippet', '')}"
            for r in results
        )

        prompt = f"""
You are DanDooz AI, a professional research assistant.

Answer clearly and in detail using the search data.
Do not guess.

Search Data:
{context}

Question:
{question}
"""

        api_key = os.getenv("OPENAI_API_KEY")

        # 2️⃣ If API key missing → don't crash
        if not api_key:
            return {
                "answer": "AI service is not configured.",
                "sources": results
            }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        }

        # 3️⃣ Call OpenAI safely
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=25
        )

        # 4️⃣ If OpenAI fails → safe fallback
        if response.status_code != 200:
            return {
                "answer": "AI service is temporarily unavailable.",
                "sources": results
            }

        data = response.json()

        answer = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if not answer:
            answer = "No answer could be generated."

        return {
            "answer": answer.strip(),
            "sources": results
        }

    except Exception as e:
        # 5️⃣ Absolute safety net — NEVER crash
        return {
            "answer": "Internal processing error. Please try again.",
            "sources": []
        }
