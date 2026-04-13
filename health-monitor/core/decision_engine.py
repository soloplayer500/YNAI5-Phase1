def make_decisions(actions: list, insights: list,
                   confidence_threshold: float = 0.6) -> list:
    """
    Map state_manager actions + insight_engine insights into structured decisions.

    Returns list of decision dicts:
    {
        metric, issue, cause, confidence,
        recommended_action, process_target,
        insight_type,
        action_dict,   # original state_manager action
    }
    """
    decisions = []
    insight_map = {i["type"]: i for i in insights}

    for action in actions:
        if action["action"] not in ("alert", "recovery"):
            continue
        decision = _build_decision(action["metric"], action, insight_map,
                                   confidence_threshold)
        decisions.append(decision)

    return decisions


def _build_decision(metric: str, action: dict, insight_map: dict,
                    threshold: float) -> dict:
    """Build a single decision dict from one state_manager action."""
    base = {
        "metric": metric,
        "issue": metric,
        "cause": "unknown",
        "confidence": 0.5,
        "recommended_action": "monitor",
        "process_target": None,
        "insight_type": None,
        "action_dict": action,
    }

    if action["action"] == "recovery":
        base["issue"] = f"{metric}_recovered"
        base["cause"] = "condition resolved"
        base["recommended_action"] = "none"
        base["confidence"] = 1.0
        return base

    # Map metric to cause using insights
    if metric in ("ram", "memory_pressure", "baseline_deviation"):
        leak = insight_map.get("memory_leak_suspected")
        offender = insight_map.get("repeat_offender")

        if leak and leak["confidence"] >= threshold:
            base["insight_type"] = "memory_leak_suspected"
            base["confidence"] = leak["confidence"]
            if offender and offender["process_name"]:
                base["cause"] = (
                    f"possible memory leak — {offender['process_name']} is top consumer"
                )
                base["process_target"] = offender["process_name"]
                base["recommended_action"] = "restart_process"
            else:
                base["cause"] = "memory leak suspected — unknown process"
                base["recommended_action"] = "investigate_top_processes"

        elif offender and offender["confidence"] >= threshold:
            base["insight_type"] = "repeat_offender"
            base["confidence"] = offender["confidence"]
            base["cause"] = (
                f"{offender['process_name']} repeatedly consuming high RAM"
            )
            base["process_target"] = offender["process_name"]
            base["recommended_action"] = "renice_process"

        else:
            base["cause"] = "high RAM usage — no specific pattern detected"
            base["recommended_action"] = "monitor_top_processes"

    elif metric in ("swap", "swap_growth"):
        growth = insight_map.get("swap_growth_trend")
        if growth and growth["confidence"] >= threshold:
            base["insight_type"] = "swap_growth_trend"
            base["confidence"] = growth["confidence"]
            total = growth["evidence"]["total_growth_mb"]
            base["cause"] = f"swap growing steadily ({total:.0f}MB)"
            base["recommended_action"] = "free_memory"
        else:
            base["cause"] = "swap usage high"
            base["recommended_action"] = "monitor_memory"

    elif metric == "cpu":
        base["cause"] = "CPU usage spike"
        base["recommended_action"] = "identify_cpu_process"

    elif metric == "disk":
        base["cause"] = "disk space low"
        base["recommended_action"] = "check_disk_usage"

    return base
