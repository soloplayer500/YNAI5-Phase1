---
name: stockresearch
description: >
  STOCKRESEARCH — Activate this skill whenever Solo wants to properly research a stock before making a buy or sell decision. Triggers on: "research [ticker]", "break down [company]", "should I invest in X", "help me understand [stock]", "do a deep dive on", "is [company] worth buying", "analyze [ticker] fundamentals", "what do you know about [company]", or any request to understand a company before investing. Runs a structured research pipeline based on the flowchart framework: starting from business understanding → financials → key ratios → risks → valuation → final decision. Adapts depth based on how much Solo already knows about the company.
---

# STOCKRESEARCH — Stock Research Pipeline

Structured 5-phase research framework for any stock before a buy or sell decision. When MCPs are connected, it pulls live data automatically and feeds APEX for the final trade call.

Full methodology → `references/pipeline.md`

---

## MCP Integration — Live Data Throughout

### When RESEARCH MCP connected:
```python
# Phase 1 — Business Overview
company_brief = research.research_stock(ticker)  # pulls fundamentals + news

# Phase 4 — Key Risks (news catalyst)
recent_news = research.research_stock(ticker)  # includes last 2 weeks news

# Deep dive on business
deep = research.deep_research(f"{company_name} business model competitive advantage")
```

### When PERPLEXITY MCP connected:
```python
# Verify facts + get latest data
latest_earnings = perplexity.perplexity_search(f"{ticker} latest earnings EPS revenue")
analyst_ratings = perplexity.perplexity_search(f"{ticker} analyst price target upgrade downgrade")
```

### When OPENNEWS MCP connected (for stocks):
```python
# News sentiment check
news = opennews.get_coingecko_news(ticker.lower())  # fallback for stocks
```

### Data pull sequence:
```
1. research.research_stock(ticker)  → fundamentals + news
2. perplexity.perplexity_search()   → latest earnings + analyst ratings
3. perplexity.perplexity_search()   → key risks + competitive landscape
4. → All data loaded into 5-phase analysis
5. → Feed verdict to APEX for trade decision (optional)
```

---

## Familiarity Check — Step 1

First ask via `ask_user_input_v0`:

**"How well do you know [COMPANY]?"**
- I know it well — skip to Phase 2 (financials)
- I know the name, not the details — give me Phase 1 brief first
- Never heard of it — full pipeline from zero

---

## Research Phases

| Phase | What | MCPs Used |
|---|---|---|
| 1 | Business Overview | research-mcp + perplexity |
| 2 | Financial Statements | research-mcp + perplexity |
| 3 | Key Ratios | research-mcp |
| 4 | Key Risks | research-mcp + opennews |
| 5 | Valuation | research-mcp + perplexity |
| — | Final Verdict | → APEX if trade decision needed |

Full methodology for each phase → `references/pipeline.md`

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 STOCKRESEARCH — [COMPANY] ([TICKER])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 LIVE DATA: [research-mcp + perplexity — timestamp]

📁 PHASE 1 — BUSINESS OVERVIEW
[business brief, moat rating, industry trend, management]

📊 PHASE 2 — FINANCIAL STATEMENTS
[income statement, balance sheet, cash flow — tables]

📐 PHASE 3 — KEY RATIOS
[ROE, net margin, efficiency ratios — with signals]

⚠️ PHASE 4 — KEY RISKS
[concentration, competition, disruption — rated]

💲 PHASE 5 — VALUATION
[P/E, P/FCF, fair value estimate, margin of safety]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 VERDICT: [BUY / WATCH / AVOID]
[2-3 sentence reasoning — specific, no hedging]
📌 MCPs used: [list] | 🔍 Live data: [yes/no]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Output Rules

1. **Pull live data before analysis** when MCPs connected
2. **Phases run in order** — never skip to valuation without fundamentals
3. **Always end with Verdict** — BUY / WATCH / AVOID + 3 specific reasons
4. **Flag data limitations** — if live data unavailable, say so clearly
5. **Tables for financials** — phases 2, 3, 5 always tabular
6. **"Just the verdict"** → run all phases internally, surface only verdict + top 3 reasons

---

## Pipeline Connections

- **→ APEX**: After STOCKRESEARCH verdict, pass to APEX for trade timing (Lens #6 TA)
- **→ TRADING**: APEX verdict → TRADING formats as signal → DISTRIBUTION sends
- **← ALIGN**: ALIGN scopes the research task before STOCKRESEARCH runs
- **← RESEARCH**: For broader market/sector context, RESEARCH runs first
