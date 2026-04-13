# Graph Report - .  (2026-04-13)

## Corpus Check
- 14 files · ~15,642 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 121 nodes · 180 edges · 14 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 10 edges
2. `read_heartbeat()` - 8 edges
3. `fetchStatus()` - 8 edges
4. `main()` - 6 edges
5. `get_status_compat()` - 6 edges
6. `boot()` - 6 edges
7. `get_lyra_prompt()` - 5 edges
8. `route_and_run()` - 5 edges
9. `chat()` - 5 edges
10. `get_status()` - 5 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (23): BaseModel, delete_task(), get_claude_logs(), get_gemini_logs(), get_heartbeat(), get_service_status(), get_status(), get_status_compat() (+15 more)

### Community 1 - "Community 1"
Cohesion: 0.32
Nodes (11): get_billing_logs(), get_checks(), get_containers(), get_docker_logs(), get_logs(), get_orchestrator_logs(), get_ram(), get_spend() (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (9): call_gemini(), call_gemini_api(), call_gemini_cli(), classify_task(), get_lyra_prompt(), log_decision(), Fallback: use gemini CLI if API call fails., Build the full Lyra 5-layer system prompt with live VM context. (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.29
Nodes (9): build_system_prompt(), call_gemini(), call_gemini_vertex(), chat(), get_env(), get_vm_context(), Call Gemini 1.5 Pro via Vertex AI using service account credentials ($10/month c, Returns safe VM config for dashboard JS — NO API keys ever. (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.33
Nodes (9): get_gcp_spend(), get_openrouter_balance(), is_month_end(), log_alert(), main(), Get GCP spend via gcloud CLI (no service account needed)., Get OpenRouter remaining credits., Check if we're in the last 3 days of the month. (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.44
Nodes (9): fetchStatus(), getDetailText(), initMetrics(), renderBudget(), renderServiceLogs(), renderStatusBoard(), renderSystemMetrics(), setEl() (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.39
Nodes (8): appendMsg(), appendWelcome(), escHtml(), hideTyping(), initChat(), sendMessage(), setLoading(), showTyping()

### Community 7 - "Community 7"
Cohesion: 0.52
Nodes (6): boot(), checkAuth(), initKillSwitch(), initLogTabs(), initNav(), initTabs()

### Community 8 - "Community 8"
Cohesion: 0.4
Nodes (0): 

### Community 9 - "Community 9"
Cohesion: 0.6
Nodes (3): applyTheme(), initTheme(), toggleTheme()

### Community 10 - "Community 10"
Cohesion: 0.4
Nodes (4): log_event(), Append a structured event to YNAI5Logs. Keeps last 200 entries., Read last N events from YNAI5Logs., read_logs()

### Community 11 - "Community 11"
Cohesion: 0.5
Nodes (0): 

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (2): setup(), w()

### Community 13 - "Community 13"
Cohesion: 0.67
Nodes (0): 

## Knowledge Gaps
- **13 isolated node(s):** `Build the full Lyra 5-layer system prompt with live VM context.`, `Fallback: use gemini CLI if API call fails.`, `Call Gemini 1.5 Pro via Vertex AI using service account credentials ($10/month c`, `Returns safe VM config for dashboard JS — NO API keys ever.`, `Get GCP spend via gcloud CLI (no service account needed).` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Build the full Lyra 5-layer system prompt with live VM context.`, `Fallback: use gemini CLI if API call fails.`, `Call Gemini 1.5 Pro via Vertex AI using service account credentials ($10/month c` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._