#!/usr/bin/env python3
"""
YNAI5-Phase1 Dashboard — FastAPI backend
Serves live system status, heartbeat state, and task queue management.
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import uuid
import subprocess
from datetime import datetime, timezone
from pydantic import BaseModel

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

app = FastAPI(title="YNAI5-Phase1 Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HEARTBEAT_PATH = "/mnt/gdrive/SYNC/HEARTBEAT.json"
DRIVE_ROOT = "/mnt/gdrive"
GEMINI_LOG = "/ynai5_runtime/logs/gemini_worker.log"
CLAUDE_LOG = "/ynai5_runtime/logs/claude_runner.log"
DASHBOARD_HTML = os.path.join(os.path.dirname(__file__), "index.html")


class TaskRequest(BaseModel):
    command: str
    assigned_to: str  # "claude" | "gemini"
    priority: int = 1
    context: str = ""


def read_heartbeat() -> dict:
    try:
        with open(HEARTBEAT_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "Drive not mounted", "status": "offline"}
    except json.JSONDecodeError:
        return {"error": "HEARTBEAT.json corrupted", "status": "error"}


def write_heartbeat(data: dict):
    data["last_update"] = datetime.now(timezone.utc).isoformat()
    tmp = HEARTBEAT_PATH + ".dashboard.tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, HEARTBEAT_PATH)


def get_vm_metrics() -> dict:
    if not PSUTIL_OK:
        return {"error": "psutil not installed"}
    import psutil
    try:
        boot_ts = psutil.boot_time()
        uptime_s = int(datetime.now().timestamp() - boot_ts)
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.5),
            "ram_percent": psutil.virtual_memory().percent,
            "ram_used_gb": round(psutil.virtual_memory().used / 1e9, 2),
            "ram_total_gb": round(psutil.virtual_memory().total / 1e9, 2),
            "disk_percent": psutil.disk_usage("/").percent,
            "disk_free_gb": round(psutil.disk_usage("/").free / 1e9, 2),
            "uptime_hours": round(uptime_s / 3600, 1),
        }
    except Exception as e:
        return {"error": str(e)}


def get_service_status(service: str) -> str:
    try:
        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def tail_log(path: str, lines: int = 20) -> list:
    try:
        with open(path) as f:
            all_lines = f.readlines()
        return [l.rstrip() for l in all_lines[-lines:]]
    except FileNotFoundError:
        return [f"Log not found: {path}"]
    except Exception as e:
        return [f"Error reading log: {e}"]


@app.get("/api/status")
def get_status():
    hb = read_heartbeat()
    vm = get_vm_metrics()
    drive_mounted = os.path.exists(DRIVE_ROOT) and bool(os.listdir(DRIVE_ROOT))
    services = {
        "ynai5-drive": get_service_status("ynai5-drive"),
        "ynai5-gemini": get_service_status("ynai5-gemini"),
        "ynai5-claude": get_service_status("ynai5-claude"),
        "ynai5-dashboard": get_service_status("ynai5-dashboard"),
    }
    return {
        "heartbeat": hb,
        "vm": vm,
        "drive_mounted": drive_mounted,
        "services": services,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/task")
def post_task(task: TaskRequest):
    if task.assigned_to not in ("claude", "gemini"):
        raise HTTPException(400, "assigned_to must be 'claude' or 'gemini'")
    if not task.command.strip():
        raise HTTPException(400, "command cannot be empty")

    hb = read_heartbeat()
    if "error" in hb:
        raise HTTPException(503, f"Cannot reach HEARTBEAT: {hb['error']}")

    new_task = {
        "id": str(uuid.uuid4())[:8],
        "type": "manual",
        "command": task.command.strip(),
        "priority": task.priority,
        "assigned_to": task.assigned_to,
        "context": task.context,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    hb.setdefault("task_queue", []).append(new_task)
    write_heartbeat(hb)
    return {"status": "queued", "task_id": new_task["id"], "assigned_to": task.assigned_to}


@app.delete("/api/task/{task_id}")
def delete_task(task_id: str):
    hb = read_heartbeat()
    before = len(hb.get("task_queue", []))
    hb["task_queue"] = [t for t in hb.get("task_queue", []) if t["id"] != task_id]
    if len(hb["task_queue"]) == before:
        raise HTTPException(404, f"Task {task_id} not found")
    write_heartbeat(hb)
    return {"status": "deleted", "task_id": task_id}


@app.get("/api/logs/gemini")
def get_gemini_logs(lines: int = 30):
    return {"logs": tail_log(GEMINI_LOG, lines)}


@app.get("/api/logs/claude")
def get_claude_logs(lines: int = 30):
    return {"logs": tail_log(CLAUDE_LOG, lines)}


@app.get("/api/heartbeat")
def get_heartbeat():
    return read_heartbeat()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    try:
        with open(DASHBOARD_HTML) as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Dashboard HTML not found</h1><p>Place index.html in /ynai5_runtime/dashboard/</p>"
