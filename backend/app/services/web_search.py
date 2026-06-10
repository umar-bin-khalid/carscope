import httpx
from typing import List, Dict, Any


async def web_search_tool(query: str, max_results: int = 4) -> List[Dict[str, Any]]:
    """
    Search using the DuckDuckGo Instant Answers API — no API key required.
    Returns a list of {title, snippet, url} dicts.
    """
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": query,
                    "format": "json",
                    "no_html": "1",
                    "skip_disambig": "1",
                    "no_redirect": "1",
                },
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []

    results: List[Dict[str, Any]] = []

    # Primary abstract (e.g. Wikipedia summary)
    if data.get("AbstractText"):
        results.append({
            "title": data.get("Heading", query),
            "snippet": data["AbstractText"][:400],
            "url": data.get("AbstractURL", ""),
        })

    # Related topic snippets
    for topic in data.get("RelatedTopics", []):
        if len(results) >= max_results:
            break
        if isinstance(topic, dict) and topic.get("Text"):
            raw_url = topic.get("FirstURL", "")
            title = raw_url.rstrip("/").split("/")[-1].replace("_", " ")
            results.append({
                "title": title,
                "snippet": topic["Text"][:300],
                "url": raw_url,
            })

    return results
