
import time
from typing import Dict, Tuple
import requests
from bs4 import BeautifulSoup
from modules.providers import call_model

_CACHE: Dict[str, Tuple[float, str]] = {}
_TTL_SEC = 15 * 60

def _ttl_get(q: str) -> str | None:
    row = _CACHE.get(q)
    if not row:
        return None
    ts, val = row
    if time.time() - ts > _TTL_SEC:
        _CACHE.pop(q, None)
        return None
    return val

def _ttl_set(q: str, val: str):
    _CACHE[q] = (time.time(), val)

def fetch_and_summarize(q: str) -> Dict:
    cached = _ttl_get(q)
    if cached:
        return {"ok": True, "query": q, "summary": cached, "cached": True}

    text = ""
    source = ""
    try:
        resp = requests.get(
            "https://duckduckgo.com/html/",
            params={"q": q},
            headers={"User-Agent": "AutoserGPT-T1/1.0"},
            timeout=10,
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        first = soup.select_one(".result__a")
        if first and first.get("href"):
            link = first.get("href")
            page = requests.get(link, headers={"User-Agent": "AutoserGPT-T1/1.0"}, timeout=10)
            page.raise_for_status()
            psoup = BeautifulSoup(page.text, "html.parser")
            body_text = " ".join([p.get_text(strip=True) for p in psoup.select("p")])[:4000]
            text = body_text or psoup.get_text(" ", strip=True)[:4000]
            source = link
    except Exception:
        text = f"(offline) Mocked web content for query: {q}. Provide 5 concise insights and a one-line takeaway."
        source = "mock://offline"

    prompt = (
        f"Summarize the following content for the query '{q}'. "
        "Return 5 concise bullet points and a one-line actionable takeaway.\n\n"
        f"CONTENT:\n{text[:3500]}"
    )
    summary = call_model(prompt, provider_hint=None)
    _ttl_set(q, summary)
    return {"ok": True, "query": q, "summary": summary, "cached": False, "source": source}
