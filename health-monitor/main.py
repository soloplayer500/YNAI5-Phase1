"""
Health Monitor — Phase 1
Full production loop: collect -> evaluate -> persist -> state -> alert -> log.
Self-awareness: loop duration, consecutive failure tracking, stall detection.
Systemd handles restarts — this process never self-restarts.
"""
import yaml
import time
from pathlib import Path
from collections import defaultdict

from core.collector import collect
from core.evaluator import evaluate
from core.state_manager import process_events
from core.alert_engine import send_alerts
from core.insight_engine import run_analysis
from core.decision_engine import make_decisions
from core.action_engine import handle as handle_actions
from storage.db import init_db
from storage.repository import (
    insert_event,
    insert_memory_trend,
    insert_process_snapshots,
    insert_baseline_metric,
    log_self_error,
    insert_decision_trace,
)
from utils.logger import get_logger
from utils.time_utils import utcnow_iso

BASE = Path(__file__).parent

# Credential search order: Ubuntu deploy path, then dev Windows path
_ENV_CANDIDATES = [
    Path.home() / "YNAI5-SU" / ".env.local",
    Path("C:/Users/shema/OneDrive/Desktop/YNAI5-SU/.env.local"),
]


def load_config() -> dict:
    with open(BASE / "config.yaml") as f:
        return yaml.safe_load(f)


def load_env() -> dict:
    for path in _ENV_CANDIDATES:
        if path.exists():
            env = {}
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip()
            return env
    return {}


def _safe_self_log(error_type: str, message: str):
    """Write to monitor_self_log table — silently swallow DB errors here."""
    try:
        log_self_error(error_type, message)
    except Exception:
        pass  # already logged to monitor.log by caller


def main():
    cfg = load_config()
    env = load_env()

    sys_log = get_logger("system", str(BASE / cfg["logging"]["system_log"]))
    mon_log = get_logger("monitor", str(BASE / cfg["logging"]["monitor_log"]))

    init_db()

    # ── Config ────────────────────────────────────────────────────────────────
    interval     = cfg["monitor"]["interval_seconds"]
    cooldown     = cfg["monitor"]["cooldown_minutes"]
    top_procs    = cfg["monitor"]["top_processes"]
    stall_limit  = cfg["monitor"]["stall_detection_cycles"]
    offender_min = cfg["monitor"]["offender_min_appearances"]
    thresholds   = cfg["thresholds"]

    # Credentials: .env.local first, then config.yaml inline fallback
    bot_token = env.get("TELEGRAM_BOT_TOKEN") or cfg["telegram"].get("bot_token", "")
    chat_id   = env.get("TELEGRAM_CHAT_ID")   or cfg["telegram"].get("chat_id", "")

    # ── Phase 2 config ────────────────────────────────────────────────────────
    phase2_cfg     = cfg.get("phase2", {})
    mode           = phase2_cfg.get("mode", "observe")
    lookback       = phase2_cfg.get("insight_lookback_cycles", 10)
    conf_threshold = phase2_cfg.get("confidence_threshold", 0.6)
    whitelist      = cfg.get("safe_process_whitelist", ["systemd", "bash", "sshd"])

    # ── In-memory state (persists across cycles, reset on process restart) ────
    mem_context = {
        "pressure_cycles":            0,
        "pressure_cycles_threshold":  cfg["monitor"]["pressure_cycles_threshold"],
        "swap_growth_cycles":         cfg["monitor"]["swap_growth_cycles"],
        "baseline_window_size":       cfg["monitor"]["baseline_window_size"],
        "baseline_deviation_margin":  cfg["monitor"]["baseline_deviation_margin"],
        "swap_history":               [],
        "baseline_window":            [],
        "current_baseline_avg":       None,
    }

    # Repeat offender: {process_name: appearance_count_in_top_N}
    offender_counts: dict = defaultdict(int)

    # Self-awareness counters
    consecutive_failures = 0
    last_swap_mb = None

    sys_log.info('"health monitor started"')

    while True:
        cycle_start = time.monotonic()

        try:
            # ── 1. Collect ────────────────────────────────────────────────────
            metrics = collect(top_procs)

            # ── 2. Swap delta (MB change since last cycle) ────────────────────
            swap_delta = None
            if last_swap_mb is not None:
                swap_delta = round(metrics["swap_used_mb"] - last_swap_mb, 2)
            last_swap_mb = metrics["swap_used_mb"]

            # ── 3. Evaluate thresholds + memory intelligence ──────────────────
            events = evaluate(metrics, thresholds, mem_context)

            # ── 4. Persist threshold/intelligence events to DB ────────────────
            for ev in events:
                try:
                    insert_event(
                        ev["metric"], ev["value"], ev["level"],
                        ev.get("context", ""), ev.get("suggested_action", ""),
                    )
                except Exception as e:
                    mon_log.error(f'"DB insert_event failed: {e}"')
                    _safe_self_log("DB_ERROR", str(e))

            # ── 5. Persist memory trend (every cycle) ─────────────────────────
            try:
                insert_memory_trend(
                    metrics["ram_available_percent"],
                    metrics["swap_used_mb"],
                    swap_delta,
                )
            except Exception as e:
                mon_log.error(f'"DB insert_memory_trend failed: {e}"')

            # ── 6. Persist process snapshot (every cycle) ─────────────────────
            try:
                if metrics["processes"]:
                    insert_process_snapshots(metrics["timestamp"], metrics["processes"])
            except Exception as e:
                mon_log.error(f'"DB insert_process_snapshots failed: {e}"')

            # ── 7. Persist baseline avg (once window is populated) ────────────
            if mem_context.get("current_baseline_avg") is not None:
                try:
                    insert_baseline_metric(mem_context["current_baseline_avg"])
                except Exception as e:
                    mon_log.error(f'"DB insert_baseline failed: {e}"')

            # ── 8. Repeat offender tracking ───────────────────────────────────
            for p in metrics["processes"]:
                offender_counts[p["name"]] += 1
                if offender_counts[p["name"]] == offender_min:
                    name = p["name"]
                    mb = p["memory_mb"]
                    sys_log.warning(
                        f'"repeat_offender process={name} '
                        f'appearances={offender_min} memory_mb={mb}"'
                    )

            # ── 9. State manager → decide which alerts to fire ─────────────────
            actions = process_events(events, cooldown)

            # ── 9a. Insight Engine ────────────────────────────────────────────
            insights = []
            try:
                insights = run_analysis(lookback)
                for ins in insights:
                    ins_type = ins["type"]
                    ins_conf = ins["confidence"]
                    sys_log.info(
                        f'"insight type={ins_type} confidence={ins_conf}"'
                    )
            except Exception as e:
                mon_log.error(f'"insight_engine error: {e}"')
                _safe_self_log("INSIGHT_ERROR", str(e))

            # ── 9b. Decision Engine ───────────────────────────────────────────
            decisions = []
            try:
                decisions = make_decisions(actions, insights, conf_threshold)
            except Exception as e:
                mon_log.error(f'"decision_engine error: {e}"')
                _safe_self_log("DECISION_ERROR", str(e))

            # ── 9c. Action Engine ─────────────────────────────────────────────
            action_results = []
            try:
                action_results = handle_actions(decisions, mode, whitelist, mon_log)
            except Exception as e:
                mon_log.error(f'"action_engine error: {e}"')
                _safe_self_log("ACTION_ERROR", str(e))

            # ── 10. Send Telegram alerts (enhanced) ───────────────────────────
            if actions:
                sent = send_alerts(
                    actions, bot_token, chat_id,
                    metrics["processes"], mon_log,
                    decisions=decisions,
                    action_results=action_results,
                )
                for a in actions:
                    metric = a["metric"]
                    action = a["action"]
                    new_st = a["new_state"]
                    val    = a["value"]
                    sys_log.info(
                        f'"alert metric={metric} action={action} '
                        f'state={new_st} value={val}"'
                    )
                sys_log.info(f'"alerts_sent={sent}/{len(actions)}"')

            # ── 11. Cycle summary log ─────────────────────────────────────────
            loop_ms = round((time.monotonic() - cycle_start) * 1000)
            cpu  = metrics["cpu"]
            ram  = metrics["ram_percent"]
            swap = metrics["swap_percent"]
            disk = metrics["disk"]
            sys_log.info(
                f'"cycle cpu={cpu} ram={ram} swap={swap} disk={disk} '
                f'events={len(events)} loop_ms={loop_ms}"'
            )

            # ── 12. Write decision traces ─────────────────────────────────────
            dec_map = {d["metric"]: d for d in decisions}
            res_map = {r["metric"]: r for r in action_results}
            for a in actions:
                if a["action"] != "alert":
                    continue
                m   = a["metric"]
                dec = dec_map.get(m, {})
                res = res_map.get(m, {})
                try:
                    insert_decision_trace(
                        metric=m,
                        observation=a.get("context", f"{m}={a['value']}"),
                        insight=dec.get("insight_type", "none"),
                        decision=dec.get("cause", "unknown"),
                        action=dec.get("recommended_action", "none"),
                        action_status=res.get("action_status", "none"),
                        confidence=dec.get("confidence", 0.5),
                    )
                except Exception as e:
                    mon_log.error(f'"insert_decision_trace failed: {e}"')

            # Reset failure counter on clean cycle
            consecutive_failures = 0

        except Exception as e:
            consecutive_failures += 1
            mon_log.error(
                f'"main_loop_error={e} consecutive_failures={consecutive_failures}"'
            )
            _safe_self_log("LOOP_ERROR", str(e))

            if consecutive_failures >= stall_limit:
                mon_log.error(
                    f'"stall_detected consecutive_failures={consecutive_failures}'
                    f' — systemd watchdog will restart if configured"'
                )

        time.sleep(interval)


if __name__ == "__main__":
    main()
