import os, base64, httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("spotify")
CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
BASE          = "https://api.spotify.com/v1"
_token_cache  = {"token": "", "expires": 0}

import time

def _get_token() -> str:
    if _token_cache["token"] and time.time() < _token_cache["expires"]:
        return _token_cache["token"]
    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    r = httpx.post("https://accounts.spotify.com/api/token",
                   headers={"Authorization": f"Basic {creds}"},
                   data={"grant_type": "client_credentials"}, timeout=30)
    r.raise_for_status()
    data = r.json()
    _token_cache["token"] = data["access_token"]
    _token_cache["expires"] = time.time() + data["expires_in"] - 60
    return _token_cache["token"]

def _get(endpoint: str, params: dict = {}) -> dict:
    r = httpx.get(f"{BASE}{endpoint}",
                  headers={"Authorization": f"Bearer {_get_token()}"},
                  params=params, timeout=30)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def search_track(query: str, limit: int = 5) -> str:
    """Search for tracks on Spotify. Returns name, artist, BPM-ready info."""
    data = _get("/search", {"q": query, "type": "track", "limit": limit})
    tracks = data["tracks"]["items"]
    results = []
    for t in tracks:
        artists = ", ".join([a["name"] for a in t["artists"]])
        results.append(f"ID: {t['id']}\n{t['name']} — {artists}\nAlbum: {t['album']['name']} ({t['album']['release_date'][:4]})\nPopularity: {t['popularity']}/100")
    return "\n\n".join(results) if results else "No tracks found"

@mcp.tool()
def get_track_features(track_id: str) -> str:
    """Get audio features for a track — BPM, key, energy, danceability, valence."""
    data = _get(f"/audio-features/{track_id}")
    return f"""BPM (Tempo): {data['tempo']:.1f}
Key: {['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][data['key']]} {'Major' if data['mode'] == 1 else 'Minor'}
Energy: {data['energy']:.2f} / 1.0
Danceability: {data['danceability']:.2f} / 1.0
Valence (positivity): {data['valence']:.2f} / 1.0
Instrumentalness: {data['instrumentalness']:.2f}
Acousticness: {data['acousticness']:.2f}
Duration: {int(data['duration_ms']/1000)}s"""

@mcp.tool()
def get_artist_info(artist_name: str) -> str:
    """Get artist info including genres, popularity, and followers."""
    data = _get("/search", {"q": artist_name, "type": "artist", "limit": 1})
    artists = data["artists"]["items"]
    if not artists:
        return "Artist not found"
    a = artists[0]
    return f"""Artist: {a['name']}
ID: {a['id']}
Genres: {', '.join(a['genres'][:5]) if a['genres'] else 'N/A'}
Popularity: {a['popularity']}/100
Followers: {a['followers']['total']:,}"""

@mcp.tool()
def get_artist_top_tracks(artist_name: str, market: str = "US") -> str:
    """Get top tracks by an artist — useful for Symphony reference analysis."""
    search = _get("/search", {"q": artist_name, "type": "artist", "limit": 1})
    artists = search["artists"]["items"]
    if not artists:
        return "Artist not found"
    artist_id = artists[0]["id"]
    data = _get(f"/artists/{artist_id}/top-tracks", {"market": market})
    results = []
    for t in data["tracks"][:8]:
        results.append(f"ID: {t['id']} | {t['name']} | Popularity: {t['popularity']}/100")
    return "\n".join(results)

@mcp.tool()
def get_recommendations(seed_artists: str = "", seed_tracks: str = "",
                         seed_genres: str = "", limit: int = 10,
                         target_energy: float = None, target_tempo: float = None) -> str:
    """Get Spotify track recommendations for Symphony reference research."""
    params = {"limit": limit}
    if seed_artists: params["seed_artists"] = seed_artists
    if seed_tracks:  params["seed_tracks"]  = seed_tracks
    if seed_genres:  params["seed_genres"]  = seed_genres
    if target_energy: params["target_energy"] = target_energy
    if target_tempo:  params["target_tempo"]  = target_tempo
    data = _get("/recommendations", params)
    results = []
    for t in data["tracks"]:
        artists = ", ".join([a["name"] for a in t["artists"]])
        results.append(f"ID: {t['id']} | {t['name']} — {artists}")
    return "\n".join(results) if results else "No recommendations found"

if __name__ == "__main__":
    mcp.run()
