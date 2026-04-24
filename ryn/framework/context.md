# context.md — Context Window Discipline
_Inspired by CARL's context brackets. Keep sessions lean and purposeful._

---

## Context Brackets

| Bracket | Remaining | Mode | Rules |
|---------|-----------|------|-------|
| **FRESH** | >60% | Full analysis | New plans OK, subagents OK, research OK |
| **MODERATE** | 30–60% | Focused execution | No new research, complete current plan only |
| **DEPLETED** | 10–30% | Wrap up | Finish current task, no new tasks, commit |
| **CRITICAL** | <10% | Emergency close | Stop mid-task, commit what's done, session-close |

**Rule:** Never start a Complex task in MODERATE or lower.

---

## Token-Efficient Habits

**DO:**
- Read only the sections of a file you need
- Reference existing knowledge ("as noted in system_summary.md") instead of re-reading
- Write outputs to files directly — don't leave results in chat
- Use `tail -20` not `cat` for log files
- Batch parallel tool calls when independent

**DON'T:**
- Re-read CLAUDE.md mid-session (it's already loaded)
- Re-read brain files you've already processed
- Launch subagents for implementation (discovery/research only)
- Keep large tool outputs in context — summarize and move on

---

## Just-In-Time Rule Loading (CARL pattern)

RYN skills load on keyword match — not all at once:

| Keywords | Domain Loaded |
|----------|--------------|
| trade, position, entry, BTC, ETH, setup | TRADING domain |
| SSH, VM, service, systemctl, restart, deploy | VM-OPS domain |
| /status, /logs, bot, Telegram, commander | TELEGRAM domain |
| commit, push, GitHub, snapshot, brain | GITHUB domain |
| log, audit, heartbeat, alert, monitor | LOG-AUDIT domain |

---

## Star-Commands (Explicit Mode Triggers)

| Command | Effect |
|---------|--------|
| `*brief` | Summary only — no deep analysis |
| `*deep` | Full analysis mode, all context used |
| `*vm` | SSH context — next actions are VM commands |
| `*trade` | Trading analysis mode — fetch data then analyze |
| `*snapshot` | GitHub brain snapshot mode |
| `*plan` | Force plan-before-execute discipline |

---

## Subagent Rules (PAUL-inspired)

- **Use subagents for:** discovery, research, codebase exploration, parallel reads
- **Do NOT use for:** implementation, writing files, executing commands
- **Max subagents in MODERATE:** 0
- **Max subagents in DEPLETED:** 0
