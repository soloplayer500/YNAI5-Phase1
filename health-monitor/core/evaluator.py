def evaluate(metrics: dict, thresholds: dict, mem_context: dict) -> list:
    """
    Evaluate metrics against thresholds and memory intelligence.

    mem_context (mutated in place across cycles by main loop):
        pressure_cycles: int         — consecutive cycles with low available RAM
        swap_history: list[float]    — recent swap_used_mb values (last N)
        baseline_window: list[float] — recent ram_available_percent values
        current_baseline_avg: float  — set here, read by main loop for DB persist

    Returns list of event dicts:
        {metric, value, level, context, suggested_action}
    """
    events = []

    # ── 1. Basic threshold checks (cpu, ram, disk, swap) ─────────────────────
    for metric, key, val_key in [
        ("cpu",  "cpu",  "cpu"),
        ("ram",  "ram",  "ram_percent"),
        ("disk", "disk", "disk"),
    ]:
        value = metrics[val_key]
        warn = thresholds[key]["warning"]
        crit = thresholds[key]["critical"]
        if value >= crit:
            events.append(_event(
                metric, value, "CRITICAL",
                f"{metric.upper()} at {value:.1f}% exceeds critical threshold {crit}%",
                f"Investigate top processes consuming {metric.upper()}",
            ))
        elif value >= warn:
            events.append(_event(
                metric, value, "WARNING",
                f"{metric.upper()} at {value:.1f}% exceeds warning threshold {warn}%",
                f"Monitor {metric.upper()} — approaching critical",
            ))

    # Swap threshold
    swap_val = metrics["swap_percent"]
    sw_warn = thresholds["swap"]["warning"]
    sw_crit = thresholds["swap"]["critical"]
    if swap_val >= sw_crit:
        events.append(_event(
            "swap", swap_val, "CRITICAL",
            f"Swap at {swap_val:.1f}% — system under severe memory pressure",
            "Free RAM immediately — identify memory leaks",
        ))
    elif swap_val >= sw_warn:
        events.append(_event(
            "swap", swap_val, "WARNING",
            f"Swap at {swap_val:.1f}% — RAM pressure growing",
            "Monitor memory usage trend",
        ))

    # ── 2. Memory Pressure (sustained low available RAM for N cycles) ─────────
    avail = metrics["ram_available_percent"]
    pressure_threshold = 20.0  # available RAM % below this = pressure

    if avail < pressure_threshold:
        mem_context["pressure_cycles"] = mem_context.get("pressure_cycles", 0) + 1
    else:
        mem_context["pressure_cycles"] = 0

    n_pressure = mem_context.get("pressure_cycles_threshold", 3)
    if mem_context["pressure_cycles"] >= n_pressure:
        events.append(_event(
            "memory_pressure", avail, "WARNING",
            f"RAM available {avail:.1f}% for {mem_context['pressure_cycles']} consecutive cycles",
            "Check for memory leaks or reduce running services",
        ))

    # ── 3. Swap Growth (continuously increasing across N cycles) ─────────────
    swap_history = mem_context.setdefault("swap_history", [])
    swap_history.append(metrics["swap_used_mb"])
    n_swap = mem_context.get("swap_growth_cycles", 3)
    # Keep only what we need (n_swap + a small buffer)
    if len(swap_history) > n_swap + 2:
        swap_history.pop(0)

    if len(swap_history) >= n_swap:
        recent = swap_history[-n_swap:]
        if all(recent[i] < recent[i + 1] for i in range(len(recent) - 1)):
            delta = recent[-1] - recent[0]
            events.append(_event(
                "swap_growth", metrics["swap_used_mb"], "WARNING",
                f"Swap growing +{delta:.1f}MB over {n_swap} cycles",
                "Identify processes leaking memory",
            ))

    # ── 4. Baseline Deviation (rolling average vs current) ───────────────────
    baseline_window = mem_context.setdefault("baseline_window", [])
    baseline_window.append(avail)
    window_size = mem_context.get("baseline_window_size", 20)
    if len(baseline_window) > window_size:
        baseline_window.pop(0)

    if len(baseline_window) >= 5:  # minimum samples before comparing
        avg = sum(baseline_window) / len(baseline_window)
        margin = mem_context.get("baseline_deviation_margin", 15.0)
        deviation = avg - avail   # positive = RAM dropped below baseline
        if deviation > margin:
            events.append(_event(
                "baseline_deviation", avail, "WARNING",
                f"RAM available {avail:.1f}% is {deviation:.1f}% below baseline avg {avg:.1f}%",
                "Unusual memory drop — investigate recent process changes",
            ))
        # Expose current avg for the main loop to persist to DB
        mem_context["current_baseline_avg"] = round(avg, 2)

    return events


def _event(metric: str, value: float, level: str,
           context: str = "", suggested_action: str = "") -> dict:
    return {
        "metric": metric,
        "value": value,
        "level": level,
        "context": context,
        "suggested_action": suggested_action,
    }
