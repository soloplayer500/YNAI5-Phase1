---
name: symphony
description: >
  SYMPHONY — Activate this skill for ALL music production tasks. Triggers on: writing lyrics, making a song, Suno prompt, trap beat, R&B track, music production, "make something that sounds like [artist]", artist reference (NBA YoungBoy, Gunna, Juice WRLD, Drake, Rod Wave, etc.), "write bars", "create a hook", "help with my music", "generate a track", "write a verse", genre words (trap, drill, R&B, melodic rap, sad rap), or any music creative request. SYMPHONY handles the full pipeline: concept → lyrics with Suno formatting → Suno generation prompt → style tags → track ready. Uses bitwize music skill library (52 skills, 72 genre profiles), Suno MCP for direct generation, Genius MCP for reference lyrics, and Spotify MCP for artist DNA analysis.
---

# SYMPHONY — AI Music Production Pipeline

Full concept-to-track pipeline. When MCPs are connected, SYMPHONY pulls real artist data, generates directly in Suno, and delivers a finished track.

Genre profiles + Suno tags → `references/genres.md`
Artist DNA → `references/artists.md`

---

## Full Pipeline — How It Runs

```
Solo: "write a YB-style trap song about loyalty"
         ↓
SYMPHONY Step 1: Load artist DNA
  → spotify: get_artist_info("NBA Youngboy")
  → spotify: get_artist_top_tracks("NBA Youngboy")
  → genius: search_artist("NBA YoungBoy") → get_artist_songs(artist_id)
  → Load references/artists.md for YB DNA profile
         ↓
SYMPHONY Step 2: Context gather (if needed)
  → ask_user_input_v0: vibe / topic / any specific direction
         ↓
SYMPHONY Step 3: Write lyrics
  → Apply genre profile from references/genres.md
  → Blend artist DNA at 40% max — Solo's YNAI5 voice is 60%
  → Format with Suno section tags [verse] [chorus] [bridge]
  → Apply phonetic rules for AI pronunciation
         ↓
SYMPHONY Step 4: Build Suno prompt
  → Style tags from genre profile
  → Artist voice tags
  → Generation notes
         ↓
SYMPHONY Step 5: Generate (if Suno MCP connected)
  → suno: generate_song(title, style_tags, lyrics)
  → suno: get_track_status(clip_id) — poll until ready
  → Return audio URL to Solo
```

---

## MCP Integration

### When GENIUS MCP connected:
```python
# Research reference artist
artist_data = genius.search_artist(artist_name)
top_songs   = genius.get_artist_songs(artist_id, sort="popularity", per_page=10)
song_detail = genius.get_song_details(song_id)  # for lyric style analysis
```

### When SPOTIFY MCP connected:
```python
# Get audio DNA of reference tracks
artist_info = spotify.get_artist_info(artist_name)
top_tracks  = spotify.get_artist_top_tracks(artist_name)
# For each reference track:
features    = spotify.get_track_features(track_id)
# → BPM, key, energy, danceability → inform Suno style tags
```

### When SUNO MCP connected:
```python
# Direct generation after lyrics are approved
credits  = suno.get_credits()  # check before generating
result   = suno.generate_song(title, style_tags, lyrics)
clip_id  = result[0]["id"]
# Poll for completion:
status   = suno.get_track_status(clip_id)
# Return audio_url when status = "complete"
```

### When RESEARCH MCP connected:
```python
# Deep artist style research
artist_style = research.research_music_artist(artist_name)
# → Signature sound, themes, flow patterns, Suno tags, reference tracks
```

---

## Context Gathering

If Solo doesn't specify, use `ask_user_input_v0`:

**Q1: Vibe?**
Options: [Trap banger | Melodic rap | R&B smooth | Sad | Hype | Storytelling | Street]

**Q2: Artist reference?**
Options: [NBA YoungBoy | Gunna | Juice WRLD | Rod Wave | Drake | Lil Baby | Original — no reference]

**Q3: What's the song about?**
Options: [Loyalty | Flexing | Pain | Love | Street life | Motivation | Let me tell you the concept]

If Solo gives a clear brief — skip questions, go straight to writing.

---

## Lyrics Writing Rules

- **Voice split**: Solo's YNAI5 voice = 60% minimum. Artist DNA = max 40%
- **Language**: Natural AAVE, Caribbean cadence where authentic. No forced slang.
- **Suno section tags**: `[verse]` `[chorus]` `[bridge]` `[outro]` `[hook]` `[rap verse]` `[melodic verse]`
- **Phonetic rules for Suno**:
  - Stretched syllables: `ba-a-aby` not `baby`
  - Emphasis: `LOYALTY` (caps)
  - Pauses: `I been gone... but I'm back`
  - Common Suno-friendly: `lil`, `da`, `wit`, `gon`

---

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 SYMPHONY — [TRACK TITLE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STYLE TAGS:
[genre, subgenre, mood, tempo, instruments]

LYRICS:
[full lyrics with section tags]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎛 Suno Mode: [Custom / Instrumental]
🎤 Artist DNA: [artists referenced + % blend]
🔍 Data pulled: [Genius + Spotify if connected]
📊 BPM: [from Spotify features if available]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If Suno MCP connected — append:
```
🎵 GENERATING...
Track ID: [clip_id]
Status: [polling...]
Audio: [url when ready]
```

---

## Output Rules

1. **Always write lyrics first** — show Solo before generating
2. **Confirm before Suno generation** — credits cost money
3. **Check credits first** (`suno.get_credits()`) before every generation
4. **"Shorter"/"longer"/"more X"** = revise lyrics, regenerate
5. **"More YB less Gunna"** = adjust DNA blend ratio in lyrics
6. **If Suno MCP not connected** → output lyrics + prompt only, Solo pastes manually

---

## Pipeline Connections

- **← RESEARCH**: `research_music_artist(artist)` for deep artist style when Genius/Spotify aren't enough
- **→ DISTRIBUTION**: After track is generated, DISTRIBUTION handles posting to YNAI5 social channels
- **→ PLAYWRIGHT**: If Suno web interface needed (session expired, MCP down) → use Playwright to navigate suno.ai
