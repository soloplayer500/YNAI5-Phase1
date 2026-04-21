# YNAI5 VM Dashboard

FastAPI-based control center for the YNAI5-VM (GCP e2-micro, 34.45.31.188).

## Stack
- **Backend:** FastAPI (`dashboard/main.py`) — uvicorn on 127.0.0.1:8000
- **Frontend:** Vanilla HTML/CSS/JS (`dashboard/index.html`)
- **Design tokens:** `dashboard/assets/css/tokens.css` (source of truth)
- **Config:** `dashboard/config/models.json`, `dashboard/config/agents.json`
- **Deploy:** Push to GitHub → `vm-sync.yml` → rsync to `/ynai5_runtime/dashboard/`

## Services (systemd)
| Service | Purpose | Status |
|---|---|---|
| `ynai5-dashboard` | FastAPI/uvicorn — port 8000 | enabled + active |
| `ynai5-gemini` | Gemini worker script | enabled + active |
| `ynai5-claude` | Claude CLI runner | enabled + active |
| `ynai5-drive` | rclone Google Drive mount | enabled + active |
| `nginx` | Reverse proxy (port 80 → 8000) | enabled + active |

---

## Model Router (`router.py`)

Free-first model router with 5-tier cascade. Accepts a prompt and complexity level,
routes to the cheapest model that can handle it, logs each call.

### Usage

```python
from router import route

# Simple query → tries Ollama first, then HuggingFace, OpenRouter, Gemini, Claude
result = route("What is 2+2?", complexity="simple")

# Medium → skips Ollama, starts at HuggingFace
result = route("Explain RSI in 3 sentences.", complexity="medium")

# Complex → goes straight to Gemini, falls back to Claude
result = route("Analyse BTC market structure for the next 30 days.", complexity="complex")

print(result)
# {
#   "response":   "...",
#   "model_used": "gemini/gemini-1.5-flash",
#   "tier":       4,
#   "cost_usd":   0.0,
#   "elapsed_s":  1.4,
#   "complexity": "complex"
# }
```

### Routing Table

| Complexity | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
|---|---|---|---|---|---|
| simple | Ollama | HuggingFace | OpenRouter | Gemini | Claude Haiku |
| medium | HuggingFace | OpenRouter | Gemini | Claude Haiku | — |
| complex | Gemini | Claude Haiku | — | — | — |

### Required Env Vars

| Var | Required | Notes |
|---|---|---|
| `HF_API_TOKEN` | For HuggingFace tier | Free at huggingface.co/settings/tokens |
| `OPENROUTER_API_KEY` | For OpenRouter tier | Free at openrouter.ai |
| `GEMINI_API_KEY` | For Gemini tier | Free at aistudio.google.com |
| `ANTHROPIC_API_KEY` | For Claude tier | Paid — last resort only |
| `OLLAMA_HOST` | Optional | Default: http://localhost:11434 |

### Run Live Tests

```bash
python router.py --test
```

Fires 3 test calls (simple / medium / complex) and prints model used per tier.

### Adding a New Model

1. Implement `_try_yourmodel(prompt: str) -> str | None`
   - Return the response string on success
   - Return `None` on ANY failure (exception, timeout, rate limit, missing key)
2. Add it to the relevant tier(s) in the `ROUTES` dict
3. Add its cost info to `MODEL_META`
4. Add the env var to the header docstring

### Logs

Each call is logged to `/ynai5_runtime/logs/router.log` (or `./router.log` on RYN):
```
[2026-04-21T14:00:00Z] complexity=simple model=openrouter/mistral-7b-instruct:free cost=$0.0000 tokens=142 elapsed=1.2s
```
