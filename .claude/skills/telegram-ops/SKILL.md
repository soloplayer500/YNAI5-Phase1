---
name: telegram-ops
description: Telegram bot and VM commander operations. Use when user says "test bot", "send Telegram", "check commander", "bot health", "send /status", or wants to interact with @SoloClaude5_bot
---

# /telegram-ops [command?]

Manage and test the Telegram control layer for YNAI5.

**Bot:** @SoloClaude5_bot  
**Chat ID:** 8569520396  
**Commander:** ~/ynai5-agent/commander.py (on VM)  
**Python wrapper:** ryn/runtime/telegram_tasks.py

## Quick Commands (via Python wrapper)

```bash
# Test bot health + /status command
python ryn/runtime/telegram_tasks.py --test

# Get VM status via Telegram
python ryn/runtime/telegram_tasks.py --status

# Get last 20 log lines
python ryn/runtime/telegram_tasks.py --logs

# Trigger snapshot (commits brain state locally on VM)
python ryn/runtime/telegram_tasks.py --snapshot

# Restart a safe service
python ryn/runtime/telegram_tasks.py --restart ynai5-dashboard
python ryn/runtime/telegram_tasks.py --restart ynai5-gemini
python ryn/runtime/telegram_tasks.py --restart nginx

# Send a custom message to yourself
python ryn/runtime/telegram_tasks.py --send "Custom alert text"
```

## Commander Health Check

Step 1 — Verify commander service is running:
```bash
ssh ... 'systemctl is-active ynai5-commander && tail -5 ~/ynai5-agent/command.log'
```

Step 2 — Run bot test:
```bash
python ryn/runtime/telegram_tasks.py --test
```

Expected output:
```
Bot: @SoloClaude5_bot (id=XXXX) — REACHABLE ✓
Commander responding ✓
YNAI5 STATUS [timestamp] ...
```

## If Bot Not Responding

1. Check commander is active: `ssh ... 'systemctl is-active ynai5-commander'`
2. Check .env has TELEGRAM_BOT_TOKEN: `ssh ... 'grep TELEGRAM ~/ynai5-agent/.env | head -2'`
3. Check offset file isn't stuck: `ssh ... 'cat ~/ynai5-agent/.cmd_offset'`
4. Restart commander: `ssh ... 'sudo systemctl restart ynai5-commander && sleep 3 && systemctl is-active ynai5-commander'`

## Safe Services for /restart

Only these are whitelisted in commander.py:
- `ynai5-dashboard`
- `ynai5-gemini`
- `nginx`

## Manual Message Format

For custom Telegram notifications to self:
```bash
python ryn/runtime/telegram_tasks.py --send "⚠️ YNAI5: [alert text] at $(date -u)"
```

## Output Report

```
TELEGRAM OPS REPORT [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━━
Bot reachable: YES/NO
Commander active: YES/NO
Last command logged: [timestamp + cmd]
/status test: PASS/FAIL
Response time: Xs
━━━━━━━━━━━━━━━━━━━━━━━━
```
