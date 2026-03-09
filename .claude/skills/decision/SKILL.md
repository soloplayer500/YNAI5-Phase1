---
name: decision
description: Capture and archive a structured decision. Use when making any significant decision that should be documented for future reference.
argument-hint: [decision topic/title]
disable-model-invocation: true
---

Capture a structured decision about: $ARGUMENTS

## Steps

1. Ask clarifying questions if needed to fully understand the decision
2. Structure the decision using the template below
3. Save to `decisions/YYYY-MM-DD-[topic-slug].md`
4. Append a summary line to `memory/decisions-log.md`

## Decision Template

```markdown
# Decision: [Title]
Date: YYYY-MM-DD

## Context
[Why this decision was needed. What problem or situation prompted it?]

## Options Considered
1. [Option A]
2. [Option B]
3. [Option C — if applicable]

## Decision
[What was decided]

## Reasoning
[Why this option was chosen over the alternatives]

## Trade-offs Accepted
[What are we giving up with this choice?]

## Success Criteria
[How will we know if this was the right decision?]

## Outcome
[Fill in later once the decision plays out]
```

After saving, add this line to `memory/decisions-log.md`:
```
### [YYYY-MM-DD] [Title]
**Decision:** [1-line summary]
**File:** decisions/YYYY-MM-DD-[slug].md
```
