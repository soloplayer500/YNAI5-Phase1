# Research: AI Prompt Engineering — Video & Image Generation 2026
Date: 2026-03-09
Sources:
- https://www.truefan.ai/blogs/ai-video-prompt-engineering-2026-guide
- https://wavespeed.ai/blog/posts/sora-2-prompting-tips-better-videos-2026/
- https://cookbook.openai.com/examples/sora/sora2_prompting_guide
- https://medium.com/@creativeaininja/how-to-actually-control-next-gen-video-ai-runway-kling-veo-and-sora-prompting-strategies-92ef0055658b
- https://letsenhance.io/blog/article/ai-text-prompt-guide/
- https://invideo.io/blog/best-prompts-for-ai-image-to-video/

---

## Summary
In 2026, AI prompt engineering has evolved from "describe what you want" to **Technical
Orchestration** — structured, multi-layer prompts that speak the language of cinematographers.
The models are trained on professional filmmaking datasets. They respond to lens specs,
lighting ratios, and motion vectors better than adjectives. One reusable prompt template can
eliminate 60–70% of iteration time.

**Key shift:** Stop describing what things LOOK like. Describe the FORCES and PHYSICS acting on them.

---

## The 8 Control Layers Framework

Every high-quality AI video/image prompt controls all 8 dimensions:

| Layer | What It Controls | Example |
|-------|-----------------|---------|
| **1. Subject/Scene** | Core entity + environment | "25-year-old woman in cream linen, modern cafe, Aruba morning" |
| **2. Emotion Arc** | Explicit emotional tokens | "Curiosity → Satisfaction" |
| **3. Optics** | Lens, focal length, aperture | "85mm prime, f/1.4, shallow depth of field" |
| **4. Camera Motion** | Movement type + velocity | "Slow dolly-in 0.3 m/s, handheld tracking shot" |
| **5. Lighting Stack** | Key/fill/rim + color temp | "5600K key light, 3200K rim, soft fill, 3:1 ratio" |
| **6. Style/Look** | Film stock, color grade | "Kodak Portra 400, teal-orange grade, grain" |
| **7. Audio/Mood** | Sound cues, sync | "EDM bass drop at 4s, foley footsteps, ambient cafe" |
| **8. Continuity Anchors** | Cross-shot consistency | "Seed: 1024, cream linen saree, morning light 5000K" |

---

## Master Prompt Template (Universal)

```
[SUBJECT + SCENE], [LENS SPECS], [CAMERA MOTION], [LIGHTING SETUP],
[EMOTION ARC], [STYLE/COLOR GRADE], [AUDIO], [ASPECT RATIO], [DURATION],
Negative: [what to avoid], Seed: [NUMBER]
```

**Full Example (TikTok product reveal):**
```
Studio close-up of glowing AI chip on black surface, 50mm prime f/1.8 bokeh,
slow dolly-in 0.2 m/s, soft rim light 3200K, reflective acrylic base.
Emotion: Curiosity to Excitement. Style: modern tech noir, teal-orange grade.
Audio: ambient hum building to synth pulse. Aspect: 9:16. Duration: 8s.
Negative: jitter, aliasing, plastic texture, flat lighting. Seed: 42.
```

---

## Sora 2 — Specific Strategy

**Sora's strength:** Physics simulation — liquid, cloth, inertia, cause-and-effect chains.
**Key principle:** Describe forces, not appearances.

### Sora Prompt Structure:
```
[Scene Description — what physically happens]
Style: [cinematography + lighting + lens aesthetic]
Audio: [dialogue, foley, music, sync requirements]
Duration: [seconds — keep under 25s for best quality]
```

### Sora Camera Terms (These Work):
- Shot types: `Close-Up`, `Over-the-Shoulder`, `High Angle`, `Dutch Angle`, `Bird's Eye View`, `Wide Shot`
- Movements: `Pan`, `Tilt`, `Dolly`, `Truck`, `Crane`, `Zoom`, `Steadicam`, `Handheld`
- Advanced: `Slow push-in over 4 seconds`, `Circular camera movement`, `Static wide with deep focus f/11`

### Sora Physics Language:
```
"water sloshes with realistic surface tension"
"cloth simulation with wind resistance 15 km/h"
"paper curls naturally under heat, slight char at edges"
"dust particles settle realistically after impact"
```

### Sora Best Practice — Stitch Short Clips:
- Better results: two 4-second clips stitched in CapCut vs. one 8-second clip
- Shorter = model follows instructions more reliably

---

## Kling 2.6 — Specific Strategy

**Kling's strength:** Audio-visual choreography, beat-matched generation, human realism.
**Key principle:** Write timeline scripts with beat markers. Match audio beats to visual actions.

### Kling Timeline Prompt Format:
```
Beat 0-4s: [action], [camera], [lighting]
Beat 4s: [event — e.g. EXPLOSION at bass drop]
Beat 4-8s: [next action], [camera movement]
Negative: plastic skin, rubbery motion, ghosting, waxy sheen
```

### Kling Example (TikTok hook):
```
Beat 0-3s: Slow-motion close-up of hands opening a mystery box, 60fps,
           soft key light 5600K, anticipation.
Beat 3s: Cut — rapid zoom out synced to beat drop.
Beat 3-7s: Wide shot reveal, neon rim lighting, excited face reaction.
Negative: plastic skin, ghosting, rubbery motion, low contrast. Seed: 201.
```

---

## Veo 3.1 / Runway — JSON Structure

**Veo strength:** Strict adherence to JSON-structured prompts — prevents "concept bleed."
**Runway strength:** Reference frames, style locking, most flexible.

### JSON Prompt Schema (works for API/automation):
```json
{
  "subject": "young man in dark hoodie, urban rooftop at night",
  "optics": {
    "lens": "35mm",
    "aperture": "f/2.8",
    "depth_of_field": "shallow"
  },
  "motion": {
    "type": "slow dolly-in",
    "velocity": "0.3m/s"
  },
  "lighting": [
    {"type": "key", "color_temp": "3200K", "direction": "side"},
    {"type": "rim", "color_temp": "5600K", "intensity": "high"}
  ],
  "emotion_arc": "loneliness to determination",
  "style": "cinematic noir, desaturated with blue tones",
  "audio": "ambient wind, distant city hum, building orchestral swell",
  "continuity_anchor": {"seed": 1024, "wardrobe": "dark hoodie, silver chain"},
  "negative_prompts": ["jitter", "aliasing", "overexposed", "flat lighting"],
  "aspect_ratio": "9:16",
  "duration_seconds": 8
}
```

---

## Multi-Shot Continuity (Seed Locking)

The #1 trick for consistent TikTok series characters and worlds:

**Rule:** Same Seed ID + identical subject descriptors across ALL shots in a sequence.

```
Shot 1 (Establish):
"Wide shot of YNAI5 World logo materializing from digital particles,
 4K volumetric lighting, 35mm wide, static. Seed: 777"

Shot 2 (Detail):
"Close-up of YNAI5 logo glowing, particles settling, 85mm macro.
 MAINTAIN: same particle style, same volumetric lighting. Seed: 777"

Shot 3 (Transition):
"Logo dissolves into circuit board, camera pulls back, 24mm wide.
 MAINTAIN: digital particle aesthetic, YNAI5 blue+gold palette. Seed: 777"
```

### Visual Consistency Document (save and reuse):
```
Brand: YNAI5 World
Style: Modern tech-noir, neon blue + gold accents
Camera: 35mm or 85mm prime, shallow DOF preferred
Lighting: 5600K key, 3200K rim, volumetric fog when possible
Motion: Slow dolly preferred, no shaky-cam
Audio: Ambient electronic, building to synth pulse
Aspect: 9:16 (TikTok), 16:9 (YouTube)
Master Seed: 777 (use for all brand content)
Negative: plastic texture, aliasing, jitter, flat lighting, cheap CGI look
```

---

## Image Generation — Layered Prompt Formula

**Universal image formula:**
```
[Subject] + [Style] + [Lighting] + [Composition] + [Quality modifiers]
```

**Model-specific approach:**

| Model | Best Prompt Style | Key Modifiers |
|-------|------------------|---------------|
| **ChatGPT / DALL-E 3** | Full paragraphs, conversational | Multi-turn editing works well |
| **Midjourney V7** | Short, high-signal phrases + `--ar` ratio | `--style raw`, reference images |
| **Stable Diffusion / ComfyUI** | Structured weighted keywords | `(keyword:1.3)` weighting, LoRA names |
| **Flux (in ComfyUI)** | Dense descriptive phrases | Strong photorealism, negative prompts essential |
| **Gemini Imagen 4** | Descriptive paragraphs | Strong at photorealism + text in image |

### Image Prompt Example (TikTok thumbnail):
```
Cinematic close-up portrait of a faceless AI robot holding a glowing smartphone,
neon-lit tech lab background, teal and orange color grade, cinematic depth of field,
85mm lens, volumetric lighting, ultra-detailed, 4K, professional photography aesthetic.
Negative: blurry, pixelated, cartoon, overexposed.
```

---

## TikTok-Specific Prompt Tactics

**Hook-first architecture — your first 2 seconds must contain the visual hook:**
```
Opening shot (0-2s): [HIGH IMPACT VISUAL — explosion, transformation, reveal, face reaction]
Body shots (2-45s): [supporting visuals with camera movement]
Closing (last 2s): [CTA visual or loop-back moment]
```

**What gets high completion rate:**
- Fast visual cuts (1-2s per shot) for trend content
- Slow cinematic for storytelling (builds watch time)
- Unexpected transformations (before/after, zoom reveals)
- Text overlays synced to beat drops

**Formats that work with your stack:**
1. **AI Tool Demo** → screen-recorded + Sora cinematic B-roll
2. **AI Storytelling** → Sora narrative clips + ElevenLabs voice
3. **Crypto Commentary** → Kling charts/graphs animation + ElevenLabs voice
4. **YNAI5 World Brand** → Sora logo/world clips + Suno music

---

## Prompt Generation Skill (Next Build)

Recommendation: Build a `/prompt-gen` skill that uses Claude to auto-generate
structured prompts using the 8-layer framework above.

Inputs: content type, platform, subject, emotion, style
Output: ready-to-paste prompt for Sora / Kling / image tools

This would make the full pipeline:
```
/prompt-gen → copy prompt → Sora/Kling → download clip → /voice-gen → CapCut → TikTok
```

---

## Community Resources
- Reddit r/ChatGPT (7M+) — active prompt sharing and daily templates
- Reddit r/midjourney (600K+) — image formulas, style references
- Reddit r/StableDiffusion (600K+) — ComfyUI workflows, LoRA guides
- PromptBase (promptbase.com) — paid/free prompt marketplace
- OpenAI Cookbook — official Sora 2 guide
