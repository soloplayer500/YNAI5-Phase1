#!/usr/bin/env python3
"""
Get Telegram channel IDs for Block Syndicate channels.
Run AFTER adding @SoloClaude5_bot as admin to your channels.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Usage: py projects/passive-income/get_channel_ids.py
"""
import json, sys, urllib.request
from pathlib import Path

env = {}
for line in (Path(__file__).parent.parent.parent / ".env.local").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"')

token = env.get("TELEGRAM_BOT_TOKEN", "")
if not token:
    print("ERROR: No TELEGRAM_BOT_TOKEN found in .env.local")
    sys.exit(1)

print(f"Bot: @SoloClaude5_bot")
print("Checking recent updates for channel messages...\n")

url = f"https://api.telegram.org/bot{token}/getUpdates?limit=50&offset=-50"
with urllib.request.urlopen(url, timeout=10) as r:
    data = json.loads(r.read())

seen = set()
channels_found = []

for update in data.get("result", []):
    # Channel posts come as channel_post
    msg = update.get("channel_post") or update.get("message") or {}
    chat = msg.get("chat", {})
    chat_id   = chat.get("id")
    chat_type = chat.get("type")
    chat_title = chat.get("title", "")
    username  = chat.get("username", "")

    if chat_type == "channel" and chat_id not in seen:
        seen.add(chat_id)
        channels_found.append({
            "id": chat_id,
            "title": chat_title,
            "username": username or "(no public username)",
        })

if channels_found:
    print("Channels found in recent updates:")
    for ch in channels_found:
        print(f"  Title:    {ch['title']}")
        print(f"  Username: @{ch['username']}")
        print(f"  Chat ID:  {ch['id']}")
        print(f"  Use this in screener-channel-bot.py as the chat_id")
        print()
else:
    print("No channel messages found yet.")
    print()
    print("To get the IDs:")
    print("1. Add @SoloClaude5_bot as admin to BOTH channels")
    print("2. Post any message in each channel (e.g. 'test')")
    print("3. Run this script again")
    print()
    print("Or: forward any message from your channels to @SoloClaude5_bot")
    print("    then run this script.")
