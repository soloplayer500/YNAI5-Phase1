# Research: ChatGPT API + Sora API + OpenAI MCP
Date: 2026-03-09
Sources:
- https://platform.openai.com/docs/guides/video-generation
- https://platform.openai.com/docs/models/sora-2
- https://github.com/mzxrai/mcp-openai
- https://developers.openai.com/api/docs/mcp/
- https://community.openai.com/t/built-an-mcp-server-that-connects-chatgpt-claude-gemini-perplexity-to-ai-coding-tools-no-api-keys-needed/1373147

---

## Summary
Sora has a live public API (Videos API, in preview). OpenAI and Anthropic both adopted MCP — OpenAI MCP servers exist that let Claude call GPT-4 and potentially Sora. Two build paths: (1) OpenAI API key → `/sora-gen` skill, (2) MCP server for full OpenAI tool access from Claude.

---

## Key Findings

### 1. Sora API — EXISTS and is Available
- **Endpoint:** `https://api.openai.com/v1/videos/generations`
- **Models:** `sora-2` (fast, cheaper) | `sora-2-pro` (higher quality, slower)
- **Endpoints available:** Create video, Get status (async), Download video, List videos
- **Access:** Requires OpenAI API key + API credits (SEPARATE from ChatGPT Pro subscription)
- **Format support:** 9:16 vertical (TikTok-native) confirmed
- **Cost estimate:** ~$0.01–0.03/second generated → 8-sec clip ≈ $0.08–$0.24

### 2. OpenAI + Anthropic MCP (Both Adopted Jan 2026)
- Both platforms announced MCP app support simultaneously (January 2026)
- MCP 1.0 spec targeting June 2026 (Linux Foundation governance)
- OpenAI Connectors = essentially MCP wrappers
- Existing open-source MCP server: `mcp-openai` on GitHub — lets Claude call OpenAI models

### 3. GPT-4 via MCP from Claude
- `mcp-openai` server: Claude Desktop → config → add OpenAI MCP → access GPT-4 from Claude
- No API keys needed for some implementations (community-built)
- Use case: run GPT-4 analysis as sub-agent from Claude, compare outputs

---

## Build Options for YNAI5-SU

### Option A: `/sora-gen` Skill (RECOMMENDED — needs OpenAI API key)
Build a skill similar to `/gemini` that:
- Reads `OPENAI_API_KEY` from `.env.local`
- Calls `POST /v1/videos/generations` with prompt + reference image
- Polls for completion (async operation)
- Downloads video to `projects/social-media-automation/videos/`

**Cost:** Pay-per-use (~$0.08–$0.24 per 8-sec clip) — affordable for testing
**Benefit:** Full automation — Claude generates Sora video without ChatGPT UI

### Option B: OpenAI MCP Server (for GPT-4 access from Claude)
- Install `mcp-openai` server in Claude Desktop config
- Gives Claude access to GPT-4 as a sub-agent tool
- Useful for: research, content drafts, second opinions from GPT
- Does NOT automate Sora (Sora is different from GPT-4)

### Option C: Manual (Current — No API Key Needed)
- ChatGPT Pro subscription → Sora tab → manual generation
- Free within Pro tier, unlimited
- Download manually, bring to CapCut
- No setup, works today

---

## Recommendation for Now
**Option C (manual) → then build Option A when we want automation**

Current state: ChatGPT Pro already paid = free Sora generations.
Next step: Get OpenAI API key (free to create, pay only when used) → build `/sora-gen`.
This turns manual → automated pipeline later.

---

## Next Steps
1. **Now:** Use ChatGPT Pro UI manually for Sora batch 001
2. **Soon:** Get OpenAI API key at platform.openai.com/api-keys
3. **Build:** `/sora-gen` skill → automated Sora from Claude via code
4. **Optional:** Add OpenAI MCP server to Claude Desktop for GPT-4 sub-agent access
