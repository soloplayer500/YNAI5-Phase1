# think.md — Pre-Task Thinking Protocol
_Invoke before any task with 3+ steps or architectural decisions._

---

## Stop → Frame

Before writing a single line, state in one sentence:
> "I am going to [action] so that [outcome]."

If you can't say it clearly, the task isn't ready.

---

## Classify Scope

| Class | Criteria | Ceremony |
|-------|----------|----------|
| **Quick-fix** | 1 file, <30 min | Jump in — no plan needed |
| **Standard** | 2–5 steps, multiple files | Brief PLAN block before executing |
| **Complex** | 6+ steps, architectural | Full PLAN + boundaries + acceptance criteria |

---

## Acceptance Criteria First (Complex tasks only)

Write criteria BEFORE any code:
```
GIVEN [context]
WHEN  [action taken]
THEN  [observable outcome]
```
Every task must map to at least one criterion. If a task doesn't satisfy a criterion, it's scope creep.

---

## Boundaries — Mark Off-Limits

Always declare what NOT to touch:
- Which files are read-only this session
- Which VM services must not restart
- Which env files are off-limits
- What state must be preserved

---

## Token Budget Check (from context.md)

Before starting, check context bracket (see `context.md`):
- FRESH → proceed with full plan
- MODERATE → execute only, no new plans
- DEPLETED → finish current task only, then close
- CRITICAL → stop, commit, session-close

---

## Failure Classification

If something goes wrong, classify BEFORE fixing:
| Type | Symptom | Fix |
|------|---------|-----|
| **Intent failure** | Built the wrong thing | Re-read requirement |
| **Spec failure** | Built right thing wrong way | Check constraints |
| **Code failure** | Syntax/logic bug | Debug + patch |

Never re-attempt without classifying first.

---

## Status Reporting

Use four-tier status — never binary pass/fail:
- `DONE` — complete, verified
- `DONE_WITH_CONCERNS` — works but has known issue
- `NEEDS_CONTEXT` — blocked on information
- `BLOCKED` — cannot proceed, escalate
