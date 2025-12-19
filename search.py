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

    try:
        res = requests.get("https://serpapi.com/search", params=params, timeout=10)
        data = res.json()
    except Exception:
        return []

    results = []

    for r in data.get("organic_results", []):
        results.append({
            "title": r.get("title", "No title"),
            "snippet": r.get("snippet", "No description available"),
            "link": r.get("link", "")
        })

    return results
