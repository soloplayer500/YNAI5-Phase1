---
name: playwright
description: >
  PLAYWRIGHT — Activate this skill whenever Solo needs to interact with a live browser, website, or web-based data. Triggers on: scraping crypto prices or market data from any website, monitoring TikTok/X/Instagram/YouTube for AI news or trends, automating content posting flows, testing or debugging web builds and UIs, looking up live portfolio or exchange data, checking any URL for current information, taking screenshots of websites, filling forms automatically, navigating multi-step web flows, or any task where Claude needs to SEE or INTERACT with a real webpage. This is Solo's live browser layer — it sees what a browser sees and can act on it. Works across all YNAI5 infrastructure areas simultaneously.
---

# PLAYWRIGHT — Live Browser Automation Layer

PLAYWRIGHT is the fallback and amplifier for every YNAI5 skill. When an MCP doesn't cover something or data needs to be pulled directly from a live page — PLAYWRIGHT handles it.

Task patterns + scraping templates → `references/tasks.md`

---

## When PLAYWRIGHT Fires vs When MCPs Handle It

| Task | Use MCP | Use PLAYWRIGHT |
|---|---|---|
| Crypto price | hive-crypto MCP | Only if MCP down |
| Kraken portfolio | kraken MCP | kraken.com UI if MCP down |
| Telegram send | telegram MCP | Never — always use MCP |
| TikTok post | No MCP available | ✅ Always PLAYWRIGHT |
| X post confirmation | distribution MCP | ✅ Verify post went through |
| Suno generation | suno MCP | ✅ If session expired |
| Reddit scraping | research-mcp handles | ✅ For specific posts/threads |
| Web build debug | Claude Code | ✅ Live browser test |
| Screenshot any page | — | ✅ Always PLAYWRIGHT |
| Platform analytics | distribution MCP | ✅ For deeper data |

---

## YNAI5 Use Cases by Area

### Block Syndicate — Crypto Data
```
When hive-crypto MCP is down or data needed from specific site:
1. Navigate to coingecko.com/coins/{coin}
2. Wait for price widget to load
3. Extract: price, 24h%, volume, market cap
4. Pass to TRADING for signal scoring

When checking TradingView charts:
1. Navigate to tradingview.com/symbols/{PAIR}/
2. Extract: technical summary (buy/neutral/sell)
3. Extract: RSI, MACD readings from summary panel
4. Pass to APEX Lens #6
```

### OpenMind AI — Content Monitoring
```
AI news scraping:
1. Navigate to reddit.com/r/artificial/hot/
2. Extract top 10: title, upvotes, comment count, link
3. Navigate to x.com/explore → Technology
4. Extract trending AI topics
5. Return news brief → RESEARCH synthesizes → DISTRIBUTION posts

TikTok trend monitoring:
1. Navigate to tiktok.com/discover
2. Search "AI" or "artificial intelligence"
3. Extract: trending hashtags, top sounds, view counts
4. Return trend brief for OpenMind AI content strategy
```

### Symphony — Suno Fallback
```
When suno MCP session expires:
1. Navigate to suno.ai
2. Click "Create" → "Custom"
3. Paste style tags into Style field
4. Paste lyrics into Lyrics field
5. Set title
6. CONFIRM WITH SOLO before clicking Generate
7. Poll for completion → return audio URL

When checking Suno credits:
1. Navigate to suno.ai/account
2. Extract credit count
3. Return to Symphony
```

### Distribution — TikTok Posting
```
TikTok has no MCP — always use PLAYWRIGHT:
1. Navigate to tiktok.com (logged in)
2. Click upload/create
3. Paste caption + hashtags
4. Handle video upload if applicable
5. CONFIRM with Solo before posting
6. Click Post
7. Confirm: "Posted to TikTok at [time]"
```

### Web Builds — Debug & QA
```
Testing Claude Code or Cowork outputs:
1. Navigate to localhost:[port] or deployed URL
2. Screenshot full page
3. JS evaluate: check console errors
4. JS evaluate: check layout overflow
5. Check mobile: resize viewport to 375x812
6. Return: visual issues + JS errors + mobile issues + fixes
```

---

## Execution Pattern

For every PLAYWRIGHT task:

1. **State what you're doing**: "Navigating to coingecko.com to pull BTC data..."
2. **Navigate and wait**: Allow dynamic content to load fully
3. **Extract structured data**: Never return raw HTML
4. **Screenshot on ambiguity**: If page looks unexpected, screenshot + describe
5. **Confirm before submitting**: Any form, post, or purchase needs Solo's OK
6. **Return clean output**: Tables for data, bullets for lists, summary for research

---

## Output Rules

1. **Always describe navigation** before acting — no silent browsing
2. **Structured output only** — not raw HTML or page dumps
3. **Screenshot on confusion** — if something looks wrong, capture it
4. **Flag login walls** — stop and ask for credentials, never guess
5. **Confirm before submitting** anything: forms, posts, purchases, orders
6. **Live data timestamp** — always note when data was pulled
7. **Playwright is fallback** — always try MCPs first, Playwright only if MCP can't cover it

---

## Pipeline Connections

- **→ RESEARCH**: Live scraped data passes to RESEARCH for synthesis
- **→ TRADING**: Live crypto prices from web feed into signal scoring
- **→ SYMPHONY**: Suno generation fallback when MCP session expired
- **→ DISTRIBUTION**: TikTok posting (no MCP), X verification, platform analytics
- **← ALIGN**: ALIGN decides when PLAYWRIGHT is needed vs an MCP
