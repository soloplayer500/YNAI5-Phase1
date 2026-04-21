---
name: trading
description: >
  TRADING — Activate this skill for all crypto and stock trading operations, signal generation, portfolio management, and Block Syndicate signal pipeline tasks. Triggers on: "run a signal", "check my Kraken portfolio", "what's the setup on [coin/stock]", "Block Syndicate signal for", "generate a trade alert", "portfolio risk check", "entry for [asset]", "what's the technical setup", "trading signals today", "run the scanner", or any operational trading task. Different from APEX (which analyzes) — TRADING executes: pulls live data via Kraken CLI MCP + Hive Crypto MCP, runs the signal logic, formats Block Syndicate output, and routes via DISTRIBUTION to Telegram. The full operational signal pipeline.
---

# TRADING — Block Syndicate Signal Pipeline

TRADING is the execution layer. APEX thinks. TRADING acts.

Full signal logic + Kraken commands → `references/signals.md`

---

## Full Pipeline — How It Runs

```
Solo: "run a signal for ETH"
         ↓
TRADING Step 1: Pull live data
  → hive-crypto: get_market_data("ethereum")
  → hive-crypto: get_price_history("ethereum", 30)
  → hive-crypto: get_fear_greed()
  → trading-signals: full_technical_analysis("ethereum")
  → opennews: get_crypto_news("ETH")
         ↓
TRADING Step 2: Run signal logic
  → Score against 6 criteria
  → Calculate entry/stop/targets/R:R
  → Check R:R ≥ 2:1 (if not → abort, return "setup not favorable")
         ↓
TRADING Step 3: Format signal
  → Build public signal (condensed)
  → Build VIP signal (full)
         ↓
TRADING Step 4: Route via DISTRIBUTION
  → telegram: send_block_syndicate_signal(public_channel, ...)
  → telegram: send_block_syndicate_signal(vip_channel, ..., vip=True)
  → telegram: pin_message(vip_channel, message_id)
         ↓
TRADING Step 5: Confirm
  → Return: "Signal published to Block Syndicate at [time]"
```

---

## MCP Calls by Mode

### Signal Generation Mode
```python
# Step 1 — Live data
price_data = hive_crypto.get_market_data(coin_id)
history    = hive_crypto.get_price_history(coin_id, days=30)
fear_greed = hive_crypto.get_fear_greed()
ta_data    = trading_signals.full_technical_analysis(coin_id)
news       = opennews.get_crypto_news(ticker)

# Step 2 — Score
score = _run_signal_logic(price_data, history, ta_data, fear_greed)

# Step 3 — Format
if score.rr >= 2.0:
    telegram.send_block_syndicate_signal(PUBLIC_CHANNEL, **signal_params, vip=False)
    telegram.send_block_syndicate_signal(VIP_CHANNEL, **signal_params, vip=True)
    telegram.pin_message(VIP_CHANNEL, last_message_id)
else:
    return "R:R below 2:1 — signal not published"
```

### Portfolio Check Mode
```python
portfolio  = kraken.get_portfolio_summary()
balances   = kraken.get_balance()
open_orders = kraken.get_open_orders()
# Then run APEX Lens #3 (Bridgewater) on the portfolio data
```

### Scanner Mode
```python
scan = hive_crypto.run_signal_scan(coins)
momentum = trading_signals.momentum_scan(coins)
volume = trading_signals.volume_anomaly_detector(coins)
# Combine → triage list → Solo picks → full signal
```

---

## Signal Scoring (6 Criteria)

**LONG fires when 3+ align:**
| Criteria | MCP Source | Signal |
|---|---|---|
| RSI < 35 (oversold) | trading-signals: full_technical_analysis | rsi < 35 |
| MACD bullish crossover | trading-signals: full_technical_analysis | macd > signal |
| Price above 200 EMA | trading-signals: full_technical_analysis | current > ema_200 |
| Volume spike | trading-signals: volume_anomaly_detector | ratio > 1.5x |
| Fear & Greed < 30 | hive-crypto: get_fear_greed | fg < 30 (max fear = buy zone) |
| Positive news catalyst | opennews: get_crypto_news | bullish news detected |

**SHORT fires when 3+ align:** RSI > 70, MACD bearish, below 200 EMA, rising volume on red, F&G > 75, negative news.

**Hard rule: R:R must be ≥ 2:1. If not — do not publish.**

---

## Signal Formats

### Public Channel
```
🚨 BLOCK SYNDICATE

📊 $[TICKER] | [LONG/SHORT/WATCH]
💵 Entry: $[X] – $[X]
🎯 Target: $[X] (+[X]%)
🛑 Stop: $[X]
⚡ [1-line thesis]

⚠️ NFA
#BlockSyndicate #[TICKER]
```

### VIP Channel
```
🔐 BLOCK SYNDICATE VIP

📊 $[TICKER] — [direction] | [timeframe]
📍 Entry: $[X] – $[X]
🎯 T1: $[X] (+[X]%) | T2: $[X] (+[X]%)
🛑 Stop: $[X] | R:R [X]:1
📐 Confidence: [HIGH/MEDIUM] | Score: [X]/6

📝 THESIS:
• [Technical reason]
• [News catalyst]
• [Market context]

⚠️ NFA — Size responsibly
#BlockSyndicate #YNAI5 #[TICKER]
```

---

## Telegram Channel Map

When routing signals, use these:
- **Public Block Syndicate** → `@BlockSyndicate` or channel ID
- **VIP Block Syndicate** → private channel ID (stored in .env)
- **Openclaw** → command hub channel

Always confirm channel IDs with: `telegram.get_chats(limit=30)`

---

## Output Rules

1. **Never publish R:R < 2:1** — quality over quantity
2. **Always NFA disclaimer** on public signals
3. **VIP always gets more** than public — never reverse
4. **Confirm before publishing** — show preview, Solo confirms, then send
5. **Scanner → triage list only** — full signal is a separate step
6. **Route through DISTRIBUTION** for anything beyond Telegram (cross-post to X, etc.)
7. **After publishing** → confirm back: "Signal sent to [channels] at [time]"

---

## Pipeline Connections

- **← APEX**: When APEX verdict is LONG/SHORT → hand to TRADING to format + distribute
- **← RESEARCH**: News context feeds into signal thesis
- **→ DISTRIBUTION**: After Telegram signal, DISTRIBUTION handles cross-posting to X/IG
- **→ TELEGRAM MCP**: Direct calls for send_block_syndicate_signal + pin_message
