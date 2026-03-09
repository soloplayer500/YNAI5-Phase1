---
name: project-update
description: Update a project's README status section. Use when project status changes or after significant progress on a project.
argument-hint: [project name, e.g. psychecore or crypto-monitoring]
disable-model-invocation: true
---

Update the status for project: $ARGUMENTS

## Steps

1. Read the project's README.md from `projects/$ARGUMENTS/README.md`
2. Ask what has changed (if not already provided in context)
3. Update the **Status** line in the README with the new status
4. Update the project entry in `projects/README.md` table
5. Optionally add a session-log entry if the project has a session-log.md

## Status Options
- 🔨 Building — actively in development
- 🧪 Concept/Dev — concept defined, starting development
- 📋 Strategy Phase — planning/documenting strategy
- 🔄 Ongoing — continuous background project
- ✅ Done — completed
- ⏸ Paused — on hold

Confirm what was updated after making changes.
