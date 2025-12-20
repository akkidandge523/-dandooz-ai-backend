"use client";

import { useState } from "react";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const askDanDooz = async () => {
    if (!question) return;

    setLoading(true);
    setAnswer("");

    try {
      const res = await fetch(
        "https://dandooz-ai-backend-production.up.railway.app/ask?question=" +
          encodeURIComponent(question)
      );
      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      setAnswer("Something went wrong. Try again.");
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-lg p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">
          🤖 DanDooz AI
        </h1>

        <input
          type="text"
          placeholder="Ask anything..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full border p-3 rounded-xl mb-4"
        />

        <button
          onClick={askDanDooz}
          className="w-full bg-black text-white py-3 rounded-xl hover:opacity-90"
        >
          {loading ? "Thinking..." : "Ask DanDooz"}
        </button>

        {answer && (
          <div className="mt-4 p-4 bg-gray-50 rounded-xl">
            <p className="whitespace-pre-line">{answer}</p>
          </div>
        )}
      </div>
    </main>
  );
}
