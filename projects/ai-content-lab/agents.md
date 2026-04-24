# AI Content Lab — Agents

_Lightweight model: Manager / Worker / Research. Activates only post-unlock._

## Manager Agent
**Identity:** Claude Code (operator's working session)
**Role:** Approves trends, picks daily topic, reviews scripts pre-voice, final-pass video before upload
**Inputs:** `/trend-check` output, `tasks.md`, niche rotation calendar
**Outputs:** Approved-to-publish flag, queue/YYYY-MM-DD/posted/ moves
**Cadence:** Daily 8–9 AM AST (15 min review window)
**Boundaries:** Never auto-uploads. Operator approves every video.

## Worker Agent
**Identity:** `/content-batch` skill + Kling MCP + ElevenLabs API + Pexels API
**Role:** Generates daily batch — script → voice → video → captions → B-roll keywords
**Inputs:** Daily trend (from Research), niche rotation slot, character bible
**Outputs:** `queue/YYYY-MM-DD/{topic}/` folder with all assets ready to assemble
**Cadence:** Once daily, 6 AM AST (so output ready by Manager review window)
**Boundaries:** No publishing. No external API calls beyond the 4 listed. Stays under free-tier quotas.

## Research Agent
**Identity:** `/trend-check` skill + `/niche-finder` skill + Brave Search MCP
**Role:** Daily trend scan + weekly niche pulse + monthly competitor analysis
**Inputs:** TikTok For You sample, Twitter trending, AI news headlines
**Outputs:** Top 5 trends with virality scores → fed to Worker
**Cadence:** Daily 5 AM AST (1 hour before Worker)
**Boundaries:** Read-only. Doesn't generate content. Hands off to Worker.

## Decision: No more agents
A "publisher" agent (auto-upload to TikTok/Reels) tempting but BLOCKED by:
- TikTok API access requires business verification
- Risk of TOS violation if auto-publishing without operator review
Decision: stay manual on the upload step.
