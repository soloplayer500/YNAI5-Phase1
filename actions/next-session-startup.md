# Next Session Startup — YNAI5 VM
_Updated: 2026-04-10 (end of Session 22)_

## VM Status Check (Run First)
```bash
ssh -i ~/.ssh/google_compute_engine -o StrictHostKeyChecking=no shema@34.45.31.188 "df -h / | tail -1 && free -m | grep Mem && for svc in ynai5-dashboard ynai5-chat nginx docker; do printf '%-20s' \$svc; systemctl is-active \$svc; done"
```

Expected: disk ~72% (8.4GB free), RAM ~550MB used, all services active.

---

## VM Is Stable — All Issues Fixed This Session

### What Works Now
| Component | Status | Notes |
|-----------|--------|-------|
| Disk | ✅ 8.4GB free | Was 100% full — fixed by removing old snap revisions |
| All API endpoints | ✅ 200 OK | Fixed blocking GDrive FUSE hang in main.py |
| ynai5-dashboard (port 8000) | ✅ active | FastAPI + uvicorn |
| ynai5-chat (port 8001) | ✅ active | Flask LLM proxy (Gemini + Vertex) |
| nginx (port 80) | ✅ active | Reverse proxy |
| Docker stack | ✅ active | n8n + SearXNG + Portainer |
| Ollama systemd | ⏸ disabled | phi3:mini installed, enable when ready |

### What Was Fixed
1. **Disk 100% full** → Removed old snap revisions (core20/core22/gcloud/lxd old revisions) → 8.4GB freed
2. **docker-compose ollama error** → Docker Ollama image is 8GB+ (CUDA). Removed from compose. Use systemd instead.
3. **GDrive FUSE hang blocking all API endpoints** → Fixed `is_drive_mounted()` to read `/proc/mounts` instead of calling `os.listdir()` or `mountpoint -q` (both hang on stuck FUSE)
4. **models.json** → Updated to v0.4.0 with phi3:mini as rank-1

---

## Next Session: phi3 + Own LLM Server

### Step 1 — Enable Ollama (phi3:mini already installed)
```bash
ssh -i ~/.ssh/google_compute_engine -o StrictHostKeyChecking=no shema@34.45.31.188 "sudo systemctl enable --now ollama && sleep 5 && curl -s http://127.0.0.1:11434/api/tags | python3 -c 'import sys,json; [print(m[\"name\"]) for m in json.load(sys.stdin)[\"models\"]]'"
```

### Step 2 — Test phi3:mini inference via REST API
```bash
ssh -i ~/.ssh/google_compute_engine -o StrictHostKeyChecking=no shema@34.45.31.188 "curl -s --max-time 120 -X POST http://127.0.0.1:11434/api/generate -H 'Content-Type: application/json' -d '{\"model\":\"phi3:mini\",\"prompt\":\"In one sentence: what is an AI assistant?\",\"stream\":false}' | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d[\"response\"][:200]); print(\"Speed:\",round(d[\"eval_count\"]/d[\"eval_duration\"]*1e9,1),\"tok/s\")'"
```
Expected: 1-2 tok/s on e2-micro (slow but working). Real speed after VM upgrade.

### Step 3 — Wire phi3 into chat_server.py
Add a `call_ollama(message)` function and route short/simple prompts to it as rank-0 (before Gemini Flash).

### Step 4 — Own LLM Server (planned)
Build a thin FastAPI wrapper around Ollama that exposes a clean `/v1/chat` endpoint compatible with OpenAI format. This becomes the local LLM tier in the AI routing stack.

---

## End of Month — VM Upgrade
Upgrade e2-micro → e2-small ($13/mo) via GCP Console:
- GCP Console → Compute Engine → ynai5-vm → Stop → Edit → Machine type = e2-small → Save → Start
- After upgrade: phi3:mini goes from 1-2 tok/s → 8-15 tok/s (usable for real-time chat)

---

## VM Quick Reference
| Thing | Location |
|-------|----------|
| Dashboard source | `~/YNAI5_AI_CORE/dashboard/` |
| Start Docker stack | `cd ~/YNAI5_AI_CORE && docker compose up -d` |
| Full health check | `curl -s http://127.0.0.1:8000/status.json` |
| API status | `curl -s http://127.0.0.1:8000/api/status` |
| Logs | `/ynai5_runtime/logs/` |
| YNAI5 event log | `~/YNAI5_AI_CORE/logs/ynai5logs.json` |
| Models config | `~/YNAI5_AI_CORE/dashboard/config/models.json` |
| Chat server | Flask on port 8001 (`chat_server.py`) |
| Dashboard API | FastAPI on port 8000 (`main.py`) |
| Ollama (systemd) | port 11434 — enable with `sudo systemctl enable --now ollama` |
| n8n | port 5678 — `http://34.45.31.188/n8n/` (via nginx) |

---

## Other Things Queued
- Perplexity API key → perplexity.ai/settings/api → paste in YNAI5-KEY-INPUT.txt
- n8n agent orchestration — wire Gemini worker + Claude runner through n8n
- GitHub SSH key on VM → allows `git push` from VM directly
- Health check Telegram workflow → activates on first 9AM AST scheduled run
