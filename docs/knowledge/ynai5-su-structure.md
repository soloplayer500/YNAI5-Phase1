# YNAI5-SU Workspace Knowledge

_Generated: 2026-04-13 | Graphify v0.4.11 + Mermaid Visualizer skill_

---

## YNAI5-SU Folder Structure

```mermaid
graph TB
    root["YNAI5-SU (Root)"]

    subgraph config["Configuration & Meta"]
        claude[".claude/\n(rules, skills, hooks)"]
        github[".github/\n(CI/CD workflows)"]
        gsync["drive-sync/\n(GDrive sync layers)"]
    end

    subgraph knowledge["Knowledge & Memory"]
        context["context/\n(profile, priorities,\nsession state, goals)"]
        memory["memory/\n(MEMORY.md, preferences,\npatterns, decisions-log)"]
        decisions["decisions/\n(decision archives)"]
        sessions["sessions/\n(per-session summaries)"]
        notes["notes/\n(scratch ideas)"]
    end

    subgraph docs_grp["Documentation"]
        docs["docs/\n(research + claude-docs\n+ knowledge + plans)"]
        playbooks["playbooks/\n(repeatable SOPs)"]
        actions["actions/\n(open TODO items)"]
    end

    subgraph infra["Infrastructure & Tools"]
        health["health-monitor/\n(Phase 2 daemon:\ncollect→evaluate→persist)"]
        tools["tools/\n(utility scripts)"]
        gout["graphify-out/\n(knowledge graph:\n771 nodes, 1151 edges)"]
    end

    subgraph assets_grp["Assets"]
        assets["assets/ynai-world/\n(YNAI5 visual library:\ncharacters, environments, brand)"]
    end

    subgraph projects_grp["Projects (11 Active)"]
        crypto["crypto-monitoring/\n(Kraken, alerts, screener)"]
        passive["passive-income/\n(Block Syndicate\nTelegram channel)"]
        social["social-media-automation/\n(TikTok/YT/IG pipeline)"]
        vm["vm-dashboard/\n(GCP VM FastAPI)"]
        mcps["ynai5-mcps/\n(custom MCP servers)"]
        niche["niche-research/\n(BRAINAI5 V3 agent)"]
        syshealth["system-health/\n(session backup,\nbootstrap, health)"]
        psyche["psychecore/\n(AI reasoning framework)"]
        ralph["ralph-automation/\n(autonomous dev agent)"]
        prompt["multi-ai-prompt-optimization/\n(CPO, LYNX-K)"]
        personal["personal-ai-infrastructure/\n(AI ecosystem design)"]
    end

    root --> config
    root --> knowledge
    root --> docs_grp
    root --> infra
    root --> assets_grp
    root --> projects_grp

    style root fill:#e7f5ff,stroke:#1971c2,color:#1971c2
    style config fill:#f8f9fa,stroke:#868e96
    style knowledge fill:#fff4e6,stroke:#e67700
    style docs_grp fill:#e5dbff,stroke:#5f3dc4
    style infra fill:#ffe8cc,stroke:#d9480f
    style assets_grp fill:#f3d9fa,stroke:#862e9c
    style projects_grp fill:#d3f9d8,stroke:#2f9e44

    style crypto fill:#d3f9d8,stroke:#2f9e44
    style passive fill:#d3f9d8,stroke:#2f9e44
    style social fill:#c5f6fa,stroke:#0c8599
    style vm fill:#c5f6fa,stroke:#0c8599
    style mcps fill:#ffe3e3,stroke:#c92a2a
    style niche fill:#ffe3e3,stroke:#c92a2a
    style syshealth fill:#ffe8cc,stroke:#d9480f
    style psyche fill:#e5dbff,stroke:#5f3dc4
    style ralph fill:#e5dbff,stroke:#5f3dc4
    style prompt fill:#fff4e6,stroke:#e67700
    style personal fill:#f8f9fa,stroke:#868e96
```

_Renders in Obsidian (graph view), GitHub markdown, and any Mermaid-compatible renderer._

---

## Graphify Knowledge Graph Summary

_Source: `graphify-out/GRAPH_REPORT.md` — AST-extracted, 0 tokens used_

| Metric | Value |
|--------|-------|
| Files analyzed | 79 |
| Total words | ~172,133 |
| Graph nodes | 771 |
| Graph edges | 1,151 |
| Communities detected | 71 |

### Core Abstractions (God Nodes — Most Connected)

| Rank | Node | Edges | Domain |
|------|------|-------|--------|
| 1 | `_cg()` | 17 | CoinGecko price fetcher (crypto monitoring) |
| 2 | `get_portfolio_summary()` | 13 | Kraken portfolio aggregator |
| 3 | `_get()` | 13 | Generic HTTP getter (music/media MCP) |
| 4-8 | `main()` (×5) | 10–12 | Entry points across 5 different scripts |
| 9 | `full_technical_analysis()` | 10 | Trading signals MCP |
| 10 | `save_backup()` | 9 | Session backup engine |

### Key Functional Communities

| Community | Size | Domain |
|-----------|------|--------|
| Community 0 | 66 nodes | Trading signals — Kraken, technical analysis, indicators |
| Community 2 | 29 nodes | Kraken portfolio — balance, orders, price monitoring |
| Community 5 | 27 nodes | Content distribution — cross-platform formatting, social media |
| Community 6 | 26 nodes | Block Syndicate — crypto/stock screener signals |
| Community 7 | 22 nodes | VM Dashboard — FastAPI, service status, logs |
| Community 8 | 22 nodes | Session Backup Engine — compact/stop/start hooks |
| Community 16 | 12 nodes | Health Monitor daemon — Windows laptop metrics |
| Community 20 | 12 nodes | Kimi Swarm — parallel K2.5 agent dispatch |

### Surprising Connections Found by Graphify
- Kraken order book → content distribution formatter (`format_for_platform`)
- Perplexity news fetcher → Genius music search (`get_artist_songs`)
- Perplexity news → Kraken balance check (unified news-to-finance bridge)
- OHLC candle data → trading signals computation (direct pipeline link)

### Knowledge Gaps (200 isolated nodes)
Most isolated nodes are in the health-monitor subsystem — components that need better cross-linking or documentation to show their role in the broader architecture.
