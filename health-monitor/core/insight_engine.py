from collections import Counter

from storage.db import get_connection


def run_analysis(lookback: int = 10) -> list:
    """
    Analyze recent DB data to detect memory patterns.
    Returns list of insight dicts: {type, confidence, evidence, process_name}
    Called once per cycle — reads only the last N rows (lightweight).
    """
    insights = []
    insights.extend(_detect_memory_leak(lookback))
    insights.extend(_detect_swap_growth(lookback))
    insights.extend(_detect_repeat_offenders(lookback))
    return insights


def _detect_memory_leak(lookback: int) -> list:
    """
    Suspect memory leak if available RAM has been declining steadily
    across the last N cycles (monotonically decreasing trend).
    Confidence scales with slope magnitude.
    """
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT available_ram_percent FROM memory_trends "
            "ORDER BY id DESC LIMIT ?",
            (lookback,),
        ).fetchall()

    if len(rows) < 5:
        return []

    # Rows come back newest-first; reverse to chronological order
    values = [r["available_ram_percent"] for r in reversed(rows)]

    # Count consecutive decreases
    drops = sum(1 for i in range(len(values) - 1) if values[i] > values[i + 1])
    drop_ratio = drops / (len(values) - 1)

    # Slope: total drop over window
    slope = (values[0] - values[-1]) / len(values)  # % per cycle

    if drop_ratio >= 0.7 and slope > 0.5:
        confidence = min(0.95, 0.5 + drop_ratio * 0.3 + min(slope / 10, 0.2))
        return [{
            "type": "memory_leak_suspected",
            "confidence": round(confidence, 2),
            "evidence": {
                "drop_ratio": round(drop_ratio, 2),
                "slope_per_cycle": round(slope, 2),
                "samples": len(values),
                "start_avail": round(values[0], 1),
                "end_avail": round(values[-1], 1),
            },
            "process_name": None,
        }]
    return []


def _detect_swap_growth(lookback: int) -> list:
    """
    Detect if swap is consistently growing across recent cycles.
    """
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT swap_used_mb, swap_delta_mb FROM memory_trends "
            "ORDER BY id DESC LIMIT ?",
            (lookback,),
        ).fetchall()

    if len(rows) < 3:
        return []

    # Filter rows with valid delta
    deltas = [r["swap_delta_mb"] for r in rows if r["swap_delta_mb"] is not None]
    if len(deltas) < 3:
        return []

    positive = sum(1 for d in deltas if d > 0)
    ratio = positive / len(deltas)
    total_growth = sum(d for d in deltas if d > 0)

    if ratio >= 0.7 and total_growth > 50:
        confidence = min(0.90, 0.4 + ratio * 0.3 + min(total_growth / 500, 0.2))
        return [{
            "type": "swap_growth_trend",
            "confidence": round(confidence, 2),
            "evidence": {
                "positive_ratio": round(ratio, 2),
                "total_growth_mb": round(total_growth, 1),
                "samples": len(deltas),
            },
            "process_name": None,
        }]
    return []


def _detect_repeat_offenders(lookback: int) -> list:
    """
    Find processes that repeatedly appear in the top-3 memory consumers.
    Returns one insight per offender with high recurrence.
    """
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT process_name, COUNT(*) AS appearances, AVG(memory_mb) AS avg_mb
            FROM process_snapshots
            WHERE rank <= 3
            ORDER BY id DESC
            LIMIT ?
            """,
            (lookback * 3,),  # top-3 per cycle × N cycles
        ).fetchall()

    counts: Counter = Counter()
    avg_mb: dict = {}
    for r in rows:
        counts[r["process_name"]] += r["appearances"]
        avg_mb[r["process_name"]] = round(r["avg_mb"], 1)

    insights = []
    for name, count in counts.most_common(3):
        if count >= max(3, lookback // 2):
            confidence = min(0.85, 0.4 + min(count / lookback, 0.5))
            insights.append({
                "type": "repeat_offender",
                "confidence": round(confidence, 2),
                "evidence": {
                    "appearances": count,
                    "avg_memory_mb": avg_mb.get(name, 0),
                    "lookback_cycles": lookback,
                },
                "process_name": name,
            })
    return insights
