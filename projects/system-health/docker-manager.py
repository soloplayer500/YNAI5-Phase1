#!/usr/bin/env python3
"""
YNAI5 Docker Manager — auto-starts Docker Desktop if needed.
Usage:
    python docker-manager.py status
    python docker-manager.py start
    python docker-manager.py ps
    python docker-manager.py "run hello-world"
"""
import sys
import subprocess
import time
import os
from pathlib import Path

DOCKER_DESKTOP = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
MAX_WAIT = 60


def is_running():
    try:
        r = subprocess.run(["docker", "ps"], capture_output=True, text=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False


def start():
    if is_running():
        print("[Docker] Already running")
        return True
    print("[Docker] Starting Docker Desktop...")
    if not Path(DOCKER_DESKTOP).exists():
        print(f"[Docker] Not found at {DOCKER_DESKTOP}")
        return False
    os.startfile(DOCKER_DESKTOP)
    for i in range(MAX_WAIT):
        time.sleep(1)
        if is_running():
            print(f"[Docker] Ready in {i + 1}s")
            return True
        if i % 15 == 14:
            print(f"[Docker] Waiting... {i + 1}s")
    print("[Docker] Timeout — Docker Desktop did not start in time")
    return False


def run_cmd(cmd):
    if not is_running():
        if not start():
            return 1
    parts = ["docker"] + cmd.split()
    return subprocess.run(parts).returncode


def main():
    if len(sys.argv) < 2:
        print("Usage: docker-manager.py <status|start|command>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "status":
        if is_running():
            print("[Docker] Running")
        else:
            print("[Docker] Not running")
    elif action == "start":
        sys.exit(0 if start() else 1)
    else:
        sys.exit(run_cmd(" ".join(sys.argv[1:])))


if __name__ == "__main__":
    main()
