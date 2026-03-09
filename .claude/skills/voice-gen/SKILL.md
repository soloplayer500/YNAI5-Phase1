---
name: voice-gen
description: Generate AI voiceover MP3 from text using ElevenLabs.
             Use when creating audio for TikTok, YouTube, or any video content.
             Reads API key from .env.local automatically.
argument-hint: "[text to speak] [optional: --voice voice_id] [optional: --out filename]"
allowed-tools: Bash
---

# Voice Gen Skill

Generate a voiceover MP3 using ElevenLabs text-to-speech.

## How to Use

When invoked with `/voice-gen [text]`, run:

```bash
python ".claude/skills/voice-gen/generate.py" --text "$ARGUMENTS"
```

## What It Does
1. Reads `ELEVENLABS_API_KEY` from `.env.local` in workspace root
2. Calls ElevenLabs TTS API (model: `eleven_multilingual_v2`)
3. Saves MP3 to `projects/social-media-automation/audio/YYYY-MM-DD-{slug}.mp3`
4. Reports: file path, size in KB, character count

## Default Voice
- **Rachel** (ID: `21m00Tcm4TlvDq8ikWAM`) — neutral English, clear, works well for TikTok

## Other Useful Voices
- Cloned or custom voice: pass the voice ID from your ElevenLabs dashboard
- Browse voices at: https://elevenlabs.io/voice-lab

## Examples

**Basic usage:**
```bash
python ".claude/skills/voice-gen/generate.py" --text "Welcome to YNAI5 World. Here are 5 AI tools that will change how you work."
```

**Custom voice:**
```bash
python ".claude/skills/voice-gen/generate.py" --text "Your script here" --voice "EXAVITQu4vr4xnSDxMaL"
```

**Custom output filename:**
```bash
python ".claude/skills/voice-gen/generate.py" --text "Your script here" --out "tiktok-ep1-hook"
```

## Free Tier Limits
- ElevenLabs free: 10,000 characters/month (~10 min of audio)
- Check usage: https://elevenlabs.io/app/subscription

## After Running
- MP3 is in `projects/social-media-automation/audio/`
- Import into CapCut for TikTok assembly
- MP3s are gitignored — they don't get committed to git
