import json
from pathlib import Path

from utils.time_utils import utcnow_iso, minutes_since
from storage.repository import get_state, set_state, record_alert

CACHE_PATH = Path(__file__).parent.parent / "state" / "runtime_cache.json"

# All trackable issue keys — base metrics + memory intelligence events
ALL_ISSUES = [
    "cpu", "ram", "disk", "swap",
    "memory_pressure", "swap_growth", "baseline_deviation",
]


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text())
        except Exception:
            pass
    return {}


def _save_cache(cache: dict):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2))


def process_events(events: list, cooldown_minutes: float) -> list:
    """
    Given current-cycle events, decide which alerts to fire.

    ALL_ISSUES not present in events are treated as OK (enables recovery detection).

    State machine per metric: OK → WARNING/CRITICAL → RECOVERED → OK
    Alert fires only on state change AND cooldown expired.

    Returns list of action dicts:
        {metric, action, old_state, new_state, value, context, suggested_action}
    action: "alert" | "recovery"
    """
    cache = _load_cache()
    event_map = {e["metric"]: e for e in events}
    actions = []

    for metric in ALL_ISSUES:
        db_state = get_state(metric)
        old_state = db_state["current_state"]
        last_alert = db_state["last_alert_sent"]

        ev = event_map.get(metric)
        new_state = ev["level"] if ev else "OK"

        if new_state == old_state:
            continue  # no state change — nothing to do

        if new_state == "OK" and old_state in ("WARNING", "CRITICAL"):
            # ── Recovery ──────────────────────────────────────────────────
            set_state(metric, "OK", last_changed=utcnow_iso(), last_alert_sent=None)
            record_alert(metric, "recovery")
            cache[metric] = {"state": "OK", "last_alert": None}
            actions.append({
                "metric": metric,
                "action": "recovery",
                "old_state": old_state,
                "new_state": "OK",
                "value": ev["value"] if ev else None,
                "context": "",
                "suggested_action": "",
            })

        elif new_state in ("WARNING", "CRITICAL"):
            # ── New alert — check cooldown ─────────────────────────────────
            elapsed = minutes_since(last_alert)
            if elapsed >= cooldown_minutes:
                set_state(metric, new_state,
                          last_changed=utcnow_iso(), last_alert_sent=utcnow_iso())
                record_alert(metric, "trigger")
                cache[metric] = {"state": new_state, "last_alert": utcnow_iso()}
                actions.append({
                    "metric": metric,
                    "action": "alert",
                    "old_state": old_state,
                    "new_state": new_state,
                    "value": ev["value"],
                    "context": ev.get("context", ""),
                    "suggested_action": ev.get("suggested_action", ""),
                })
            else:
                # Cooldown active — silently update state, no Telegram message
                set_state(metric, new_state, last_changed=utcnow_iso())
                cache[metric] = {"state": new_state, "last_alert": last_alert}

    _save_cache(cache)
    return actions
