# 00_CONTEXT_README -- 00_YNAI5_CORE
> Pinned context file. Read this first when entering this folder.

## Role
Strategy, vision, and roadmap storage for the YNAI5 ecosystem.

## What Belongs Here
- Master roadmaps and project vision documents
- Quarterly / annual goal files
- CLAUDE.md snapshots (archival copies)
- PROTOCOL_HANDOFF.md -- shared Claude <-> Gemini communication log
- Playbooks subdirectory -- repeatable SOPs

## What Does NOT Belong Here
- Code, scripts, configs -> 01_Infrastructure_GCP
- Finance data -> 02_Finance_Markets
- Research docs -> 06_Knowledge_Base

## Current Contents
| File | Description |
|------|-------------|
| PROTOCOL_HANDOFF.md | Append-only Claude <-> Gemini task handoff log |
| playbooks/tiktok-video-assembly.md | SOP for video assembly pipeline |

## Agent Notes
- Claude: Update PROTOCOL_HANDOFF.md when handing off to Gemini. Append only -- never overwrite.
- Gemini: Read PROTOCOL_HANDOFF.md first. Append your response below the last Claude entry.
- Both: Strategy-only folder. No operational files here.
