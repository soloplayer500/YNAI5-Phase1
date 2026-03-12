# System Health — YNAI5
**Status:** ✅ Active | **Priority:** High

Crash recovery, system diagnostics, Docker on-demand, Windows auto-start.

## What It Is
Infrastructure layer that keeps the YNAI5 workspace alive and recoverable.
Runs health diagnostics locally, backs up sessions on crash, and monitors APIs
from the cloud (GitHub Actions) even when the laptop is off.

## Problem It Solves
- Laptop crashes mid-session → session context is lost
- Need to know when critical APIs (CoinGecko, Kraken, GitHub) go down
- Scripts need to start automatically on boot without manual intervention
- Docker Desktop shouldn't run 24/7 but should be available on demand

## Components
| File | Purpose |
|------|---------|
| session-backup.py | Crash recovery (called by PreCompact/Stop/SessionStart hooks) |
| health-check.py | Local diagnostics (RAM/CPU/disk/internet/Docker) |
| cloud-health.py | API health check (GitHub Actions — runs even when laptop is OFF) |
| docker-manager.py | Docker on-demand (auto-starts Desktop, spins up containers) |
| startup.bat | Windows startup automation (auto-starts all YNAI5 scripts at login) |
| install-startup.py | One-time installer — copies startup.bat to Windows Startup folder |

## Current Stage
All components built and active. Hooks configured. startup.bat installed in Windows Startup folder.

## Skills
- `/health-check [--telegram] [--quick]` — system diagnostics
- `/docker [command]` — Docker on-demand (auto-starts)
- `/backup` — manually trigger session backup

## Hooks (auto-configured)
- PreCompact → session-backup.py --trigger=compact
- Stop → session-backup.py --trigger=stop
- SessionStart → session-backup.py --trigger=start

## GitHub Actions
- Workflow: `.github/workflows/system-health.yml`
- Schedule: 9AM AST daily (13:00 UTC)
- Sends Telegram report with API status

## Quick Commands
```bash
# Run full health check and send to Telegram
python projects/system-health/health-check.py --telegram

# Quick health (RAM/disk/internet only)
python projects/system-health/health-check.py --quick

# Manual session backup
python projects/system-health/session-backup.py --trigger=stop

# Docker status
python projects/system-health/docker-manager.py status

# Reinstall startup automation
python projects/system-health/install-startup.py
```
