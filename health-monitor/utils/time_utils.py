from datetime import datetime, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def utcnow_iso() -> str:
    return utcnow().isoformat()


def minutes_since(iso_str: str) -> float:
    """
    Returns minutes elapsed since iso_str (UTC ISO format).
    Returns inf if iso_str is None or empty — treats as never alerted.
    """
    if not iso_str:
        return float("inf")
    past = datetime.fromisoformat(iso_str)
    if past.tzinfo is None:
        past = past.replace(tzinfo=timezone.utc)
    return (utcnow() - past).total_seconds() / 60
