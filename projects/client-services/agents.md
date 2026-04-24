# Client Services — Agents

_Lightweight model: Manager / Worker / Research._

## Manager Agent
**Identity:** Operator (Shami) — this is the human-in-the-loop lane
**Role:** Reviews each inquiry, scopes the project, commits to delivery date, packages handoff
**Inputs:** Fiverr inbox, gig description, client requirements
**Outputs:** Project plan per order, scope decision, delivery package
**Cadence:** On-demand (every inquiry/order)
**Boundaries:** Doesn't auto-respond. Reviews every message before reply. Holds the quality bar.

## Worker Agent
**Identity:** Claude Code (this session, called per-order)
**Role:** Builds the deliverable from templates — Telegram bot / GH Action / portfolio monitor
**Inputs:** Client requirements (tickers, alert conditions, etc.), template folder
**Outputs:** Working code + README + setup video script + handoff checklist
**Cadence:** Per-order — typically 1–4 hour build
**Boundaries:** No client communication. No payment handling. Manager packages and delivers.

## Research Agent
**Identity:** Brave Search MCP + `/research` skill
**Role:** Pre-gig market research (pricing, competitor gigs, keyword optimization)
**Inputs:** Niche query (e.g., "Fiverr Telegram bot automation")
**Outputs:** Competitor pricing, keyword density patterns, gig description improvements
**Cadence:** Once at gig launch + monthly refresh
**Boundaries:** Read-only. Doesn't modify gigs without Manager approval.

## Decision: No more agents
A "delivery-bot" agent (auto-build from client spec) would risk shipping unreviewed code to
paying clients. Decision: Manager + Worker (with operator review) is the safe model.
The friction is the moat against quality drift.
