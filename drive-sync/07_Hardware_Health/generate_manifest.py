#!/usr/bin/env python3
"""
YNAI5 Hardware Asset Manager — Manifest Generator
Detects current machine hardware and outputs a standardized JSON manifest.

Usage:
  python generate_manifest.py              # Print to stdout
  python generate_manifest.py --save       # Save to inventory/<hostname>.json
  python generate_manifest.py --save --upload  # Save + rclone push to Drive

Schema:
  device_name, os, cpu, ram_gb, gpu, storage_gb
  (plus extended fields: hostname, timestamp, disk_free_gb, platform_detail, manifest_version)
"""

import json
import os
import platform
import subprocess
import sys
import socket
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_VERSION = "1.0.0"
DRIVE_DEST = "gdrive:/YNAI5_AI_CORE/07_Hardware_Health/inventory/"


# ── Helpers ─────────────────────────────────────────────────────────────────

def _run(cmd: list[str], default: str = "Unknown") -> str:
    """Run a subprocess command, return stripped stdout or default on error."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=8
        )
        output = result.stdout.strip()
        return output if output else default
    except Exception:
        return default


def _pwsh(query: str, default: str = "Unknown") -> str:
    """Run a PowerShell CimInstance query, return first non-empty line."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", query],
            capture_output=True, text=True, timeout=8
        )
        lines = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        return lines[0] if lines else default
    except Exception:
        return default


def _try_import(module: str):
    try:
        import importlib
        return importlib.import_module(module)
    except ImportError:
        return None


# ── Detectors ────────────────────────────────────────────────────────────────

def get_device_name() -> str:
    """Human-readable device name. Falls back to hostname."""
    system = platform.system()
    if system == "Windows":
        return _pwsh("(Get-CimInstance Win32_ComputerSystem).Name")
    elif system == "Linux":
        # Try /etc/hostname or hostnamectl
        try:
            return Path("/etc/hostname").read_text().strip()
        except Exception:
            pass
        return _run(["hostnamectl", "--static"])
    elif system == "Darwin":
        return _run(["scutil", "--get", "ComputerName"])
    return socket.gethostname()


def get_os() -> str:
    """Full OS string including version."""
    system = platform.system()
    if system == "Windows":
        ver = platform.version()
        release = platform.release()
        return f"Windows {release} (build {ver})"
    elif system == "Linux":
        # Try /etc/os-release
        try:
            lines = Path("/etc/os-release").read_text().splitlines()
            info = {k: v.strip('"') for k, v in
                    (line.split("=", 1) for line in lines if "=" in line)}
            return info.get("PRETTY_NAME", platform.platform())
        except Exception:
            return platform.platform()
    elif system == "Darwin":
        return f"macOS {platform.mac_ver()[0]}"
    return platform.platform()


def get_cpu() -> str:
    """CPU model string."""
    system = platform.system()
    if system == "Windows":
        return _pwsh("(Get-CimInstance Win32_Processor).Name")
    elif system == "Linux":
        try:
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except Exception:
            pass
        return _run(["lscpu"])  # fallback
    elif system == "Darwin":
        return _run(["sysctl", "-n", "machdep.cpu.brand_string"])
    return platform.processor() or "Unknown CPU"


def get_ram_gb() -> float:
    """Total physical RAM in GB, rounded to 1 decimal."""
    psutil = _try_import("psutil")
    if psutil:
        return round(psutil.virtual_memory().total / (1024 ** 3), 1)
    # Fallback: PowerShell (Windows)
    if platform.system() == "Windows":
        val = _pwsh("(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory", "0")
        try:
            return round(int(val) / (1024 ** 3), 1)
        except ValueError:
            pass
    # Fallback: /proc/meminfo (Linux)
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal"):
                kb = int(line.split()[1])
                return round(kb / (1024 ** 2), 1)
    except Exception:
        pass
    return 0.0


def get_gpu() -> str:
    """Primary GPU name."""
    system = platform.system()
    if system == "Windows":
        # Get all adapters, prefer non-Microsoft ones
        val = _pwsh(
            "(Get-CimInstance Win32_VideoController | Where-Object { $_.Name -notlike '*Microsoft*' } | Select-Object -First 1).Name"
        )
        if val and val != "Unknown":
            return val
        # Fallback: take first adapter regardless
        return _pwsh("(Get-CimInstance Win32_VideoController | Select-Object -First 1).Name")
    elif system == "Linux":
        # Try lspci
        val = _run(["lspci"])
        for line in val.splitlines():
            if any(k in line.upper() for k in ["VGA", "3D", "DISPLAY"]):
                # "00:02.0 VGA compatible controller: Intel..."
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
        # Try nvidia-smi
        val = _run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"])
        if val and "Unknown" not in val:
            return val.splitlines()[0].strip()
    elif system == "Darwin":
        val = _run(["system_profiler", "SPDisplaysDataType"])
        for line in val.splitlines():
            if "Chipset Model" in line:
                return line.split(":", 1)[1].strip()
    return "Unknown GPU"


def get_storage_gb() -> dict:
    """Primary disk total and free space in GB."""
    psutil = _try_import("psutil")
    system = platform.system()
    root = "C:\\" if system == "Windows" else "/"
    if psutil:
        usage = psutil.disk_usage(root)
        return {
            "total": round(usage.total / (1024 ** 3), 1),
            "free":  round(usage.free  / (1024 ** 3), 1),
        }
    # Fallback: shutil
    import shutil
    total, used, free = shutil.disk_usage(root)
    return {
        "total": round(total / (1024 ** 3), 1),
        "free":  round(free  / (1024 ** 3), 1),
    }


# ── Manifest Builder ─────────────────────────────────────────────────────────

def build_manifest() -> dict:
    storage = get_storage_gb()
    return {
        # ── Required schema ──────────────────────────
        "device_name":   get_device_name(),
        "os":            get_os(),
        "cpu":           get_cpu(),
        "ram_gb":        get_ram_gb(),
        "gpu":           get_gpu(),
        "storage_gb":    storage["total"],
        # ── Extended fields ──────────────────────────
        "disk_free_gb":  storage["free"],
        "hostname":      socket.gethostname(),
        "platform":      platform.system(),
        "timestamp":     datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "manifest_version": MANIFEST_VERSION,
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    save   = "--save"   in sys.argv
    upload = "--upload" in sys.argv

    manifest = build_manifest()
    json_str = json.dumps(manifest, indent=2)

    # Always print to stdout
    print(json_str)

    if save or upload:
        hostname = manifest["hostname"].replace(" ", "_").lower()
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{hostname}_{date_str}.json"

        # Save to inventory/ relative to this script's location
        script_dir = Path(__file__).parent
        inventory_dir = script_dir / "inventory"
        inventory_dir.mkdir(exist_ok=True)
        out_path = inventory_dir / filename

        out_path.write_text(json_str, encoding="utf-8")
        print(f"\n✅ Saved: {out_path}", file=sys.stderr)

        if upload:
            result = subprocess.run(
                ["rclone", "copy", str(out_path), DRIVE_DEST],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"✅ Uploaded to {DRIVE_DEST}{filename}", file=sys.stderr)
            else:
                print(f"❌ Upload failed: {result.stderr}", file=sys.stderr)
                sys.exit(1)

    return manifest


if __name__ == "__main__":
    main()
