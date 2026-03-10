# YNAI World — Asset Library
_Visual assets for YNAI / OpenMindAI content production_

---

## Folder Structure

```
assets/ynai-world/
├── characters/
│   ├── protagonist/          ← Main character (8 refs + CHARACTER-BIBLE.md)
│   └── other/                ← Future characters
├── environments/             ← World locations, backgrounds
└── brand/                    ← Logos, overlays, UI elements
```

## How Claude Uses These

Claude reads these images directly using the Read tool (multimodal).
When generating Sora/Veo prompts, Claude references the CHARACTER-BIBLE.md
to ensure visual consistency across all content.

## Adding New Assets

- New character variants → `characters/protagonist/ref-XX-description.jpeg`
- New characters → `characters/other/[name]/`
- New environments → `environments/[location-name].jpeg`
- Brand elements → `brand/[element-name].png`

## Primary References (Quick Access)

| Use | File |
|-----|------|
| **Main brand identity** | characters/protagonist/ref-06-flat-hooded-purple-flames.jpeg |
| **Detailed character** | characters/protagonist/ref-02-anime-skulls-mature.jpeg |
| **Cartoon/social** | characters/protagonist/ref-08-cartoon-redgreen-skulls.jpeg |
| **Character rules** | characters/protagonist/CHARACTER-BIBLE.md |
