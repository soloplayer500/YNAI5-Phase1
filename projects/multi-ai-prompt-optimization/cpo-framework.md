# Claude Prompt Optimizer (CPO)
_Framework for getting maximum performance from Claude_

Last Updated: 2026-03-09

---

## Core Principles

1. **Role + Context first** — tell Claude who it is and what the situation is before asking anything
2. **Specific over vague** — concrete instructions produce consistent results
3. **Constraints matter** — tell Claude what NOT to do, not just what to do
4. **Structure your output request** — specify format explicitly
5. **Chain of thought** — for complex tasks, ask Claude to reason step by step

---

## CPO Template Structure

```
## Role
[Who Claude is for this prompt]

## Context
[What situation/project/background is relevant]

## Task
[Specific, concrete task description]

## Constraints
- [What to avoid]
- [What NOT to include]
- [Format requirements]

## Output Format
[Exactly how you want the output structured]

## Examples (if needed)
[Input → Output example]
```

---

## Claude-Specific Behaviors

**What works well:**
- Structured markdown output
- Multi-step reasoning tasks
- Code generation with constraints
- Analysis and comparison tasks
- File management and organization

**Requires explicit instruction:**
- "Save to file" — Claude defaults to chat output otherwise
- "Challenge weak reasoning" — Claude defaults to agreeable
- "Be concise" — Claude defaults to thorough

---

## Prompt Patterns

### Pattern: Executive Summary
```
Analyze [X] and provide a 3-bullet executive summary.
Do not include background or context — only conclusions and actions.
```

### Pattern: Devil's Advocate
```
I believe [X]. Challenge this. Find the strongest counterarguments.
Don't validate my position — stress-test it.
```

### Pattern: MVP Scoper
```
I want to build [X]. What's the simplest version that delivers value?
List only what's essential for MVP. Ignore nice-to-haves.
```

---

## Notes
[Add observations and refinements as you develop the framework]
