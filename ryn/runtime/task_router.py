#!/usr/bin/env python3
"""
RYN Task Router — Routes tasks to the right execution layer.
Decides: local script | SSH to VM | GitHub Actions trigger | Telegram command.

Usage:
    python ryn/runtime/task_router.py --task vm-repair
    python ryn/runtime/task_router.py --task market-scan
    python ryn/runtime/task_router.py --list
"""
import os, sys, json, subprocess
from pathlib import Path
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent.parent
SSH_KEY  = Path.home() / ".ssh" / "google_compute_engine"
VM_HOST  = "shema@34.45.31.188"
SSH_OPTS = ["-i", str(SSH_KEY), "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10"]

# Route map: task → {layer, description, action}
ROUTES = {
    # VM tasks → SSH
    "vm-status":       {"layer": "ssh",      "cmd": "python3 ~/ynai5-agent/commander.py"},
    "vm-repair":       {"layer": "skill",    "skill": "/vm-repair",    "desc": "SSH diagnostic loop"},
    "log-audit":       {"layer": "skill",    "skill": "/log-audit",    "desc": "VM log analysis"},
    "vm-snapshot":     {"layer": "telegram", "tg_cmd": "/snapshot",    "desc": "Telegram /snapshot"},
    "vm-restart-dash": {"layer": "telegram", "tg_cmd": "/restart ynai5-dashboard"},
    "vm-restart-gem":  {"layer": "telegram", "tg_cmd": "/restart ynai5-gemini"},

    # Local tasks
    "rag-rebuild":     {"layer": "local", "cmd": ["python", "ryn/ryn-core/rag_indexer.py", "--index"]},
    "scheduler-run":   {"layer": "local", "cmd": ["python", "ryn/runtime/scheduler.py"]},

    # Skill invocations (Claude handles)
    "market-scan":     {"layer": "skill", "skill": "/market-scan",     "desc": "Daily market brief"},
    "trading-setup":   {"layer": "skill", "skill": "/trading-analysis","desc": "Trade setup analysis"},
    "github-snapshot": {"layer": "skill", "skill": "/github-snapshot", "desc": "Brain commit + push"},

    # GitHub Actions (remote trigger via gh CLI)
    "deploy-sync":     {"layer": "github", "workflow": "vm-sync.yml",     "desc": "Deploy latest to VM"},
    "health-report":   {"layer": "github", "workflow": "system-health.yml","desc": "Run system health check"},
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def ssh_run(cmd: str, timeout: int = 30) -> tuple[int, str, str]:
    full = ["ssh"] + SSH_OPTS + [VM_HOST, cmd]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", f"TIMEOUT ({timeout}s)"
    except Exception as e:
        return -1, "", str(e)

def local_run(cmd: list, timeout: int = 60) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(BASE_DIR))
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return -1, str(e)

def github_trigger(workflow: str) -> bool:
    code, out = local_run(["gh", "workflow", "run", workflow, "--repo",
                           "soloplayer500/YNAI5-SU"])
    if code == 0:
        log(f"  GitHub Actions: {workflow} triggered")
        return True
    else:
        log(f"  GitHub Actions FAILED: {out}")
        return False

# ── Router ────────────────────────────────────────────────────────────────────

def route(task_name: str) -> bool:
    if task_name not in ROUTES:
        log(f"Unknown task: {task_name}. Run --list to see options.")
        return False

    route_cfg = ROUTES[task_name]
    layer = route_cfg["layer"]
    desc  = route_cfg.get("desc", task_name)
    log(f"ROUTE: {task_name} → [{layer.upper()}] {desc}")

    if layer == "ssh":
        cmd = route_cfg.get("cmd", "echo 'no cmd'")
        code, out, err = ssh_run(cmd)
        if code == 0:
            log(f"  SSH OK:\n{out[:400]}")
            return True
        else:
            log(f"  SSH FAILED (exit {code}): {err[:200]}")
            return False

    elif layer == "local":
        code, out = local_run(route_cfg["cmd"])
        log(f"  LOCAL {'OK' if code == 0 else 'FAILED'}: {out[:300]}")
        return code == 0

    elif layer == "github":
        return github_trigger(route_cfg["workflow"])

    elif layer == "skill":
        log(f"  SKILL: Invoke '{route_cfg['skill']}' via Claude Code")
        return True  # instruction to Claude — always succeeds as routing

    elif layer == "telegram":
        log(f"  TELEGRAM: Send '{route_cfg['tg_cmd']}' to @SoloClaude5_bot")
        return True

    return False

def list_routes():
    print(f"\n{'TASK':<22} {'LAYER':<10} DESCRIPTION")
    print("-" * 65)
    for name, cfg in ROUTES.items():
        layer = cfg["layer"].upper()
        desc  = cfg.get("desc", cfg.get("skill", cfg.get("workflow", cfg.get("tg_cmd", ""))))
        print(f"{name:<22} {layer:<10} {desc}")
    print()

def main():
    args = sys.argv[1:]
    if "--list" in args:
        list_routes()
    elif "--task" in args:
        idx  = args.index("--task")
        task = args[idx + 1] if idx + 1 < len(args) else None
        if not task:
            print("Usage: --task <task_name>")
            sys.exit(1)
        ok = route(task)
        sys.exit(0 if ok else 1)
    else:
        print(__doc__)
        list_routes()

if __name__ == "__main__":
    main()
