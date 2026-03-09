# Claude Code — Memory System
_Source: https://code.claude.com/docs/en/memory | Fetched: 2026-03-09_

## Two Memory Systems

| | CLAUDE.md files | Auto memory |
|--|--|--|
| Who writes it | You | Claude |
| What it contains | Instructions and rules | Learnings and patterns |
| Scope | Project, user, or org | Per working tree |
| Loaded into | Every session | Every session (first 200 lines) |

---

## CLAUDE.md File Locations (Priority Order)
1. **Managed policy** — `C:\Program Files\ClaudeCode\CLAUDE.md` (org-wide)
2. **Project** — `./CLAUDE.md` or `./.claude/CLAUDE.md` (team-shared via git)
3. **User** — `~/.claude/CLAUDE.md` (personal, all projects)
4. **Local** — `./CLAUDE.local.md` (personal, not git-tracked)

---

## Writing Effective CLAUDE.md

- **Target under 200 lines** — longer files reduce adherence
- **Use markdown headers and bullets** — Claude scans structure like readers do
- **Be specific and concrete**:
  - "Use 2-space indentation" NOT "Format code properly"
  - "Run `npm test` before committing" NOT "Test your changes"
- **No conflicting instructions** — Claude may pick one arbitrarily

---

## Import Syntax

Reference external files without bloating CLAUDE.md:

```
See @README for project overview and @package.json for available commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
```

- Relative and absolute paths allowed
- Recursive imports up to 5 hops deep
- First-time imports require approval dialog

---

## .claude/rules/ Directory

Organize instructions into topic-specific files:

```
.claude/rules/
├── code-style.md
├── testing.md
└── security.md
```

### Path-Scoped Rules (load only for matching files):
```yaml
---
paths:
  - "src/api/**/*.ts"
---
# Rules only apply to TypeScript API files
```

---

## Auto Memory

**Storage:** `~/.claude/projects/<project>/memory/`

```
memory/
├── MEMORY.md          ← Concise index, first 200 lines loaded every session
├── debugging.md       ← Topic file (loaded on demand)
└── api-conventions.md ← Topic file (loaded on demand)
```

- **First 200 lines of MEMORY.md** loaded at session start
- Topic files loaded on demand by Claude
- All files are plain markdown — edit or delete anytime
- Run `/memory` to browse and manage

**Enable/Disable:**
```json
{ "autoMemoryEnabled": false }
```
Or: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`

---

## /memory Command
- Lists all CLAUDE.md and rules files loaded in current session
- Toggle auto memory on/off
- Open memory folder
- Tell Claude "always use pnpm" → Claude saves to auto memory

---

## Troubleshooting
- Claude not following CLAUDE.md? Run `/memory` to verify it's loaded
- CLAUDE.md too large? Split with `@path` imports or `.claude/rules/`
- Instructions lost after `/compact`? They were only in chat, not in CLAUDE.md — add them
