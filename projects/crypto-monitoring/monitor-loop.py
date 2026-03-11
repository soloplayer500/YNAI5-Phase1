#!/usr/bin/env python3
"""
YNAI5 Monitor Loop — Heartbeat & Real-time Alert System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Runs continuously. Checks every 15 minutes.
Sends Telegram alerts when:
  - A price threshold is crossed
  - Any coin moves >5% in a single 15-min cycle
  - Daily heartbeat at 12:00 (noon) AST

Usage:
  python monitor-loop.py           # default: 15min interval
  python monitor-loop.py 5         # custom: 5min interval

Stop: Ctrl+C (sends shutdown message to Telegram)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ── UTF-8 fix
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── Config
DEFAULT_INTERVAL_MIN = 15
BIG_MOVE_THRESHOLD   = 5.0   # % change in one cycle to trigger alert


# ── Load .env.local ───────────────────────────────────────────────────────────
def load_env() -> dict:
    env_path = Path(__file__).resolve().parent.parent.parent / ".env.local"
    env = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


ENV = load_env()
TELEGRAM_BOT_TOKEN = ENV.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = ENV.get("TELEGRAM_CHAT_ID", "")
COINGECKO_API_KEY  = ENV.get("COINGECKO_API_KEY", "")

WATCHLIST = {
    "opinion":        {"symbol": "OPN",   "alerts": [(0.18, "DOWN"), (0.45, "UP"), (0.60, "UP")]},
    "bitcoin":        {"symbol": "BTC",   "alerts": [(55000, "DOWN"), (90000, "UP"), (110000, "UP")]},
    "ethereum":       {"symbol": "ETH",   "alerts": [(1500, "DOWN"), (3000, "UP"), (4000, "UP")]},
    "solana":         {"symbol": "SOL",   "alerts": [(60, "DOWN"), (120, "UP"), (200, "UP")]},
    "eigenlayer":     {"symbol": "EIGEN", "alerts": [(0.10, "DOWN"), (0.40, "UP"), (1.00, "UP")]},
    "pudgy-penguins": {"symbol": "PENGU", "alerts": [(0.003, "DOWN"), (0.015, "UP"), (0.040, "UP")]},
    "bitcoin-cash":   {"symbol": "BCH",   "alerts": [(250, "DOWN"), (450, "UP"), (600, "UP")]},
    "babylon":        {"symbol": "BABY",  "alerts": [(0.008, "DOWN"), (0.025, "UP"), (0.050, "UP")]},
}

# Track which thresholds have already fired (reset on restart)
fired_alerts: set = set()


# ── Helpers ───────────────────────────────────────────────────────────────────
def ts() -> str:
    return datetime.now().strftime("%H:%M")


def fmt_price(price: float) -> str:
    if price >= 1000:  return f"${price:,.0f}"
    if price >= 1:     return f"${price:,.2f}"
    if price >= 0.01:  return f"${price:.4f}"
    return f"${price:.6f}"


# ── Fetch Prices ──────────────────────────────────────────────────────────────
def fetch_prices() -> dict:
    ids = ",".join(WATCHLIST.keys())
    url = (
        f"https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies=usd&include_24hr_change=true"
    )
    headers = {"Accept": "application/json", "User-Agent": "YNAI5-Monitor/1.0"}
    if COINGECKO_API_KEY:
        headers["x-cg-demo-api-key"] = COINGECKO_API_KEY
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[{ts()}] Price fetch error: {e}")
        return {}


# ── Telegram ──────────────────────────────────────────────────────────────────
def send_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        payload = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
        }).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10):
            pass
        print(f"[{ts()}] Telegram ✓")
    except Exception as e:
        print(f"[{ts()}] Telegram failed: {e}")


# ── Check Cycle ───────────────────────────────────────────────────────────────
def check_cycle(prev_prices: dict) -> tuple:
    """
    Fetch latest prices, detect:
      1. Threshold crossings (only fires once per threshold until reset)
      2. Big moves vs previous check
    Returns (new_prices, alert_lines)
    """
    prices = fetch_prices()
    if not prices:
        return prev_prices, []

    alert_lines = []

    for coin_id, cfg in WATCHLIST.items():
        sym   = cfg["symbol"]
        data  = prices.get(coin_id, {})
        price = data.get("usd")
        if price is None:
            continue

        # 1. Threshold crossing (fires once, tracked in fired_alerts)
        for threshold, direction in cfg["alerts"]:
            key = f"{coin_id}:{threshold}:{direction}"
            if direction == "DOWN" and price <= threshold:
                if key not in fired_alerts:
                    fired_alerts.add(key)
                    alert_lines.append(
                        f"⬇️ <b>{sym}</b> {fmt_price(price)}\n"
                        f"   → Crossed ${threshold} support"
                    )
            elif direction == "UP" and price >= threshold:
                if key not in fired_alerts:
                    fired_alerts.add(key)
                    alert_lines.append(
                        f"⬆️ <b>{sym}</b> {fmt_price(price)}\n"
                        f"   → Hit ${threshold} target"
                    )
            else:
                # Price moved away from threshold — allow re-firing later
                if key in fired_alerts:
                    fired_alerts.discard(key)

        # 2. Big move vs last check
        prev = prev_prices.get(coin_id, {}).get("usd")
        if prev and prev > 0:
            move_pct = abs((price - prev) / prev * 100)
            if move_pct >= BIG_MOVE_THRESHOLD:
                direction_word = "📈 UP" if price > prev else "📉 DOWN"
                alert_lines.append(
                    f"⚡ <b>{sym}</b> {direction_word} {move_pct:.1f}% in 15 min\n"
                    f"   {fmt_price(prev)} → {fmt_price(price)}"
                )

    return prices, alert_lines


# ── Heartbeat ─────────────────────────────────────────────────────────────────
def heartbeat_message(prices: dict, check_count: int, interval_min: int) -> str:
    greens = sum(
        1 for cid in WATCHLIST if prices.get(cid, {}).get("usd_24h_change", 0) >= 0
    )
    reds = len(WATCHLIST) - greens
    return (
        f"💓 <b>YNAI5 Heartbeat</b>  ·  {ts()} AST\n"
        f"Status: LIVE ✅  |  Market: {greens}🟢 {reds}🔴\n"
        f"Checks done: {check_count}  ·  Interval: {interval_min} min\n"
        f"<i>Watching {len(WATCHLIST)} assets around the clock</i>"
    )


# ── Main Loop ─────────────────────────────────────────────────────────────────
def main():
    interval_min = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INTERVAL_MIN
    interval_sec = interval_min * 60

    print(f"\n{'━'*48}")
    print(f"  YNAI5 Monitor Loop — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Interval: {interval_min} min  |  Ctrl+C to stop")
    print(f"{'━'*48}\n")

    send_telegram(
        f"🟢 <b>YNAI5 Monitor STARTED</b>  ·  {ts()} AST\n"
        f"Watching {len(WATCHLIST)} assets  ·  Alerts on thresholds + big moves\n"
        f"Interval: {interval_min} min  ·  Heartbeat: noon daily"
    )

    prev_prices: dict = {}
    last_heartbeat_hour = -1
    check_count = 0

    while True:
        try:
            check_count += 1
            now = datetime.now()
            print(f"[{ts()}] Check #{check_count}...", end=" ", flush=True)

            prev_prices, alert_lines = check_cycle(prev_prices)

            if alert_lines:
                alert_msg = (
                    f"🚨 <b>YNAI5 ALERT</b>  ·  {ts()} AST\n\n" +
                    "\n\n".join(alert_lines) +
                    f"\n\n<i>— @SoloClaude5_bot</i>"
                )
                send_telegram(alert_msg)
                print(f"{len(alert_lines)} alert(s) fired")
            else:
                print("clean")

            # Daily noon heartbeat
            if now.hour == 12 and now.hour != last_heartbeat_hour:
                send_telegram(heartbeat_message(prev_prices, check_count, interval_min))
                last_heartbeat_hour = now.hour

        except KeyboardInterrupt:
            print(f"\n[{ts()}] Stopped by user.")
            send_telegram(
                f"🔴 <b>YNAI5 Monitor STOPPED</b>  ·  {ts()} AST\n"
                f"Total checks: {check_count}"
            )
            break
        except Exception as e:
            print(f"\n[{ts()}] Error: {e}")

        time.sleep(interval_sec)


if __name__ == "__main__":
    main()
