# memory.md — Memory Architecture Guide
_What lives where, what gets committed, what gets rebuilt each session._

---

## Memory Layers

| Layer | File | Committed | Rebuilt | Purpose |
|-------|------|-----------|---------|---------|
| **Brain State** | `ryn/brain/state.json` | ❌ gitignored | Each session | Model availability, VM state |
| **Event Log** | `ryn/brain/last_report.md` | ✅ | Append only | Chronological event log |
| **VM Snapshot** | `ryn/brain/system_summary.md` | ✅ | After major events | Human-readable system state |
| **Priority Stack** | `ryn/brain/priority_stack.md` | ✅ | When priorities shift | ROI-ranked objective list |
| **Session Index** | `memory/MEMORY.md` | ✅ | Append (max 200 lines) | Cross-session learnings |
| **Preferences** | `memory/preferences.md` | ✅ | On change | Saved user preferences |
| **Decisions** | `memory/decisions-log.md` | ✅ | Append only | Significant decisions |
| **RAG Index** | `ryn/brain/index/` | ❌ gitignored | On demand | Keyword chunk index |

---

## Session Startup Protocol

```
1. Read CLAUDE.md (auto-loaded)
2. Check ryn/brain/priority_stack.md → what's #1 right now?
3. Check ryn/brain/system_summary.md → VM state known?
4. Check memory/MEMORY.md last 10 entries → anything critical?
5. If RAG stale: python ryn/ryn-core/rag_indexer.py --index
```

---

## Session Close Protocol

```
1. Append to ryn/brain/last_report.md (what happened, metrics)
2. Update ryn/brain/system_summary.md if VM state changed
3. Update memory/MEMORY.md with key learnings (max 2-3 lines)
4. Update ryn/brain/priority_stack.md if priorities shifted
5. git add + commit + push
```

---

## What Gets Committed vs Ignored

**Committed (brain state shared via GitHub):**
- `ryn/brain/last_report.md`
- `ryn/brain/system_summary.md`
- `ryn/brain/priority_stack.md`
- `ryn/framework/*.md`
- `ryn/runtime/*.py`
- `ryn/profit/*.md`
- `.claude/skills/*/SKILL.md`

**Gitignored (local runtime artifacts):**
- `ryn/brain/state.json`
- `ryn/brain/chunks/`
- `ryn/brain/index/`
- `ryn/brain/*.log`

---

## Memory Overflow Rule

`memory/MEMORY.md` must stay under 200 lines.  
When it overflows → move older entries to topic files:
- `memory/patterns.md` — recurring insights
- `memory/decisions-log.md` — decisions made
- `sessions/YYYY-MM-DD-session.md` — per-session summaries

---

## Brain Rebuild Triggers

Rebuild RAG index when:
- New skill files added
- New docs added to docs/ or context/
- New ryn/framework/ or ryn/profit/ files
- More than 2 weeks since last rebuild

Command: `python ryn/ryn-core/rag_indexer.py --index`
