---
name: weekly-review
description: Perform a weekly review of the workspace — scan open actions, surface stale items, and refresh memory. Run once a week to keep the system sharp.
disable-model-invocation: true
---

Perform the weekly review of the YNAI5-SU workspace.

## Steps

1. **Scan `actions/`** — list all open `- [ ]` items, flag any overdue
2. **Review `context/current-priorities.md`** — are current priorities still accurate? Flag if update needed
3. **Scan `sessions/`** — review last 7 days of session summaries for open items not yet actioned
4. **Check `memory/MEMORY.md`** — is it under 200 lines? If over, suggest topics to move to topic files
5. **Scan project session logs** — any project with no activity in 7+ days? Flag it
6. **Review `memory/preferences.md`** — any conflicting or outdated preferences?

## Output

Produce a structured weekly review summary:

```markdown
# Weekly Review: YYYY-MM-DD

## Open Actions
[list all open items from actions/]

## Stale Projects
[projects with no recent activity]

## Priority Check
[are current-priorities.md entries still valid?]

## Memory Health
- MEMORY.md line count: [X]
- Action needed: [yes/no — what]

## Last Week Summary
[1-3 bullet points of what got done last week]

## This Week Focus
[suggested top priorities based on open items]
```

Save the review to `sessions/YYYY-MM-DD-weekly-review.md`.
