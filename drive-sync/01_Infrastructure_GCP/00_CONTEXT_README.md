# 00_CONTEXT_README -- 01_Infrastructure_GCP
> Pinned context file. Read this first when entering this folder.

## Role
All VM infrastructure, MCP configs, deployment scripts, and cross-agent context files.

## What Belongs Here
- VM scripts and systemd service configs
- MCP server definition files
- 05_Work_Profile.md -- cross-device context injection file
- Architecture diagrams (combined-architecture.md, vm-structure.md)
- CROSS_MODEL_SYNC/ subfolder -- files shared between Claude, Gemini, and Kimi

## CROSS_MODEL_SYNC Subfolder
| File | Purpose |
|------|---------|
| CORE_IDENTITY.md | Universal AI identity and persona guide |
| UNIVERSAL_AI_GUIDE.md | Collaboration rules for all agents |
| PROTOCOL_HANDOFF.md | Mirrored copy of the handoff log |

## Current Contents
| File | Description |
|------|-------------|
| 05_Work_Profile.md | Active project, next steps, system state -- update at session end |
| combined-architecture.md | Full infra map: local <-> VM <-> GitHub Actions <-> APIs |
| vm-structure.md | VM directory layout and service reference table |

## Agent Notes
- New device / new session: Read 05_Work_Profile.md FIRST.
- Gemini handoff: Place files in CROSS_MODEL_SYNC/ before ending session.
- SSH to VM: ssh -i ~/.ssh/google_compute_engine shema@34.45.31.188
- Run maintenance: bash /ynai5_runtime/scripts/maintenance.sh
