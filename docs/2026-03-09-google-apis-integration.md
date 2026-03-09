# Research: Google APIs — Free Tiers, Integration Plan
Date: 2026-03-09
Sources:
- https://ai.google.dev/gemini-api/docs/rate-limits
- https://aistudio.google.com/app/apikey
- https://ai.google.dev/gemini-api/docs/quickstart
- https://developers.google.com/youtube/v3
- https://developers.google.com/youtube/analytics

---

## Summary
Google gives away an extraordinary amount of AI capability for free.
Gemini API (AI Studio) = the best free AI API in existence right now.
Gmail is already connected via MCP — no setup needed.
YouTube API unlocks your own channel analytics + trending research.
Priority: Get Gemini API key first. Build sub-agent skill around it.

---

## ✅ Gmail — ALREADY INTEGRATED (No Setup Needed)

Gmail is connected via MCP and working RIGHT NOW.

**What Claude can do with your Gmail today:**
| Action | Command |
|--------|---------|
| Search emails | Search by sender, subject, label, date |
| Read emails / threads | Full email content |
| Create draft replies | Draft ready to review and send |
| List labels | See all Gmail labels and IDs |
| List drafts | See all saved drafts |

**Potential skills to build:**
- `/email-check [query]` — search for brand deals, platform notifications, collab requests
- `/email-draft [thread context]` — draft a reply to a business inquiry
- Alert on keywords: "partnership", "collaboration", "sponsorship", "payment"

**Account confirmed:** shemarpantophlet@gmail.com | 71,488 messages

---

## 🔥 Gemini API — FREE, BEST VALUE, BUILD THIS FIRST

**Get your API key here:** https://aistudio.google.com/app/apikey
(Just sign in with your Google account — no billing required)

### Free Tier Limits (2026)

| Model | RPM | TPM | RPD | Best For |
|-------|-----|-----|-----|----------|
| **Gemini 2.0 Flash** | 15 | 1M | 1,500 | Fast tasks, automation, scripting |
| **Gemini 2.5 Flash** | 10 | 250K | 250 | Balanced quality + speed |
| **Gemini 2.5 Pro** | 5 | 250K | 100 | Complex analysis, long context |

**Key advantages over other free APIs:**
- **1 million token context window** — can analyze entire videos, long transcripts
- **Multimodal** — understands images, audio, video natively
- **Key doesn't expire** — set it once, use forever
- **No credit card required** for free tier

### What Gemini Adds to Your Stack
| Use Case | How It Helps |
|----------|-------------|
| **Video analysis** | Feed it a YouTube video URL → it analyzes content, trends, structure |
| **Image understanding** | Analyze screenshots of TikTok analytics, describe what's trending |
| **Long-form research** | 1M context = feed it entire transcripts, multiple articles at once |
| **Script writing** | Gemini 2.5 Pro rivals Claude for creative writing, second opinion |
| **Trend analysis** | Feed trending content → extract patterns → suggest hooks |

### Sub-Agent Skill Plan: `/gemini [task]`
```python
# Simple Python sub-agent: calls Gemini API for specific tasks
# Tasks: analyze, summarize, compare, research, generate-script
# Reads GEMINI_API_KEY from .env.local
# Endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
```

### Setup Steps (5 minutes):
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API key"
3. Copy key → add to `.env.local`:
   ```
   GEMINI_API_KEY=AIza...your_key_here
   ```
4. Claude builds sub-agent skill around it

---

## 📺 YouTube Data API v3 — FREE (10,000 units/day)

**What it does:** Access YouTube video data, search trends, channel analytics

**Get key:** Google Cloud Console → https://console.cloud.google.com → Enable YouTube Data API v3

### Free Quota
- 10,000 units per day (resets at midnight PT)
- Cost per operation: Search = 100 units | Video details = 1 unit | Channel info = 1 unit
- At 100 units/search: you get ~100 searches/day for free

### What This Unlocks for YNAI5 World
| Use Case | API Cost |
|----------|---------|
| Search trending AI/crypto videos | 100 units/search |
| Get video stats (views, likes, comments) | 1 unit/video |
| Find competitor channel top videos | 100 + 1 units |
| Get channel subscriber count | 1 unit |
| List your own uploaded videos | 1-5 units |

### Skill Plan: `/yt-trends [niche]`
- Search YouTube for trending videos in a niche (AI tools, crypto, etc.)
- Pull top 10 results with view counts, published date, titles
- Claude analyzes: what hooks work, what formats are trending
- Save findings to niche research log in content-tracker.md

---

## 📊 YouTube Analytics API — FREE (Your Own Channel Only)

**What it does:** Real-time stats for YOUR YouTube channel.
**Access:** Same API key as YouTube Data API, but requires OAuth (your own account login)

- Views by day/week/month
- Watch time, audience retention data
- Traffic sources, device breakdown
- Revenue estimates (once monetized)

**Setup:** More complex (OAuth flow) — build this after first videos are live.

---

## 🔍 Google Custom Search API — SEMI-FREE

- 100 free searches/day via Programmable Search Engine
- Upgradeable: $5 per 1,000 queries
- **Better alternative for Claude:** Use WebSearch (already available) for general web search
- **Only worth setting up** if you need to search a specific site domain or index

**Verdict:** Skip for now — Claude's built-in WebSearch covers this.

---

## 📈 Google Trends — NO OFFICIAL API

Google Trends doesn't have an official API. Options:
- `pytrends` — unofficial Python library (scrapes Google Trends data)
- Apify Google Trends scraper (free tier available)
- **Practical approach:** Claude searches Google Trends manually via browser when needed

**Verdict:** Use manually for now. Can add pytrends later.

---

## 🗃️ Google Sheets API — FREE (but overkill for now)

- Can make CSV trackers into live Google Sheets with real-time sync
- More complex setup (OAuth required)
- **Verdict:** Current CSV system works fine. Add Sheets API in Phase 2 if needed.

---

## Integration Priority Order

| Priority | API | Action | Effort |
|----------|-----|--------|--------|
| **1st** | Gemini API | Get key → add to .env.local → build sub-agent | 10 min |
| **2nd** | YouTube Data API | Get key → build /yt-trends skill | 20 min |
| **3rd** | Gmail skills | Build /email-check skill (MCP already connected) | 15 min |
| Later | YouTube Analytics | After first videos are live | Medium |
| Later | Google Sheets | After CSV system needs upgrading | Medium |
| Skip | Google Trends | Manual is fine | — |

---

## .env.local After Google Setup

```
ELEVENLABS_API_KEY=sk_...your_key
GEMINI_API_KEY=AIza...your_key
YOUTUBE_API_KEY=AIza...your_key (can be same project as Gemini)
```

Note: YouTube Data API key and Gemini API key can both be in the same Google Cloud project.
