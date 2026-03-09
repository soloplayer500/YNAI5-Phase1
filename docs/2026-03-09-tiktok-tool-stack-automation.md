# Research: TikTok AI Tool Stack + Automation Pipeline
Date: 2026-03-09
Sources:
- https://pinokio.co/docs/
- https://autoshorts.ai/
- https://elevenlabs.io/
- https://magichour.ai/blog/elevenlabs-pricing
- https://www.superside.com/blog/ai-tiktok-generators
- https://zenn.dev/taku_sid/articles/20250507_capcutapi_mcp

---

## Summary
A full TikTok AI content pipeline is buildable with your current stack (Claude + ChatGPT Pro + Pinokio)
at near-zero marginal cost. Most steps can be automated — upload to TikTok remains manual
due to API restrictions. Pinokio is your secret weapon: free unlimited local video/image generation.

---

## Your Current Stack vs What's Needed

| You Have | Role in Pipeline | Cost |
|----------|-----------------|------|
| Claude Pro | Script, caption, strategy, research | Already paid |
| ChatGPT Pro | DALL-E 3 images, Sora video (limited) | Already paid |
| Kimi Pro | Long-context script drafting | Already paid |
| Gemini | Image gen (Imagen 3), video analysis | Already paid |
| Suno | AI music for videos | Already have |
| Pinokio (localhost) | LOCAL video/image gen — FREE unlimited | Already have |

---

## Full TikTok Production Stack

### 🎬 Video Generation (Pick 1 to start)
| Tool | Type | Quality | Cost | Verdict |
|------|------|---------|------|---------|
| **Pinokio + Wan2.1** | Local, text-to-video | High | FREE (unlimited) | ✅ Best for zero cost |
| **Pinokio + ComfyUI** | Local, image+video | Very High | FREE (unlimited) | ✅ Most powerful |
| **ChatGPT Pro (Sora)** | Cloud, text-to-video | Excellent | Included (limited) | Use for hero content |
| InVideoAI | Cloud, prompt-to-TikTok | Good | Free tier | ✅ Fastest pipeline |
| Magic Hour | Cloud, text-to-video | Good | Free trial | Backup option |
| CapCut AI | Cloud, editing + AI | Good | FREE | ✅ Best for assembly |

### 🖼️ Image Generation
| Tool | Cost | Notes |
|------|------|-------|
| Pinokio + Stable Diffusion | FREE | Unlimited local generation |
| Pinokio + Fooocus | FREE | High quality portraits/scenes |
| ChatGPT (DALL-E 3) | Included | Use for premium images |
| Gemini (Imagen 3) | Included | Strong photorealism |

### 🎙️ Voice / Audio
| Tool | Free Tier | Notes |
|------|-----------|-------|
| **ElevenLabs** | 10K credits/month (~10 min audio) | TikTok-specific voices, API available |
| CapCut TTS | FREE unlimited | Built-in, decent quality |
| Suno | Already have | Music, not voiceover |
| TikTok built-in TTS | FREE | Use as fallback |

### ✂️ Video Assembly + Captions
| Tool | Cost | Notes |
|------|------|-------|
| **CapCut** | FREE | Best for TikTok. Auto-captions, effects, templates |
| CapCutAPI (Python) | FREE | Automates CapCut editing via code |
| Opus Clip | Free tier | Repurpose long → shorts |

---

## TikTok Automation Pipeline — What Can Be Automated vs Manual

```
STEP 1: Niche + Idea Selection
  Tool: Claude (/research skill)
  Status: ✅ AUTOMATED — Claude pulls from content-tracker.md backlog

STEP 2: Script Generation
  Tool: Claude
  Status: ✅ AUTOMATED — prompt template → full script in seconds

STEP 3: Voiceover
  Tool: ElevenLabs (API) or CapCut TTS
  Status: ✅ CAN BE AUTOMATED — ElevenLabs has API + Zapier integration

STEP 4: Video / Visual Generation
  Tool: Pinokio (Wan2.1 or ComfyUI) or ChatGPT Sora
  Status: ⚙️ SEMI-AUTOMATED — Pinokio runs locally, needs GPU. Manual trigger.

STEP 5: Assembly + Captions
  Tool: CapCut (manual) or CapCutAPI (Python script)
  Status: ⚙️ SEMI-AUTOMATED — CapCutAPI can automate with Python code
           Manual for now while learning the format

STEP 6: Review + Finalize
  Tool: You
  Status: 🔴 MANUAL — quality check before posting (important to avoid AI slop flag)

STEP 7: Upload to TikTok
  Tool: TikTok app or browser
  Status: 🔴 MANUAL — TikTok API restricts direct posting for individual creators
           Workaround: Buffer or Later for scheduling (limited free tiers)

STEP 8: Track Performance
  Tool: Claude updates niche-tracker.csv
  Status: ✅ AUTOMATED — Claude logs ideas, status, upload date, views when you report back
```

---

## MVP Pipeline (Start Tomorrow)

The fastest path to first TikTok video:

1. **Claude** → generates script (5 min)
2. **CapCut** → AI text-to-video OR import Pinokio visuals + add TTS voice (15 min)
3. **You** → review, add music from Suno (5 min)
4. **You** → upload manually to TikTok (2 min)
5. **Claude** → log it in tracker

Total: ~30 min per video → target 1/day

---

## What to Install / Set Up First

### ✅ Already Have — Just Use It
- Claude (scripts, captions, research)
- ChatGPT (DALL-E images, Sora for premium videos)
- Suno (background music)
- Pinokio (just need to install the right apps)

### 🔧 Install in Pinokio (One-Click, Free)
1. **Wan2.1** — text-to-video, best quality free local model
2. **ComfyUI** — advanced image/video workflow
3. **Fooocus** — high-quality images with simple interface
4. **Stable Diffusion WebUI** — backup image generation

### 📲 Sign Up (Free)
1. **ElevenLabs** — https://elevenlabs.io (free 10K credits/month)
2. **CapCut Desktop** — https://capcut.com (free, download desktop version)
3. **InVideoAI** — https://invideo.io (free tier, fastest full pipeline)

---

## Phase 2 Automation (After First 10 Videos)
Once you know what content format works:
- CapCutAPI Python script: auto-assemble videos from clips + captions
- n8n (free, self-hosted via Pinokio): connect Claude → ElevenLabs → CapCut pipeline
- TikTok scheduling: Buffer or Later free tier for consistent posting

---

## Next Steps
1. Install Wan2.1 and ComfyUI in Pinokio
2. Sign up for ElevenLabs free tier
3. Download CapCut desktop
4. Produce first test TikTok using MVP pipeline above
5. Log it in niche-tracker.csv
