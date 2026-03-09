---
name: remember
description: Save a preference or persistent instruction to memory. Use when told "remember I always prefer X" or "always do Y" or "never do Z".
argument-hint: [preference to remember]
---

Save this preference to memory: $ARGUMENTS

## Steps

1. Determine the category this preference belongs to:
   - Communication (tone, format, style)
   - Workflow (how to work, order of operations)
   - Output Format (structure, detail level)
   - Technical (tools, languages, frameworks)
   - Decision Making (criteria, priorities)
   - Other (anything else)

2. Format the entry:
   ```
   - [YYYY-MM-DD] [Preference description]
   ```

3. Add it to the appropriate section in `memory/preferences.md`

4. Confirm to the user: "Saved: [preference] under [category]"

This preference will now apply to all future sessions.
