from storage.db import get_connection
from utils.time_utils import utcnow_iso


def daily_summary() -> str:
    """
    Generate a plain-text 24h health summary.
    No scheduling — call on demand (e.g., piped to Telegram or logged).
    """
    with get_connection() as conn:
        # Alerts fired per metric in the last 24h
        alert_counts = conn.execute("""
            SELECT metric, COUNT(*) AS count
            FROM alerts_sent
            WHERE timestamp >= datetime('now', '-1 day')
            GROUP BY metric
            ORDER BY count DESC
        """).fetchall()

        # Alert windows (first→last trigger per metric)
        alert_windows = conn.execute("""
            SELECT metric,
                   MIN(timestamp) AS first_alert,
                   MAX(timestamp) AS last_alert
            FROM alerts_sent
            WHERE type = 'trigger'
              AND timestamp >= datetime('now', '-1 day')
            GROUP BY metric
        """).fetchall()

        # Top memory offenders (appeared most in top-3 per cycle)
        top_offenders = conn.execute("""
            SELECT process_name,
                   COUNT(*)      AS appearances,
                   MAX(memory_mb) AS peak_mb
            FROM process_snapshots
            WHERE timestamp >= datetime('now', '-1 day')
              AND rank <= 3
            GROUP BY process_name
            ORDER BY appearances DESC
            LIMIT 5
        """).fetchall()

        # Average available RAM over 24h (from baseline_metrics)
        baseline_row = conn.execute("""
            SELECT AVG(avg_available_ram) AS avg
            FROM baseline_metrics
            WHERE timestamp >= datetime('now', '-1 day')
        """).fetchone()

        # Memory trend: min available RAM (worst point)
        worst_ram = conn.execute("""
            SELECT MIN(available_ram_percent) AS worst,
                   MAX(swap_used_mb)          AS peak_swap
            FROM memory_trends
            WHERE timestamp >= datetime('now', '-1 day')
        """).fetchone()

        # Phase 2: Decision trace summary
        traces = conn.execute("""
            SELECT metric, insight, action_status, COUNT(*) AS count
            FROM decision_trace
            WHERE timestamp >= datetime('now', '-1 day')
            GROUP BY metric, insight, action_status
            ORDER BY count DESC
        """).fetchall()

        # Phase 2: Action effectiveness
        outcomes = conn.execute("""
            SELECT action_status, result, COUNT(*) AS count
            FROM decision_trace
            WHERE timestamp >= datetime('now', '-1 day')
            GROUP BY action_status, result
        """).fetchall()

    lines = [
        "=== Daily Health Summary ===",
        f"Generated: {utcnow_iso()}",
        "",
    ]

    # Alert counts
    if alert_counts:
        lines.append("Alerts fired (24h):")
        for r in alert_counts:
            lines.append(f"  {r['metric'].upper()}: {r['count']} alert(s)")
    else:
        lines.append("No alerts in the last 24 hours.")

    # Alert time windows
    if alert_windows:
        lines.append("\nAlert windows:")
        for d in alert_windows:
            lines.append(
                f"  {d['metric'].upper()}: {d['first_alert']} -> {d['last_alert']}"
            )

    # Memory stats
    if worst_ram and worst_ram["worst"] is not None:
        lines.append(
            f"\nMemory (24h): worst available={worst_ram['worst']:.1f}% "
            f"| peak swap={worst_ram['peak_swap']:.1f}MB"
        )

    if baseline_row and baseline_row["avg"] is not None:
        lines.append(f"RAM baseline avg (24h): {baseline_row['avg']:.1f}% available")

    # Top memory offenders
    if top_offenders:
        lines.append("\nTop memory offenders (24h):")
        for o in top_offenders:
            lines.append(
                f"  {o['process_name']}: {o['appearances']}x in top-3, "
                f"peak {o['peak_mb']:.1f}MB"
            )

    # Phase 2: Intelligence section
    lines.append("\n=== Phase 2 Intelligence ===")

    if traces:
        lines.append("Decision traces (24h):")
        for t in traces:
            insight_label = t["insight"] or "none"
            lines.append(
                f"  {t['metric'].upper()}: {insight_label} → "
                f"{t['action_status']} ({t['count']}x)"
            )
    else:
        lines.append("No decision traces in the last 24 hours.")

    if outcomes:
        lines.append("\nAction outcomes:")
        for o in outcomes:
            lines.append(
                f"  {o['action_status']}/{o['result']}: {o['count']}"
            )

    return "\n".join(lines)
