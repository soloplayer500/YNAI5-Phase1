# Claude Code — Skills System
_Source: https://code.claude.com/docs/en/skills | Fetched: 2026-03-09_

## What Are Skills?

Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you invoke directly with `/skill-name`.

---

## Skill File Structure

```
.claude/skills/my-skill/
├── SKILL.md           ← Required: instructions + frontmatter
├── templates/         ← Optional: templates Claude fills in
├── examples/          ← Optional: example outputs
└── scripts/           ← Optional: scripts Claude can execute
```

---

## SKILL.md Format

```yaml
---
name: skill-name
description: What it does and when to use it. Claude uses this to decide.
disable-model-invocation: true   # optional: only YOU can invoke, not Claude
user-invocable: false            # optional: only CLAUDE invokes, not you
allowed-tools: Read, Grep        # optional: tools allowed without permission
context: fork                    # optional: run in isolated subagent
agent: Explore                   # optional: which subagent type
---

Your skill instructions here.
Use $ARGUMENTS for passed arguments.
Use $0, $1, $2 for positional args.
```

---

## Where Skills Live

| Location | Path | Applies to |
|----------|------|------------|
| Personal | `~/.claude/skills/<skill>/SKILL.md` | All your projects |
| Project  | `.claude/skills/<skill>/SKILL.md` | This project only |

---

## Key Frontmatter Fields

| Field | Purpose |
|-------|---------|
| `name` | The `/slash-command` name |
| `description` | When Claude should auto-invoke (keep specific) |
| `disable-model-invocation: true` | Manual only — you invoke, Claude never does automatically |
| `user-invocable: false` | Claude background knowledge — not a user command |
| `allowed-tools` | Tools usable without permission approval |
| `context: fork` | Run in isolated subagent |
| `argument-hint` | Shown in autocomplete: e.g., `[ticker]` |

---

## Arguments

```yaml
---
name: fix-issue
---
Fix GitHub issue $ARGUMENTS following our standards.
```

- `/fix-issue 123` → replaces `$ARGUMENTS` with `123`
- `$0`, `$1`, `$2` for positional arguments

---

## Invocation Control

| Frontmatter | You invoke | Claude invokes |
|-------------|-----------|----------------|
| (default) | Yes | Yes |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

---

## Running in a Subagent

```yaml
---
name: deep-research
context: fork
agent: Explore
---
Research $ARGUMENTS thoroughly...
```

Agent options: `Explore`, `Plan`, `general-purpose`, or custom subagent name.

---

## Dynamic Context (Shell Commands)

```yaml
---
name: pr-summary
allowed-tools: Bash(gh *)
---
PR diff: !`gh pr diff`
PR comments: !`gh pr view --comments`

Summarize this pull request...
```

`!`command`` runs before Claude sees anything — output replaces the placeholder.

---

## Bundled Skills (Built-In)

| Skill | Usage |
|-------|-------|
| `/simplify` | Review and clean up recently changed files |
| `/batch <instruction>` | Large-scale parallel changes across codebase |
| `/debug` | Troubleshoot current Claude session |
| `/loop [interval] <prompt>` | Run a prompt repeatedly on a schedule |
| `/claude-api` | Load Claude API reference material |

---

## Best Practices

- Keep SKILL.md under 500 lines — move details to supporting files
- Use `disable-model-invocation: true` for anything with side effects (deploy, send, delete)
- Be specific in `description` — Claude uses it to decide when to auto-invoke
- For background knowledge: use `user-invocable: false`
- Reference supporting files from SKILL.md so Claude knows what's there
