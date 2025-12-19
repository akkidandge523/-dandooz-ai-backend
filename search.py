import os
import requests

def web_search(query: str):
    try:
        api_key = os.getenv("SERPAPI_KEY")
        if not api_key:
            return []

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": 5
        }

        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            return []

        data = response.json()
        results = []

        # Answer box
        answer_box = data.get("answer_box")
        if isinstance(answer_box, dict):
            results.append({
                "title": answer_box.get("title", "Answer"),
                "snippet": answer_box.get("answer") or answer_box.get("snippet", ""),
                "link": answer_box.get("link", "")
            })

        # Knowledge graph
        kg = data.get("knowledge_graph")
        if isinstance(kg, dict):
            desc = kg.get("description")
            if desc:
                results.append({
                    "title": kg.get("title", "Overview"),
                    "snippet": desc,
                    "link": kg.get("source", {}).get("link", "")
                })

        # Organic results
        for r in data.get("organic_results", []):
            if isinstance(r, dict):
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("snippet", ""),
                    "link": r.get("link", "")
                })

        return results[:7]

    except Exception:
        # 🔒 Absolute safety: never crash search
        return []
