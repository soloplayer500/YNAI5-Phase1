import os, httpx, json
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("research")
PERP_KEY = os.getenv("PERPLEXITY_API_KEY", "")
PERP_URL = "https://api.perplexity.ai/chat/completions"

def _perplexity(prompt: str, model: str = "sonar", max_tokens: int = 2000) -> str:
    if not PERP_KEY:
        return "Perplexity API key not set. Add PERPLEXITY_API_KEY to .env"
    r = httpx.post(
        PERP_URL,
        headers={"Authorization": f"Bearer {PERP_KEY}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens},
        timeout=120
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

@mcp.tool()
def research_ai_news(topic: str = "artificial intelligence", timeframe: str = "today") -> str:
    """Research latest AI news for YNAI5/OpenMind AI content pipeline."""
    prompt = f"""Find the most important and viral AI news about "{topic}" from {timeframe}.

Return:
1. TOP 5 STORIES (title, source, why it matters, viral potential 1-10)
2. CONTENT ANGLES (3 angles for short-form content - TikTok/X)
3. SIGNAL (Bullish/Bearish/Neutral for AI sector)

Be specific, cite dates and sources."""
    return _perplexity(prompt, "sonar")

@mcp.tool()
def research_crypto_intel(asset: str, timeframe: str = "past 48 hours") -> str:
    """Research crypto market intel for Block Syndicate signal generation."""
    prompt = f"""Research {asset} cryptocurrency for the {timeframe}.

Return:
1. PRICE ACTION NARRATIVE (what happened and why)
2. KEY CATALYSTS (news, partnerships, on-chain events)
3. MARKET SENTIMENT (community + institutional)
4. RISKS (what could invalidate a long/short)
5. OUTLOOK (1 week, 1 month)

Cite specific sources and dates."""
    return _perplexity(prompt, "sonar")

@mcp.tool()
def deep_research(topic: str) -> str:
    """Deep research synthesis — 2-3 minutes, 20-50 sources. For major decisions or content."""
    return _perplexity(
        f"Conduct comprehensive research on: {topic}. Synthesize findings from multiple sources. Include recent developments, key facts, expert opinions, and actionable insights.",
        model="sonar-deep-research",
        max_tokens=4000
    )

@mcp.tool()
def trend_analysis(platform: str = "all", topic: str = "AI") -> str:
    """Analyze trending topics across social platforms for content strategy."""
    prompt = f"""What is currently trending about "{topic}" on {platform}?

Return:
1. TOP TRENDING TOPICS (last 24-48h)
2. VIRAL CONTENT FORMATS (what's working)
3. HASHTAGS TO USE
4. BEST CONTENT ANGLE for a solo creator in AI/crypto space
5. COMPETITOR EXAMPLES (who's crushing it on this topic right now)"""
    return _perplexity(prompt, "sonar")

@mcp.tool()
def competitor_research(creator_or_brand: str, platform: str = "TikTok") -> str:
    """Research a competitor or brand in the AI/crypto content space."""
    prompt = f"""Research {creator_or_brand} on {platform}.

Return:
1. CONTENT STRATEGY (what they post, how often, what performs)
2. TOP PERFORMING CONTENT (themes, formats, hooks)
3. AUDIENCE (who follows them)
4. GAPS (what they're missing that YNAI5 could own)
5. TACTICS to outperform them"""
    return _perplexity(prompt, "sonar")

@mcp.tool()
def research_music_artist(artist: str) -> str:
    """Research an artist's style for Symphony music production reference."""
    prompt = f"""Analyze {artist}'s music style for production reference.

Return:
1. SIGNATURE SOUND (genre, BPM range, key signatures, production style)
2. LYRICAL THEMES (top 5 recurring themes)
3. FLOW PATTERNS (delivery style, cadence, signature techniques)
4. VOCABULARY (common words, slang, phrases)
5. SUNO TAGS (exact style tags to use when generating music inspired by them)
6. TOP 5 REFERENCE TRACKS (their most characteristic songs)"""
    return _perplexity(prompt, "sonar")

@mcp.tool()
def research_stock(ticker: str) -> str:
    """Quick stock research for APEX/STOCKRESEARCH pipeline."""
    prompt = f"""Research {ticker} stock.

Return:
1. BUSINESS (what they do, revenue model, market position)
2. KEY METRICS (recent revenue, EPS, growth rate, P/E if available)
3. RECENT NEWS (last 2 weeks — earnings, guidance, catalysts)
4. BULL CASE (top 3 reasons to be bullish)
5. BEAR CASE (top 3 risks)
6. ANALYST SENTIMENT (upgrade/downgrades, price targets if available)"""
    return _perplexity(prompt, "sonar")

@mcp.tool()
def fact_check(claim: str) -> str:
    """Fact-check a claim with web sources before publishing as Block Syndicate signal or YNAI5 content."""
    prompt = f"""Fact-check this claim: "{claim}"

Return:
1. VERDICT: TRUE / FALSE / PARTLY TRUE / UNVERIFIED
2. EVIDENCE (sources that support or contradict)
3. NUANCE (what's missing from the claim)
4. CONFIDENCE: HIGH / MEDIUM / LOW"""
    return _perplexity(prompt, "sonar-reasoning-pro")

if __name__ == "__main__":
    mcp.run()
