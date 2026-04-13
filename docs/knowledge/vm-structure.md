# YNAI5_AI_CORE — VM Structure & Knowledge Graph

_Generated: 2026-04-13 | GCP VM @ 34.45.31.188 (e2-micro) | Graphify v0.4.11_

---

## VM Project Structure (Mermaid)

```mermaid
graph TB
    root["YNAI5_AI_CORE\n「GCP e2-micro @ 34.45.31.188」"]

    subgraph services["Active Services"]
        chat["chat_server.py\n「port 8001 — Flask」\nGemini + Vertex AI proxy\nLyra prompt routing"]
        orch["orchestrator.py\nAgent task dispatch\nClaude + Gemini workers"]
    end

    subgraph dash["dashboard/ 「port 8000 — FastAPI」"]
        main_py["main.py\n10 endpoints\ngod node — 10 edges"]
        dash_ui["index.html + assets/\nReact-style frontend\nfetchStatus 「8 edges」"]
        dash_cfg["config/\nagents.json\nmodels.json 「phi3:mini rank-1」"]
    end

    subgraph docker_stack["Docker Stack 「docker-compose.yml」"]
        n8n["n8n\nport 5678\nWorkflow automation"]
        searxng["SearXNG\nSelf-hosted search"]
        portainer["Portainer\nContainer management"]
    end

    subgraph skills_grp["skills/ 「10 skill docs」"]
        ai_routing["ai-routing.md\nLyra prompt layer"]
        other_skills["billing.md\ndashboard.md\nn8n.md\ndocker.md\nsearxng.md\nmcp.md\nportainer.md"]
    end

    subgraph infra["Infrastructure"]
        logs["logs/\nchat.log\nynai5logs.json\nstatus.log\nuptime.log"]
        scripts["scripts/\ngdrive-backup.sh\nynai5_logger.py"]
        finance["FINANCE/\nbilling_sentinel.py\nbilling_cron.sh"]
        state["state_files.py\nstatus_writer.py\nynai5-vm-state.md"]
        gout_vm["graphify-out/\n121 nodes, 180 edges\n14 communities"]
    end

    root --> services
    root --> dash
    root --> docker_stack
    root --> skills_grp
    root --> infra

    chat -->|"LLM calls"| ai_routing
    orch -->|"dispatches to"| chat
    main_py --> dash_ui
    main_py --> dash_cfg

    style root fill:#e7f5ff,stroke:#1971c2,color:#1971c2
    style services fill:#d3f9d8,stroke:#2f9e44
    style dash fill:#e5dbff,stroke:#5f3dc4
    style docker_stack fill:#ffe8cc,stroke:#d9480f
    style skills_grp fill:#fff4e6,stroke:#e67700
    style infra fill:#f8f9fa,stroke:#868e96

    style chat fill:#d3f9d8,stroke:#2f9e44
    style orch fill:#d3f9d8,stroke:#2f9e44
    style main_py fill:#e5dbff,stroke:#5f3dc4
    style dash_ui fill:#c5f6fa,stroke:#0c8599
    style dash_cfg fill:#fff4e6,stroke:#e67700
    style n8n fill:#ffe8cc,stroke:#d9480f
    style searxng fill:#ffe3e3,stroke:#c92a2a
    style portainer fill:#f3d9fa,stroke:#862e9c
    style ai_routing fill:#ffe8cc,stroke:#d9480f
    style gout_vm fill:#c5f6fa,stroke:#0c8599
```

_Renders in Obsidian, GitHub markdown, and any Mermaid-compatible renderer._

---

## Graphify VM Knowledge Graph Summary

_Source: `graphify-out/GRAPH_REPORT.md` — AST-extracted, 0 tokens used_

| Metric | Value |
|--------|-------|
| Files analyzed | 14 |
| Total words | ~15,642 |
| Graph nodes | 121 |
| Graph edges | 180 |
| Communities detected | 14 |

### God Nodes (Most Connected)

| Rank | Node | Edges | Domain |
|------|------|-------|--------|
| 1 | `main()` (dashboard) | 10 | FastAPI app entry — all routes registered here |
| 2 | `read_heartbeat()` | 8 | Health pulse reader — polled by all status checks |
| 3 | `fetchStatus()` | 8 | JS frontend status poller — drives dashboard UI |
| 4 | `main()` (chat) | 6 | Flask chat server entry |
| 5 | `get_status_compat()` | 6 | Compat endpoint — translates /api/status for metrics.js |
| 6 | `boot()` | 6 | Frontend boot — initializes all dashboard modules |
| 7 | `get_lyra_prompt()` | 5 | Lyra prompt router — AI model selection layer |
| 8 | `route_and_run()` | 5 | Chat request router — Gemini/Vertex/Ollama dispatch |
| 9 | `chat()` | 5 | Flask /chat endpoint handler |
| 10 | `get_status()` | 5 | Primary /api/status endpoint |

### Key Communities

| Community | Size | Domain |
|-----------|------|--------|
| Community 0 | 23 nodes | FastAPI dashboard — all REST endpoints, heartbeat, metrics |
| Community 1 | ~8 nodes | Chat server — Flask, Lyra prompt routing, model dispatch |
| Community 9 | ~4 nodes | JavaScript frontend — theme toggle, UI initialization |

### Surprising Connections
None detected (all connections within same source files — VM project is well-encapsulated with clear boundaries).

---

## VM Quick Reference

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| FastAPI Dashboard | 8000 | Active | main.py — health, status, tasks, logs |
| Flask Chat Server | 8001 | Active | Gemini + Vertex AI proxy + Lyra routing |
| nginx | 80 | Active | Reverse proxy for both services |
| n8n | 5678 | Active | Workflow automation (via Docker) |
| SearXNG | - | Active | Self-hosted search (via Docker) |
| Portainer | - | Active | Container management |
| Ollama | 11434 | Disabled | phi3:mini installed — enable when ready |

---

## Graphify Permanent Install on VM

```bash
# Rebuild graph after code changes:
export PATH=$PATH:/home/shema/.local/bin
cd ~/YNAI5_AI_CORE && graphify update .

# Query the graph:
graphify query "your question"

# Explain a node:
graphify explain "main()"
```

PATH is permanently added to `~/.bashrc`.
