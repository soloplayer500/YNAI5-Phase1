# YNAI5-SU Graphify Knowledge Graph — Query Results

_Generated: 2026-04-13 | Graphify v0.4.11_

---

## Test Query: "What are the main projects and their relationships?"

Graphify performed a BFS traversal of the knowledge graph and returned the following key relationships:

### Key Nodes Found (by community cluster)

| Project / File | Community | Purpose |
|---|---|---|
| `projects/ynai5-mcps/mcps/trading-signals-mcp/server.py` | 0 | Trading signals MCP — RSI, OHLC, correlation |
| `projects/ynai5-mcps/mcps/kraken-mcp/server.py` | 0 | Kraken exchange API — balance, orders, tickers |
| `projects/ynai5-mcps/mcps/perplexity-mcp/server.py` | 5 | Perplexity AI news + web search |
| `projects/ynai5-mcps/mcps/distribution-mcp/server.py` | 5 | Cross-platform content distribution |
| `projects/ynai5-mcps/mcps/genius-mcp/server.py` | 1 | Music/lyrics search (Genius API) |
| `projects/crypto-monitoring/price-alert.py` | 15 | Price threshold alerts → Telegram |
| `tools/gmail-manager.py` | 22 | Gmail inbox triage + Claude AI analysis |

### Key Edges Discovered

| Source | Relationship | Target |
|---|---|---|
| Perplexity news function | `rationale_for` | `post_to_platforms()` — distribution MCP |
| Perplexity news function | `rationale_for` | `get_balance()` — Kraken MCP |
| Perplexity news function | `rationale_for` | `get_artist_songs()` — Genius MCP |
| `correlation_analysis()` | `calls` | `_get_prices()` — fetches live prices |
| `post_to_platforms()` | `calls` | `_ayr()` + `post_ynai5_content()` |
| `_send_telegram_report()` | `calls` | `send_telegram()` + `main()` |
| `run_triage()` | `calls` | Gmail load_state → log → main |
| Price alert | `sends` | Telegram notification |

### Surprising Connection Confirmed

Graphify confirmed the cross-community bridge:
- **Perplexity news fetcher** (Community 5) acts as a common rationale for components in three different communities:
  - Community 0 (Kraken trading) — news context for trade decisions
  - Community 1 (Genius music) — AI news repurposed for content  
  - Community 5 (Distribution) — news fed into social posting pipeline

---

## God Node Explanation: `_cg()` (Most Connected, 17 edges)

**Source:** `projects/ynai5-mcps/mcps/trading-signals-mcp/server.py:L10`  
**Community:** 0 (Trading signals cluster)  
**Degree:** 17 connections

`_cg()` is the CoinGecko gateway function — every market data call in the workspace routes through it:

| Called Function | Purpose |
|---|---|
| `_get_prices()` | Live price fetch for all watched tickers |
| `_get_ohlc()` | OHLC candle data for RSI/TA calculations |
| `get_trending_coins()` | Trending coins feed |
| `get_coingecko_news()` | Crypto news via CoinGecko |
| `get_price()` | Single-ticker price check |
| `get_market_data()` | Full market cap + volume data |
| `get_top_coins()` | Top N coins by market cap |
| `get_global_market()` | Global crypto market overview |
| `get_ohlc_data()` | Extended OHLC for backtesting |
| `get_price_history()` | Historical price series |
| `get_exchange_volumes()` | Exchange volume comparison |
| `run_signal_scan()` | Full technical signal scan |
| `get_market_overview()` | Summary market status |
| `volume_anomaly_detector()` | Unusual volume detection |

**Graphify insight:** `_cg()` is the single most critical function in the entire workspace. All crypto market intelligence — from price alerts to trading signals to Block Syndicate screener — flows through this CoinGecko gateway. If this function breaks, the entire crypto intelligence layer goes dark.

---

## Graphify Usage in Future Sessions

Graphify is now permanently integrated into YNAI5-SU:

- **Graph location:** `graphify-out/graph.json` (771 nodes, 1151 edges)
- **Report:** `graphify-out/GRAPH_REPORT.md`
- **CLAUDE.md section:** Auto-added — Claude reads graph before architecture questions
- **PreToolUse hook:** Fires before Glob/Grep — reminds Claude to check graph first
- **Rebuild command:** `graphify update .` (run after code changes)

### Slash Commands Available
```
graphify query "your question"     # BFS traversal for a question
graphify explain "function_name"   # Node details + all connections
graphify path "node_A" "node_B"    # Shortest path between two nodes
graphify update .                  # Rebuild graph after code changes
```
