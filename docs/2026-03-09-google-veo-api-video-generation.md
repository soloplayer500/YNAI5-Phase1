# Research: Google Veo API — Video Generation Access & Free Tier
Date: 2026-03-09
Sources:
- https://developers.googleblog.com/veo-2-video-generation-now-generally-available/
- https://ai.google.dev/gemini-api/docs/video
- https://developers.googleblog.com/en/introducing-veo-3-1-and-new-creative-capabilities-in-the-gemini-api/
- https://ai.google.dev/gemini-api/docs/pricing
- https://aistudio.google.com/models/veo-3

---

## Summary
Google's Veo 2 and Veo 3.1 are accessible via AI Studio UI for free with daily limits (~1–5 videos/day). API access (code/programmatic) for Veo 3.x requires a PAID tier Gemini API account. The existing free API key (gemini-flash-latest) cannot call Veo for video generation. Best free path: use AI Studio UI manually or use Sora (already paid via ChatGPT Pro).

---

## Key Findings

- **Veo 3.1** is Google's latest model — generates 8-second videos at 720p/1080p/4K WITH natively generated audio, portrait 9:16 supported (TikTok-ready)
- **AI Studio UI** (aistudio.google.com/models/veo-3): FREE to use with limited daily quota (~30 videos/month via Gemini app, UI-only)
- **Gemini API (code/programmatic)**: Veo 3.1 is in **paid preview only** — model name `veo-3.1-generate-preview`, requires billing
- **Veo 2 API**: Available via Vertex AI only → requires Google Cloud project + billing enabled
- **Our current free API key** (`gemini-flash-latest`): Cannot call Veo for video — text/code/analysis only
- **Veo 3 Fast**: ~3 videos/day (paid preview) | **Veo 3**: ~5 videos/day (paid preview)

---

## Details

### Access Tiers

| Access Method | Cost | Video Generation | Quota |
|---------------|------|-----------------|-------|
| AI Studio UI (browser) | FREE | Yes — Veo 2 & 3.1 | ~1 video/day (UI) |
| Gemini App (consumer) | FREE | Yes — Veo 2 | ~30/month |
| Gemini API free tier | FREE | No — text/image only | N/A |
| Gemini API paid tier | Pay-per-use | Yes — Veo 3.1 | 3–5/day preview |
| Vertex AI | Billing required | Yes — Veo 2 + 3 | Custom |

### Python API Code (Paid Tier — For Future Reference)
```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")  # must be paid tier

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="9:16 vertical video. [your prompt here]",
    config=types.GenerateVideosConfig(
        aspect_ratio="9:16",    # TikTok format
        duration_seconds=8,
    )
)
# Poll for completion — async operation
```

### Veo 3.1 Capabilities (2026)
- 8-second clips at 720p, 1080p, or 4K
- Native audio generation (music, SFX, ambient)
- 9:16 portrait format (TikTok-native)
- Image-to-video (up to 3 reference images for consistency)
- First/last frame control
- Seed support for consistency across clips

### AI Studio UI Access
- Go to: https://aistudio.google.com/models/veo-3
- Sign in with Google account (same one used for API key)
- Free to test — no API call needed
- Export video file directly

---

## Current Situation for YNAI5-SU

**What works right now (free):**
1. AI Studio UI → Veo 3.1 → manual video generation (limited but free)
2. Sora via ChatGPT Pro (already paid) → best quality, most credits
3. Kling 2.6 free daily credits → backup
4. Seedance 2.0 free daily credits → backup

**What requires upgrade:**
- Veo via API/code automation → needs paid Gemini API tier (~$0.35/sec generated)

**Recommendation:** Don't pay for Veo API yet. Use AI Studio UI for free Veo, Sora as primary. When revenue comes in, upgrade Gemini API to paid for full automation.

---

## Next Steps / Follow-up
1. **Now:** Try AI Studio UI at aistudio.google.com/models/veo-3 — test a free Veo 3.1 video
2. **For Phase 1 TikTok:** Screen record + CapCut is actually MORE authentic for the "normal user" format — don't over-produce
3. **Future:** When upgrading to paid Gemini API, extend `/gemini` skill to call Veo via code
4. **Research next:** Best CapCut workflow for TikTok batch production (auto-captions, templates)
