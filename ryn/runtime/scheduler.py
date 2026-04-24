#!/usr/bin/env python3
"""
RYN Scheduler — Lightweight task scheduler for RYN automation.
Runs scheduled tasks on cron-like intervals without external dependencies.
Designed for local execution on RYN (HP Laptop 15).

Usage:
    python ryn/runtime/scheduler.py          # run all due tasks
    python ryn/runtime/scheduler.py --list   # show schedule
    python ryn/runtime/scheduler.py --run <task>  # force run specific task
"""
import os, sys, json, time, subprocess
from pathlib import Path
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent.parent
AGENT_DIR  = BASE_DIR / "ryn" / "brain"
STATE_FILE = AGENT_DIR / "scheduler_state.json"
LOG_FILE   = AGENT_DIR / "scheduler.log"

# Task definitions: {name: {interval_hours, script_or_skill, description}}
TASKS = {
    "market-scan": {
        "interval_hours": 24,
        "description": "Morning market scan — fear/greed + top movers + signals",
        "type": "skill",
        "skill": "market-scan",
    },
    "vm-health": {
        "interval_hours": 6,
        "description": "SSH VM health check — services, RAM, disk",
        "type": "ssh",
        "cmd": "python3 ~/ynai5-agent/heartbeat.sh",
    },
    "brain-snapshot": {
        "interval_hours": 24,
        "description": "GitHub brain snapshot — commit system state",
        "type": "skill",
        "skill": "github-snapshot",
    },
    "log-audit": {
        "interval_hours": 48,
        "description": "VM log audit — check sizes, errors, patterns",
        "type": "skill",
        "skill": "log-audit",
    },
    "rag-rebuild": {
        "interval_hours": 168,  # weekly
        "description": "Rebuild RAG index after new files added",
        "type": "local",
        "cmd": ["python", "ryn/ryn-core/rag_indexer.py", "--index"],
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {}

def save_state(state: dict):
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def log(msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass

def is_due(name: str, interval_hours: int, state: dict) -> bool:
    last_run = state.get(name, {}).get("last_run_utc")
    if not last_run:
        return True
    elapsed = (datetime.now(timezone.utc).timestamp()
               - datetime.fromisoformat(last_run.replace("Z", "+00:00")).timestamp())
    return elapsed >= (interval_hours * 3600)

def mark_done(name: str, state: dict, success: bool):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state[name] = {"last_run_utc": ts, "success": success}

def run_local_task(task: dict) -> bool:
    try:
        r = subprocess.run(task["cmd"], capture_output=True, text=True, timeout=120,
                           cwd=str(BASE_DIR))
        if r.returncode == 0:
            log(f"  OK: {r.stdout.strip()[:200]}")
            return True
        else:
            log(f"  FAIL (exit {r.returncode}): {r.stderr.strip()[:200]}")
            return False
    except Exception as e:
        log(f"  ERROR: {e}")
        return False

# ── Main ──────────────────────────────────────────────────────────────────────

def list_tasks(state: dict):
    print(f"\n{'TASK':<20} {'INTERVAL':<12} {'LAST RUN':<22} {'DUE':<6} DESCRIPTION")
    print("-" * 85)
    for name, cfg in TASKS.items():
        last = state.get(name, {}).get("last_run_utc", "never")
        due  = "YES" if is_due(name, cfg["interval_hours"], state) else "no"
        ivl  = f"{cfg['interval_hours']}h"
        print(f"{name:<20} {ivl:<12} {last:<22} {due:<6} {cfg['description']}")
    print()

def run_due(state: dict, force: str = None):
    ran = 0
    for name, cfg in TASKS.items():
        if force and name != force:
            continue
        if force or is_due(name, cfg["interval_hours"], state):
            log(f"RUNNING: {name} ({cfg['description']})")
            if cfg["type"] == "local":
                ok = run_local_task(cfg)
            elif cfg["type"] in ("skill", "ssh"):
                # Skills and SSH tasks are invoked by Claude — log as reminder
                log(f"  ACTION NEEDED: invoke /{cfg.get('skill', name)} manually or via Claude")
                ok = True  # mark as done so it doesn't spam
            else:
                ok = False
            mark_done(name, state, ok)
            ran += 1
    if ran == 0 and not force:
        log("No tasks due.")
    save_state(state)

def main():
    state = load_state()
    args  = sys.argv[1:]

    if "--list" in args:
        list_tasks(state)
    elif "--run" in args:
        idx   = args.index("--run")
        task  = args[idx + 1] if idx + 1 < len(args) else None
        if not task or task not in TASKS:
            print(f"Unknown task. Valid: {', '.join(TASKS)}")
            sys.exit(1)
        run_due(state, force=task)
    else:
        log("=== RYN Scheduler — checking due tasks ===")
        run_due(state)

if __name__ == "__main__":
    main()
