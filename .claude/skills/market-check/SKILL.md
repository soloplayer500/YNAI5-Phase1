---
name: market-check
description: Check current price, news, and market sentiment for a crypto or stock ticker. Saves research to the crypto-monitoring project.
argument-hint: [ticker or ticker list, e.g. BTC or BTC ETH SOL]
allowed-tools: Bash, Read, Write
---

Run a market check for: $ARGUMENTS

## Steps

1. Use WebSearch to find:
   - Current price and 24h % change
   - Recent news (last 48 hours) for each ticker
   - General market sentiment (bullish/bearish/neutral)
   - Any notable events (upgrades, listings, regulation news, etc.)

2. For each ticker, compile a structured report

3. Save to `projects/crypto-monitoring/research/YYYY-MM-DD-[ticker].md`

4. Return a quick summary in chat

## Research File Format

```markdown
# Market Check: [TICKER]
Date: YYYY-MM-DD
Price at Check: $X (24h: +/-X%)

## Current Sentiment
[bullish/bearish/neutral — 1-2 sentences]

## Recent News
- [News item 1 — source — date]
- [News item 2 — source — date]
- [News item 3 — source — date]

## Key Levels
- Support: $X
- Resistance: $X

## Notable Events
[Any upcoming events, catalysts, or risks]

## Ledger Check
[Quick risk assessment — is this a good time to be active in this asset?]
```

If multiple tickers are passed, create a separate file for each.
Save each file and confirm in chat.
