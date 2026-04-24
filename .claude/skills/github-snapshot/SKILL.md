---
name: github-snapshot
description: Commit current brain state and all changed files to GitHub. Use when user says "snapshot", "save state", "commit brain", "push to GitHub", "save progress", or at session end
---

# /github-snapshot [--brain-only | --full]

Commit and push the current system state to GitHub master.

**Default:** --full (all changed files + brain update)  
**--brain-only:** Only brain/framework/profit files

## Step 1 — Build State Summary

Collect current state to write to brain files:
- VM service states (from last known or SSH check)
- Key metrics if available (disk, RAM)
- What changed this session

## Step 2 — Update Brain Files

**Append to ryn/brain/last_report.md:**
```markdown
## [YYYY-MM-DDThh:mm:ssZ] — [EVENT NAME]

**Event:** [brief description]
**Changes:**
- [list of what was done]

**State at event:**
- [key metrics]
```

**Update ryn/brain/system_summary.md** if VM state changed.

**Update ryn/brain/priority_stack.md** if priorities shifted.

## Step 3 — Check What's Changed

```bash
git -C "C:\Users\shema\OneDrive\Desktop\YNAI5-SU" status --short
git -C "C:\Users\shema\OneDrive\Desktop\YNAI5-SU" diff --stat HEAD
```

Review: nothing in .gitignore should be staged (no state.json, no chunks/, no *.log).

## Step 4 — Stage Relevant Files

```bash
git -C "C:\Users\shema\OneDrive\Desktop\YNAI5-SU" add ryn/framework/ ryn/runtime/ ryn/profit/ ryn/brain/last_report.md ryn/brain/system_summary.md ryn/brain/priority_stack.md .claude/skills/ PROJECT_OPERATING_MODEL.md CLAUDE.md
```

Do NOT stage:
- ryn/brain/state.json
- ryn/brain/chunks/
- ryn/brain/index/
- .env.local
- *.log files

## Step 5 — Commit

Commit message format:
```
brain: [session summary in <60 chars]

Co-Authored-By: RYN <ryn@ynai5.local>
```

Examples:
```
brain: framework + 6 skills + profit layer deployed
brain: vm-repair + priority stack update
brain: trading session — 3 new predictions logged
```

## Step 6 — Push

```bash
git -C "C:\Users\shema\OneDrive\Desktop\YNAI5-SU" push origin master
```

Verify: check GitHub confirms push, no errors.

## Step 7 — Report

```
GITHUB SNAPSHOT [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━━
FILES COMMITTED: X
COMMIT: [short hash] "[message]"
PUSH: SUCCESS / FAILED
BRAIN UPDATED: last_report ✓ | system_summary ✓ | priority_stack ✓
━━━━━━━━━━━━━━━━━━━━━━━━
```
