import requests
from utils.time_utils import utcnow_iso

METRIC_LABELS = {
    "cpu":                  "CPU",
    "ram":                  "RAM",
    "disk":                 "DISK",
    "swap":                 "SWAP",
    "memory_pressure":      "MEMORY PRESSURE",
    "swap_growth":          "SWAP GROWTH",
    "baseline_deviation":   "RAM BASELINE",
    # Phase 2
    "memory_leak_suspected": "MEMORY LEAK",
    "swap_growth_trend":     "SWAP GROWTH TREND",
    "repeat_offender":       "REPEAT OFFENDER",
}


def _format_processes(processes: list, top_n: int = 5) -> str:
    """Format top N processes as HTML for Telegram."""
    if not processes:
        return ""
    lines = ["\n\n<b>Top Processes:</b>"]
    for i, p in enumerate(processes[:top_n], 1):
        name = p["name"][:20]
        lines.append(
            f"  {i}. <code>{name}</code> [{p['pid']}]"
            f" — {p['memory_mb']:.1f}MB / {p['cpu_percent']:.1f}%CPU"
        )
    return "\n".join(lines)


def _build_message(action: dict, processes: list) -> str:
    """Phase 1 Telegram message format."""
    label = METRIC_LABELS.get(action["metric"], action["metric"].upper())
    ts = utcnow_iso()

    if action["action"] == "recovery":
        value_str = f"{action['value']:.1f}%" if action["value"] is not None else "N/A"
        return (
            f'✅ <b>RECOVERED: {label}</b>\n'
            f'Now: <b>{value_str}</b>\n'
            f'<i>{ts}</i>'
        )

    value_str = f"{action['value']:.1f}%" if action["value"] is not None else "N/A"
    proc_str = _format_processes(processes)
    return (
        f'🚨 <b>{action["new_state"]}: {label}</b>\n'
        f'Value: <b>{value_str}</b>\n'
        f'ℹ️ {action["context"]}\n'
        f'💡 {action["suggested_action"]}'
        f'{proc_str}\n'
        f'<i>{ts}</i>'
    )


def _build_enhanced_message(action: dict, processes: list,
                             decision: dict = None,
                             action_result: dict = None) -> str:
    """Phase 2 enhanced Telegram message with root cause + action status."""
    label = METRIC_LABELS.get(action["metric"], action["metric"].upper())
    ts = utcnow_iso()

    if action["action"] == "recovery":
        val = f"{action['value']:.1f}%" if action["value"] is not None else "N/A"
        return (
            f'✅ <b>RECOVERED: {label}</b>\n'
            f'Now: <b>{val}</b>\n'
            f'<i>{ts}</i>'
        )

    val = f"{action['value']:.1f}%" if action["value"] is not None else "N/A"
    cause = decision.get("cause", "unknown") if decision else "unknown"
    confidence = decision.get("confidence", 0.5) if decision else 0.5
    rec_action = decision.get("recommended_action", "monitor") if decision else "monitor"
    act_status = action_result.get("action_status", "none") if action_result else "none"
    act_detail = action_result.get("result_detail", "") if action_result else ""

    proc_str = _format_processes(processes)

    status_line = {
        "none":      "No action taken (observe mode)",
        "suggested": f"Suggested: {rec_action}",
        "executed":  f"Executed: {act_detail}",
        "failed":    f"Action failed: {act_detail}",
    }.get(act_status, act_status)

    conf_pct = f"{confidence * 100:.0f}%"
    return (
        f'⚠️ <b>{action["new_state"]}: {label}</b>\n'
        f'Value: <b>{val}</b>\n'
        f'🔍 Cause: {cause}\n'
        f'📊 Confidence: {conf_pct}\n'
        f'💡 Suggested: {rec_action}'
        f'{proc_str}\n'
        f'🤖 Status: {status_line}\n'
        f'<i>{ts}</i>'
    )


def send_alerts(actions: list, bot_token: str, chat_id: str,
                processes: list, mon_log,
                decisions: list = None,
                action_results: list = None) -> int:
    """
    Send one Telegram message per action.
    Phase 2: uses enhanced format when decisions provided.
    Backward-compatible: decisions=None falls back to Phase 1 format.
    Returns count of successfully sent messages.
    Never raises — all failures are logged to mon_log.
    """
    if not bot_token or not chat_id:
        mon_log.warning('"Telegram credentials missing — alerts skipped"')
        return 0

    # Build lookup maps if Phase 2 data provided
    dec_map = {d["metric"]: d for d in decisions} if decisions else {}
    res_map = {r["metric"]: r for r in action_results} if action_results else {}

    sent = 0
    for action in actions:
        metric = action["metric"]
        if dec_map:
            msg = _build_enhanced_message(
                action, processes,
                decision=dec_map.get(metric),
                action_result=res_map.get(metric),
            )
        else:
            msg = _build_message(action, processes)

        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"},
                timeout=10,
            )
            if resp.ok:
                sent += 1
            else:
                mon_log.error(
                    f'"Telegram API error: status={resp.status_code}"'
                )
        except Exception as e:
            mon_log.error(f'"Telegram send failed: {e}"')
    return sent
