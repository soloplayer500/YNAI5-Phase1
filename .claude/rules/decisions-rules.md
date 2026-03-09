---
paths:
  - "decisions/**/*.md"
  - "memory/decisions-log.md"
---

# Decision File Rules

When creating or editing files in the `decisions/` directory or `memory/decisions-log.md`:

- Decision filename format: `YYYY-MM-DD-[descriptive-slug].md`
- All decision files must include: Context, Options Considered, Decision, Reasoning, Trade-offs Accepted, Success Criteria, Outcome (even if empty)
- Every new decision file must also get a summary line added to `memory/decisions-log.md`
- decisions-log.md format: `### [YYYY-MM-DD] [Title]` followed by Decision and File fields
- Never delete decisions — they are the permanent record
- When Outcome is filled in later, also update the decisions-log.md entry
