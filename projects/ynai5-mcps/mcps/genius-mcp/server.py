import os, httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("genius")
TOKEN = os.getenv("GENIUS_ACCESS_TOKEN", "")
BASE  = "https://api.genius.com"

def _get(endpoint: str, params: dict = {}) -> dict:
    r = httpx.get(f"{BASE}{endpoint}",
                  headers={"Authorization": f"Bearer {TOKEN}"},
                  params=params, timeout=30)
    r.raise_for_status()
    return r.json()["response"]

@mcp.tool()
def search_songs(query: str, per_page: int = 5) -> str:
    """Search for songs on Genius. Returns title, artist, and song ID."""
    data = _get("/search", {"q": query, "per_page": per_page})
    hits = data.get("hits", [])
    results = []
    for h in hits:
        s = h["result"]
        results.append(f"ID: {s['id']}\nTitle: {s['full_title']}\nArtist: {s['primary_artist']['name']}\nViews: {s.get('pageviews', 'N/A')}")
    return "\n\n".join(results) if results else "No results found"

@mcp.tool()
def get_song_details(song_id: int) -> str:
    """Get full details about a song including description, album, and metadata."""
    data = _get(f"/songs/{song_id}", {"text_format": "plain"})
    s = data["song"]
    return f"""Title: {s['full_title']}
Artist: {s['primary_artist']['name']}
Album: {s.get('album', {}).get('name', 'N/A') if s.get('album') else 'N/A'}
Release Date: {s.get('release_date', 'N/A')}
Page Views: {s.get('pageviews', 'N/A')}
Description: {s.get('description', {}).get('plain', 'N/A')[:500] if s.get('description') else 'N/A'}
Lyrics URL: {s.get('url', 'N/A')}"""

@mcp.tool()
def get_artist_songs(artist_id: int, sort: str = "popularity", per_page: int = 10) -> str:
    """Get top songs by an artist. sort: popularity or title"""
    data = _get(f"/artists/{artist_id}/songs", {"sort": sort, "per_page": per_page})
    songs = data.get("songs", [])
    results = [f"ID: {s['id']} | {s['full_title']}" for s in songs]
    return "\n".join(results) if results else "No songs found"

@mcp.tool()
def search_artist(name: str) -> str:
    """Find an artist on Genius and get their ID."""
    data = _get("/search", {"q": name, "per_page": 3})
    hits = data.get("hits", [])
    seen = set()
    results = []
    for h in hits:
        artist = h["result"]["primary_artist"]
        if artist["id"] not in seen:
            seen.add(artist["id"])
            results.append(f"Artist: {artist['name']}\nID: {artist['id']}\nURL: {artist.get('url', 'N/A')}")
    return "\n\n".join(results) if results else "Artist not found"

@mcp.tool()
def get_song_annotations(song_id: int) -> str:
    """Get community annotations/explanations for a song — great for understanding meaning."""
    data = _get(f"/songs/{song_id}", {"text_format": "plain"})
    referents = data.get("song", {})
    return f"Song: {referents.get('full_title', 'Unknown')}\nURL (view lyrics + annotations): {referents.get('url', 'N/A')}"

if __name__ == "__main__":
    mcp.run()
