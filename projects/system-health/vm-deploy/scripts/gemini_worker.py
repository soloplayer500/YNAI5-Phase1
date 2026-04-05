#!/usr/bin/env python3
"""
YNAI5-Phase1 Gemini Worker
Reads HEARTBEAT.json every 30s, executes tasks assigned to 'gemini' via Gemini API,
writes results back to HEARTBEAT.json on Google Drive mount.
"""
import json
import os
import time
import sys
from datetime import datetime, timezone

HEARTBEAT_PATH = "/mnt/gdrive/SYNC/HEARTBEAT.json"
CORE_IDENTITY_PATH = "/mnt/gdrive/SYSTEM/CORE_IDENTITY.md"
LOG_PATH = "/ynai5_runtime/logs/gemini_worker.log"
POLL_INTERVAL = 30  # seconds


def log(msg: str):
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] [GEMINI] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def read_heartbeat() -> dict:
    with open(HEARTBEAT_PATH) as f:
        return json.load(f)


def write_heartbeat(data: dict):
    data["last_update"] = datetime.now(timezone.utc).isoformat()
    # Atomic write: write to temp then rename
    tmp = HEARTBEAT_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, HEARTBEAT_PATH)


def execute_gemini_task(task: dict) -> str:
    try:
        import google.generativeai as genai
    except ImportError:
        return "ERROR: google-generativeai not installed. Run: pip install google-generativeai"

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: GEMINI_API_KEY not set in environment"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    # Load system identity for context
    identity = ""
    try:
        with open(CORE_IDENTITY_PATH) as f:
            identity = f.read()
    except FileNotFoundError:
        identity = "YNAI5-Phase1 — Multi-AI persistent intelligence system. Owner: Solo/Shemar, Aruba."

    context = task.get("context", "")
    prompt = f"""You are the Gemini worker for the YNAI5-Phase1 AI system.

SYSTEM IDENTITY:
{identity}

{"ADDITIONAL CONTEXT: " + context if context else ""}

TASK:
{task['command']}

Respond with actionable, concise results. Be direct and specific."""

    response = model.generate_content(prompt)
    return response.text


def update_vm_status(hb: dict):
    """Update the VM's live status in HEARTBEAT without changing other fields."""
    hb["vm_status"]["running"] = True
    hb["vm_status"]["last_seen"] = datetime.now(timezone.utc).isoformat()
    return hb


def run_worker():
    log("Gemini worker started — polling every 30s")

    while True:
        try:
            hb = read_heartbeat()
            queue = hb.get("task_queue", [])
            my_tasks = [t for t in queue if t.get("assigned_to") == "gemini"]

            if my_tasks:
                task = my_tasks[0]
                log(f"Picking up task {task['id']}: {task['command'][:80]}")

                # Mark as working
                hb["status"] = "working"
                hb["active_agent"] = "gemini"
                write_heartbeat(hb)

                # Execute
                try:
                    result = execute_gemini_task(task)
                    hb["stats"]["gemini_calls"] = hb["stats"].get("gemini_calls", 0) + 1
                    hb["stats"]["tasks_completed"] = hb["stats"].get("tasks_completed", 0) + 1
                except Exception as e:
                    result = f"ERROR during execution: {e}"
                    hb["stats"]["tasks_failed"] = hb["stats"].get("tasks_failed", 0) + 1
                    hb.setdefault("errors", []).append({
                        "task_id": task["id"],
                        "error": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })

                # Write result + remove task from queue
                hb = read_heartbeat()  # Re-read to avoid race conditions
                hb["task_queue"] = [t for t in hb["task_queue"] if t["id"] != task["id"]]
                hb["status"] = "idle"
                hb["active_agent"] = None
                hb["last_task_result"] = {
                    "task_id": task["id"],
                    "agent": "gemini",
                    "result": result,
                    "completed_at": datetime.now(timezone.utc).isoformat()
                }
                update_vm_status(hb)
                write_heartbeat(hb)
                log(f"Task {task['id']} complete")

            else:
                # Just update VM heartbeat
                hb = update_vm_status(hb)
                write_heartbeat(hb)

        except FileNotFoundError:
            log(f"HEARTBEAT.json not found at {HEARTBEAT_PATH} — is Drive mounted?")
        except json.JSONDecodeError as e:
            log(f"HEARTBEAT.json parse error: {e} — skipping cycle")
        except Exception as e:
            log(f"Unexpected error: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run_worker()
