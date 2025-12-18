import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def web_search(query):
    if not SERPAPI_KEY:
        return []

    params = {
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_KEY,
        "num": 5
    }

    res = requests.get("https://serpapi.com/search", params=params)
    data = res.json()

    results = []
    for r in data.get("organic_results", []):
        results.append({
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet")
        })

    return results
