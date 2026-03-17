"""
trend.py — Finds today's top viral AI topic for TikTok.
3 Brave Search queries → score virality → return top pick + save trends file.
"""
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

BRAVE_URL = "https://api.search.brave.com/res/v1/web/search"

VIRALITY_KEYWORDS = [
    "just announced", "breaking", "shocking", "everyone", "viral",
    "billions", "trillion", "beats", "surpasses", "replaces", "fires",
    "launches", "acquires", "banned", "leaked", "exposed", "partnership",
    "apple", "google", "openai", "anthropic", "meta", "nvidia", "microsoft",
    "chatgpt", "gemini", "claude", "gpt", "siri", "ai model",
]


def _brave_search(query: str) -> list:
    params = urllib.parse.urlencode({
        "q": query, "count": 10, "search_lang": "en", "freshness": "pd",
    })
    req = urllib.request.Request(
        f"{BRAVE_URL}?{params}",
        headers={"Accept": "application/json", "X-Subscription-Token": config.BRAVE_API_KEY}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()).get("web", {}).get("results", [])
    except Exception as e:
        print(f"  [trend] Search error '{query}': {e}")
        return []


def _score(result: dict) -> float:
    text = (result.get("title", "") + " " + result.get("description", "")).lower()
    score = sum(0.5 for kw in VIRALITY_KEYWORDS if kw in text)
    big = ["apple", "google", "openai", "meta", "nvidia", "microsoft"]
    score += sum(0.8 for name in big if name in text)
    return min(score, 10.0)


def _hook(title: str, desc: str) -> str:
    text = (title + desc).lower()
    if any(w in text for w in ["replac", "partner", "beats", "surpass"]):
        return f"Nobody expected this: {title}"
    if any(w in text for w in ["billion", "trillion"]):
        return f"The money behind this is wild: {title}"
    if any(w in text for w in ["ban", "expos", "leak"]):
        return f"They tried to hide this: {title}"
    return f"Wait— {title}"


def get_top_trend() -> dict:
    date_str = datetime.now().strftime("%B %d %Y")
    queries = [
        f"AI news today {date_str}",
        f"trending AI tools viral TikTok {date_str}",
        f"ChatGPT Claude Gemini news this week {date_str}",
    ]
    print("[trend] Running 3 Brave searches...")
    all_results = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        for results in ex.map(_brave_search, queries):
            all_results.extend(results)

    if not all_results:
        return {"title": "AI is changing everything in 2026", "hook": "Wait— AI just did something wild",
                "source_url": "", "virality": 5.0, "description": "General AI trends"}

    seen, unique = set(), []
    for r in all_results:
        url = r.get("url", "")
        if url not in seen:
            seen.add(url); unique.append(r)

    scored = sorted(unique, key=_score, reverse=True)
    top = scored[0]
    title = top.get("title", "AI News Today")
    desc = top.get("description", "")
    result = {
        "title": title, "hook": _hook(title, desc),
        "source_url": top.get("url", ""),
        "virality": round(_score(top), 1),
        "description": desc,
    }
    _save(result, scored[:5])
    return result


def _save(top: dict, all_scored: list) -> None:
    date = config.today()
    path = config.TRENDS_DIR / f"{date}-trends.md"
    lines = [f"# Trend Check: {date}", "Platform: TikTok (auto-pipeline)", "",
             "## Top Pick", f"**{top['title']}**",
             f"- Hook: {top['hook']}", f"- Virality: {top['virality']}/10",
             f"- Source: {top['source_url']}", "", "## All Candidates"]
    for i, r in enumerate(all_scored, 1):
        lines.append(f"{i}. [{r.get('title','')}]({r.get('url','')}) — {round(_score(r),1)}/10")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  [trend] Saved -> {path.name}")


if __name__ == "__main__":
    result = get_top_trend()
    print(f"\n[trend] Top pick: {result['title']}")
    print(f"        Hook: {result['hook']}")
    print(f"        Virality: {result['virality']}/10")
