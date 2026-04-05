#!/usr/bin/env python3
"""
YNAI5-Phase1 Claude Runner
Reads HEARTBEAT.json every 30s, executes tasks assigned to 'claude' via claude --print CLI,
writes results back to HEARTBEAT.json on Google Drive mount.
"""
import json
import os
import subprocess
import time
from datetime import datetime, timezone

HEARTBEAT_PATH = "/mnt/gdrive/SYNC/HEARTBEAT.json"
LOG_PATH = "/ynai5_runtime/logs/claude_runner.log"
WORKSPACE = "/ynai5_runtime"
POLL_INTERVAL = 30
TASK_TIMEOUT = 120  # seconds


def log(msg: str):
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] [CLAUDE] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def read_heartbeat() -> dict:
    with open(HEARTBEAT_PATH) as f:
        return json.load(f)


def write_heartbeat(data: dict):
    data["last_update"] = datetime.now(timezone.utc).isoformat()
    tmp = HEARTBEAT_PATH + ".claude.tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, HEARTBEAT_PATH)


def execute_claude_task(task: dict) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "ERROR: ANTHROPIC_API_KEY not set in environment"

    command = task["command"]
    env = {**os.environ, "ANTHROPIC_API_KEY": api_key}

    try:
        result = subprocess.run(
            ["claude", "--print", command],
            capture_output=True,
            text=True,
            timeout=TASK_TIMEOUT,
            env=env,
            cwd=WORKSPACE
        )
        output = result.stdout.strip()
        if result.returncode != 0 and not output:
            output = result.stderr.strip() or f"Exit code: {result.returncode}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return f"ERROR: Task timed out after {TASK_TIMEOUT}s"
    except FileNotFoundError:
        return "ERROR: 'claude' CLI not found — run: npm install -g @anthropic-ai/claude-code"
    except Exception as e:
        return f"ERROR: {e}"


def run_runner():
    log("Claude runner started — polling every 30s")

    while True:
        try:
            hb = read_heartbeat()
            queue = hb.get("task_queue", [])
            my_tasks = [t for t in queue if t.get("assigned_to") == "claude"]

            if my_tasks:
                task = my_tasks[0]
                log(f"Picking up task {task['id']}: {task['command'][:80]}")

                try:
                    result = execute_claude_task(task)
                    hb = read_heartbeat()
                    hb["stats"]["claude_calls"] = hb["stats"].get("claude_calls", 0) + 1
                    hb["stats"]["tasks_completed"] = hb["stats"].get("tasks_completed", 0) + 1
                except Exception as e:
                    result = f"ERROR: {e}"
                    hb = read_heartbeat()
                    hb["stats"]["tasks_failed"] = hb["stats"].get("tasks_failed", 0) + 1

                hb["task_queue"] = [t for t in hb["task_queue"] if t["id"] != task["id"]]
                hb["last_task_result"] = {
                    "task_id": task["id"],
                    "agent": "claude",
                    "result": result,
                    "completed_at": datetime.now(timezone.utc).isoformat()
                }
                write_heartbeat(hb)
                log(f"Task {task['id']} complete")

        except FileNotFoundError:
            log(f"HEARTBEAT.json not found — is Drive mounted at /mnt/gdrive?")
        except json.JSONDecodeError as e:
            log(f"HEARTBEAT.json parse error: {e}")
        except Exception as e:
            log(f"Unexpected error: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run_runner()
