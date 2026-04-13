import os
import signal

import psutil

from utils.time_utils import utcnow_iso  # noqa: F401 — available for callers

# Modes
OBSERVE   = "observe"
SUGGEST   = "suggest"
ASSIST    = "assist"
AUTO_SAFE = "auto_safe"

# Actions we will never execute regardless of mode
FORBIDDEN_ACTIONS = {"restart_process", "kill_system_process", "modify_config"}

# Safe executable actions
SAFE_ACTIONS = {"renice_process", "kill_user_process", "free_memory"}


def handle(decisions: list, mode: str, whitelist: list, mon_log) -> list:
    """
    Process decisions according to current mode.

    Returns list of action_result dicts:
    {
        metric, decision, recommended_action, process_target,
        action_status,   # 'none' | 'suggested' | 'executed' | 'failed'
        result_detail,   # description of what happened
        pid,             # if a process was targeted
    }
    """
    return [_handle_one(dec, mode, whitelist, mon_log) for dec in decisions]


def _handle_one(decision: dict, mode: str, whitelist: list, mon_log) -> dict:
    rec_action = decision.get("recommended_action", "none")
    target = decision.get("process_target")
    metric = decision["metric"]

    base = {
        "metric": metric,
        "decision": decision,
        "recommended_action": rec_action,
        "process_target": target,
        "action_status": "none",
        "result_detail": "",
        "pid": None,
    }

    if mode == OBSERVE:
        base["result_detail"] = "observe mode — logged only"
        return base

    if mode == SUGGEST:
        base["action_status"] = "suggested"
        base["result_detail"] = f"suggested: {rec_action}"
        return base

    if mode == ASSIST:
        base["action_status"] = "suggested"
        base["result_detail"] = f"assist mode — action prepared but not executed: {rec_action}"
        return base

    if mode == AUTO_SAFE:
        return _execute_safe(base, rec_action, target, whitelist, mon_log)

    # Unknown mode — default to observe
    base["result_detail"] = f"unknown mode={mode} — defaulting to observe"
    return base


def _execute_safe(base: dict, rec_action: str, target: str,
                  whitelist: list, mon_log) -> dict:
    """Execute only safe, reversible actions. Never touches system processes."""
    if rec_action not in SAFE_ACTIONS:
        base["result_detail"] = f"action '{rec_action}' not in safe list — skipped"
        return base

    if not target:
        base["result_detail"] = "no process target — skipped"
        return base

    if target in whitelist:
        base["result_detail"] = f"'{target}' is whitelisted — skipped"
        return base

    pid = _find_user_process(target)
    if pid is None:
        base["result_detail"] = f"process '{target}' not found or is system process"
        return base

    base["pid"] = pid

    if rec_action == "renice_process":
        return _renice(base, pid, target, mon_log)
    elif rec_action == "kill_user_process":
        return _kill_user(base, pid, target, mon_log)
    elif rec_action == "free_memory":
        base["action_status"] = "suggested"
        base["result_detail"] = (
            "suggest: run 'sync && echo 3 > /proc/sys/vm/drop_caches' manually"
        )
        return base

    base["result_detail"] = f"unhandled safe action: {rec_action}"
    return base


def _find_user_process(name: str):
    """Return PID of the first matching process owned by non-root user, or None."""
    try:
        for p in psutil.process_iter(["pid", "name", "uids"]):
            try:
                if p.info["name"] == name:
                    uids = p.info["uids"]
                    if uids and uids.real != 0:
                        return p.info["pid"]
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        pass
    return None


def _renice(base: dict, pid: int, name: str, mon_log) -> dict:
    try:
        p = psutil.Process(pid)
        old_nice = p.nice()
        p.nice(10)
        base["action_status"] = "executed"
        base["result_detail"] = f"reniced '{name}' pid={pid} from {old_nice} to 10"
    except Exception as e:
        base["action_status"] = "failed"
        base["result_detail"] = f"renice failed: {e}"
        mon_log.error(f'"action_engine renice failed: {e}"')
    return base


def _kill_user(base: dict, pid: int, name: str, mon_log) -> dict:
    try:
        os.kill(pid, signal.SIGTERM)
        base["action_status"] = "executed"
        base["result_detail"] = f"SIGTERM sent to '{name}' pid={pid}"
    except Exception as e:
        base["action_status"] = "failed"
        base["result_detail"] = f"kill failed: {e}"
        mon_log.error(f'"action_engine kill failed: {e}"')
    return base
