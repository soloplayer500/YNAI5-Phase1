#!/usr/bin/env python3
"""
YNAI5 Cloud Health — runs on GitHub Actions when laptop is OFF.
Checks all critical APIs and sends Telegram report.
"""
import os, requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8569520396")

APIS = [
    ("CoinGecko",  "https://api.coingecko.com/api/v3/ping",       {}),
    ("GitHub",     "https://api.github.com",                       {}),
    ("Kraken",     "https://api.kraken.com/0/public/SystemStatus", {}),
]

def check(name, url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=8)
        return name, r.status_code, r.status_code < 400
    except Exception as e:
        return name, 0, False

def send_telegram(msg):
    if not TOKEN:
        print("No TELEGRAM_BOT_TOKEN set — skipping send.")
        return
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"},
        timeout=10
    )

def main():
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    results = []
    with ThreadPoolExecutor(max_workers=len(APIS)) as ex:
        futures = {ex.submit(check, *a): a[0] for a in APIS}
        for f in as_completed(futures):
            results.append(f.result())

    lines = [f"☁️ *YNAI5 Cloud Health* — {ts}", ""]
    all_ok = True
    for name, code, ok in sorted(results):
        icon = "✅" if ok else "❌"
        if not ok:
            all_ok = False
        lines.append(f"{icon} {name}: HTTP {code}")

    lines += [
        "",
        "✅ All APIs healthy" if all_ok else "⚠️ Some APIs unreachable",
        "_(GitHub Actions — laptop may be OFF)_"
    ]

    report = "\n".join(lines)
    print(report)
    send_telegram(report)

if __name__ == "__main__":
    main()
