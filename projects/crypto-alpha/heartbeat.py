#!/usr/bin/env python3
"""
Block Syndicate Heartbeat
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
One-shot health check for the Block Syndicate revenue lane.
Run daily via cron or manually:  python projects/crypto-alpha/heartbeat.py

Checks:
  1. Telegram bot reachable
  2. Free channel resolvable (-1003860200579)
  3. VIP channel resolvable (-1003689725571)
  4. Screener last run age (< 26h = healthy)
  5. Gumroad URL present in distribution kit (= funnel live)
  6. Distribution placeholders resolved (no [Gumroad link] / [Telegram FREE link] left)

Output: stdout report + log file at projects/crypto-alpha/logs/heartbeat-YYYY-MM-DD.log
Exit 0 = healthy, 1 = warning, 2 = critical.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# UTF-8 fix for Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── Config ────────────────────────────────────────────────────────────────────
ROOT          = Path(__file__).resolve().parent.parent.parent
ENV_PATH      = ROOT / ".env.local"
SCREENER_LOGS = ROOT / "projects" / "passive-income" / "logs"
DIST_DIR      = ROOT / "projects" / "passive-income" / "distribution"
HEARTBEAT_LOG = Path(__file__).parent / "logs" / f"heartbeat-{datetime.now().strftime('%Y-%m-%d')}.log"
HEARTBEAT_LOG.parent.mkdir(exist_ok=True)

FREE_CHAT  = "-1003860200579"
VIP_CHAT   = "-1003689725571"

PLACEHOLDERS = ["[Gumroad link]", "[GUMROAD_URL]", "[Telegram FREE link]", "[TELEGRAM_FREE_LINK]"]


# ── Helpers ───────────────────────────────────────────────────────────────────
def load_env() -> dict:
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"')
    return env


def tg_get(token: str, method: str, **params) -> dict:
    qs = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
    url = f"https://api.telegram.org/bot{token}/{method}?{qs}"
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ── Checks ────────────────────────────────────────────────────────────────────
def check_bot(token: str) -> tuple[str, str]:
    if not token:
        return "FAIL", "TELEGRAM_BOT_TOKEN missing in .env.local"
    r = tg_get(token, "getMe")
    if r.get("ok"):
        return "OK", f"@{r['result'].get('username','?')} reachable"
    return "FAIL", f"getMe error: {r.get('error') or r.get('description')}"


def check_chat(token: str, chat_id: str, label: str) -> tuple[str, str]:
    if not token:
        return "FAIL", "no token"
    r = tg_get(token, "getChat", chat_id=chat_id)
    if r.get("ok"):
        title = r["result"].get("title", "?")
        return "OK", f"{label}: {title}"
    return "FAIL", f"{label}: {r.get('description', r.get('error', 'unknown'))}"


def check_screener_log() -> tuple[str, str]:
    if not SCREENER_LOGS.exists():
        return "FAIL", "logs dir missing"
    logs = sorted(SCREENER_LOGS.glob("*.log"), key=os.path.getmtime, reverse=True)
    if not logs:
        return "FAIL", "no screener logs found"
    latest = logs[0]
    age_hours = (time.time() - latest.stat().st_mtime) / 3600
    if age_hours < 26:
        return "OK", f"{latest.name} ({age_hours:.1f}h old)"
    if age_hours < 72:
        return "WARN", f"{latest.name} stale ({age_hours:.1f}h old, expected <26h)"
    return "FAIL", f"{latest.name} VERY STALE ({age_hours:.1f}h old)"


def check_funnel_live() -> tuple[str, str]:
    """Gumroad URL present + no placeholders left."""
    if not DIST_DIR.exists():
        return "FAIL", "distribution dir missing"
    files = list(DIST_DIR.glob("*.md"))
    if not files:
        return "FAIL", "no distribution files"

    placeholder_files = []
    has_gumroad_url = False
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="ignore")
        if any(p in txt for p in PLACEHOLDERS):
            placeholder_files.append(f.name)
        if "gumroad.com/" in txt or "gum.co/" in txt:
            has_gumroad_url = True

    if not has_gumroad_url:
        return "FAIL", "no Gumroad URL found in distribution kit"
    if placeholder_files:
        return "WARN", f"placeholders remain in: {', '.join(placeholder_files[:3])}"
    return "OK", "Gumroad URL embedded, no placeholders"


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> int:
    env = load_env()
    token = env.get("TELEGRAM_BOT_TOKEN", "")

    checks = [
        ("Bot reachable",   *check_bot(token)),
        ("Free channel",    *check_chat(token, FREE_CHAT, "free")),
        ("VIP channel",     *check_chat(token, VIP_CHAT,  "vip")),
        ("Screener fresh",  *check_screener_log()),
        ("Funnel live",     *check_funnel_live()),
    ]

    fail = sum(1 for _, status, _ in checks if status == "FAIL")
    warn = sum(1 for _, status, _ in checks if status == "WARN")

    ICON = {"OK": "✅", "WARN": "⚠️ ", "FAIL": "❌"}
    overall = "🔴 CRITICAL" if fail else "🟡 WARN" if warn else "🟢 HEALTHY"

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"BLOCK SYNDICATE HEARTBEAT — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Overall: {overall}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]
    for name, status, detail in checks:
        lines.append(f"{ICON[status]} {name:18} {detail}")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    report = "\n".join(lines)
    print(report)

    HEARTBEAT_LOG.write_text(report + "\n", encoding="utf-8")

    return 2 if fail else 1 if warn else 0


if __name__ == "__main__":
    sys.exit(main())
