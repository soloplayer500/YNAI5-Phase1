#!/bin/bash
# ============================================================
# YNAI5 Dual-Index Maintenance Script
# Refreshes PERSONAL_MASTER_INDEX.md and AGENT_CONTEXT_MAP.md
# on Google Drive from the VM's rclone mount.
#
# Usage:  bash /ynai5_runtime/scripts/maintenance.sh
# Cron:   0 9 * * * /bin/bash /ynai5_runtime/scripts/maintenance.sh >> /ynai5_runtime/logs/maintenance.log 2>&1
# Hook:   Call at end of any file-transfer operation to keep indexes current
# ============================================================

set -e
DRIVE_ROOT="/mnt/gdrive"
YNAI5_ROOT="$DRIVE_ROOT"
LOG_FILE="/ynai5_runtime/logs/maintenance.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() { echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"; }

log "=== maintenance.sh START ==="

# ── Guard: Drive must be mounted ────────────────────────────
if ! mountpoint -q "$DRIVE_ROOT" 2>/dev/null; then
  if [ ! -d "$DRIVE_ROOT/YNAI5_AI_CORE" ] && [ ! -f "$DRIVE_ROOT/PERSONAL_MASTER_INDEX.md" ]; then
    log "ERROR: Drive not mounted at $DRIVE_ROOT and no files found. Aborting."
    exit 1
  fi
fi

log "Drive accessible at $DRIVE_ROOT"

# ── Count files per taxonomy folder ─────────────────────────
count_files() {
  local dir="$YNAI5_ROOT/$1"
  if [ -d "$dir" ]; then
    find "$dir" -type f 2>/dev/null | wc -l | tr -d ' '
  else
    echo "0"
  fi
}

C00=$(count_files "00_YNAI5_CORE")
C01=$(count_files "01_Infrastructure_GCP")
C02=$(count_files "02_Finance_Markets")
C03=$(count_files "03_Music_Symphony")
C04=$(count_files "04_Personal_Archive")
C05=$(count_files "05_Inbox_Unsorted")
C06=$(count_files "06_Knowledge_Base")

# ── Build folder tree ────────────────────────────────────────
log "Scanning Drive folder tree..."
FOLDER_TREE=$(find "$YNAI5_ROOT" -maxdepth 2 -type d 2>/dev/null | sort | sed "s|$YNAI5_ROOT/||g" | grep -v '^$' | head -60)

# ── Preserve Manual Notes from existing index ────────────────
MANUAL_NOTES=""
EXISTING="$YNAI5_ROOT/PERSONAL_MASTER_INDEX.md"
if [ -f "$EXISTING" ]; then
  MANUAL_NOTES=$(awk '/^## Manual Notes/{found=1} found{print}' "$EXISTING")
  log "Preserved Manual Notes section from existing index"
fi

# If no manual notes found, set a default
if [ -z "$MANUAL_NOTES" ]; then
  MANUAL_NOTES="## Manual Notes
> ✏️ This section is YOURS — add notes freely. maintenance.sh will never overwrite content here.
"
fi

# ── Regenerate PERSONAL_MASTER_INDEX.md ─────────────────────
log "Regenerating PERSONAL_MASTER_INDEX.md..."
{
cat << HEADER_EOF
# YNAI5 Personal Master Index
> Human navigation guide for the YNAI5 Google Drive ecosystem.
> **Manual Notes section is NEVER overwritten by this script.**

**Last Updated:** $(date '+%Y-%m-%d %H:%M AST') by maintenance.sh (VM)
**Drive Root:** \`gdrive:/YNAI5_AI_CORE/\`

---

## Taxonomy Folders

| Folder | Purpose | Files | What Goes Here |
|--------|---------|-------|----------------|
| \`00_YNAI5_CORE\` | Strategy & Roadmaps | $C00 | Master roadmaps, vision docs, quarterly goals |
| \`01_Infrastructure_GCP\` | VM + MCP Configs | $C01 | VM scripts, systemd configs, rclone setup, MCP files |
| \`01_Infrastructure_GCP/CROSS_MODEL_SYNC\` | Cross-agent handoffs | — | Files shared between Claude ↔ Gemini ↔ Kimi |
| \`02_Finance_Markets\` | Trading & Crypto | $C02 | Kraken exports, prediction logs, screener outputs |
| \`03_Music_Symphony\` | Music & Audio | $C03 | Suno generations, lyrics, voice-gen MP3s |
| \`04_Personal_Archive\` | Pre-2026 Documents | $C04 | CVs, IDs, old projects from 2025 and earlier |
| \`05_Inbox_Unsorted\` | Landing Zone | $C05 | Anything not yet categorized — review weekly |
| \`06_Knowledge_Base\` | Research & Docs | $C06 | Research PDFs, Claude docs, architecture diagrams |

---

## Drive Folder Tree (auto-generated $(date '+%Y-%m-%d'))
\`\`\`
YNAI5_AI_CORE/
HEADER_EOF
echo "$FOLDER_TREE" | sed 's/^/  /'
cat << FOOTER_EOF
\`\`\`

---

## Legacy Folders (Pre-Taxonomy)

| Folder | Status | Notes |
|--------|--------|-------|
| \`CONTEXT\` | Active | context/ + memory/ synced every 2h via drive-sync.bat |
| \`MEMORY\` | Active | Memory files synced via drive-sync.bat |
| \`SESSIONS\` | Active | Session summaries pushed manually |
| \`SKILLS_LIBRARY\` | Active | Skill .md files |
| \`SYNC\` | Active | Bidirectional heartbeat/sync files |
| \`SYSTEM\` | Active | System-level configs |

---

## How to Use This System

**Upload a file:** \`rclone copy <local> "gdrive:/YNAI5_AI_CORE/<taxonomy_folder>/"\`
**Refresh this index:** \`bash /ynai5_runtime/scripts/maintenance.sh\` (on VM) or invoke \`/gdrive-org\` skill
**Move files:** Review \`05_Inbox_Unsorted/pending_tasks.json\`, approve, then run \`/gdrive-org execute\`

---

$MANUAL_NOTES
FOOTER_EOF
} > /tmp/PERSONAL_MASTER_INDEX.md

cp /tmp/PERSONAL_MASTER_INDEX.md "$YNAI5_ROOT/PERSONAL_MASTER_INDEX.md"
log "PERSONAL_MASTER_INDEX.md updated ✓"

# ── Regenerate AGENT_CONTEXT_MAP.md ─────────────────────────
log "Regenerating AGENT_CONTEXT_MAP.md..."

# Build dynamic rows for Drive files (md, json, sh — up to 3 levels)
DYNAMIC_ROWS=""
while IFS= read -r filepath; do
  rel_path="${filepath#$YNAI5_ROOT/}"
  mod_date=$(stat -c '%y' "$filepath" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
  size=$(stat -c '%s' "$filepath" 2>/dev/null || echo "?")
  ext="${filepath##*.}"
  # Infer summary from extension and path
  summary="File (${size}B, .${ext})"
  if [[ "$rel_path" == *"Work_Profile"* ]]; then
    summary="Cross-device context injection — active project, next steps, system state"
  elif [[ "$rel_path" == *"pending_tasks"* ]]; then
    summary="Proposed file moves — review and approve before executing"
  elif [[ "$rel_path" == *"PERSONAL_MASTER_INDEX"* ]]; then
    summary="Human navigation guide — taxonomy descriptions, folder status"
  elif [[ "$rel_path" == *"AGENT_CONTEXT_MAP"* ]]; then
    summary="RAG index of all Drive + key local + VM files"
  elif [[ "$rel_path" == *"CORE_IDENTITY"* ]]; then
    summary="Universal AI identity guide for cross-model collaboration"
  elif [[ "$rel_path" == *"HEARTBEAT"* ]]; then
    summary="VM health heartbeat — last ping timestamp, service status"
  fi
  DYNAMIC_ROWS="${DYNAMIC_ROWS}| \`${rel_path}\` | ${summary} | ${mod_date} | maintenance.sh | Active |\n"
done < <(find "$YNAI5_ROOT" -maxdepth 3 \( -name '*.md' -o -name '*.json' -o -name '*.sh' -o -name '*.txt' \) -type f 2>/dev/null | sort)

{
cat << MAP_HEADER_EOF
# YNAI5 Agent Context Map
> RAG-optimized machine-readable index. Read this FIRST before searching raw directories.
> Auto-refreshed by: VM \`maintenance.sh\` (daily 9AM AST) | Manual: \`/gdrive-org\` skill

**Last Updated:** $(date '+%Y-%m-%d %H:%M AST') by maintenance.sh on VM
**Format:** FilePath relative to \`gdrive:/YNAI5_AI_CORE/\` unless prefixed with \`local:\` or \`vm:\`

---

## Drive File Index (auto-generated)

| FilePath | ContentSummary | LastModified | AgentResponsible | SyncStatus |
|----------|----------------|--------------|------------------|------------|
MAP_HEADER_EOF
echo -e "$DYNAMIC_ROWS"
cat << MAP_FOOTER_EOF

---

## Key Local + VM Files (static — update manually or via /gdrive-org)

| FilePath | ContentSummary | LastModified | AgentResponsible | SyncStatus |
|----------|----------------|--------------|------------------|------------|
| \`local:CLAUDE.md\` | Master workspace file — role, workspace map, skills, workflow rules | 2026-04-10 | Claude | Active |
| \`local:context/current-priorities.md\` | Top priorities — crypto/stocks focus, passive income Telegram channel | 2026-04-10 | Claude | Active |
| \`local:memory/MEMORY.md\` | Auto-memory index — key learnings, session index, decisions | 2026-03-22 | Claude | Active |
| \`local:docs/INDEX.md\` | Documentation index — all research docs, reference files | 2026-04-13 | Claude | Active |
| \`local:projects/README.md\` | Project index — 11 active projects with status and paths | 2026-04-10 | Claude | Active |
| \`vm:~/main.py\` | FastAPI dashboard — 10 endpoints, port 8000 | ongoing | VM auto-restart | Active |
| \`vm:~/chat_server.py\` | Flask Gemini proxy — Lyra routing, port 8001 | ongoing | VM auto-restart | Active |
| \`vm:/ynai5_runtime/scripts/maintenance.sh\` | This script — scans Drive + VM, refreshes indexes daily | $(date '+%Y-%m-%d') | VM cron 9AM | Active |

---

## SyncStatus Key
| Value | Meaning |
|-------|---------|
| \`Active\` | In use, regularly updated |
| \`Archive\` | Finalized, kept for reference |
| \`Pending\` | Needs review or action |
| \`Stale\` | Not updated in >30 days |

## Agent Lookup
- **New device / Gemini handoff:** read \`01_Infrastructure_GCP/05_Work_Profile.md\` first
- **Find any file:** search FilePath column in table above
- **Cross-model files:** \`01_Infrastructure_GCP/CROSS_MODEL_SYNC/\`
- **VM access:** \`ssh -i ~/.ssh/ynai5_gcp shema@34.45.31.188\`
MAP_FOOTER_EOF
} > /tmp/AGENT_CONTEXT_MAP.md

cp /tmp/AGENT_CONTEXT_MAP.md "$YNAI5_ROOT/AGENT_CONTEXT_MAP.md"
log "AGENT_CONTEXT_MAP.md updated ✓"

log "=== maintenance.sh COMPLETE ==="
echo "Done. Both index files refreshed on Drive at $YNAI5_ROOT"
