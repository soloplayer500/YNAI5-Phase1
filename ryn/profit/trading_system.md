# Trading System — RYN Edge Framework
_Systematic approach to crypto/stock trading. Edge > luck._

Last Updated: 2026-04-24

---

## Trading Philosophy

1. **System over intuition** — every trade follows the framework
2. **Risk-first** — define stop before entry, always
3. **Log everything** — predictions tracked, accuracy measured
4. **Edge-building** — no scaling until 70%+ accuracy over 20 calls
5. **Asymmetric setups** — risk:reward minimum 1:2, prefer 1:3+

---

## Daily Workflow

```
[09:00 AST] /market-scan  → fear/greed + top movers + macro context
[09:15 AST] /crypto-screen → top 3 setups with entry/stop/target
[09:30 AST] /trading-analysis [best setup] → full conviction analysis
[If entry] → /crypto-portfolio --predict TICKER DIR TARGET HOURS CONF REASON
[Weekly] → /crypto-portfolio --stats → accuracy review
```

---

## Position Sizing Framework

| Conviction | Max Position Size | R:R Required |
|------------|------------------|-------------|
| High (80%+) | 5% of portfolio | ≥ 1:2 |
| Medium (65–80%) | 3% of portfolio | ≥ 1:2.5 |
| Low (<65%) | Skip | — |

**Rule:** Never risk more than 2% of total portfolio on a single trade.

---

## Setup Criteria (Must hit 4/5)

- [ ] Volume spike (>1.5× 20-day avg)
- [ ] Clear S/R level holding
- [ ] Trend alignment (15m + 4h + daily)
- [ ] RSI not overbought/oversold against trade direction
- [ ] Clear invalidation level (stop is obvious)

---

## Current Positions (Kraken)

| Asset | Status | Notes |
|-------|--------|-------|
| BTC | Underwater ~21% | Reserve asset — DCA on dips |
| ETH | Underwater ~30% | Wait for BTC dominance peak |
| SOL | Underwater ~40% | High beta — hold for bull cycle |
| PENGU | ~84% of portfolio | Meme play — watch exit |
| Others | Dust | Ignore, costs > value |

**Strategy:** No new alts until BTC dominance peaks and turns down. DCA BTC on significant dips.

---

## Macro Context

| Indicator | Current | Signal |
|-----------|---------|--------|
| BTC Dominance | ~56% | Risk-off — NOT alt season |
| Fear & Greed | Check daily | Run /market-scan |
| Fed Rate | Check quarterly | Run /macro-impact |
| DXY trend | Check weekly | Strong DXY = crypto headwind |

---

## Prediction Tracking

All trade ideas logged via:
```
/crypto-portfolio --predict TICKER DIRECTION TARGET HOURS CONFIDENCE "REASON"
```

Weekly review:
```
/crypto-portfolio --stats
```

**Target:** 70% accuracy over 20 predictions before increasing position sizes.

---

## Risk Management Rules

1. Stop-loss is non-negotiable — set on entry
2. Never average down on a losing trade more than once
3. Take partial profits at 1:1 R:R, let rest run
4. If portfolio drawdown >15% — pause trading, review system
5. Macro trumps technicals — if Fed pivots hawkish, reduce risk
