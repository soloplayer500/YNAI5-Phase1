---
name: session-close
description: Close the current session by creating a session summary document. Use at the end of every work session to capture what was done, decisions made, and next steps.
disable-model-invocation: true
argument-hint: [optional: brief session focus description]
---

Close this session and create a session summary.

1. Review what was accomplished in this session
2. Identify all decisions made
3. List open items and next steps
4. Check if any preferences were learned — save to `memory/preferences.md`
5. Check if any decisions should be archived — save to `decisions/YYYY-MM-DD-[topic].md`
6. Create the session summary file at `sessions/YYYY-MM-DD-session.md`
7. Update `memory/MEMORY.md` Session Index with this session

## Session Summary Template

```markdown
# Session: YYYY-MM-DD
**Focus:** [what this session covered]
**Time/Effort:** [rough sense of how much was done]

## What Got Done
- [item 1]
- [item 2]

## Decisions Made
- [decision 1]
- [decision 2]

## Open Items
- [ ] [item 1]
- [ ] [item 2]

## Next Steps
- [next step 1]
- [next step 2]

## Memory Updates
- Preferences learned: [any new preferences discovered]
- Decisions logged: [any decisions archived]
- Files created/updated: [list of files changed]
```

If $ARGUMENTS is provided, use it as the session Focus description.

Always save the file — do not just output it in chat.
