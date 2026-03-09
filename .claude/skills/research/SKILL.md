---
name: research
description: Research a topic using web search, synthesize findings, and save as a dated document. Use when asked to research, look up, investigate, or find information on any topic.
argument-hint: [topic to research]
---

Research the topic: $ARGUMENTS

Follow these steps:

1. Use WebSearch to find current, relevant information on the topic
2. Search at least 2-3 different angles or sources
3. Synthesize the findings — identify key themes, facts, and insights
4. Save the research to `docs/YYYY-MM-DD-[topic-slug].md` using today's date
5. Update `docs/INDEX.md` with the new entry (date, topic, file path)
6. Return a brief summary of what was found and where it was saved

## Output File Format
```markdown
# Research: [Topic]
Date: YYYY-MM-DD
Sources: [list URLs used]

## Summary
[2-3 sentence executive summary]

## Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

## Details
[Expanded notes organized by theme]

## Next Steps / Follow-up
[What to research next, or actions to take based on findings]
```

Keep research actionable. End with concrete next steps or implications.
