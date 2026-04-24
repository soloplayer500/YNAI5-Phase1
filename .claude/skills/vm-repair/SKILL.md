---
name: vm-repair
description: SSH diagnostic and repair loop for YNAI5 VM. Use when a service is down, SSH is failing, VM is unresponsive, or user says "fix VM", "service down", "restart failed", "repair X on VM"
---

# /vm-repair [service?]

Systematic SSH diagnostic → fix → verify loop. Never guess. Always check before touching.

**VM:** shema@34.45.31.188  
**SSH key:** ~/.ssh/google_compute_engine

## Step 0 — Connectivity Check

```bash
ssh -i ~/.ssh/google_compute_engine -o StrictHostKeyChecking=no -o ConnectTimeout=10 shema@34.45.31.188 'echo "SSH OK" && uptime'
```

If fails → **STOP. Report: VM unreachable. Cannot proceed.**

## Step 1 — Snapshot Current State

```bash
ssh ... 'systemctl is-active ynai5-dashboard ynai5-gemini ynai5-claude nginx ynai5-heartbeat ynai5-commander && df -h / && free -m | head -2'
```

Record: which services are active vs failed.

## Step 2 — Triage Failed Services

For each failed service:
```bash
ssh ... 'journalctl -u [SERVICE] -n 20 --no-pager'
```

Classify failure type:
- **OOM (out of memory)** → free RAM first, then restart
- **Port conflict** → find what's on the port (`ss -tulnp | grep [PORT]`)
- **Config error** → read error in logs, fix config
- **Crash loop** → read last exit code, identify cause

## Step 3 — Fix (One Change at a Time)

**RAM pressure fix:**
```bash
ssh ... 'free -m && cat /proc/meminfo | grep Available'
# If <100MB available:
ssh ... 'sudo systemctl restart ynai5-gemini'  # gemini is heaviest non-critical
```

**Service restart (max 1 attempt per service):**
```bash
ssh ... 'sudo systemctl restart [SERVICE] && sleep 3 && systemctl is-active [SERVICE]'
```

If fails after 1 restart → capture full logs, STOP and report. Do NOT retry.

**Disk full:**
```bash
ssh ... 'df -h / && sudo journalctl --vacuum-size=100M && df -h /'
```

## Step 4 — Verify

After any fix:
```bash
ssh ... 'for svc in ynai5-dashboard ynai5-gemini nginx ynai5-heartbeat ynai5-commander; do echo "$svc: $(systemctl is-active $svc)"; done'
ssh ... 'curl -s --max-time 5 http://127.0.0.1:8000/api/status | head -c 100'
```

Pass: all critical services active + dashboard HTTP 200.

## Step 5 — Report

```
VM REPAIR REPORT [timestamp]
━━━━━━━━━━━━━━━━━━━━━━━━
ISSUE: [what was wrong]
FIX APPLIED: [what was done]
RESULT: RESOLVED | PARTIAL | FAILED
SERVICES NOW:
  dashboard: OK/DOWN
  nginx: OK/DOWN
  heartbeat: OK/DOWN
  commander: OK/DOWN
DISK: X% used
RAM avail: XMB
DEFERRED: [anything not fixed]
━━━━━━━━━━━━━━━━━━━━━━━━
```

Update `ryn/brain/last_report.md` with repair event.
