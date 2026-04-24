# YNAI5 Project Operating Model
_How this system works. Who does what. How decisions get made._

Last Updated: 2026-04-24

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  RYN (HP Laptop — Local)                                    │
│  Claude Code + skills + ryn/framework/ + ryn/runtime/       │
│  Execution relay — NOT a 24/7 server                        │
└────────────────┬────────────────────────────────────────────┘
                 │ SSH / git push / Telegram
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  YNAI5-VM (GCP e2-micro 34.45.31.188)                       │
│  ynai5-dashboard | ynai5-gemini | ynai5-claude              │
│  ynai5-heartbeat | ynai5-commander | nginx                  │
│  Runs 24/7 — always-on runtime                              │
└────────────────┬────────────────────────────────────────────┘
                 │ GitHub Actions (push triggers)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  GitHub (soloplayer500/YNAI5-SU)                            │
│  Source of truth — vm-sync.yml | market-report.yml          │
│  portfolio-monitor.yml | system-health.yml                  │
└──────────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  Telegram (@SoloClaude5_bot)                                │
│  /status /logs /restart /snapshot                           │
│  Heartbeat alerts | Market briefings                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Decision Flow — Who Does What

| Task | How |
|------|-----|
| Check VM status | Telegram `/status` OR `/telegram-ops` |
| Fix broken service | `/vm-repair` (SSH diagnostic loop) |
| Analyze logs | `/log-audit` |
| Morning market check | `/market-scan` |
| Trade setup | `/trading-analysis [TICKER]` |
| Deploy code to VM | `git push origin master` → vm-sync.yml |
| Save brain state | `/github-snapshot` |
| Run scratchpad commands on VM | SSH directly |
| Restart a service | Telegram `/restart [svc]` (safe list only) |

---

## Control Channels (Priority Order)

1. **Telegram** — for real-time VM ops, quick checks, alerts
2. **Claude Code (RYN)** — for all analysis, planning, code writing
3. **SSH** — for deep VM work, file edits, log inspection
4. **GitHub Actions** — for scheduled automation, deploys

**Rule:** Use the highest-level channel that can handle the task. SSH is last resort.

---

## Session Protocol

### Session Start
```
1. Claude reads CLAUDE.md (auto)
2. Check ryn/brain/priority_stack.md → what's #1?
3. Check ryn/brain/system_summary.md → VM state OK?
4. Check memory/MEMORY.md last section → anything urgent?
5. Run /market-scan if trading session
```

### Session End
```
1. Update ryn/brain/last_report.md → append what happened
2. Update ryn/brain/priority_stack.md if priorities changed
3. /github-snapshot → commit + push
```

---

## Upgrade Cadence

| Type | Frequency | What |
|------|-----------|------|
| Framework Pass | Monthly | Review ryn/framework/ + ryn/profit/ for freshness |
| RAG Rebuild | After new files added | `python ryn/ryn-core/rag_indexer.py --index` |
| Priority Re-rank | Weekly | Update ryn/brain/priority_stack.md |
| VM Health | Daily (auto) | ynai5-heartbeat + GitHub Actions system-health.yml |
| Brain Snapshot | Per session | /github-snapshot at session close |

---

## Failure Response Matrix

| Symptom | First Response | Second Response |
|---------|---------------|-----------------|
| Service down (dashboard/nginx) | Telegram `/restart [svc]` | `/vm-repair` via SSH |
| RAM critical alert | `/vm-repair` → restart ynai5-gemini | Monitor |
| High load alert | SSH → `ps aux --sort=-%cpu` | Identify + kill runaway |
| Log >20MB | `/log-audit` → logrotate | Manual gzip backup |
| SSH unreachable | Wait 2 min, retry | GCP Console → check instance |
| Bot not responding | Check ynai5-commander active | SSH restart |
| GitHub Actions failing | Check workflow logs → fix → push | |

---

## What NEVER Runs Locally (RYN)

- 24/7 monitoring loops
- Telegram bot polling loops
- Database servers
- Video generation (cloud-only)
- Any daemon processes

---

## Key File Locations

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Master config — loaded every session |
| `ryn/framework/think.md` | Pre-task thinking protocol |
| `ryn/framework/build.md` | Execution + closure protocol |
| `ryn/framework/context.md` | Context window discipline |
| `ryn/framework/skills.md` | Skill registry |
| `ryn/framework/memory.md` | Memory architecture |
| `ryn/runtime/scheduler.py` | Task scheduler |
| `ryn/runtime/task_router.py` | Task → layer router |
| `ryn/runtime/heartbeat_actions.py` | Auto-response to VM alerts |
| `ryn/runtime/telegram_tasks.py` | Telegram bot wrapper |
| `ryn/profit/income_map.md` | Revenue streams |
| `ryn/profit/trading_system.md` | Trading framework |
| `ryn/profit/monetization_ideas.md` | Revenue backlog |
| `ryn/brain/priority_stack.md` | Current objective ranking |
| `ryn/brain/last_report.md` | Event log (committed) |
| `ryn/brain/system_summary.md` | VM snapshot (committed) |
| `.env.local` | All API keys (NEVER committed) |

---

## The One Rule

> **Every session ends with a commit.**  
> If nothing was committed, nothing was done.
