# Social Media Strategy — YNAI5 World
Last Updated: 2026-03-28 (Session 15 — Dual-Channel Architecture + Kling AI)

---

## Dual-Channel Architecture (ACTIVE)

### Channel A — Growth Engine (YNAI5 World)
**Goal:** Follower base. No monetization pressure. Feed the algorithm.
**Content niches:** AI Brainrot / Elemental Fantasy AI / AI News Reactions
**Full niche definitions:** `channel-a-niches.md`
**Automation:** `/content-batch` → 2 videos/day dispatched via parallel Claude agents

### Channel B — Revenue Engine (Block Syndicate)
**Goal:** Paid Telegram subs ($9.99/mo). Crypto + stock signals.
**Status:** Infrastructure live (screener-channel-bot.py, GitHub Actions 8AM AST)
**Funnel activation:** when Channel A hits 1K+ followers → add CTA → drive to screener

### Funnel Flow
```
TikTok/Shorts (Channel A) → bio link → Free Telegram → VIP upgrade (Gumroad $9.99/mo)
```

---

---

## YouTube Strategy

**Channel Brand:** YNAI5 World
**Niche:** AI-native creator — AI music (Suno), AI stories, AI automation, crypto/finance content
**Target Audience:** AI-curious people, crypto followers, automation enthusiasts, content creator community
**Upload Cadence:** 2–3x per week (automated pipeline target)

**Content Pillars:**
1. AI Music Videos — Suno-generated tracks with visuals (pending Distrokid for distribution)
2. AI Stories & News — AI-generated storytelling, AI world news, crypto market stories
3. AI Automation Tutorials — How to use AI tools, build systems, make money with AI

**Growth Tactics:**
- SEO-optimized titles and descriptions (research trending keywords)
- YouTube Shorts for discovery → funnel to long-form
- Thumbnail A/B testing — high contrast, faces or bold text
- End screen CTAs to TikTok and Instagram
- Consistent upload schedule (algorithm rewards consistency)

**Monetization Path:**
- YouTube Partner Program: 1,000 subscribers + 4,000 watch hours
- Channel memberships, Super Thanks after monetization
- Affiliate links (AI tools, crypto platforms)

**Current Metrics:**
- Subscribers: —
- Avg Views: —
- Best Performing Video: —

---

## TikTok Strategy

**Phase 1 (NOW — Active):** AI News but Funny / Relatable
**Phase 2 (After traction):** AI Tools + Finance/Crypto Hybrid (high RPM)
**Phase 3 (Long game):** YNAI5 World cartoon universe (brand building)

### Phase 1 Format — MVP
**Vibe:** Normal user TikTok energy — rapid, casual, slightly chaotic, very shareable
**Niche:** AI/tech news reaction — "bro did you see what Claude/Gemini just did??"
**Tone:** Cliché funny, relatable, slightly shocked — like texting your friend about wild AI news
**Length:** 15–40 seconds
**Hook (first 2 sec):** shock/curiosity — "nobody's talking about this" / "wait they actually did this?"
**Body:** show the actual update/moment, quick reaction, funny observation
**End:** punchline or mini-cliffhanger + "follow for AI updates"
**Posting Cadence:** 1x per day minimum — batch produce 5 at a time
**Target Audience:** Gen Z/Millennial, casually AI-curious, regular TikTok scrollers

**Why this works:**
- Authentic casual energy = algorithm-friendly (TikTok disfavors polished AI slop)
- AI news = always fresh, always shareable
- Funny angle = comments, saves, shares > passive views
- Builds audience AND teaches us what content format/topic resonates
- Low production cost — can do text-on-screen + voiceover, no need for Sora every video

**Growth Tactics:**
- Post during peak hours (7–9am, 12–1pm, 7–9pm AST)
- Trending audio under the voiceover
- Stitch/Duet real AI demos to add your reaction layer
- Hooks that create curiosity gaps ("this changes everything" / "they added WHAT")

**Goal:** First 1,000 followers → identify best-performing format → move to Phase 2

**Current Metrics:**
- Followers: —
- Avg Views: —

---

## Instagram Strategy

**Role:** Supporting layer — awareness, cross-posting, alerts, re-engagement
**Niche:** AI news alerts, crypto market updates, YouTube/TikTok content reposts
**Posting Cadence:** 4–5x per week (repurposed content + Stories)
**Content Mix:** 50% Reels (TikTok reposts) | 30% Carousels (AI/crypto news) | 20% Stories

**Content Types:**
- Reels: Direct reposts from TikTok
- Carousels: "5 AI tools that..." or "Crypto this week" roundups
- Stories: Daily market moves, AI tool tips, polls, links to YouTube

**Growth Tactics:**
- Hashtag strategy: AI, crypto, automation, content creation tags
- Link in bio → YouTube channel
- Story polls to drive engagement

**Current Metrics:**
- Followers: —
- Avg Reach: —

---

## Cross-Platform Content Flow
```
Idea (content-tracker.md)
  → Produce once
    → Post on TikTok first (highest organic reach)
      → Repost to Instagram Reels (same day)
        → Expand to YouTube if it performs well
```

## Tools Being Used / Planned
| Tool | Purpose | Status |
|------|---------|--------|
| Claude | Niche research, scripts, captions, tracker | Active |
| Suno | AI music generation | Active |
| ElevenLabs | AI voiceover (TTS) | Active — free 10K credits/month |
| ChatGPT Sora | AI video generation (PRIMARY) | Active — included in Pro |
| Kling 2.6 | AI video generation (backup) | Active — free daily credits |
| Seedance 2.0 | AI video generation (backup) | Active — free daily credits |
| CapCut | Video assembly + captions | Active — free |
| ComfyUI (Pinokio) | Image generation (CPU-based) | Installed — slow but usable |
| Distrokid | Music distribution to YouTube | Planned (pending purchase) |
| Buffer / Later | Auto-posting scheduler | Research needed |
