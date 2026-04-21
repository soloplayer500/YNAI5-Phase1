# 05 Work Profile — YNAI5 Context Injection File
> **Purpose:** Cross-device continuity. When starting Claude Code on a new machine, read this file first.
> Upon reading, Claude must: (1) adopt this persona/context, (2) summarize status back to confirm alignment, (3) acknowledge readiness to resume without full file access.

**Last Updated:** 2026-04-18 (Session — Dual-Index System COMPLETE)
**Updated by:** Claude (update at every major milestone or session end)

---

## Active Project
**Crypto & Stock Trading — Capital Growth** ← CURRENT FOCUS

YNAI5 Executive Systems infrastructure is **fully complete** as of 2026-04-18. All taxonomy folders, index files, pinned context files, hardware manifest, maintenance script, and gdrive-org skill are live and verified. Infrastructure phase is closed — returning to top priority.

---

## Next Steps (Top 3)
1. **Crypto screening** — Run `/crypto-screen medium crypto 500` for high-probability setups. Log any trade ideas via `/crypto-portfolio --predict`.
2. **Portfolio review** — ETH -30%, SOL -40%, BTC -21% underwater. Use `/technical-analysis` + `/risk-analyze` to decide: DCA, hold, or cut.
3. **Block Syndicate Telegram screener** — Week 1 tasks in `actions/passive-income-week1.md`. Build `screener-channel-bot.py` + Gumroad page.

---

## System State
YNAI5 Executive Systems infrastructure **COMPLETE**. Three-layer ecosystem (local SOLOL + GCP VM 34.45.31.188 + Google Drive) fully organized: 9 taxonomy folders (00–99), dual index files auto-refreshed daily by maintenance.sh at 9AM AST, all folders pinned with `00_CONTEXT_README.md`, hardware manifest live in `07_Hardware_Health/inventory/`, `gdrive-org` skill active in Claude Code.

---

## Agent Handoffs

**For Gemini:**
- Read `gdrive:/YNAI5_AI_CORE/01_Infrastructure_GCP/CROSS_MODEL_SYNC/CORE_IDENTITY.md` for persona context
- Read `AGENT_CONTEXT_MAP.md` at Drive root for file locations
- VM proxy available at `http://34.45.31.188:8001` (Flask chat server with Lyra routing)
- Pending handoff files: `01_Infrastructure_GCP/CROSS_MODEL_SYNC/` (folders created, files to be moved — see pending_tasks.json PM-001, PM-002)

**For Claude on new machine:**
- SSH key: `~/.ssh/google_compute_engine` ← use this, NOT `ynai5_gcp` (permission denied)
- Rclone remote: `gdrive:` (must be configured — run `rclone config` if not present)
- Local workspace: clone `https://github.com/soloplayer500/YNAI5-SU` to Desktop
- Then read `CLAUDE.md` → `context/current-priorities.md` → this file

---

## Infrastructure Quick Reference
| Component | Location | Access |
|-----------|----------|--------|
| VM Dashboard | `http://34.45.31.188:8000` | FastAPI — 10 endpoints |
| VM Chat (Gemini) | `http://34.45.31.188:8001` | Flask — Lyra routing |
| VM SSH | `ssh -i ~/.ssh/google_compute_engine shema@34.45.31.188` | Linux VM |
| Drive Root | `gdrive:/YNAI5_AI_CORE/` | rclone or Drive MCP |
| Maintenance Script | `vm:/ynai5_runtime/scripts/maintenance.sh` | Run via SSH |
| Kraken MCP | Local MCP tool | `/kraken` skill |
| GitHub Repo | `https://github.com/soloplayer500/YNAI5-SU` | git push/pull |

---

## Current Priorities (as of 2026-04-18)
1. **Crypto & Stock Trading** — capital growth. Positions mostly underwater. Need strategy.
2. **Passive Income** — Block Syndicate Telegram screener. Week 1: screener-channel-bot.py + Gumroad.
3. **Prediction Feedback Loop** — log every trade idea, score weekly, target 70%+ accuracy.
4. **Social Media Pipeline** — ON HOLD (hardware blocker — no local video gen, 8GB RAM).
