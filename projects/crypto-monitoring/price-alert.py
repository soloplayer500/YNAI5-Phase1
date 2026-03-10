#!/usr/bin/env python3
"""
Price Alert Checker — YNAI5-SU Crypto Monitoring
Checks current prices vs alert thresholds. Uses CoinGecko free API (no key needed).
Optional: add COINGECKO_API_KEY to .env.local for higher rate limits (demo key = 30 calls/min).
Run manually: python price-alert.py
Schedule: Windows Task Scheduler → run daily or on-demand

No external dependencies — stdlib only (urllib, json, os, pathlib).
"""

import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path


# ── Load .env.local ──────────────────────────────────────────────────────────

def load_env() -> dict:
    """Load key=value pairs from .env.local (two levels up from this file)."""
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
COINGECKO_API_KEY = ENV.get("COINGECKO_API_KEY", "")

# ── Alert Config ────────────────────────────────────────────────────────────────
# Format: "coingecko_id": { "symbol": "TICKER", "alerts": [(price, label), ...] }
# alert label: "DOWN" = below threshold, "UP" = above threshold

WATCHLIST = {
    "opinion": {
        "symbol": "OPN",
        "alerts": [
            (0.18,  "DOWN - Accumulation zone reached"),
            (0.45,  "UP   - Recovery signal, re-evaluate"),
            (0.60,  "UP   - Near ATH resistance, consider exit"),
        ],
        "note": "Post-Binance listing. 80% supply unlocked. Watch March 2027 cliff."
    },
    "bitcoin": {
        "symbol": "BTC",
        "alerts": [
            (55000, "DOWN - Major support test"),
            (90000, "UP   - Back at avg buy zone"),
            (110000,"UP   - All-time high territory"),
        ],
        "note": "Kraken + Revolut holding. Avg buy $90,111."
    },
    "ethereum": {
        "symbol": "ETH",
        "alerts": [
            (1500,  "DOWN - Critical support"),
            (3000,  "UP   - Back at avg buy zone"),
            (4000,  "UP   - ATH territory"),
        ],
        "note": "Kraken holding. Avg buy $3,151."
    },
    "solana": {
        "symbol": "SOL",
        "alerts": [
            (60,    "DOWN - Deep support"),
            (120,   "UP   - Recovery level"),
            (200,   "UP   - Bull run territory"),
        ],
        "note": "Kraken + Revolut. Small positions."
    },
    "eigenlayer": {
        "symbol": "EIGEN",
        "alerts": [
            (0.10,  "DOWN - Near zero, review exit"),
            (0.40,  "UP   - Back at avg buy"),
            (1.00,  "UP   - Strong recovery signal"),
        ],
        "note": "Restaking protocol. Avg buy $0.30."
    },
    "pudgy-penguins": {
        "symbol": "PENGU",
        "alerts": [
            (0.003, "DOWN - Critical support, review exit"),
            (0.015, "UP   - 2x recovery signal"),
            (0.040, "UP   - Strong recovery toward ATH"),
        ],
        "note": "Kraken: 1,873 tokens. Meme/NFT token. ATH ~$0.07."
    },
    "bitcoin-cash": {
        "symbol": "BCH",
        "alerts": [
            (250,   "DOWN - Major support test"),
            (450,   "UP   - Recovery signal, re-evaluate"),
            (600,   "UP   - Resistance zone, consider exit"),
        ],
        "note": "Revolut: 0.01896 BCH. Secondary BTC fork."
    },
    "babylon": {
        "symbol": "BABY",
        "alerts": [
            (0.008, "DOWN - Critical support"),
            (0.025, "UP   - Back at avg buy zone ($0.028)"),
            (0.050, "UP   - Strong recovery signal"),
        ],
        "note": "Kraken: 0.00308 BABY. BTC staking protocol. Avg buy $0.028."
    },
}

# ── CoinGecko API ───────────────────────────────────────────────────────────────

def get_prices(coin_ids: list) -> dict:
    """Fetch current prices from CoinGecko.
    - No key: free public endpoint (10–15 calls/min, may 429 occasionally)
    - With COINGECKO_API_KEY in .env.local: demo endpoint (30 calls/min, more reliable)
    """
    ids_str = ",".join(coin_ids)

    if COINGECKO_API_KEY:
        # Demo/Pro endpoint — higher rate limits
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_change=true"
        headers = {
            "Accept": "application/json",
            "User-Agent": "YNAI5-PriceAlert/1.0",
            "x-cg-demo-api-key": COINGECKO_API_KEY,
        }
    else:
        # Free public endpoint — no key, lower limits
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_change=true"
        headers = {"Accept": "application/json", "User-Agent": "YNAI5-PriceAlert/1.0"}

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"[ERROR] CoinGecko API failed: {e}")
        return {}


# ── Alert Logic ─────────────────────────────────────────────────────────────────

def check_alerts(symbol: str, current: float, alerts: list) -> list:
    """Return list of triggered alerts."""
    triggered = []
    for threshold, label in alerts:
        direction = label.split()[0]
        if direction == "DOWN" and current <= threshold:
            triggered.append((threshold, label))
        elif direction == "UP" and current >= threshold:
            triggered.append((threshold, label))
    return triggered


def format_change(change: float) -> str:
    sign = "+" if change >= 0 else ""
    return f"{sign}{change:.2f}%"


def big_move_flag(change: float) -> str:
    """Return a warning label if 24h change is unusually large."""
    abs_change = abs(change)
    if abs_change >= 15:
        return " !! EXTREME MOVE"
    elif abs_change >= 8:
        return " !  BIG MOVE"
    return ""


def log_results(lines: list):
    """Append run output to a daily log file."""
    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"alerts-{datetime.now().strftime('%Y-%m-%d')}.log"
    with log_file.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    api_mode = "Demo key (30 req/min)" if COINGECKO_API_KEY else "Free tier (no key)"

    header = [
        "",
        "=" * 60,
        f"  YNAI5 Price Alert Check — {now}",
        f"  CoinGecko: {api_mode}",
        "=" * 60,
        "",
    ]
    for line in header:
        print(line)

    coin_ids = list(WATCHLIST.keys())
    prices = get_prices(coin_ids)

    if not prices:
        print("[ERROR] Could not fetch prices. Check internet connection.")
        return

    alerts_fired = []
    big_moves = []
    log_lines = header[:]

    for coin_id, config in WATCHLIST.items():
        symbol = config["symbol"]
        data = prices.get(coin_id, {})
        current = data.get("usd")
        change_24h = data.get("usd_24h_change", 0)

        if current is None:
            line = f"  {symbol:<8} [NO DATA — check CoinGecko ID: {coin_id}]"
            print(line)
            log_lines.append(line)
            continue

        # Check for triggered price alerts
        triggered = check_alerts(symbol, current, config["alerts"])

        # Check for big moves
        move_flag = big_move_flag(change_24h)
        if move_flag:
            big_moves.append((symbol, current, change_24h, move_flag))

        # Status display
        change_str = format_change(change_24h)
        status = "*** ALERT ***" if triggered else ("BIG MOVE" if move_flag else "OK")
        line = f"  {symbol:<8} ${current:<12.4f} 24h: {change_str:<10} [{status}]{move_flag}"
        print(line)
        log_lines.append(line)

        if triggered:
            for threshold, label in triggered:
                alert_line = f"           >> ${threshold} — {label}"
                print(alert_line)
                log_lines.append(alert_line)
                alerts_fired.append((symbol, current, threshold, label))

        if config.get("note"):
            note_line = f"           Note: {config['note']}"
            print(note_line)
        print()
        log_lines.append("")

    # Summary
    summary = ["=" * 60]
    if alerts_fired:
        summary.append(f"  PRICE ALERTS FIRED: {len(alerts_fired)}")
        for symbol, price, threshold, label in alerts_fired:
            summary.append(f"  {symbol}: ${price:.4f} — {label}")
    else:
        summary.append("  No price alert thresholds crossed.")

    if big_moves:
        summary.append(f"")
        summary.append(f"  BIG MOVES (>8% in 24h):")
        for symbol, price, change, flag in big_moves:
            summary.append(f"  {symbol}: ${price:.4f}  {format_change(change)}{flag}")

    if not alerts_fired and not big_moves:
        summary.append("  Market status: normal. No action needed.")

    summary.append("=" * 60)
    summary.append("")

    for line in summary:
        print(line)
    log_lines.extend(summary)

    # Write to daily log file
    log_results(log_lines)

    print("Tip: Run this script anytime for a quick check.")
    print("     Schedule: Windows Task Scheduler -> Action -> 'python price-alert.py'")
    print(f"     Logs saved to: projects/crypto-monitoring/logs/\n")


if __name__ == "__main__":
    main()
