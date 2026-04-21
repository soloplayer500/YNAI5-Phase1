# YNAI5 Agent Context Map
> RAG-optimized machine-readable index. Used by Claude, Gemini, and other agents to locate files fast.
> Read this FIRST before searching raw directories.
> Auto-refreshed by: VM `maintenance.sh` | Manual updates: `/gdrive-org` skill

**Last Updated:** 2026-04-18
**Format:** FilePath is relative to `gdrive:/YNAI5_AI_CORE/` unless prefixed with `local:` or `vm:`

---

## Index Table

| FilePath | ContentSummary | LastModified | AgentResponsible | SyncStatus |
|----------|----------------|--------------|------------------|------------|
| `PERSONAL_MASTER_INDEX.md` | Human navigation guide — taxonomy descriptions, folder status, manual notes | 2026-04-18 | Claude | Active |
| `AGENT_CONTEXT_MAP.md` | This file — RAG index of all Drive + key local + VM files | 2026-04-18 | Claude + VM maintenance.sh | Active |
| `01_Infrastructure_GCP/05_Work_Profile.md` | Cross-device context injection — active project, next steps, system state, agent handoffs | 2026-04-18 | Claude (update at session end) | Active |
| `05_Inbox_Unsorted/pending_tasks.json` | Proposed file moves for taxonomy organization — review and approve before executing | 2026-04-18 | Claude | Pending |
| `CONTEXT/profile.md` | Who Shami is — background, hardware constraints, collaboration style | 2026-04-05 | drive-sync.bat (auto) | Active |
| `CONTEXT/current-priorities.md` | Top priorities this month — crypto/stocks focus, passive income Telegram channel | 2026-04-10 | drive-sync.bat (auto) | Active |
| `CONTEXT/goals.md` | Annual Q1–Q4 milestones — revenue first, content automation, $10K goal | 2026-03-09 | drive-sync.bat (auto) | Active |
| `MEMORY/MEMORY.md` | Auto-memory index — key learnings, session index, decisions, skills list | 2026-03-22 | drive-sync.bat (auto) | Active |
| `MEMORY/preferences.md` | Saved preferences — tone, workflow, output format, decision-making style | 2026-03-09 | drive-sync.bat (auto) | Active |
| `SYNC/HEARTBEAT.json` | VM health heartbeat — last ping timestamp, service status | auto | ynai5-drive.service (VM) | Active |
| `SYNC/CORE_IDENTITY.md` | Universal AI guide — how to collaborate with Shami across all AI tools | 2026-04-05 | manual | Active |
| `local:CLAUDE.md` | Master workspace file — role, workspace map, skills, workflow rules | 2026-04-10 | Claude (manual update) | Active |
| `local:docs/INDEX.md` | Documentation index — all research docs, knowledge graphs, reference files | 2026-04-13 | Claude | Active |
| `local:docs/knowledge/combined-architecture.md` | Full infrastructure map — local ↔ GCP VM ↔ GitHub Actions ↔ External APIs | 2026-04-13 | Claude | Active |
| `local:docs/knowledge/vm-structure.md` | VM directory layout — services, ports, file paths, quick reference table | 2026-04-13 | Claude | Active |
| `local:projects/README.md` | Project index — 11 active projects with status and folder paths | 2026-04-10 | Claude | Active |
| `local:projects/passive-income/README.md` | Block Syndicate Telegram screener — week 1 checklist, revenue target, distribution plan | 2026-03-22 | Claude | Active |
| `local:projects/crypto-monitoring/kraken/predictions.json` | Trade predictions log — entry/target/stop/confidence for accuracy tracking | ongoing | Claude (/crypto-portfolio) | Active |
| `vm:~/main.py` | FastAPI dashboard — 10 endpoints, health/status/tasks/logs, port 8000 | ongoing | VM auto-restart | Active |
| `vm:~/chat_server.py` | Flask Gemini proxy — Lyra prompt routing, port 8001 | ongoing | VM auto-restart | Active |
| `vm:~/scripts/gdrive-backup.sh` | VM → Drive backup script | ongoing | VM cron | Active |
| `vm:/ynai5_runtime/scripts/maintenance.sh` | Scans Drive + VM, refreshes both index files | 2026-04-18 | VM cron (daily 9AM) | Active |

---

## Agent Lookup Guide

### Claude (local)
- Start here: `local:CLAUDE.md` → `local:context/current-priorities.md`
- Finance tasks: `local:projects/crypto-monitoring/` → Kraken MCP
- Content tasks: `local:projects/social-media-automation/` (ON HOLD)
- New session on different device: read `01_Infrastructure_GCP/05_Work_Profile.md` first

### Gemini (via VM chat_server.py)
- Route through: `vm:~/chat_server.py` → Lyra prompt layer (`get_lyra_prompt()`)
- Handoff files: `01_Infrastructure_GCP/CROSS_MODEL_SYNC/`
- Context file: `01_Infrastructure_GCP/05_Work_Profile.md`

### VM Agents (autonomous)
- Health: `vm:~/orchestrator.py` + `read_heartbeat()` function
- Billing: `vm:~/FINANCE/billing_sentinel.py`
- Maintenance: `vm:/ynai5_runtime/scripts/maintenance.sh`

---

## SyncStatus Key
| Value | Meaning |
|-------|---------|
| `Active` | In use, regularly updated |
| `Archive` | Finalized, kept for reference |
| `Pending` | Needs review or action before use |
| `Stale` | Not updated in >30 days — may be outdated |
