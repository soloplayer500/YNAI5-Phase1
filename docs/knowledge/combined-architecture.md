# YNAI5 Combined Infrastructure Architecture

_Generated: 2026-04-13 | Local + GCP VM + External APIs_

---

## Full Architecture Diagram

```mermaid
graph TB
    subgraph local["Local — Windows 11 HP Laptop"]
        cc["Claude Code\nYNAI5-SU Workspace\n40+ Skills + Graphify"]
        gh_actions["GitHub Actions\nCI/CD + Cron Jobs"]
        kp["Kraken Portfolio\nmonitor-loop.py\n15min heartbeat"]
        tg_bridge["Telegram Claude Bridge\n@SoloClaude5_bot\nAI assistant on mobile"]
    end

    subgraph vm["GCP VM — e2-micro @ 34.45.31.188"]
        nginx["nginx\nport 80\nReverse Proxy"]
        dash_api["FastAPI Dashboard\nport 8000\nStatus + Tasks + Logs"]
        chat_svc["Flask Chat Server\nport 8001\nGemini + Vertex proxy"]
        lyra["Lyra Prompt Router\nget_lyra_prompt\nmodel selection layer"]
        docker_apps["Docker Stack\nn8n 「5678」\nSearXNG\nPortainer"]
        ollama_svc["Ollama\nphi3:mini installed\n「disabled — pending upgrade」"]
        graphs_vm["graphify-out/\n121 nodes, 180 edges\nVM knowledge graph"]
    end

    subgraph apis["External APIs"]
        kraken_api["Kraken Exchange\nREST API\nPortfolio + Orders + OHLC"]
        gemini_api["Gemini / Vertex AI\nFlash + Pro\nLLM inference"]
        telegram_api["Telegram API\n@SoloClaude5_bot\nAlerts + Commands"]
        coingecko["CoinGecko API\nFree tier\nMarket data + OHLC"]
        github_api["GitHub\nsoloplayer500/YNAI5-SU\nCI/CD + secrets"]
        perplexity["Perplexity API\nReal-time web search\n「key pending」"]
    end

    subgraph cloud_ci["Cloud CI/CD 「GitHub Actions」"]
        briefing["Morning Briefing\n9AM AST daily\nTelegram report"]
        portfolio_mon["Portfolio Monitor\nEvery 30 min\nKraken snapshot"]
        market_rep["Market Report\n9AM + 3PM AST\nCrypto + stock signals"]
        vm_health["VM Health Check\nDaily\nPings VM status endpoint"]
    end

    cc -->|"SSH + SCP"| vm
    cc -->|"git push"| github_api
    cc -->|"API calls"| gemini_api
    gh_actions -->|"triggers"| cloud_ci
    kp -->|"alerts via"| telegram_api
    tg_bridge -->|"Claude Haiku API"| cc

    nginx -->|"routes to"| dash_api
    nginx -->|"routes to"| chat_svc
    chat_svc -->|"routes via Lyra"| lyra
    lyra -->|"model calls"| gemini_api
    dash_api -->|"reads heartbeat"| graphs_vm

    briefing -->|"sends to"| telegram_api
    briefing -->|"fetches from"| kraken_api
    briefing -->|"fetches from"| coingecko
    portfolio_mon -->|"reads"| kraken_api
    portfolio_mon -->|"sends to"| telegram_api
    market_rep -->|"sends to"| telegram_api
    vm_health -->|"pings"| dash_api

    dash_api -.->|"future: Ollama"| ollama_svc
    chat_svc -.->|"future: Ollama"| ollama_svc

    style local fill:#e7f5ff,stroke:#1971c2
    style vm fill:#d3f9d8,stroke:#2f9e44
    style apis fill:#ffe8cc,stroke:#d9480f
    style cloud_ci fill:#e5dbff,stroke:#5f3dc4

    style cc fill:#a5d8ff,stroke:#1971c2
    style gh_actions fill:#b2f2bb,stroke:#2f9e44
    style kp fill:#fff3bf,stroke:#e67700
    style tg_bridge fill:#ffd8a8,stroke:#d9480f
    style nginx fill:#d0bfff,stroke:#5f3dc4
    style dash_api fill:#b2f2bb,stroke:#2f9e44
    style chat_svc fill:#c3fae8,stroke:#0c8599
    style lyra fill:#eebefa,stroke:#862e9c
    style docker_apps fill:#ffe8cc,stroke:#d9480f
    style ollama_svc fill:#ffc9c9,stroke:#c92a2a
    style graphs_vm fill:#c5f6fa,stroke:#0c8599
    style kraken_api fill:#fff3bf,stroke:#e67700
    style gemini_api fill:#eebefa,stroke:#862e9c
    style telegram_api fill:#ffd8a8,stroke:#d9480f
    style coingecko fill:#c3fae8,stroke:#0c8599
    style github_api fill:#d3f9d8,stroke:#2f9e44
    style perplexity fill:#f3d9fa,stroke:#862e9c
    style briefing fill:#b2f2bb,stroke:#2f9e44
    style portfolio_mon fill:#b2f2bb,stroke:#2f9e44
    style market_rep fill:#b2f2bb,stroke:#2f9e44
    style vm_health fill:#c3fae8,stroke:#0c8599
```

_Solid arrows = active data flows. Dashed arrows = planned/future connections._
_Renders in Obsidian, GitHub markdown, and any Mermaid-compatible renderer._

---

## Summary: How Everything Connects

### Local → Cloud
| Flow | Mechanism | Frequency |
|------|-----------|-----------|
| Local → VM | SSH/SCP | On-demand |
| Local → GitHub | git push | Per session |
| Local → Gemini API | Direct REST | Per AI task |
| Laptop alerts | monitor-loop.py → Telegram | Every 15 min (threshold) |

### GitHub Actions (Cloud CI/CD) → Everything
| Workflow | Target | Schedule |
|----------|--------|----------|
| Morning Briefing | Kraken + CoinGecko → Telegram | 9AM AST |
| Portfolio Monitor | Kraken → Telegram | Every 30 min |
| Market Report | Crypto signals → Telegram | 9AM + 3PM AST |
| VM Health Check | GCP VM /api/status | Daily |

### GCP VM → APIs
| Service | API | Purpose |
|---------|-----|---------|
| chat_server.py | Gemini/Vertex AI | LLM inference for chat |
| Lyra router | Gemini Flash → Pro → Ollama | Model tier selection |
| Dashboard | None (reads local files) | Status display |
| Scripts | GDrive backup | Session state backup |

### Key Architecture Decisions
1. **Separation of concerns:** Local = Claude Code + analysis tools. VM = persistent services + LLM proxy.
2. **Telegram as notification bus:** All async alerts (market, health, chat) route through Telegram.
3. **GitHub Actions = orchestration layer:** Not just CI/CD — it's the scheduled automation backbone.
4. **Lyra prompt routing:** VM's `get_lyra_prompt()` selects model tier dynamically (Flash → Pro → Ollama) based on task complexity and cost.
5. **Graphify on both:** Local graph (771 nodes) maps the full YNAI5-SU codebase; VM graph (121 nodes) maps the active infrastructure. Both queryable for architecture questions.

---

## Graphify Findings Summary

### Local YNAI5-SU
- **79 files, 771 nodes, 1151 edges, 71 communities**
- Top abstraction: `_cg()` — CoinGecko gateway (17 edges, everything flows through it)
- Key finding: Perplexity news bridges 3 communities (trading, music, content distribution)
- 200 isolated nodes in health-monitor — documentation gap

### GCP VM YNAI5_AI_CORE
- **14 files, 121 nodes, 180 edges, 14 communities**
- Top abstraction: `main()` in dashboard — all 10 FastAPI routes register here
- Key finding: `read_heartbeat()` is the health bus — all status checks poll it
- No surprising cross-community connections (clean architecture)
