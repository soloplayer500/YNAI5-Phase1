---
name: gdrive-org
description: Manage Google Drive files for the YNAI5 ecosystem. Use for uploading files to Drive, creating folders, moving files between taxonomy folders, listing Drive contents, and refreshing the dual index. Trigger when user says "push to drive", "upload to drive", "organize drive files", "refresh the index", or "move file to [taxonomy folder]".
---

# gdrive-org — Google Drive Organization Skill

## Purpose
Give Claude persistent ability to read and write Google Drive for the YNAI5 ecosystem using rclone (write) and the Google Drive MCP (read).

**Drive Root:** `gdrive:/YNAI5_AI_CORE/`
**Read tool:** Google Drive MCP (`google_drive_search` + `google_drive_fetch`)
**Write tool:** rclone CLI via Bash
**VM Maintenance:** `ssh -i ~/.ssh/google_compute_engine shema@34.45.31.188 "bash /ynai5_runtime/scripts/maintenance.sh"`

---

## Taxonomy Reference

| Folder | What Goes Here |
|--------|----------------|
| `00_YNAI5_CORE` | Strategy, roadmaps, vision docs, CLAUDE.md snapshots |
| `01_Infrastructure_GCP` | VM scripts, configs, MCP files, `05_Work_Profile.md` |
| `01_Infrastructure_GCP/CROSS_MODEL_SYNC` | Cross-agent handoff files (Claude ↔ Gemini ↔ Kimi) |
| `02_Finance_Markets` | Kraken exports, predictions, screener outputs, trade journals |
| `03_Music_Symphony` | Suno generations, lyrics, voice-gen MP3s |
| `04_Personal_Archive` | Pre-2026 docs, CVs, IDs, old projects |
| `05_Inbox_Unsorted` | Unorganized landing zone — review weekly |
| `06_Knowledge_Base` | Research PDFs, Claude docs, architecture diagrams |

---

## Operations

### 1. List Drive Contents
```bash
# Top-level folders
rclone lsd "gdrive:/YNAI5_AI_CORE/"

# Files in a specific folder
rclone ls "gdrive:/YNAI5_AI_CORE/<folder>/"

# Everything up to 2 levels deep
rclone lsd "gdrive:/YNAI5_AI_CORE/" --max-depth 2
```

### 2. Upload a File to Drive
Always categorize into the correct taxonomy folder. Never dump in root.
```bash
# Identify correct taxonomy folder (use table above), then:
rclone copy "<local_file_path>" "gdrive:/YNAI5_AI_CORE/<taxonomy_folder>/"

# Example: research doc → Knowledge Base
rclone copy "C:\Users\shema\OneDrive\Desktop\YNAI5-SU\docs\2026-04-18-topic.md" "gdrive:/YNAI5_AI_CORE/06_Knowledge_Base/"
```

### 3. Create a Folder
```bash
rclone mkdir "gdrive:/YNAI5_AI_CORE/<new_folder>"
```

### 4. Move a File Between Folders (Drive-to-Drive)
```bash
rclone moveto "gdrive:/YNAI5_AI_CORE/<source_path>" "gdrive:/YNAI5_AI_CORE/<dest_path>"
```

### 5. Read a Drive File
Use the Google Drive MCP tools (read-only):
1. `google_drive_search` — find file by name or keyword
2. `google_drive_fetch` — read file content by ID

### 6. Refresh the Dual Index
SSH to VM and run maintenance.sh:
```bash
ssh -i ~/.ssh/google_compute_engine -o StrictHostKeyChecking=no shema@34.45.31.188 "bash /ynai5_runtime/scripts/maintenance.sh"
```
Regenerates both `PERSONAL_MASTER_INDEX.md` and `AGENT_CONTEXT_MAP.md` on Drive.

### 7. Update 05_Work_Profile.md (End of Session / Milestone)
Edit the local copy, then push:
```bash
rclone copy "C:\Users\shema\OneDrive\Desktop\YNAI5-SU\drive-sync\05_Work_Profile.md" "gdrive:/YNAI5_AI_CORE/01_Infrastructure_GCP/"
```

### 8. Execute Approved Moves from pending_tasks.json
Only run after user sets `"status": "approved"` on entries:
```bash
# Drive-to-Drive reorganization:
rclone moveto "gdrive:/YNAI5_AI_CORE/<from>" "gdrive:/YNAI5_AI_CORE/<to>"

# Local-to-Drive copy (preserves local file):
rclone copy "<local_path>" "gdrive:/YNAI5_AI_CORE/<dest_folder>/"
```
After executing: offer to refresh index via maintenance.sh.

---

## Rules (Non-Negotiable)

1. **Never bulk-sync** entire local folders to Drive — always explicit file or named folder operations
2. **Always categorize** — every file goes into a taxonomy folder, never dumped in root
3. **Agent handoffs** — files for Gemini go to `01_Infrastructure_GCP/CROSS_MODEL_SYNC/`
4. **No moves without approval** — pending_tasks.json entries require user approval first
5. **Copy vs Move** — local→Drive: `rclone copy`. Drive→Drive reorganization: `rclone moveto`
6. **After any upload** — offer to refresh index (run maintenance.sh or add AGENT_CONTEXT_MAP.md row)

---

## Common Workflows

### "Push this file to Drive"
1. Identify taxonomy folder from content type
2. `rclone copy` to correct folder
3. Offer to refresh indexes via maintenance.sh

### "What's on Drive?"
1. `rclone lsd gdrive:/YNAI5_AI_CORE/` for folder list
2. Or read `AGENT_CONTEXT_MAP.md` via Drive MCP for file-level detail

### "Hand off context to Gemini"
1. Write/update the relevant file locally
2. `rclone copy` → `gdrive:/YNAI5_AI_CORE/01_Infrastructure_GCP/CROSS_MODEL_SYNC/`
3. Update `05_Work_Profile.md` → Agent Handoffs section
4. Push `05_Work_Profile.md` to Drive

### "Start session on new machine"
Read `gdrive:/YNAI5_AI_CORE/01_Infrastructure_GCP/05_Work_Profile.md` via Drive MCP.
Claude summarizes current status and confirms readiness to resume.

### "Organize inbox"
1. Read `05_Inbox_Unsorted/pending_tasks.json` via Drive MCP
2. Present proposed moves to user
3. User approves/rejects each entry
4. Execute approved moves only
5. Run maintenance.sh to refresh indexes
