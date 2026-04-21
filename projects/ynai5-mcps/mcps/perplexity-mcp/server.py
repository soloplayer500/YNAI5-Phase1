import os, httpx
from fastmcp import FastMCP

mcp = FastMCP("perplexity")
API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
BASE = "https://api.perplexity.ai"

def _call(model: str, messages: list, max_tokens=2000):
    r = httpx.post(
        f"{BASE}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "max_tokens": max_tokens},
        timeout=120
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

@mcp.tool()
def perplexity_search(query: str, recency: str = "week") -> str:
    """Fast web search via Perplexity. recency: hour, day, week, month, year"""
    return _call("sonar", [
        {"role": "system", "content": f"Search the web. Focus on results from the past {recency}. Be concise and cite sources."},
        {"role": "user", "content": query}
    ])

@mcp.tool()
def perplexity_research(query: str) -> str:
    """Deep research synthesis across 20-50 sources. Takes 60-90 seconds. Use for comprehensive intel."""
    return _call("sonar-deep-research", [
        {"role": "system", "content": "You are a research analyst. Synthesize comprehensive findings with citations. Structure your response clearly."},
        {"role": "user", "content": query}
    ], max_tokens=4000)

@mcp.tool()
def perplexity_reason(query: str) -> str:
    """Complex reasoning with web grounding. Best for analysis, not just lookup."""
    return _call("sonar-reasoning-pro", [
        {"role": "system", "content": "Think through this carefully with web-grounded reasoning."},
        {"role": "user", "content": query}
    ], max_tokens=3000)

@mcp.tool()
def perplexity_news(topic: str, hours: int = 24) -> str:
    """Get latest news on a topic from the past N hours. Perfect for AI news and crypto signals."""
    return _call("sonar", [
        {"role": "system", "content": f"Find the latest news from the past {hours} hours only. Return top stories with dates and sources."},
        {"role": "user", "content": f"Latest news about: {topic}"}
    ])

if __name__ == "__main__":
    mcp.run()
