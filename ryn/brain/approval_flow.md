# RYN — Telegram Approval Flow (Design)

_Bonus deliverable from 2026-04-24 portfolio directive. Design only — implement when easy._

---

## Why
Solo operator + autonomous workflows = risk of unintended action.
Approval gates protect: git push, deployments, paid actions, deletions.

The Telegram commander already exists (`@SoloClaude5_bot` — chat 8569520396, v2 hardened).
Adding an approval pattern on top is incremental, not new infrastructure.

---

## Trigger Categories

| Action | Risk | Approval Required? |
|--------|------|-------------------|
| `git push` to master | Medium | YES — preview commit before push |
| GitHub workflow run (paid action) | Medium | YES — confirm before manual dispatch |
| VM service restart | Low | NO — `/restart` is fast & safe |
| Kraken trade execution | HIGH | YES — every order, no exceptions |
| File deletion in `ryn/brain/` | High | YES — append `archive/` instead |
| Any new file >100KB committed | Medium | YES — likely accidental binary |
| Any cost-incurring API call | Medium | YES if cost > $0.50/call |
| Telegram broadcast to free/VIP channel | Medium | NO if from screener-bot.yml (already filtered) |
| Telegram broadcast manual | High | YES — never auto |

---

## Mechanism (MVP — keep simple)

### Pattern 1: Pre-action approval
Bot asks before acting. Operator replies `/approve` or `/deny` within 5 minutes.

```
[BOT] 🔐 APPROVAL REQUIRED
Action: git push to master (3 files)
Files: screener-bot.yml, distribution/*.md, brain/*.md
Reply /approve [ID] within 5 min to proceed
```

### Pattern 2: Post-action notification
For low-risk actions, no approval required, but notification fires.

```
[BOT] ✅ ACTION COMPLETED
- Restarted ynai5-commander (uptime: 0s)
- All endpoints 200 OK
```

### Pattern 3: Daily digest
Catch-all. Every day at 8 PM AST, bot summarizes all actions taken in last 24h.

---

## Implementation Notes (when ready)

**Where it lives:** Extend `ryn/runtime/telegram_tasks.py` — already has `send/receive` helpers.

**Where to gate:**
- `task_router.py` already routes layers — add an `approval_required(action)` predicate
- For git pushes, hook into commit-push command via `.claude/skills/`
- For Kraken orders, only the `/kraken` skill calls `place_order` — add gate there

**State file:** `ryn/brain/approvals/{ID}.json`
- Created on request
- Updated on `/approve` or `/deny`
- Auto-expires after 5 min (treated as deny)

**Auth:** Trust chat ID 8569520396 only. Reject everything else.

---

## Phase Plan (when implementing)

| Phase | Effort | Coverage |
|-------|--------|----------|
| 1 | 2h | Daily digest only (Pattern 3). Read-only, easy ship. |
| 2 | 4h | Pre-action approval for `git push` + Kraken orders only (Pattern 1). |
| 3 | 4h | Post-action notification for VM restarts + workflow runs (Pattern 2). |
| 4 | 2h | Approval state file + 5-min timeout logic. |

**Total: ~12 hours of work, ship in 2 sessions.**

---

## Don't implement until
- Block Syndicate has 5+ paid VIP subs (proves operator is acting through automated lanes)
- Or operator triggers an unintended action that costs $5+ and wants the gate

Until then: this design lives here as a reference.
