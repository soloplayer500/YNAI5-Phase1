import psutil
from datetime import datetime, timezone


def collect(top_n: int = 10, disk_path: str = "/") -> dict:
    """
    Collect system metrics and top-N processes by RSS memory.
    disk_path: "/" for Linux/Ubuntu, "C:\\" for Windows.
    Returns structured dict. Raises on psutil failure (caller handles).
    """
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()
    cpu = psutil.cpu_percent(interval=1)
    disk = psutil.disk_usage(disk_path).percent

    # Top N processes by RSS
    processes = []
    try:
        procs = []
        for p in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent"]):
            try:
                info = p.info
                rss_mb = info["memory_info"].rss / (1024 * 1024) if info["memory_info"] else 0
                procs.append({
                    "pid": info["pid"],
                    "name": info["name"] or "unknown",
                    "memory_mb": round(rss_mb, 2),
                    "cpu_percent": info["cpu_percent"] or 0.0,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        procs.sort(key=lambda x: x["memory_mb"], reverse=True)
        processes = procs[:top_n]
    except Exception:
        processes = []

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "cpu": cpu,
        "ram_percent": vm.percent,
        "ram_available_percent": round(100 * vm.available / vm.total, 2),
        "ram_used_mb": round(vm.used / (1024 * 1024), 1),
        "ram_total_mb": round(vm.total / (1024 * 1024), 1),
        "swap_percent": sw.percent,
        "swap_used_mb": round(sw.used / (1024 * 1024), 1),
        "disk": disk,
        "processes": processes,
    }
