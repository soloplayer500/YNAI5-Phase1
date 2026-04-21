import os, httpx, time
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("suno")
API_BASE = "https://studio-api.suno.ai/api"
SESSION_ID = os.getenv("SUNO_SESSION_ID", "")  # from browser cookies

def _headers():
    return {
        "Cookie": f"__client_uat_yWxZdoEr={SESSION_ID}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }

def _api_headers(token: str):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def _get_token() -> str:
    r = httpx.get("https://clerk.suno.ai/v1/client?_clerk_js_version=4.73.4",
                  headers=_headers(), timeout=30)
    return r.json()["response"]["sessions"][0]["last_active_token"]["jwt"]

@mcp.tool()
def generate_song(title: str, style_tags: str, lyrics: str, make_instrumental: bool = False) -> str:
    """Generate a song on Suno with custom lyrics and style.
    style_tags: comma-separated tags like 'trap, dark, 808s, melodic'
    lyrics: full song lyrics with [verse] [chorus] [bridge] section tags"""
    token = _get_token()
    payload = {
        "make_instrumental": make_instrumental,
        "mv": "chirp-v3-5",
        "prompt": lyrics,
        "tags": style_tags,
        "title": title
    }
    r = httpx.post(f"{API_BASE}/generate/v2/", headers=_api_headers(token),
                   json={"gpt_description_prompt": "", **payload}, timeout=60)
    r.raise_for_status()
    data = r.json()
    clips = data.get("clips", [])
    if not clips:
        return f"Generation started. Response: {data}"
    result = []
    for clip in clips:
        result.append(f"Track ID: {clip.get('id')}\nTitle: {clip.get('title')}\nStatus: {clip.get('status')}\nAudio: {clip.get('audio_url', 'Processing...')}")
    return "\n\n".join(result)

@mcp.tool()
def generate_from_description(description: str, style_tags: str = "") -> str:
    """Generate a song from a text description (Suno writes the lyrics). Good for quick generation."""
    token = _get_token()
    payload = {
        "gpt_description_prompt": description,
        "make_instrumental": False,
        "mv": "chirp-v3-5",
        "prompt": "",
        "tags": style_tags
    }
    r = httpx.post(f"{API_BASE}/generate/v2/", headers=_api_headers(token),
                   json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    clips = data.get("clips", [])
    result = []
    for clip in clips:
        result.append(f"Track ID: {clip.get('id')}\nTitle: {clip.get('title')}\nStatus: {clip.get('status')}")
    return "\n\n".join(result) if result else str(data)

@mcp.tool()
def get_track_status(clip_id: str) -> str:
    """Check the generation status of a Suno track."""
    token = _get_token()
    r = httpx.get(f"{API_BASE}/feed/?ids={clip_id}", headers=_api_headers(token), timeout=30)
    r.raise_for_status()
    clips = r.json()
    if not clips:
        return "Track not found"
    clip = clips[0]
    return f"""Track: {clip.get('title')}
Status: {clip.get('status')}
Audio URL: {clip.get('audio_url', 'Not ready yet')}
Video URL: {clip.get('video_url', 'Not ready yet')}
Duration: {clip.get('metadata', {}).get('duration', 'Unknown')}s"""

@mcp.tool()
def get_credits() -> str:
    """Check remaining Suno credits."""
    token = _get_token()
    r = httpx.get(f"{API_BASE}/billing/info/", headers=_api_headers(token), timeout=30)
    r.raise_for_status()
    data = r.json()
    return f"Credits remaining: {data.get('total_credits_left', 'Unknown')}\nMonthly subscription: {data.get('subscription_type', 'Unknown')}"

if __name__ == "__main__":
    mcp.run()
