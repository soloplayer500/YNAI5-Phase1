# RESEARCH — Source Methodology & Quality Guide

---

## Source Tier Rankings

### Tier 1 — Primary (highest reliability)
- Official announcements, press releases, company blogs
- Peer-reviewed papers, whitepapers
- Exchange data (Kraken, Binance, CoinGecko API)
- Government filings (SEC, regulatory bodies)

### Tier 2 — High Quality Secondary
- Perplexity deep research synthesis (cross-references 20+ sources)
- Reuters, Bloomberg, WSJ, FT (finance/crypto coverage)
- The Block, CoinDesk, Decrypt (crypto-specific)
- Wired, MIT Tech Review, Ars Technica (AI/tech)

### Tier 3 — Social Signal (trend detection only)
- X/Twitter trending — good for speed, poor for accuracy
- Reddit — good for community sentiment, moderate accuracy
- YouTube — good for reach/interest measurement
- TikTok — good for trend velocity, low accuracy

### Tier 4 — Aggregators (use with caution)
- CoinMarketCap news — aggregates from many sources
- Crypto Panic — raw news feed, unvalidated
- Generic AI news aggregators

---

## Per-Tool Quality Notes

### Perplexity MCP
- `perplexity_search` — fast, good for current events, moderate depth
- `perplexity_research` — slow (2-3 min), excellent depth, synthesizes 20-50 sources
- `perplexity_reason` — best for complex analytical questions
- `perplexity_chat` — good for follow-up questions on a topic
- Reliability: Tier 1-2 sources, well cited

### Gemini MCP
- Strong on: YouTube analysis, image understanding, Google Search grounding
- Weaker on: very recent crypto-specific news
- Best use: video trend analysis, visual content research
- `gemini_deep_research` — comparable to Perplexity deep, different source pool

### PLAYWRIGHT + Reddit
- r/artificial — AI news community, early signal on new models/papers
- r/CryptoCurrency — market sentiment gauge
- r/Bitcoin, r/ethereum — community-specific sentiment
- r/MachineLearning — technical AI research
- Sort by: Hot (trending now) or New (breaking)

### OpenNews MCP
- 72+ crypto-specific news sources
- AI-rated sentiment and trading signal
- Best for: Block Syndicate signal intelligence
- Refreshes: real-time to 15-minute delay depending on source

### last30days skill
- Covers: Reddit, X, YouTube, Hacker News, Polymarket
- 30-day window — not for breaking news
- Best for: understanding what topics are sustaining traction
- Output: synthesized summary with citation links

---

## Query Optimization by Topic

### AI News Queries (best performing)
- "latest AI model releases 2025"
- "AI news this week site:techcrunch.com OR site:wired.com"
- "GPT Claude Gemini news [current month]"
- "[specific model] announced features"

### Crypto Signal Queries
- "[COIN] price prediction analysis"
- "[COIN] whale movement on-chain"
- "[COIN] technical analysis support resistance"
- "crypto market sentiment today"

### Trend Detection Queries (Perplexity)
- "what is trending in AI right now"
- "viral AI tool [current month]"
- "[topic] social media discussion volume"

---

## Output Quality Checklist

Before finalizing any RESEARCH output:
- [ ] At least 2 sources cited
- [ ] All time-sensitive data labeled with approximate date
- [ ] Signal vs noise clearly separated
- [ ] Conflicting information flagged, not hidden
- [ ] Signal strength rating included
- [ ] "So what" conclusion present
- [ ] Content angles included (if for YNAI5 pipeline)
