---
name: content-batch
description: Daily content batch — dispatches parallel agents to produce 2 ready-to-upload videos from trend research to script to voice to Kling video. Outputs to social-media-automation/queue/YYYY-MM-DD/. Use when asked to "run content batch", "generate today's content", "batch content", or "/content-batch".
argument-hint: [optional niche override: brainrot|fantasy|news — defaults to today's rotation]
---

Run the daily content batch for Channel A (YNAI5 World).
Niche override (if provided): $ARGUMENTS

## Niche Rotation (auto if no override)
Check today's day of week and pick from schedule:
- Mon/Fri → AI News Reaction
- Tue/Thu/Sun → AI Brainrot
- Wed/Sat → Elemental/Fantasy AI

Reference: `projects/social-media-automation/channel-a-niches.md` for niche details.

---

## Phase 1 — Parallel Research (dispatch simultaneously)

**Launch 2 agents in parallel:**

**Agent A — Trend Research:**
Use the trend-check skill to find today's top AI topics. Focus on the niche for today's rotation. Return: top 2 topics with hooks.

**Agent B — Niche Read:**
Read `projects/social-media-automation/channel-a-niches.md` and return: today's niche name, prompt style, and audio direction.

Wait for both agents to finish before proceeding.

---

## Phase 2 — Parallel Script Generation

Using results from Phase 1, **dispatch 2 script agents in parallel:**

**Script Agent 1 (Primary — Niche A):**
Run `/content-gen [Topic 1 from trend check] tiktok`
Apply today's niche prompt style from channel-a-niches.md.

**Script Agent 2 (Secondary — fill niche):**
If today is brainrot day → write a brainrot-style script on [Topic 2]
If today is fantasy day → write a fantasy/elemental script (AI-generated armor/world)
If today is news day → write a reaction script on [Topic 2]

Both agents save scripts to `projects/social-media-automation/queue/[YYYY-MM-DD]/`.

Wait for both scripts to finish.

---

## Phase 3 — Asset Generation (run sequentially)

### Step 1 — Voice Over (Primary Script)
Run `/voice-gen` on the primary script text.
Save MP3 to `projects/social-media-automation/queue/[YYYY-MM-DD]/voice-primary.mp3`

### Step 2 — Video Generation (mcp-kling)
Check if mcp-kling is available in Claude Code tools.

**If mcp-kling IS available:**
Call mcp-kling with this prompt built from the primary script:
- Use the B-Roll keywords from the script as visual prompts
- Apply the niche's Kling prompt style from channel-a-niches.md
- Generate 1 video clip (5–10s)
- Save output path to `queue/[YYYY-MM-DD]/video-primary.mp4` (or URL if cloud)

**If mcp-kling is NOT yet configured:**
Skip video gen. Note: "⚠️ Kling not configured — add mcp-kling after subscribing at klingai.com"

### Step 3 — B-Roll Fetch (Secondary Script)
Use the Pexels API (PEXELS_API_KEY from .env.local) to fetch 3 B-roll clips for secondary script keywords.
Save clip URLs/paths to `queue/[YYYY-MM-DD]/broll-secondary.md`

If PEXELS_API_KEY is not set: skip and note it.

---

## Phase 4 — Queue Summary

Create `projects/social-media-automation/queue/[YYYY-MM-DD]/BATCH-SUMMARY.md` with:

```markdown
# Content Batch — [YYYY-MM-DD]
Niche Today: [Brainrot / Fantasy / News]

## Video 1 (Primary)
- Script: scripts/[filename].md
- Voice: voice-primary.mp3 [✅ / ❌ not generated]
- Video: video-primary.mp4 [✅ / ⚠️ Kling needed]
- Duration: ~[X]s
- Upload to: TikTok + YouTube Shorts

## Video 2 (Secondary)
- Script: scripts/[filename].md
- B-Roll: broll-secondary.md [✅ / ❌]
- Assemble in: CapCut (< 5 min)
- Upload to: TikTok only (test performance first)

## Upload Checklist
- [ ] Review both scripts for tone (YNAI5 brand voice)
- [ ] Check video/VO quality
- [ ] TikTok: add trending sound if VO not used
- [ ] Caption: use Option A from script file
- [ ] Upload primary first, secondary 4–6 hrs later

## Next Step
Upload primary to TikTok. Watch 48hr retention. Double down on winner niche.
```

---

## Output in Chat

After completing all phases, print:

```
✅ CONTENT BATCH COMPLETE — [YYYY-MM-DD]

Niche: [Today's niche]

📄 Script 1: [topic] → queue/[date]/scripts/[file]
📄 Script 2: [topic] → queue/[date]/scripts/[file]
🎙️ Voice: [✅ generated / ❌ skipped]
🎬 Kling Video: [✅ generated / ⚠️ Kling not configured yet]
🎞️ B-Roll: [✅ X clips fetched / ❌ skipped]

📁 Full batch: projects/social-media-automation/queue/[date]/BATCH-SUMMARY.md

⏱️ Upload schedule:
• Video 1 → TikTok now + YouTube Shorts
• Video 2 → TikTok in 4–6 hrs

Block Syndicate funnel: activate when Channel A hits 1K+ followers.
```
