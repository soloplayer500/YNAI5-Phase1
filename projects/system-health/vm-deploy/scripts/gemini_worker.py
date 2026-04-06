#!/usr/bin/env python3
"""
YNAI5-Phase1 Gemini Worker — CLI Edition
Polls HEARTBEAT.json every 30s, executes tasks via Gemini CLI subprocess.
Faster and more reliable than Python SDK.
"""
import json
import fcntl
import os
import subprocess
import time
from datetime import datetime, timezone

# Load .env file
_ENV_PATH = '/ynai5_runtime/.env'
try:
    with open(_ENV_PATH) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith('#') and '=' in _line:
                _k, _v = _line.split('=', 1)
                os.environ[_k.strip()] = _v.strip()
except FileNotFoundError:
    pass

HEARTBEAT_PATH = '/mnt/gdrive/SYNC/HEARTBEAT.json'
CORE_IDENTITY_PATH = '/mnt/gdrive/SYSTEM/CORE_IDENTITY.md'
LOG_PATH = '/ynai5_runtime/logs/gemini_worker.log'
GEMINI_CLI = '/usr/bin/gemini'
POLL_INTERVAL = 30


def log(msg):
    ts = datetime.now(timezone.utc).isoformat()
    line = f'[{ts}] [GEMINI] {msg}'
    print(line, flush=True)
    with open(LOG_PATH, 'a') as f:
        f.write(line + '\n')


def read_heartbeat():
    with open(HEARTBEAT_PATH) as f:
        return json.load(f)


def write_heartbeat(data):
    data['last_update'] = datetime.now(timezone.utc).isoformat()
    lock = HEARTBEAT_PATH + '.lock'
    with open(lock, 'w') as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            tmp = HEARTBEAT_PATH + '.tmp'
            with open(tmp, 'w') as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, HEARTBEAT_PATH)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def update_vm_status(hb):
    hb['vm_status']['running'] = True
    hb['vm_status']['last_seen'] = datetime.now(timezone.utc).isoformat()
    return hb


def execute_gemini_task(task):
    api_key = os.environ.get('GEMINI_API_KEY', '')
    if not api_key:
        return 'ERROR: GEMINI_API_KEY not set'

    identity = ''
    try:
        with open(CORE_IDENTITY_PATH) as f:
            identity = f.read()
    except FileNotFoundError:
        identity = 'YNAI5-Phase1 — Multi-AI system. Owner: Solo/Shami, Aruba.'

    context = task.get('context', '')
    prompt = f"""You are the Gemini AI worker in the YNAI5-Phase1 system.

SYSTEM IDENTITY:
{identity}

{"CONTEXT: " + context if context else ""}

TASK:
{task['command']}

Be concise, direct, and actionable."""

    env = os.environ.copy()
    env['GEMINI_API_KEY'] = api_key

    result = subprocess.run(
        [GEMINI_CLI, '-p', prompt],
        capture_output=True, text=True,
        timeout=60, env=env
    )

    output = result.stdout.strip()
    if result.returncode != 0 and not output:
        output = result.stderr.strip() or f'Exit code {result.returncode}'
    return output or '(empty response)'


def run_worker():
    log('Gemini CLI worker started — polling every 30s')

    while True:
        try:
            hb = read_heartbeat()
            my_tasks = [t for t in hb.get('task_queue', []) if t.get('assigned_to') == 'gemini']

            if my_tasks:
                task = my_tasks[0]
                log(f'Task {task["id"]}: {task["command"][:80]}')

                hb['status'] = 'working'
                hb['active_agent'] = 'gemini'
                write_heartbeat(hb)

                try:
                    result = execute_gemini_task(task)
                    hb = read_heartbeat()
                    hb['stats']['gemini_calls'] = hb['stats'].get('gemini_calls', 0) + 1
                    hb['stats']['tasks_completed'] = hb['stats'].get('tasks_completed', 0) + 1
                except Exception as e:
                    result = f'ERROR: {e}'
                    hb = read_heartbeat()
                    hb['stats']['tasks_failed'] = hb['stats'].get('tasks_failed', 0) + 1

                hb['task_queue'] = [t for t in hb['task_queue'] if t['id'] != task['id']]
                hb['status'] = 'idle'
                hb['active_agent'] = None
                hb['last_task_result'] = {
                    'task_id': task['id'],
                    'agent': 'gemini',
                    'result': result,
                    'completed_at': datetime.now(timezone.utc).isoformat()
                }
                update_vm_status(hb)
                write_heartbeat(hb)
                log(f'Task {task["id"]} done — {len(result)} chars')

            else:
                hb = update_vm_status(hb)
                write_heartbeat(hb)

        except FileNotFoundError:
            log(f'HEARTBEAT.json not found — Drive mounted?')
        except json.JSONDecodeError as e:
            log(f'HEARTBEAT parse error: {e}')
        except Exception as e:
            log(f'Error: {e}')

        time.sleep(POLL_INTERVAL)


if __name__ == '__main__':
    run_worker()
