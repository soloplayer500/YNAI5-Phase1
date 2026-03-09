---
name: prompt-gen
description: Generate structured AI prompts for video (Sora/Kling) and image generation
             using the 8-layer Technical Orchestration framework. Use for TikTok,
             YouTube, and Instagram content production. Outputs ready-to-paste prompts.
argument-hint: "[platform: tiktok|youtube|instagram] [type: video|image|both] [subject/topic] [optional: style or mood]"
allowed-tools: Read
---

# Prompt Gen Skill

Generate production-ready AI prompts using the 8-layer Technical Orchestration framework.

## When Invoked

Read the prompt engineering reference doc for context:
`docs/2026-03-09-ai-prompt-engineering-video-images.md`

Then generate structured prompts based on `$ARGUMENTS`.

---

## How to Parse Arguments

From `$ARGUMENTS`, extract:
- **Platform**: tiktok / youtube / instagram (affects aspect ratio and duration)
- **Type**: video / image / both
- **Subject/Topic**: the content idea (e.g. "5 AI tools that make money")
- **Style/Mood** (optional): cinematic / energetic / calm / dark / neon / etc.

If any key info is missing, infer from the subject topic.

---

## Output Format (Always Produce All 3 Sections)

### 1. VIDEO PROMPT — Sora / Kling
Use this template. Fill in ALL 8 layers. Be specific and technical.

```
[SUBJECT + SCENE description], [LENS: focal length, aperture],
[CAMERA MOTION: type + velocity], [LIGHTING: color temp K, type],
[EMOTION ARC: start → end], [STYLE: film stock / color grade],
[AUDIO: music type, foley, sync notes],
Aspect: [9:16 for TikTok | 16:9 for YouTube], Duration: [4-8s recommended],
Negative: [list what to avoid], Seed: 777
```

**Platform defaults:**
- TikTok/Instagram: `Aspect: 9:16`, Duration: `4-8s per clip`
- YouTube: `Aspect: 16:9`, Duration: `8-15s per clip`

**YNAI5 World brand anchors (always include for brand consistency):**
- Style: modern tech-noir, neon blue + gold accents
- Seed: 777 (maintain across series for consistency)
- Negative: always include: `flat lighting, plastic texture, aliasing, jitter, cheap CGI look`

---

### 2. IMAGE PROMPT — DALL-E / ComfyUI / Gemini Imagen
Use the layered formula:
```
[Subject] in [environment], [art style], [lighting description],
[composition: close-up/wide/overhead], [color palette], [quality modifiers],
cinematic, ultra-detailed, [aspect ratio].
Negative: [what to avoid]
```

Best for: thumbnails, social media covers, B-roll stills, carousel images.

---

### 3. CAPTION + HOOK SUGGESTIONS
Provide:
- **TikTok hook** (0-2 second text overlay, under 8 words, creates instant curiosity)
- **Caption** (1-2 sentences, includes 3-5 relevant hashtags)
- **Suggested Suno music direction** (BPM range, genre, mood)

---

## Example Output

**Input:** `/prompt-gen tiktok video "5 AI tools that make money in 2026" energetic`

**Output:**

---
### VIDEO PROMPT (Sora / Kling)
```
Futuristic tech workspace at night, neon-lit monitors displaying AI dashboards,
85mm prime f/1.4 shallow depth of field, slow dolly-in 0.3 m/s revealing screens,
volumetric blue and gold lighting 4200K key 2800K rim, split rim effect.
Emotion: Curiosity → Excitement. Style: modern tech-noir, Kodak Vision3 grain,
teal-orange grade. Audio: building electronic pulse synced to screen reveals,
subtle keyboard clicks foley. Aspect: 9:16. Duration: 6s per clip.
Negative: flat lighting, plastic texture, aliasing, jitter, cheap CGI look, cluttered.
Seed: 777
```

### IMAGE PROMPT (Thumbnail / Still)
```
Cinematic close-up of glowing holographic AI interface with dollar signs and
tool logos floating, dark tech studio environment, neon blue and gold volumetric
lighting, 85mm lens, ultra-sharp foreground with bokeh background, modern tech-noir
aesthetic, ultra-detailed, 4K, 9:16 vertical format.
Negative: cartoon, blurry, overexposed, crowded, low contrast.
```

### HOOK + CAPTION
- **TikTok hook (text overlay):** "You're sleeping on these 5 AI tools 👀"
- **Caption:** "These AI tools are quietly making creators money in 2026. Which one are you starting with? #AITools #MakeMoneyOnline #AIAutomation #TikTokGrowth #YNAI5"
- **Suno direction:** Upbeat electronic, 128 BPM, building energy, slight tension before drop

---

## Quick Reference — Key Prompt Terms

**Lenses:** 24mm (wide), 35mm (natural), 50mm (neutral), 85mm (portrait), 100mm macro
**F-stops:** f/1.4 (blurry bg), f/2.8 (slight blur), f/8 (sharp throughout), f/11 (deep focus)
**Movements:** slow dolly-in, pan left/right, handheld tracking, static wide, crane up, zoom
**Color temps:** 2800K (warm/golden), 4200K (neutral), 5600K (daylight), 6500K (cool/blue)
**Grades:** teal-orange, desaturated noir, golden hour, neon cyberpunk, clean minimal

## YNAI5 World Visual Consistency
```
Brand Seed: 777
Palette: neon blue + gold on dark backgrounds
Style: modern tech-noir
Lens preference: 85mm or 35mm prime
Motion: slow dolly or static tripod — no shaky-cam
Audio: ambient electronic → synth build
Aspect: 9:16 TikTok, 16:9 YouTube
Negative baseline: flat lighting, plastic texture, aliasing, jitter, cheap CGI
```
