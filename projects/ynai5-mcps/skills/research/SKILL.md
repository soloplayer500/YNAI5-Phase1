---
name: research
description: >
  RESEARCH — Activate this skill for any deep research task, trend analysis, AI news monitoring, market intelligence, or information gathering that requires multiple sources. Triggers on: "research X", "find out about", "what's happening with", "deep dive on", "what are people saying about", "AI news today", "latest on", "monitor X", "find trending", "summarize what's out there on", or any time Solo needs comprehensive current intelligence on a topic. Uses Perplexity MCP (web + deep research), Gemini MCP (YouTube + image analysis), last30days trend scanning, and PLAYWRIGHT for site-specific scraping. Always synthesizes across sources — never just one. Feeds directly into YNAI5 content pipeline and Block Syndicate signal intelligence.
---

# RESEARCH — Multi-Source Intelligence Skill

RESEARCH orchestrates multiple MCPs into one synthesized brief. When fully connected, it runs 4-6 sources in sequence and synthesizes everything automatically.

Source quality guide → `references/sources.md`

---

## Full Pipeline — How It Runs

```
Solo: "research latest AI news for today's content"
         ↓
RESEARCH Step 1: Identify mode
  → Content pipeline (AI news) → Mode: CONTENT BRIEF
         ↓
RESEARCH Step 2: Pull from all connected MCPs
  → perplexity: perplexity_news("artificial intelligence", hours=24)
  → research-mcp: research_ai_news("AI", "today")
  → opennews: get_trending_coins()  [if crypto angle needed]
  → playwright: navigate Reddit r/artificial → scrape top posts
         ↓
RESEARCH Step 3: Cross-reference + synthesize
  → Find overlapping stories (appear in 2+ sources = signal)
  → Rank by recency + engagement + viral potential
  → Separate signal from noise
         ↓
RESEARCH Step 4: Output
  → Structured brief with KEY FINDINGS + CONTENT ANGLES
  → Feed angles to DISTRIBUTION for posting
  → Feed market intel to TRADING for signal context
```

---

## MCP Call Matrix

| Research Type | Primary MCPs | Secondary MCPs |
|---|---|---|
| AI News | research-mcp: research_ai_news | perplexity: perplexity_news |
| Crypto Intel | research-mcp: research_crypto_intel | opennews: get_crypto_news + hive-crypto |
| Deep Research | research-mcp: deep_research | perplexity: perplexity_research |
| Trend Analysis | research-mcp: trend_analysis | playwright: X/TikTok/Reddit scrape |
| Stock Research | research-mcp: research_stock | perplexity: perplexity_search |
| Artist Research | research-mcp: research_music_artist | genius + spotify MCPs |
| Fact Check | research-mcp: fact_check | perplexity: perplexity_reason |
| Competitor Intel | research-mcp: competitor_research | playwright: profile scrape |

---

## Mode Selection

| Solo says... | Mode | MCPs called |
|---|---|---|
| "AI news today" / "what's trending in AI" | CONTENT BRIEF | research-mcp + perplexity-news + playwright |
| "research [COIN]" / "what's happening with ETH" | CRYPTO INTEL | research-mcp + opennews + hive-crypto |
| "deep dive on X" / "comprehensive research" | DEEP RESEARCH | research-mcp + perplexity-research |
| "what's trending on TikTok/X" | TREND SCAN | playwright + research-mcp |
| "research [STOCK]" for investment | STOCK INTEL | research-mcp + perplexity |
| "make me a song like [artist]" | ARTIST INTEL | research-mcp + genius + spotify |
| "is this true: [claim]" | FACT CHECK | research-mcp + perplexity-reason |
| "research [competitor]" | COMPETITIVE | research-mcp + playwright |

---

## Context Gathering

If mode is unclear, use `ask_user_input_v0`:

**Q: What's this research for?**
Options: [YNAI5 content post | Block Syndicate signal | Symphony music | Personal knowledge | Trading decision]

**Q: How deep?**
Options: [Quick summary (1 min) | Medium brief (3-5 min) | Full deep research (10+ min)]

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔎 RESEARCH — [TOPIC] | [MODE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 KEY FINDINGS
• [Finding 1 — with source]
• [Finding 2 — with source]
• [Finding 3 — with source]

📊 SIGNAL STRENGTH: [HIGH / MEDIUM / LOW]
⏱ Recency: [oldest source date]
🔍 Sources: [MCPs + platforms used]

🎯 SO WHAT
[1-2 sentences: what this means for Solo's decision/content/signal]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**For CONTENT BRIEF mode, add:**
```
📱 CONTENT ANGLES
🔥 [Hook angle — high engagement]
💡 [Educational angle]
🚨 [Breaking/urgent angle]
```

**For CRYPTO INTEL mode, add:**
```
📈 MARKET SIGNAL
Direction: [Bullish / Bearish / Neutral]
Key Catalyst: [what's driving it]
Timeframe: [when it matters]
→ Pass to TRADING for signal generation
```

---

## Output Rules

1. **Always synthesize — never paste raw results**
2. **Cross-reference minimum 2 MCPs** before finalizing any factual claim
3. **Always show recency** — stale intel labeled as current is worse than nothing
4. **Content angles only when** Solo's purpose is content creation
5. **Crypto intel always includes signal direction** → feeds TRADING
6. **Playwright fallback** when specific site data needed that MCPs don't cover

---

## Pipeline Connections

- **→ TRADING**: Crypto intel feeds signal context for Block Syndicate
- **→ DISTRIBUTION**: Content brief angles → formatted posts → published
- **→ APEX**: Stock research feeds Lens #1 (Goldman) or #2 (DCF) analysis
- **→ SYMPHONY**: Artist research feeds DNA profile for music production
- **← PLAYWRIGHT**: Live social scraping when MCP data isn't fresh enough
- **← ALIGN**: ALIGN gates and scopes research tasks before RESEARCH executes
