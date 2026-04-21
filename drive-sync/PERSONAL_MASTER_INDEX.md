# YNAI5 Personal Master Index
> Human navigation guide for the YNAI5 Google Drive ecosystem.
> Updated by: `maintenance.sh` (folder tree section only) — Manual Notes section is NEVER overwritten.

**Last Updated:** 2026-04-18
**Drive Root:** `gdrive:/YNAI5_AI_CORE/`
**Maintained by:** Claude (local) + VM maintenance.sh (auto)

---

## Taxonomy Folders

| Folder | Purpose | What Goes Here |
|--------|---------|----------------|
| `00_YNAI5_CORE` | Strategy & Roadmaps | Master roadmaps, vision docs, quarterly goals, CLAUDE.md snapshots |
| `01_Infrastructure_GCP` | VM + MCP Configs | VM scripts, systemd configs, rclone setup, MCP server files, `05_Work_Profile.md` |
| `01_Infrastructure_GCP/CROSS_MODEL_SYNC` | Cross-agent handoffs | Files shared between Claude ↔ Gemini ↔ Kimi. Context injection docs. |
| `02_Finance_Markets` | Trading & Crypto | Kraken exports, prediction logs, screener outputs, trade journals |
| `03_Music_Symphony` | Music & Audio | Suno generations, lyrics drafts, voice-gen outputs, Symphony project files |
| `04_Personal_Archive` | Pre-2026 Documents | CVs, IDs, old projects, documents from 2025 and earlier |
| `05_Inbox_Unsorted` | Landing Zone | Anything not yet categorized. Review weekly. `pending_tasks.json` lives here. |
| `06_Knowledge_Base` | Research & Docs | Research PDFs, Claude docs, niche research outputs, architecture diagrams |

---

## Legacy Folders (Pre-Taxonomy)

| Folder | Status | Notes |
|--------|--------|-------|
| `CONTEXT` | Active | context/ + memory/ synced every 2h via drive-sync.bat |
| `MEMORY` | Active | Memory files synced via drive-sync.bat |
| `SESSIONS` | Active | Session summaries pushed manually |
| `SKILLS_LIBRARY` | Active | Skill .md files |
| `SYNC` | Active | Bidirectional heartbeat/sync files |
| `SYSTEM` | Active | System-level configs |

---

## Current Sync Status

| Folder | Status | Last Activity |
|--------|--------|---------------|
| `00_YNAI5_CORE` | Empty — awaiting first file | 2026-04-18 |
| `01_Infrastructure_GCP` | Active — 05_Work_Profile.md present | 2026-04-18 |
| `01_Infrastructure_GCP/CROSS_MODEL_SYNC` | Empty — awaiting handoff files | 2026-04-18 |
| `02_Finance_Markets` | Empty — awaiting first file | 2026-04-18 |
| `03_Music_Symphony` | Empty — awaiting first file | 2026-04-18 |
| `04_Personal_Archive` | Empty — awaiting first file | 2026-04-18 |
| `05_Inbox_Unsorted` | Active — pending_tasks.json present | 2026-04-18 |
| `06_Knowledge_Base` | Empty — awaiting first file | 2026-04-18 |

---

## How to Use This System

### Adding a File to Drive
1. Identify which taxonomy folder it belongs in (use table above)
2. Run: `rclone copy <local_file> "gdrive:/YNAI5_AI_CORE/<folder>/"`
3. Update `AGENT_CONTEXT_MAP.md` row for that file
4. Or invoke `/gdrive-org` skill — Claude will handle categorization + upload

### Moving a File Between Folders
- Never drag-and-drop in Drive UI — use rclone to keep `AGENT_CONTEXT_MAP.md` accurate
- Run: `rclone moveto "gdrive:/YNAI5_AI_CORE/<old>" "gdrive:/YNAI5_AI_CORE/<new>"`

### Refreshing This Index
- On VM: `bash /ynai5_runtime/scripts/maintenance.sh`
- Locally: invoke `/gdrive-org` skill → option "refresh index"

---

## Manual Notes
> ✏️ This section is YOURS — add notes freely. maintenance.sh will never touch this section.

- Payday plan: Kling AI $6.99 → Anthropic credits $10 → crypto DCA
- Block Syndicate Telegram screener LIVE at 8AM AST daily
- Social media pipeline ON HOLD until better hardware
- VM IP: 34.45.31.188 | SSH key: ~/.ssh/ynai5_gcp
