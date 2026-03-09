# Crypto Monitoring & Analysis System
**Status:** 🧪 Concept/Dev — Starting Development
**Type:** Market monitoring, trade journaling, and structured analysis

---

## What It Is
A personal crypto intelligence system that tracks market activity, generates structured analysis, and supports disciplined trade decisions. Designed to remove emotional trading by introducing structured evaluation (via PsycheCore's Ledger Node).

## Problem It Solves
- Keeps emotional decisions out of trading
- Creates a searchable history of trades and reasoning
- Provides web-searched price/news/sentiment on demand
- Documents and refines trading strategies over time

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Watchlist | watchlist.md | Active tickers, thresholds, notes |
| Trade Journal | trade-journal.md | All trades logged with reasoning |
| Strategies | strategies.md | Documented trading rules and systems |
| Research | research/ | Dated deep dives per asset |

## Skills
- `/market-check [ticker]` — real-time price + news + sentiment → saved to research/

## Current Focus
Setting up watchlist and trade journal format.

## Tools
- Kraken — primary trading platform
- Claude `/market-check` skill — web research on demand
- PsycheCore Ledger Node — trade evaluation framework
