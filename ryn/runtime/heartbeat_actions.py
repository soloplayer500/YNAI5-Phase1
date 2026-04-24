#!/usr/bin/env python3
"""
RYN Heartbeat Actions — Automated responses to VM heartbeat alerts.
Listens to alert.state on VM (via SSH poll) and takes corrective action.

This runs ON RYN (local) polling the VM. Complements the VM-side heartbeat.sh.
Runs via scheduler.py or manually.

Usage:
    python ryn/runtime/heartbeat_actions.py --check   # single check
    python ryn/runtime/heartbeat_actions.py --watch   # poll every 60s
"""
import os, sys, json, time, subprocess
from pathlib import Path
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────────────────────
SSH_KEY  = Path.home() / ".ssh" / "google_compute_engine"
VM_HOST  = "shema@34.45.31.188"
SSH_OPTS = ["-i", str(SSH_KEY), "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10"]
POLL_SEC = 60
MAX_AUTO_RESTARTS = 1  # per service per session — don't loop-restart

_restart_counts: dict = {}

# ── Auto-actions per alert key ────────────────────────────────────────────────
# Format: key → {action: str, cmd: str|None}
ALERT_ACTIONS = {
    "dash": {
        "desc": "ynai5-dashboard is DOWN",
        "auto_restart": True,
        "service": "ynai5-dashboard",
    },
    "nginx": {
        "desc": "nginx is DOWN",
        "auto_restart": True,
        "service": "nginx",
    },
    "load": {
        "desc": "HIGH CPU LOAD on VM",
        "auto_restart": False,
        "action": "Check top processes via SSH",
    },
    "ram": {
        "desc": "CRITICAL RAM on VM (<100MB)",
        "auto_restart": False,
        "action": "Check memory consumers, consider restarting ynai5-gemini",
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log(msg: str):
    print(f"[{ts()}] {msg}")

def ssh(cmd: str, timeout: int = 15) -> tuple[int, str]:
    full = ["ssh"] + SSH_OPTS + [VM_HOST, cmd]
    try:
        r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, f"TIMEOUT ({timeout}s)"
    except Exception as e:
        return -1, str(e)

def read_alert_state() -> dict:
    """Read ~/ynai5-agent/alert.state from VM, parse key=value lines."""
    code, out = ssh("cat ~/ynai5-agent/alert.state 2>/dev/null || echo ''")
    state = {}
    for line in out.splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            state[k.strip()] = v.strip()
    return state

def restart_service(service: str) -> bool:
    count = _restart_counts.get(service, 0)
    if count >= MAX_AUTO_RESTARTS:
        log(f"  SKIP auto-restart {service} — already restarted {count}x this session")
        return False
    log(f"  AUTO-RESTART: {service}")
    code, out = ssh(f"sudo systemctl restart {service} && sleep 3 && systemctl is-active {service}")
    success = "active" in out
    _restart_counts[service] = count + 1
    log(f"  Result: {'OK' if success else 'FAILED'} — {out[:100]}")
    return success

def get_top_processes() -> str:
    _, out = ssh("ps aux --sort=-%mem | head -6 | awk '{print $1,$2,$3,$4,$11}'")
    return out

# ── Check loop ────────────────────────────────────────────────────────────────

def check_once() -> list[str]:
    """Check VM alert state, take actions. Returns list of active alerts."""
    log("Checking VM alert state...")
    code, _ = ssh("echo ping")
    if code != 0:
        log("  SSH UNREACHABLE — cannot check VM")
        return ["ssh_unreachable"]

    state = read_alert_state()
    active_alerts = []

    for key, cfg in ALERT_ACTIONS.items():
        val = state.get(key, "ok")
        # Also check logsize_ prefixed keys
        if val == "fired":
            active_alerts.append(key)
            log(f"  ALERT ACTIVE: {key} — {cfg['desc']}")
            if cfg.get("auto_restart") and cfg.get("service"):
                restart_service(cfg["service"])
            else:
                log(f"  MANUAL ACTION: {cfg.get('action', 'investigate')}")

    # Check logsize alerts
    for k, v in state.items():
        if k.startswith("logsize_") and v == "fired":
            active_alerts.append(k)
            log(f"  ALERT ACTIVE: {k} — log file over 20MB")
            log(f"  MANUAL ACTION: SSH and rotate/compress the log")

    if not active_alerts:
        log("  All clear — no active alerts")

    return active_alerts

def watch():
    log(f"=== RYN Heartbeat Watcher — polling every {POLL_SEC}s. Ctrl+C to stop. ===")
    while True:
        check_once()
        time.sleep(POLL_SEC)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if "--watch" in args:
        watch()
    elif "--check" in args or not args:
        alerts = check_once()
        sys.exit(0 if not alerts else 1)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
