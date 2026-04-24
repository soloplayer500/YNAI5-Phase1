# Crypto Alpha — Tasks

_Single ranked queue. Top item = do first. Move to logs.md when done._

## 🟢 This Week (revenue-critical)
- [ ] Commit + push 3 unpaused workflows → verify scheduled triggers in Actions tab
- [ ] **USER:** Create Gumroad product "Block Syndicate VIP — $9.99/mo recurring"
- [ ] **USER:** Paste VIP Telegram invite into Gumroad delivery field
- [ ] Replace `[Gumroad link]` + `[Telegram FREE link]` placeholders in `passive-income/distribution/*.md`
- [ ] **USER:** Pin Telegram welcome (free + VIP) from `passive-income/distribution/telegram-welcome.md`
- [ ] **USER:** Post Reddit Post 1 to r/CryptoCurrency (timing: 8 AM ET weekday)
- [ ] **USER:** Post X Thread 1 (timing: 8 AM ET weekday)
- [ ] Verify tomorrow 8 AM AST: screener-bot fires + posts to free channel
- [ ] Verify tomorrow 9 AM AST: morning-briefing posts to personal Telegram

## 🟡 Next Week
- [ ] Run `prediction_tracker.py --score` weekly (Sunday 8 PM AST) → log to `crypto-monitoring/kraken/performance.json`
- [ ] Post Reddit Post 2 to r/SatoshiStreetBets (Day 2)
- [ ] Post Reddit Post 3 to r/CryptoMarkets (Day 4)
- [ ] First weekly performance review post to VIP channel (Sunday)
- [ ] Sweep Kraken dust (<$5 positions) → consolidate into BTC

## 🔵 Later (after first 10 paid VIP subs)
- [ ] Re-enable `market-report.yml` (was paused 2026-03-29)
- [ ] Beehiiv newsletter setup (after 100 free-channel subs)
- [ ] Wire intraday alerts → VIP channel (only if filter triggers — max 3/day)
- [ ] Build signals API (FastAPI on VM port 8002) — gate behind 70% accuracy proven

## ⏸ Paused / Blocked
- Trading-signal API monetization → blocked by 20-prediction accuracy requirement
- VM upgrade e2-micro → e2-small ($13/mo) → blocked by first $100 revenue milestone

## Done (recent)
- [x] 2026-04-24 Unpause screener-bot.yml + morning-briefing.yml + portfolio-sync.yml
- [x] 2026-04-24 Author distribution kit (Reddit/X/Discord/Telegram/Fiverr)
- [x] 2026-04-24 Verify env keys + bot token + channel IDs
