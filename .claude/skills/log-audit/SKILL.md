---
name: log-audit
description: VM log analysis — check sizes, errors, patterns, alerts. Use when user says "check logs", "audit logs", "log too big", "what's in the logs", "log errors on VM"
---

# /log-audit [--quick | --full]

Systematic VM log audit. Finds oversized logs, error patterns, and alert signals.

**Default:** --quick (size check + last 20 lines of key logs)  
**--full:** Deep scan including error pattern grep

## Step 1 — Log Inventory & Size Check

```bash
ssh ... '
echo "=== LOG SIZES ===" &&
ls -lh ~/ynai5-agent/heartbeat.log ~/ynai5-agent/command.log 2>/dev/null &&
ls -lh /ynai5_runtime/logs/ 2>/dev/null &&
echo "=== ROTATED ===" &&
ls -lh ~/ynai5-agent/*.log.1 /ynai5_runtime/logs/*.log.1 2>/dev/null || echo "(none)"
'
```

**Flag:** Any log >20MB is a problem. Any .log.1 >30MB should be compressed.

## Step 2 — Heartbeat Log (Last 20 Lines)

```bash
ssh ... 'tail -20 ~/ynai5-agent/heartbeat.log'
```

Look for:
- Consistent ticks (every ~60s)
- Any "WARNING" or "DOWN" lines
- LOAD values (flag if consistently >1.5)
- RAM available trend (flag if declining)

## Step 3 — Commander Log (Last 20 Lines)

```bash
ssh ... 'tail -20 ~/ynai5-agent/command.log 2>/dev/null || echo "(empty — no commands yet)"'
```

Look for: which commands were run, any errors.

## Step 4 — Alert State

```bash
ssh ... 'cat ~/ynai5-agent/alert.state'
```

Any key showing `fired` → active alert. Investigate.

## Step 5 — (--full only) Error Pattern Scan

```bash
ssh ... '
echo "=== DASHBOARD ERRORS ===" &&
grep -i "error\|exception\|traceback" /ynai5_runtime/logs/dashboard.log 2>/dev/null | tail -10 || echo "(none)" &&
echo "=== GEMINI ERRORS ===" &&
grep -i "error\|exception" /ynai5_runtime/logs/gemini_worker.log 2>/dev/null | tail -10 || echo "(none)"
'
```

## Step 6 — Fix Oversized Logs

If any log >20MB:
```bash
ssh ... 'sudo logrotate --force /etc/logrotate.d/ynai5 && echo "Rotated OK"'
```

If .log.1 files >30MB and uncompressed:
```bash
ssh ... 'gzip ~/ynai5-agent/heartbeat.log.1 && gzip /ynai5_runtime/logs/rclone-drive.log.1 2>/dev/null; echo "Compressed"'
```

## Step 7 — Output Report

```
LOG AUDIT REPORT [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━━
SIZES:
  heartbeat.log: XMB [OK/FLAG]
  command.log: XMB [OK/FLAG]
  dashboard.log: XMB [OK/FLAG]
  rclone-drive.log: XMB [OK/FLAG]

HEARTBEAT: Ticking every ~Xs | Last: [timestamp]
LOAD trend: X.XX avg
RAM trend: X MB avail

ALERT STATE:
  dash: ok/fired
  nginx: ok/fired
  load: ok/fired
  ram: ok/fired

ERRORS FOUND: [Y/N — details if Y]
ACTIONS TAKEN: [rotated / compressed / none]
━━━━━━━━━━━━━━━━━━━━━━━━
```
