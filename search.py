import os
import requests

def web_search(query: str):
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return []

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 5
    }

    res = requests.get("https://serpapi.com/search", params=params, timeout=10)
    data = res.json()

    results = []

    # ✅ Answer box (very important)
    answer_box = data.get("answer_box")
    if answer_box:
        results.append({
            "title": answer_box.get("title", "Answer"),
            "snippet": answer_box.get("answer", answer_box.get("snippet", "")),
            "link": answer_box.get("link", "")
        })

    # ✅ Knowledge graph (people, companies)
    kg = data.get("knowledge_graph")
    if kg:
        description = kg.get("description")
        if description:
            results.append({
                "title": kg.get("title", "Overview"),
                "snippet": description,
                "link": kg.get("source", {}).get("link", "")
            })

    # ✅ Organic results
    for r in data.get("organic_results", []):
        results.append({
            "title": r.get("title", "No title"),
            "snippet": r.get("snippet", "No description"),
            "link": r.get("link", "")
        })

    return results[:7]
