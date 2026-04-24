# build.md — Execution & Closure Protocol
_The APPLY → QUALIFY → UNIFY loop for RYN._

---

## Before Executing

1. Reference `think.md` output — acceptance criteria confirmed?
2. Context bracket checked (`context.md`)
3. Backup created if touching VM/production files
4. Boundaries noted — know what NOT to touch

---

## Execute → Qualify Loop

For each task:

```
1. EXECUTE  — implement the task
2. QUALIFY  — verify against acceptance criteria
3. STATUS   — assign one of: DONE / CONCERN / BLOCKED
4. PROCEED  — only move forward on DONE or CONCERN
```

**Qualify means:** run it, check the output, read the log, confirm the service is active.  
Not: "it looks right" or "I think it worked."

---

## Task Reporting Template

```
TASK: [name]
FILE: [path]
ACTION: [what was done]
VERIFY: [how confirmed]
STATUS: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
NOTE: [anything deferred or concerning]
```

---

## UNIFY — Mandatory Closure

After ALL tasks complete:

1. Compare plan vs. actual — what changed?
2. List deferred issues (don't lose them)
3. Update brain files:
   - `ryn/brain/last_report.md` — append event entry
   - `ryn/brain/system_summary.md` — update if VM state changed
   - `ryn/brain/priority_stack.md` — re-rank if priorities shifted
4. Commit with descriptive message
5. Push to master

---

## VM Work Rules

- Always backup before patching: `cp file file.bak`
- Always syntax-check scripts: `bash -n script.sh` / `python3 -m py_compile`
- Always verify service after restart: `systemctl is-active`
- Max 1 restart attempt per service — if it fails twice, STOP + report
- SSH heredocs: use SCP for Python files (single-quote conflicts)

---

## Git Commit Convention

```
feat:  new feature or file
patch: targeted fix to existing
refactor: restructure without behavior change
docs: markdown/docs only
infra: VM/systemd/config changes
brain: brain state files update
```
