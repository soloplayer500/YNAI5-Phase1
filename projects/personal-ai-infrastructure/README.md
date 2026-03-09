# Personal AI Infrastructure
**Status:** 🔄 Ongoing
**Type:** AI ecosystem design and architecture

---

## What It Is
The meta-project: designing and maintaining the entire personal AI ecosystem. This workspace (YNAI5-SU) is the primary implementation. Documentation of architecture decisions, system design, and how everything fits together.

## Problem It Solves
- Creates a single source of truth for how the AI infrastructure is designed
- Documents architectural decisions and why they were made
- Enables systematic expansion and upgrading of the system

## Components

| File | Purpose |
|------|---------|
| README.md | This file — overview and status |
| architecture.md | Full system design and component map |

## Current Architecture
- **Full Assistant:** Claude (this workspace)
- **Memory:** CLAUDE.md + MEMORY.md + preferences.md
- **Projects:** 5 project folders with dedicated structures
- **Skills:** 7 custom skills (/research, /session-close, etc.)
- **Version Control:** Local git → GitHub (when ready)

## Future Expansions (Planned)
- Sub-agents via API for specialized tasks
- Telegram bot for alerts (crypto monitoring)
- Automation scripts (Linux environment)
- Additional AI models as sub-agents when needed
