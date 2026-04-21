# 00_CONTEXT_README — 06_Knowledge_Base
> 📌 Pinned context file. Read this first when entering this folder.

## Role
Research archive and reference library. All research outputs, PDFs, Claude documentation, and architecture diagrams live here.

## What Belongs Here
- Research docs from `/research` skill (YYYY-MM-DD-topic.md format)
- Architecture diagrams and knowledge graphs
- Claude API documentation and upgrade notes
- Niche research outputs from `/niche-finder`
- Tool comparison docs (e.g. higgsfield-vs-kling.md)
- External PDFs, whitepapers, reference materials

## What Does NOT Belong Here
- Active project files → their respective project folders
- Finance research → `02_Finance_Markets`
- Infrastructure docs → `01_Infrastructure_GCP`

## Current Contents
| File | Description |
|------|-------------|
| `2026-03-10-crypto-market-dynamics.txt` | BTC dominance, amplification effect, capital rotation study |
| `2026-03-22-higgsfield-vs-kling.md` | Video gen tool comparison — verdict: Kling Standard wins |

## Agent Notes
- **Naming convention:** Always use `YYYY-MM-DD-topic.md` for new research docs.
- **Claude:** After any `/research` skill run, push the output here via `/gdrive-org`.
- **Gemini:** This is your primary reference library for background context on YNAI5 decisions.
- **Index:** All docs here should also be listed in `local:docs/INDEX.md`.
