from storage.db import get_connection
from utils.time_utils import utcnow_iso


# ── Events ────────────────────────────────────────────────────────────────────

def insert_event(metric: str, value: float, level: str,
                 context: str = "", suggested_action: str = ""):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO events "
            "(timestamp, metric, value, level, context, suggested_action) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (utcnow_iso(), metric, value, level, context, suggested_action),
        )


# ── States ────────────────────────────────────────────────────────────────────

def get_state(metric: str) -> dict:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM states WHERE metric = ?", (metric,)
        ).fetchone()
        if row:
            return dict(row)
        return {
            "metric": metric,
            "current_state": "OK",
            "last_changed": None,
            "last_alert_sent": None,
        }


# Sentinel: distinguishes "caller didn't pass last_alert_sent" vs "caller wants NULL"
_UNSET = object()


def set_state(metric: str, state: str,
              last_changed: str = None, last_alert_sent=_UNSET):
    """
    Update (or insert) a metric's state row.

    last_alert_sent:
      - Omitted (_UNSET)  → leave existing last_alert_sent unchanged
      - None              → explicitly clear last_alert_sent to NULL (recovery)
      - str timestamp     → set to that timestamp (alert fired)
    """
    now = utcnow_iso()
    with get_connection() as conn:
        if last_alert_sent is _UNSET:
            # Only update current_state and last_changed; leave last_alert_sent alone
            conn.execute(
                """
                INSERT INTO states (metric, current_state, last_changed, last_alert_sent)
                VALUES (?, ?, ?, NULL)
                ON CONFLICT(metric) DO UPDATE SET
                    current_state = excluded.current_state,
                    last_changed  = COALESCE(excluded.last_changed, last_changed)
                """,
                (metric, state, last_changed or now),
            )
        else:
            # Explicitly set last_alert_sent (NULL clears it; timestamp records it)
            conn.execute(
                """
                INSERT INTO states (metric, current_state, last_changed, last_alert_sent)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(metric) DO UPDATE SET
                    current_state   = excluded.current_state,
                    last_changed    = COALESCE(excluded.last_changed, last_changed),
                    last_alert_sent = excluded.last_alert_sent
                """,
                (metric, state, last_changed or now, last_alert_sent),
            )


# ── Alerts sent ───────────────────────────────────────────────────────────────

def record_alert(metric: str, alert_type: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO alerts_sent (metric, timestamp, type) VALUES (?, ?, ?)",
            (metric, utcnow_iso(), alert_type),
        )


# ── Self-log ──────────────────────────────────────────────────────────────────

def log_self_error(error_type: str, message: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO monitor_self_log (timestamp, error_type, message) "
            "VALUES (?, ?, ?)",
            (utcnow_iso(), error_type, message),
        )


# ── Memory trends ─────────────────────────────────────────────────────────────

def insert_memory_trend(available_ram_percent: float,
                        swap_used_mb: float,
                        swap_delta_mb: float = None):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO memory_trends "
            "(timestamp, available_ram_percent, swap_used_mb, swap_delta_mb) "
            "VALUES (?, ?, ?, ?)",
            (utcnow_iso(), available_ram_percent, swap_used_mb, swap_delta_mb),
        )


# ── Process snapshots ─────────────────────────────────────────────────────────

def insert_process_snapshots(timestamp: str, processes: list):
    """
    processes: list of dicts {name, pid, memory_mb, cpu_percent}, ordered 1..N.
    rank is derived from list position (1 = highest memory consumer).
    """
    with get_connection() as conn:
        conn.executemany(
            "INSERT INTO process_snapshots "
            "(timestamp, process_name, pid, memory_mb, cpu_percent, rank) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [
                (timestamp, p["name"], p["pid"],
                 p["memory_mb"], p["cpu_percent"], i + 1)
                for i, p in enumerate(processes)
            ],
        )


# ── Baseline metrics ──────────────────────────────────────────────────────────

def insert_baseline_metric(avg_available_ram: float):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO baseline_metrics (timestamp, avg_available_ram) "
            "VALUES (?, ?)",
            (utcnow_iso(), avg_available_ram),
        )


# ── Decision trace ─────────────────────────────────────────────────────────────

def insert_decision_trace(metric: str, observation: str, insight: str,
                          decision: str, action: str, action_status: str,
                          confidence: float, result: str = "unknown") -> int:
    """Insert a decision trace row. Returns the new row id."""
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO decision_trace "
            "(timestamp, metric, observation, insight, decision, action, "
            "action_status, result, confidence) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (utcnow_iso(), metric, observation, insight, decision,
             action, action_status, result, confidence),
        )
        return cur.lastrowid


def update_trace_result(trace_id: int, result: str):
    """Update result field (e.g., 'resolved' on recovery) for a trace row."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE decision_trace SET result = ? WHERE id = ?",
            (result, trace_id),
        )


# ── Learning log ───────────────────────────────────────────────────────────────

def insert_learning_log(issue: str, action_suggested: str,
                        action_taken: str, outcome: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO learning_log "
            "(timestamp, issue, action_suggested, action_taken, outcome) "
            "VALUES (?, ?, ?, ?, ?)",
            (utcnow_iso(), issue, action_suggested, action_taken, outcome),
        )
