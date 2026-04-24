# Crypto Alpha — Agents

_Lightweight model: Manager / Worker / Research. No more unless justified._

## Manager Agent
**Identity:** Claude Code (this session, primary driver)
**Role:** Owns priorities, ranks tasks, commits/pushes, decides what to publish
**Inputs:** `tasks.md`, `metrics.md`, `ryn/brain/priority_stack.md`
**Outputs:** Updates to tasks.md/logs.md, git commits, Telegram approvals
**Cadence:** Every working session
**Boundaries:** Never trades real capital, never sends marketing without operator approval

## Worker Agent
**Identity:** GitHub Actions runners (screener-bot.yml, morning-briefing.yml, portfolio-sync.yml)
**Role:** Executes scheduled scripts, posts to channels, commits state files
**Inputs:** `.env.local` (built from secrets), CoinGecko / Kraken / Gemini APIs
**Outputs:** Telegram posts, `kraken_portfolio.json`, `predictions.json`, `performance.json`
**Cadence:** Daily (cron), on push (vm-sync)
**Boundaries:** Read-only on Kraken (no `place_order` permissions). No DM-style messages.

## Research Agent
**Identity:** Gemini 2.0 Flash (free tier, 1500 calls/day) + Claude Haiku (~$10/mo) for fallback
**Role:** Generates 1-line market take, drafts post copy variations, scores ambiguous setups
**Inputs:** Daily screener output, news headlines, regime context
**Outputs:** Short text strings injected into screener post template + VIP weekly review
**Cadence:** On demand (called by Worker scripts)
**Boundaries:** Output gets sanity-checked by Manager before public publish. Never trusted blindly.

## Decision: No more agents
Adding an "alerter" agent would duplicate the heartbeat layer. Adding a "writer" agent
would duplicate Research. The 3-agent model covers 100% of the lane.
