#!/usr/bin/env python3
"""
ElevenLabs Voice Generator — YNAI5-SU
Reads API key from .env.local, generates MP3 voiceover via ElevenLabs API.

Usage:
  python generate.py --text "Your script here"
  python generate.py --text "Your script here" --voice "21m00Tcm4TlvDq8ikWAM"
  python generate.py --text "Your script here" --out "my-audio"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────

# Workspace root = 3 levels up from .claude/skills/voice-gen/
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE       = WORKSPACE_ROOT / ".env.local"
AUDIO_DIR      = WORKSPACE_ROOT / "projects" / "social-media-automation" / "audio"

# Default voice: Rachel — neutral English, works well for TikTok voiceovers
DEFAULT_VOICE  = "21m00Tcm4TlvDq8ikWAM"

# ElevenLabs API
API_BASE       = "https://api.elevenlabs.io/v1"
MODEL_ID       = "eleven_multilingual_v2"
OUTPUT_FORMAT  = "mp3_44100_128"

# ── Helpers ────────────────────────────────────────────────────────────────────

def load_api_key() -> str:
    """Read ELEVENLABS_API_KEY from .env.local"""
    if not ENV_FILE.exists():
        print(f"[ERROR] .env.local not found at: {ENV_FILE}")
        print("        Create it with:  ELEVENLABS_API_KEY=sk_...")
        sys.exit(1)

    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith("ELEVENLABS_API_KEY="):
                key = line.split("=", 1)[1].strip()
                if key:
                    return key

    print("[ERROR] ELEVENLABS_API_KEY not found in .env.local")
    sys.exit(1)


def slugify(text: str, max_len: int = 40) -> str:
    """Convert text to a safe filename slug"""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text[:max_len].strip("-")


def build_output_path(out_arg: str | None, text: str) -> Path:
    """Build the full output MP3 path"""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    if out_arg:
        filename = out_arg if out_arg.endswith(".mp3") else f"{out_arg}.mp3"
    else:
        slug = slugify(text)
        filename = f"{today}-{slug}.mp3"

    return AUDIO_DIR / filename


def generate_voiceover(text: str, voice_id: str, api_key: str) -> bytes:
    """Call ElevenLabs TTS API and return raw MP3 bytes"""
    import urllib.request

    url = f"{API_BASE}/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "output_format": OUTPUT_FORMAT,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                print(f"[ERROR] API returned status {resp.status}")
                sys.exit(1)
            return resp.read()
    except Exception as e:
        # Try to extract API error message
        if hasattr(e, "read"):
            try:
                error_body = json.loads(e.read().decode())
                msg = error_body.get("detail", {})
                if isinstance(msg, dict):
                    msg = msg.get("message", str(msg))
                print(f"[ERROR] ElevenLabs API error: {msg}")
            except Exception:
                print(f"[ERROR] Request failed: {e}")
        else:
            print(f"[ERROR] Request failed: {e}")
        sys.exit(1)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate ElevenLabs voiceover MP3"
    )
    parser.add_argument(
        "--text", "-t",
        required=True,
        help="Text to convert to speech"
    )
    parser.add_argument(
        "--voice", "-v",
        default=DEFAULT_VOICE,
        help=f"ElevenLabs voice ID (default: Rachel = {DEFAULT_VOICE})"
    )
    parser.add_argument(
        "--out", "-o",
        default=None,
        help="Output filename (without .mp3 extension). Auto-generated if omitted."
    )
    args = parser.parse_args()

    # Load key
    api_key = load_api_key()

    # Build output path
    out_path = build_output_path(args.out, args.text)

    print(f"[voice-gen] Generating voiceover...")
    print(f"  Text    : {args.text[:80]}{'...' if len(args.text) > 80 else ''}")
    print(f"  Voice ID: {args.voice}")
    print(f"  Output  : {out_path}")

    # Generate
    audio_bytes = generate_voiceover(args.text, args.voice, api_key)

    # Save
    with open(out_path, "wb") as f:
        f.write(audio_bytes)

    size_kb = len(audio_bytes) / 1024
    char_count = len(args.text)

    print(f"\n[DONE] Voiceover saved!")
    print(f"  File    : {out_path}")
    print(f"  Size    : {size_kb:.1f} KB")
    print(f"  Chars   : {char_count}")


if __name__ == "__main__":
    main()
