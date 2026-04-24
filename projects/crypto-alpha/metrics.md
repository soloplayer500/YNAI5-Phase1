# Crypto Alpha — Metrics

_What we track. Update weekly (Sunday) and monthly (1st)._

## Leading Indicators (weekly)
| Metric | Source | Target Wk1 | Target Wk4 | Target Mo3 |
|--------|--------|------------|------------|------------|
| Free channel members | Telegram `-1003860200579` | 25 | 100 | 500 |
| VIP paid subs | Gumroad dashboard | 1 | 5 | 25–80 |
| Reddit post upvotes (best) | Reddit | 30 | 200 | 800 |
| X thread impressions (best) | X analytics | 1k | 10k | 50k |
| Free→VIP conversion rate | Gumroad / TG | n/a | 5% | 8% |

## Lagging Indicators (monthly)
| Metric | Target Mo1 | Target Mo3 | Target Mo6 |
|--------|------------|------------|------------|
| MRR ($) | $50 | $250 | $800 |
| Total subs | 5 | 25 | 80 |
| Churn rate | n/a | <10% | <8% |
| Cumulative revenue | $50 | $600 | $3,500 |

## Trading Edge (the only quality metric that matters)
| Metric | Source | Target |
|--------|--------|--------|
| Predictions logged | `prediction_tracker.py` | 20+ before scaling |
| Accuracy (1-week horizon) | `performance.json` | ≥70% |
| Avg expectancy per call | `performance.json` | ≥+1.0% |
| Max drawdown (paper) | `performance.json` | ≤-15% |

## How Often To Check
- **Daily (auto):** screener output → free channel (8 AM AST)
- **Daily (auto):** morning briefing → personal Telegram (9 AM AST)
- **Weekly (manual):** Sunday 8 PM AST — score predictions, post performance review
- **Monthly (manual):** 1st of month — update this file, re-rank priorities
