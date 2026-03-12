---
name: health-check
description: Run YNAI5 system health diagnostics — RAM, CPU, disk, internet, Docker, Python procs. Sends Telegram report. Use when system feels slow, before heavy tasks, or any time.
---

# Health Check Skill

## What I Do
Run parallel system diagnostics. Fast. Parallel. Actionable output.

## Usage
- `/health-check` — full diagnostics (print + save log)
- `/health-check --telegram` — also send Telegram alert
- `/health-check --quick` — RAM + disk + internet only (faster)

## Steps

1. Run the health check:
```bash
python "C:/Users/shema/OneDrive/Desktop/YNAI5-SU/projects/system-health/health-check.py" [flags]
```

2. Read output and surface the most important findings first:
   - 🔴 CRITICAL (crashes likely): RAM > 85%, Swap > 60%
   - ⚠️ WARNING: anything above threshold
   - ✅ Green: all clear

3. Always give 1-3 actionable recommendations:
   - If RAM high: list top memory hogs, suggest what to close
   - If disk low: suggest cleanup commands
   - If many Python procs: show PIDs to kill

4. If --telegram requested: add `--telegram` flag to command

5. Log auto-saved to `projects/system-health/logs/`
