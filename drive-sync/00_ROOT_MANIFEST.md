# 00_ROOT_MANIFEST
> Master manifest of the YNAI5 Google Drive ecosystem. Single source of truth for structure, purpose, and status.
> Updated by: `maintenance.sh` (auto) + Claude at session milestones

**Last Updated:** 2026-04-18
**Drive Root:** `gdrive:/YNAI5_AI_CORE/`
**System Status:** 🟢 LIVE

---

## Folder Structure (Complete)

```
gdrive:/YNAI5_AI_CORE/
│
├── 00_ROOT_MANIFEST.md          ← THIS FILE — master structure reference
├── PERSONAL_MASTER_INDEX.md     ← Human navigation guide (auto-refreshed)
├── AGENT_CONTEXT_MAP.md         ← RAG machine index (auto-refreshed)
│
├── 00_YNAI5_CORE/               ← Strategy, roadmaps, vision
│   ├── PROTOCOL_HANDOFF.md      ← Claude ↔ Gemini task handoff log
│   └── playbooks/
│       └── tiktok-video-assembly.md
│
├── 01_Infrastructure_GCP/       ← VM configs, MCP, scripts
│   ├── 05_Work_Profile.md       ← Cross-device context injection
│   ├── combined-architecture.md ← Full infra map (local+VM+APIs)
│   ├── vm-structure.md          ← VM layout + service reference
│   └── CROSS_MODEL_SYNC/        ← Cross-agent handoff zone
│       ├── CORE_IDENTITY.md     ← Universal AI identity guide
│       └── UNIVERSAL_AI_GUIDE.md← Collaboration rules for all agents
│
├── 02_Finance_Markets/          ← Trading, crypto, finance
│   └── [predictions.json — pending first log entry]
│
├── 03_Music_Symphony/           ← Suno, lyrics, audio (empty — ready)
│
├── 04_Personal_Archive/         ← Pre-2026 docs, CVs, IDs (empty — ready)
│
├── 05_Inbox_Unsorted/           ← Landing zone
│   └── pending_tasks.json       ← File move proposals (executed 2026-04-18)
│
├── 06_Knowledge_Base/           ← Research docs, PDFs
│   ├── 2026-03-10-crypto-market-dynamics.txt
│   └── 2026-03-22-higgsfield-vs-kling.md
│
├── 99_EMERGENCY_RECOVERY/       ← Cold storage for critical backups
│   └── [empty — ready for recovery keys and system snapshots]
│
├── CONTEXT/                     ← Legacy: context/ synced every 2h
├── MEMORY/                      ← Legacy: memory/ synced every 2h
├── SESSIONS/                    ← Legacy: session summaries
├── SKILLS_LIBRARY/              ← Legacy: skill .md files
├── SYNC/                        ← Legacy: VM full backup + heartbeat
└── SYSTEM/                      ← Legacy: system-level configs
```

---

## System Components

| Component | Location | Status | Updated |
|-----------|----------|--------|---------|
| Human Index | `PERSONAL_MASTER_INDEX.md` | 🟢 Live | Auto daily 9AM |
| Machine Index | `AGENT_CONTEXT_MAP.md` | 🟢 Live | Auto daily 9AM |
| Work Profile | `01_Infrastructure_GCP/05_Work_Profile.md` | 🟢 Live | Manual at milestones |
| Handoff Log | `00_YNAI5_CORE/PROTOCOL_HANDOFF.md` | 🟢 Live | Manual per handoff |
| Cross-Model Sync | `01_Infrastructure_GCP/CROSS_MODEL_SYNC/` | 🟢 Live | Manual per handoff |
| Emergency Recovery | `99_EMERGENCY_RECOVERY/` | 🟡 Empty | On-demand |
| VM Maintenance | `/ynai5_runtime/scripts/maintenance.sh` | 🟢 Cron 9AM AST | Auto |

---

## Maintenance Rules

1. **This file** (`00_ROOT_MANIFEST.md`) is updated manually when folders are added/removed
2. **PERSONAL_MASTER_INDEX.md** is auto-refreshed by `maintenance.sh` — never edit manually (except Manual Notes section)
3. **AGENT_CONTEXT_MAP.md** is auto-refreshed by `maintenance.sh` — static section can be manually appended
4. **05_Work_Profile.md** is updated by Claude at end of each major session or milestone
5. **PROTOCOL_HANDOFF.md** is append-only — never overwrite existing entries
6. **99_EMERGENCY_RECOVERY** — only Claude or Gemini write here when storing recovery-critical data

---

## Infrastructure Map

```
┌─────────────────────────────────────────────────────────┐
│                    LOCAL MACHINE                         │
│  YNAI5-SU workspace (C:\Users\shema\OneDrive\Desktop\)  │
│  Claude Code + 30 skills + 11 projects                  │
│  drive-sync.bat → syncs CONTEXT/MEMORY every 2h        │
└────────────────┬────────────────────────────────────────┘
                 │ rclone
                 ▼
┌─────────────────────────────────────────────────────────┐
│                  GOOGLE DRIVE                            │
│  gdrive:/YNAI5_AI_CORE/ ← THIS MANIFEST               │
│  Taxonomy: 00–99 folders + legacy CONTEXT/SYNC         │
└────────────────┬────────────────────────────────────────┘
                 │ rclone mount /mnt/gdrive
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    GCP VM                                │
│  YNAI5_AI_CORE @ 34.45.31.188                          │
│  FastAPI :8000 | Flask/Gemini :8001 | nginx :80        │
│  maintenance.sh → refreshes index files daily 9AM AST  │
│  gdrive-backup.sh → full VM backup daily 3AM           │
└─────────────────────────────────────────────────────────┘
```

---

## SSH / Access Quick Reference
| Target | Command |
|--------|---------|
| VM SSH | `ssh -i ~/.ssh/google_compute_engine shema@34.45.31.188` |
| Run maintenance | `ssh ... "bash /ynai5_runtime/scripts/maintenance.sh"` |
| List Drive | `rclone lsd "gdrive:/YNAI5_AI_CORE/"` |
| Upload file | `rclone copy <local> "gdrive:/YNAI5_AI_CORE/<folder>/"` |
| Invoke Drive skill | `/gdrive-org` |
