#!/usr/bin/env python3
"""
YNAI5 System Health Check — Parallel diagnostics engine.
Usage:
    python health-check.py           — full diagnostics
    python health-check.py --telegram — full + send to Telegram
    python health-check.py --quick   — RAM, disk, internet only
"""

import sys
import os
import subprocess
import time
import socket
import winreg
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import psutil
except ImportError:
    print("ERROR: psutil not installed. Run: pip install psutil")
    sys.exit(1)

# ── Paths ────────────────────────────────────────────────────────────────────
WORKSPACE = Path("C:/Users/shema/OneDrive/Desktop/YNAI5-SU")
ENV_FILE = WORKSPACE / ".env.local"
LOG_DIR = WORKSPACE / "projects/system-health/logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── Thresholds ────────────────────────────────────────────────────────────────
RAM_WARN = 80
CPU_WARN = 85
DISK_WARN = 85
SWAP_WARN = 50

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def status_icon(value, threshold, invert=False):
    """Return ✅ / ⚠️ based on threshold. invert=True means high is good."""
    if invert:
        return "✅" if value >= threshold else "⚠️"
    return "⚠️" if value >= threshold else "✅"


# ── Check Functions ───────────────────────────────────────────────────────────

def check_ram():
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()

    total_gb = vm.total / 1024**3
    used_gb = vm.used / 1024**3
    avail_gb = vm.available / 1024**3
    ram_pct = vm.percent
    swap_pct = sw.percent

    ram_icon = status_icon(ram_pct, RAM_WARN)
    swap_icon = "⚠️" if swap_pct >= SWAP_WARN else "✅"

    # Top 5 memory processes
    procs = []
    for p in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            procs.append((p.info["memory_percent"], p.info["pid"], p.info["name"]))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    top5 = sorted(procs, reverse=True)[:5]

    lines = [
        "## RAM",
        f"  Total:     {total_gb:.1f} GB",
        f"  Used:      {used_gb:.1f} GB ({ram_pct:.1f}%) {ram_icon}",
        f"  Available: {avail_gb:.1f} GB",
        f"  Swap:      {sw.used / 1024**3:.1f} / {sw.total / 1024**3:.1f} GB ({swap_pct:.1f}%) {swap_icon}",
        "  Top 5 by memory:",
    ]
    for pct, pid, name in top5:
        lines.append(f"    [{pid}] {name:<30s} {pct:.1f}%")

    alerts = []
    if ram_pct >= RAM_WARN:
        alerts.append(f"RAM at {ram_pct:.1f}% — HIGH")
    if swap_pct >= SWAP_WARN:
        alerts.append(f"SWAP at {swap_pct:.1f}% — SWAP HIGH (crash risk)")

    return "\n".join(lines), alerts, top5


def check_cpu():
    cpu_pct = psutil.cpu_percent(interval=1)
    freq = psutil.cpu_freq()
    cores = psutil.cpu_count(logical=True)
    phys = psutil.cpu_count(logical=False)

    cpu_icon = status_icon(cpu_pct, CPU_WARN)
    freq_mhz = f"{freq.current:.0f} MHz" if freq else "N/A"

    lines = [
        "## CPU",
        f"  Usage:   {cpu_pct:.1f}% {cpu_icon}",
        f"  Freq:    {freq_mhz}",
        f"  Cores:   {phys} physical / {cores} logical",
    ]

    alerts = []
    if cpu_pct >= CPU_WARN:
        alerts.append(f"CPU at {cpu_pct:.1f}% — HIGH")

    return "\n".join(lines), alerts


def check_disk():
    disk = psutil.disk_usage("C:\\")
    total_gb = disk.total / 1024**3
    used_gb = disk.used / 1024**3
    free_gb = disk.free / 1024**3
    pct = disk.percent

    disk_icon = status_icon(pct, DISK_WARN)

    lines = [
        "## Disk (C:)",
        f"  Total: {total_gb:.1f} GB",
        f"  Used:  {used_gb:.1f} GB ({pct:.1f}%) {disk_icon}",
        f"  Free:  {free_gb:.1f} GB",
    ]

    alerts = []
    if pct >= DISK_WARN:
        alerts.append(f"Disk C: at {pct:.1f}% — LOW SPACE")

    return "\n".join(lines), alerts, free_gb


def check_internet():
    results = []
    targets = [("Cloudflare", "1.1.1.1", 53), ("Google", "8.8.8.8", 53)]

    for name, host, port in targets:
        try:
            start = time.time()
            sock = socket.create_connection((host, port), timeout=3)
            sock.close()
            ms = (time.time() - start) * 1000
            results.append((name, ms, True))
        except Exception:
            results.append((name, None, False))

    lines = ["## Internet"]
    all_ok = True
    for name, ms, ok in results:
        if ok:
            icon = "✅" if ms < 150 else "⚠️"
            lines.append(f"  {name}: {ms:.0f}ms {icon}")
        else:
            lines.append(f"  {name}: ❌ UNREACHABLE")
            all_ok = False

    alerts = [] if all_ok else ["Internet connectivity issue detected"]
    return "\n".join(lines), alerts


def check_docker():
    try:
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True, text=True, timeout=8
        )
        if result.returncode == 0:
            lines_out = [l for l in result.stdout.strip().splitlines() if l]
            container_count = max(0, len(lines_out) - 1)  # subtract header
            lines = [
                "## Docker",
                f"  Status:     ✅ Running",
                f"  Containers: {container_count} active",
            ]
            if container_count > 0:
                for c in lines_out[1:]:
                    name_part = c.split()[-1] if c.split() else c
                    lines.append(f"    - {name_part}")
            return "\n".join(lines), []
        else:
            return "## Docker\n  Status: ⚠️ Not responding (daemon may be stopped)", []
    except FileNotFoundError:
        return "## Docker\n  Status: ⚪ Not installed", []
    except subprocess.TimeoutExpired:
        return "## Docker\n  Status: ⚠️ Timeout (Docker may be starting)", []
    except Exception as e:
        return f"## Docker\n  Status: ❌ Error — {e}", []


def check_python_procs():
    procs = []
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if p.info["name"] and "python" in p.info["name"].lower():
                cmd = p.info["cmdline"] or []
                cmd_str = " ".join(cmd)
                procs.append((p.info["pid"], cmd_str))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    lines = ["## Python Processes", f"  Count: {len(procs)}"]
    if procs:
        lines.append("  Top 5:")
        for pid, cmd in procs[:5]:
            snippet = cmd[:60] if len(cmd) > 60 else cmd
            lines.append(f"    [{pid}] {snippet}")

    return "\n".join(lines), []


def check_startup_apps():
    count = 0
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
        while True:
            try:
                winreg.EnumValue(key, count)
                count += 1
            except OSError:
                break
        winreg.CloseKey(key)
    except Exception:
        pass

    icon = "✅" if count <= 5 else "⚠️"
    lines = [
        "## Startup Apps (HKCU Run)",
        f"  Count: {count} {icon}",
    ]
    return "\n".join(lines), []


# ── Recommendations ───────────────────────────────────────────────────────────

def build_recommendations(all_alerts, top_ram_procs, free_disk_gb):
    recs = []

    if any("RAM" in a for a in all_alerts):
        recs.append("RAM HIGH: Close heavy apps. Top memory hogs:")
        for pct, pid, name in top_ram_procs[:3]:
            recs.append(f"    Kill [{pid}] {name} ({pct:.1f}%) — taskkill /PID {pid} /F")

    if any("SWAP" in a for a in all_alerts):
        recs.append("SWAP HIGH (crash risk): Restart PC or kill ALL non-essential processes immediately.")

    if any("CPU" in a for a in all_alerts):
        recs.append("CPU HIGH: Check Task Manager. Let current task finish before starting new ones.")

    if any("Disk" in a for a in all_alerts):
        recs.append("DISK LOW: Run cleanup:")
        recs.append("    del /Q /F /S %TEMP%\\*")
        recs.append("    cleanmgr /d C: /sagerun:1")

    if any("Internet" in a for a in all_alerts):
        recs.append("INTERNET: Check Wi-Fi connection. Restart router if needed.")

    if not recs:
        recs.append("All systems nominal. No action needed.")

    return recs


# ── Report Builder ────────────────────────────────────────────────────────────

def build_report(results: dict, all_alerts: list, top_ram_procs, free_disk_gb) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# YNAI5 System Health Report",
        f"Generated: {ts}",
        "",
    ]

    if all_alerts:
        lines.append("## ⚠️ ALERTS")
        for a in all_alerts:
            lines.append(f"  - {a}")
        lines.append("")

    for key in ["ram", "cpu", "disk", "internet", "docker", "python", "startup"]:
        if key in results:
            lines.append(results[key])
            lines.append("")

    lines.append("## Recommendations")
    recs = build_recommendations(all_alerts, top_ram_procs, free_disk_gb)
    for r in recs:
        lines.append(f"  {r}")

    return "\n".join(lines)


# ── Telegram ──────────────────────────────────────────────────────────────────

def send_telegram(report: str, env: dict):
    token = env.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = env.get("TELEGRAM_CHAT_ID", "")

    if not token or not chat_id:
        print("[Telegram] Missing credentials in .env.local")
        return

    try:
        import urllib.request
        import urllib.parse
        import json

        # Telegram max message = 4096 chars
        msg = report[:4000]
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "",
        }).encode()

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            if result.get("ok"):
                print("[Telegram] ✅ Report sent")
            else:
                print(f"[Telegram] ❌ Failed: {result}")
    except Exception as e:
        print(f"[Telegram] ❌ Error: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Force UTF-8 console output on Windows to handle emoji/unicode icons
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    args = sys.argv[1:]
    quick = "--quick" in args
    send_tg = "--telegram" in args

    env = load_env(ENV_FILE)

    print("Running YNAI5 Health Check...")
    if quick:
        print("(Quick mode: RAM, disk, internet only)\n")

    all_alerts = []
    results = {}
    top_ram_procs = []
    free_disk_gb = 0.0

    # Define tasks
    tasks = {
        "ram": check_ram,
        "disk": check_disk,
        "internet": check_internet,
    }
    if not quick:
        tasks["cpu"] = check_cpu
        tasks["docker"] = check_docker
        tasks["python"] = check_python_procs
        tasks["startup"] = check_startup_apps

    # Run concurrently
    with ThreadPoolExecutor(max_workers=7) as executor:
        future_map = {executor.submit(fn): key for key, fn in tasks.items()}
        for future in as_completed(future_map):
            key = future_map[future]
            try:
                outcome = future.result()
                if key == "ram":
                    results["ram"], alerts, top_ram_procs = outcome
                    all_alerts.extend(alerts)
                elif key == "disk":
                    results["disk"], alerts, free_disk_gb = outcome
                    all_alerts.extend(alerts)
                elif key == "internet":
                    results["internet"], alerts = outcome
                    all_alerts.extend(alerts)
                elif key == "cpu":
                    results["cpu"], alerts = outcome
                    all_alerts.extend(alerts)
                elif key == "docker":
                    results["docker"], alerts = outcome
                    all_alerts.extend(alerts)
                elif key == "python":
                    results["python"], alerts = outcome
                    all_alerts.extend(alerts)
                elif key == "startup":
                    results["startup"], alerts = outcome
                    all_alerts.extend(alerts)
            except Exception as e:
                results[key] = f"## {key.upper()}\n  ❌ Check failed: {e}"

    report = build_report(results, all_alerts, top_ram_procs, free_disk_gb)

    # Print to console
    print(report)

    # Save to log
    ts_file = datetime.now().strftime("%Y-%m-%d-%H%M")
    log_path = LOG_DIR / f"{ts_file}-health.md"
    log_path.write_text(report, encoding="utf-8")
    print(f"\nLog saved: {log_path}")

    # Telegram
    if send_tg:
        send_telegram(report, env)


if __name__ == "__main__":
    main()
