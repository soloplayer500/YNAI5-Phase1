---
name: trading-analysis
description: Full trade setup analysis for a specific ticker — screen, technicals, risk, entry/stop/target. Use when user says "analyze [TICKER]", "trade setup", "should I buy/sell X", "entry and stop for X"
---

# /trading-analysis [TICKER] [timeframe?]

Full conviction trade setup. Combines screening, technicals, risk, and action.

## Step 1 — Context Check

Before analyzing, state:
- Current BTC dominance trend (risk-on vs risk-off signal)
- Check fear & greed if available
- Is macro headwind present? (Fed, DXY)

## Step 2 — Technical Analysis

Run `/technical-analysis [TICKER] [timeframe]` and extract:
- Trend direction on 3 timeframes (15m / 4h / daily)
- Key support and resistance levels
- RSI (overbought/oversold?)
- Volume (spike or weak?)
- Pattern (breakout, breakdown, consolidation)

## Step 3 — Setup Scoring (4/5 required to trade)

Score each criterion:
- [ ] Volume: >1.5× 20-day average?
- [ ] Clear S/R level holding?
- [ ] Trend aligned on 15m + 4h + daily?
- [ ] RSI not extreme against trade direction?
- [ ] Invalidation level (stop) is obvious?

If <4/5 → **SKIP. State reason. No entry.**

## Step 4 — Trade Plan

If 4+/5:
```
TICKER:     [symbol]
DIRECTION:  LONG | SHORT
ENTRY:      [price or zone]
STOP:       [price] — invalidation at this level
TARGET 1:   [price] — take partial profit (1:1 R:R)
TARGET 2:   [price] — let rest run (1:2.5+ R:R)
R:R RATIO:  [X:Y]
CONVICTION: [%] — must be >65% to trade
TIMEFRAME:  [hold duration estimate]
```

## Step 5 — Risk Check

- Position size: Never >5% of portfolio (high conviction) or >3% (medium)
- Portfolio exposure: Are we already heavy in this sector?
- State the maximum $ loss if stop is hit

## Step 6 — Log the Prediction

If proceeding with trade idea:
```
/crypto-portfolio --predict [TICKER] [LONG|SHORT] [TARGET] [HOURS] [CONFIDENCE] "[reason]"
```

## Step 7 — Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRADE SETUP — [TICKER] [DATE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VERDICT: TRADE | SKIP | WATCH
DIRECTION: LONG / SHORT
ENTRY: $X
STOP: $X (–Y%)
T1: $X | T2: $X
R:R: 1:Z
CONVICTION: X%
SETUP SCORE: X/5
REASON: [2-3 sentences]
MACRO: [tailwind / headwind / neutral]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
