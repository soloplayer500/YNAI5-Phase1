---
name: docker
description: Run Docker commands on demand. Automatically starts Docker Desktop if not running. No manual startup needed ever.
---

# Docker On-Demand Skill

## What I Do
Execute Docker commands — auto-starting Docker Desktop if it's closed. You never need to manually open Docker again.

## Usage
- `/docker status` — is Docker running?
- `/docker start` — start Docker Desktop (takes ~30-60s)
- `/docker ps` — list containers
- `/docker [any command]` — runs it (auto-starts Docker first)

## Steps

1. Extract the Docker command from user's request

2. Run:
```bash
python "C:/Users/shema/OneDrive/Desktop/YNAI5-SU/projects/system-health/docker-manager.py" [command]
```

3. If Docker is starting: tell user "Starting Docker Desktop, ~30-60s..."

4. Show output. Ask if they need anything else with Docker.

## Notes
- On 8GB RAM: avoid running many containers simultaneously
- Docker MCP Toolkit: once running, 100+ MCP servers available in Docker Desktop extensions
