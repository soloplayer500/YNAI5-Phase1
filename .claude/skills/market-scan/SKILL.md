---
name: market-scan
description: Daily morning market scan — fear/greed index, top movers, signal scan, crypto + stock brief. Use when user says "morning scan", "market check", "what's moving", "daily brief", "scan the market"
---

# /market-scan [--crypto | --stocks | --both]

**Default:** --both (crypto + stocks)

15-minute morning brief. No deep analysis — just what to watch today.

## Step 1 — Fear & Greed + Global Macro

```
/market-check BTC
```

Extract:
- BTC price + 24h change
- Fear & Greed index (Extreme Fear / Fear / Neutral / Greed / Extreme Greed)
- BTC dominance (>55% = risk-off, <50% = alt season signal)
- DXY trend if available (strong DXY = crypto headwind)

## Step 2 — Top Crypto Movers

Find top 5 movers (gainers + losers) in last 24h:
- Use `/market-check` for key tickers: BTC, ETH, SOL, BNB, XRP
- Check for any portfolio holdings movements
- Note: any in our Kraken portfolio up/down >5%?

## Step 3 — Signal Scan (Crypto)

Run: `/crypto-screen medium` — medium complexity setups  
Extract top 2–3 setups worth watching today.

## Step 4 — Stock Watch (if --stocks or --both)

Run: `/stock-screen medium [sector?]`  
Top 2 stock setups worth watching.

## Step 5 — News Pulse

Run: `/market-check [BTC|ETH]` for news section  
Flag: any macro events today (Fed meeting, CPI, earnings)?

## Step 6 — Portfolio Alert Check

Quick Kraken check: `/kraken balance`  
Note any position moving >5% — flag for trading-analysis if breakout.

## Step 7 — Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MARKET SCAN — [DATE] [TIME] AST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MACRO:
  Fear & Greed: X/100 [label]
  BTC Dominance: X% [risk-on/off]
  DXY: [trend]
  Macro events today: [events or NONE]

TOP MOVERS (24h):
  ▲ [TICKER]: +X%
  ▲ [TICKER]: +X%
  ▼ [TICKER]: -X%

PORTFOLIO FLAGS:
  [any >5% move in holdings]

SETUPS TO WATCH:
  🟢 [TICKER] — [brief setup description]
  🟡 [TICKER] — [brief setup description]

STOCKS:
  [top 1-2 setups if relevant]

TODAY'S BIAS: RISK-ON | RISK-OFF | NEUTRAL
ACTION: [1-sentence recommendation]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 8 — Log if Trading

If any setup triggers a trade idea:
```
/trading-analysis [TICKER]
```
