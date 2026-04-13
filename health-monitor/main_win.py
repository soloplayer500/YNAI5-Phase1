"""
Windows Laptop Health Monitor — Persistent Background Daemon
- Emergency-only Telegram alerts (CRITICAL threshold only, max 1/hr per metric)
- Persistent killer: memory hogs terminated every cycle and suppressed if they return
- Runs silently via pythonw.exe — no console window
- watcher.vbs + Task Scheduler keeps it alive 24/7 even after Claude crashes

Usage: pythonw main_win.py
Logs:  health-monitor/logs/win_monitor.log
"""
import sys
import time
import signal
from pathlib import Path
from collections import defaultdict

import psutil
import yaml
import requests

BASE = Path(__file__).parent

# ── .env.local search ────────────────────────────────────────────────────────
_ENV_CANDIDATES = [
    Path("C:/Users/shema/OneDrive/Desktop/YNAI5-SU/.env.local"),
    BASE.parent / ".env.local",
    BASE / ".env.local",
]


def _load_env() -> dict:
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


def _load_config() -> dict:
    with open(BASE / "config_win.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Logging (file-only — no stdout, runs headless) ───────────────────────────
import logging
from logging.handlers import RotatingFileHandler

def _get_logger(log_path: Path) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("win_monitor")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%SZ",
        ))
        logger.addHandler(handler)
    return logger


# ── Telegram ──────────────────────────────────────────────────────────────────
def _send_telegram(bot_token: str, chat_id: str, msg: str, log) -> bool:
    if not bot_token or not chat_id:
        return False
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"},
            timeout=10,
        )
        return resp.ok
    except Exception as e:
        log.error(f"Telegram send failed: {e}")
        return False


# ── Metrics collection ────────────────────────────────────────────────────────
def _collect(disk_path: str, top_n: int) -> dict:
    vm  = psutil.virtual_memory()
    sw  = psutil.swap_memory()
    cpu = psutil.cpu_percent(interval=1)
    try:
        disk = psutil.disk_usage(disk_path).percent
    except Exception:
        disk = 0.0

    procs = []
    for p in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent"]):
        try:
            info = p.info
            rss_mb = info["memory_info"].rss / (1024 * 1024) if info["memory_info"] else 0
            procs.append({
                "pid":  info["pid"],
                "name": info["name"] or "unknown",
                "memory_mb":   round(rss_mb, 2),
                "cpu_percent": info["cpu_percent"] or 0.0,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs.sort(key=lambda x: x["memory_mb"], reverse=True)

    return {
        "cpu":                  cpu,
        "ram_percent":          vm.percent,
        "ram_available_mb":     round(vm.available / (1024 * 1024), 1),
        "ram_total_mb":         round(vm.total / (1024 * 1024), 1),
        "swap_percent":         sw.percent,
        "disk":                 disk,
        "processes":            procs[:top_n],
    }


# ── Process killer ────────────────────────────────────────────────────────────
def _kill_process(pid: int, name: str, log) -> bool:
    """Terminate a process by PID. Returns True if successful."""
    try:
        p = psutil.Process(pid)
        p.terminate()
        log.warning(f"KILLED {name} pid={pid} (SIGTERM)")
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        log.error(f"Kill failed {name} pid={pid}: {e}")
        return False


def _run_killer(processes: list, killer_cfg: dict,
                kill_counts: dict, log) -> list:
    """
    Check all processes against kill rules.
    Returns list of killed {name, pid, memory_mb, reason} dicts.
    """
    if not killer_cfg.get("enabled", False):
        return []

    whitelist       = set(killer_cfg.get("whitelist", []))
    static_targets  = set(killer_cfg.get("static_targets", []))
    threshold_mb    = killer_cfg.get("kill_threshold_mb", 1200)
    max_per_cycle   = killer_cfg.get("max_kills_per_cycle", 2)

    killed = []
    for p in processes:
        if len(killed) >= max_per_cycle:
            break
        name = p["name"]
        pid  = p["pid"]
        mb   = p["memory_mb"]

        if name in whitelist:
            continue

        reason = None
        if name in static_targets:
            reason = f"static_target"
        elif mb >= threshold_mb:
            reason = f"memory={mb:.0f}MB > {threshold_mb}MB limit"

        if reason:
            if _kill_process(pid, name, log):
                kill_counts[name] += 1
                killed.append({
                    "name": name, "pid": pid,
                    "memory_mb": mb, "reason": reason,
                    "total_kills": kill_counts[name],
                })

    return killed


# ── Alert state (in-memory cooldown) ─────────────────────────────────────────
class AlertState:
    def __init__(self, cooldown_minutes: float):
        self._cooldown = cooldown_minutes * 60
        self._last_sent: dict = {}

    def should_alert(self, metric: str) -> bool:
        last = self._last_sent.get(metric, 0)
        return (time.monotonic() - last) >= self._cooldown

    def record(self, metric: str):
        self._last_sent[metric] = time.monotonic()


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    cfg     = _load_config()
    env     = _load_env()
    mon_cfg = cfg["monitor"]
    thr     = cfg["thresholds"]
    killer  = cfg.get("killer", {})
    log_cfg = cfg.get("logging", {})

    log = _get_logger(BASE / log_cfg.get("win_log", "logs/win_monitor.log"))

    bot_token = env.get("TELEGRAM_BOT_TOKEN") or cfg["telegram"].get("bot_token", "")
    chat_id   = env.get("TELEGRAM_CHAT_ID")   or cfg["telegram"].get("chat_id", "")

    disk_path    = cfg.get("disk_path", "C:\\")
    interval     = mon_cfg.get("interval_seconds", 30)
    cooldown_min = mon_cfg.get("cooldown_minutes", 60)
    top_procs    = mon_cfg.get("top_processes", 10)

    alert_state = AlertState(cooldown_min)
    kill_counts: dict = defaultdict(int)   # name → total kills this session

    log.info("=== Windows Health Monitor started ===")
    log.info(f"disk_path={disk_path} interval={interval}s cooldown={cooldown_min}min")
    log.info(f"killer={'enabled' if killer.get('enabled') else 'disabled'} "
             f"threshold={killer.get('kill_threshold_mb', 'N/A')}MB")

    consecutive_failures = 0

    while True:
        try:
            metrics = _collect(disk_path, top_procs)

            cpu  = metrics["cpu"]
            ram  = metrics["ram_percent"]
            swap = metrics["swap_percent"]
            disk = metrics["disk"]

            log.debug(
                f"cpu={cpu:.1f}% ram={ram:.1f}% "
                f"swap={swap:.1f}% disk={disk:.1f}%"
            )

            # ── 1. Persistent killer ──────────────────────────────────────────
            killed = _run_killer(metrics["processes"], killer, kill_counts, log)

            if killed:
                summary = ", ".join(
                    f"{k['name']}({k['memory_mb']:.0f}MB)" for k in killed
                )
                log.warning(f"Killed {len(killed)} process(es): {summary}")

                # Telegram for every kill (with its own cooldown)
                if alert_state.should_alert("killer") and bot_token:
                    lines = ["🔪 <b>AUTO-KILL: Memory Hogs Terminated</b>"]
                    for k in killed:
                        lines.append(
                            f"  • <code>{k['name']}</code> [{k['pid']}] "
                            f"— {k['memory_mb']:.0f}MB ({k['reason']}) "
                            f"[killed {k['total_kills']}x this session]"
                        )
                    lines.append(f"RAM now: <b>{ram:.1f}%</b>")
                    _send_telegram(bot_token, chat_id, "\n".join(lines), log)
                    alert_state.record("killer")

            # ── 2. Emergency threshold alerts (CRITICAL only) ─────────────────
            emergencies = []

            if cpu >= thr["cpu"]["critical"]:
                emergencies.append(("cpu", cpu, "CPU"))
            if ram >= thr["ram"]["critical"]:
                emergencies.append(("ram", ram, "RAM"))
            if disk >= thr["disk"]["critical"]:
                emergencies.append(("disk", disk, "DISK"))
            if swap >= thr["swap"]["critical"]:
                emergencies.append(("swap", swap, "SWAP"))

            for metric, value, label in emergencies:
                if alert_state.should_alert(metric):
                    # Top 3 processes for context
                    top3 = metrics["processes"][:3]
                    proc_lines = "\n".join(
                        f"  {i+1}. <code>{p['name']}</code> "
                        f"— {p['memory_mb']:.0f}MB / {p['cpu_percent']:.1f}%CPU"
                        for i, p in enumerate(top3)
                    )
                    msg = (
                        f"🚨 <b>EMERGENCY: {label} CRITICAL</b>\n"
                        f"Value: <b>{value:.1f}%</b>\n"
                        f"RAM free: {metrics['ram_available_mb']:.0f}MB\n"
                        f"\n<b>Top Processes:</b>\n{proc_lines}"
                    )
                    ok = _send_telegram(bot_token, chat_id, msg, log)
                    if ok:
                        alert_state.record(metric)
                        log.warning(f"EMERGENCY alert sent: {label}={value:.1f}%")

            consecutive_failures = 0

        except Exception as e:
            consecutive_failures += 1
            log.error(f"Loop error (#{consecutive_failures}): {e}")

        time.sleep(interval)


if __name__ == "__main__":
    main()
