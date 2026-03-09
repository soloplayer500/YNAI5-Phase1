# AI Infrastructure Architecture
Last Updated: 2026-03-09

---

## Current System Design

```
YNAI5-SU Workspace
├── Core Memory Layer
│   ├── CLAUDE.md          ← Persistent instructions (loaded every session)
│   ├── context/           ← Profile, priorities, goals
│   └── memory/            ← Auto-memory, preferences, decisions
│
├── Project Layer
│   ├── psychecore/        ← Reasoning framework
│   ├── crypto-monitoring/ ← Market intelligence
│   ├── multi-ai-prompts/  ← Prompt engineering
│   ├── social-media/      ← Content strategy
│   └── personal-ai-infra/ ← This meta-project
│
├── Execution Layer
│   ├── .claude/skills/    ← Custom /commands
│   ├── .claude/rules/     ← Path-scoped behavior rules
│   └── sessions/          ← Session-by-session history
│
└── Version Control
    └── git (local → GitHub)
```

## Design Principles
1. Local-first — full control, privacy, offline capability
2. Markdown-based — readable, editable, version-controllable
3. Modular — each component is independent and swappable
4. Self-documenting — the system documents itself as it evolves
5. MVP first — build the minimum needed, expand when useful

## Expansion Roadmap
- Phase 1 (Now): Foundation workspace ← **current stage**
- Phase 2: Sub-agents via API (when complex tasks need specialization)
- Phase 3: Automation scripts (Linux-based workflows)
- Phase 4: Alert infrastructure (Telegram bot for crypto alerts)
- Phase 5: GitHub-hosted with CI/CD for automated maintenance

## Architecture Decisions
_Logged with rationale — see memory/decisions-log.md for full history_

| Decision | Choice | Why |
|----------|--------|-----|
| Single AI vs multi-AI routing | Claude as full assistant | Simpler, no context switching, sub-agents added via API when needed |
| Storage | Local markdown | Control, privacy, git-compatible |
| Memory system | CLAUDE.md + MEMORY.md | Native Claude Code support, auto-learning |
