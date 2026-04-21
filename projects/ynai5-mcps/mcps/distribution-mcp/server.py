import os, httpx, json
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("distribution")

AYRSHARE_KEY = os.getenv("AYRSHARE_API_KEY", "")
AYRSHARE_URL = "https://app.ayrshare.com/api"

def _ayr(method: str, endpoint: str, data: dict = {}) -> dict:
    headers = {"Authorization": f"Bearer {AYRSHARE_KEY}", "Content-Type": "application/json"}
    if method == "POST":
        r = httpx.post(f"{AYRSHARE_URL}{endpoint}", headers=headers, json=data, timeout=30)
    else:
        r = httpx.get(f"{AYRSHARE_URL}{endpoint}", headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

# ── PLATFORM FORMATTERS ──────────────────────────────────────────

def _format_twitter(content: str, hashtags: list = []) -> str:
    tags = " ".join([f"#{h.lstrip('#')}" for h in hashtags[:5]])
    post = f"{content}\n\n{tags}" if tags else content
    return post[:280]

def _format_instagram(content: str, hashtags: list = []) -> str:
    tags = " ".join([f"#{h.lstrip('#')}" for h in hashtags[:30]])
    return f"{content[:2000]}\n\n.\n.\n.\n{tags}"

def _format_linkedin(content: str) -> str:
    return content[:3000]

def _format_tiktok(content: str, hashtags: list = []) -> str:
    tags = " ".join([f"#{h.lstrip('#')}" for h in hashtags[:8]])
    return f"{content[:150]}\n{tags}"

# ── POSTING TOOLS ────────────────────────────────────────────────

@mcp.tool()
def post_to_platforms(content: str, platforms: str, hashtags: str = "",
                       schedule_date: str = "") -> str:
    """Post content to multiple platforms at once via Ayrshare.
    platforms: comma-separated: twitter,instagram,linkedin,facebook,youtube,tiktok
    hashtags: comma-separated tags without #
    schedule_date: ISO format '2024-12-25T10:00:00Z' or empty for immediate"""
    if not AYRSHARE_KEY:
        return "Ayrshare API key not set. Add AYRSHARE_API_KEY to .env"
    platform_list = [p.strip() for p in platforms.split(",")]
    tag_list = [h.strip() for h in hashtags.split(",") if h.strip()]
    payload = {
        "post": content,
        "platforms": platform_list,
        "hashtags": tag_list
    }
    if schedule_date:
        payload["scheduleDate"] = schedule_date
    result = _ayr("POST", "/post", payload)
    return json.dumps(result, indent=2)

@mcp.tool()
def post_ynai5_content(content: str, content_type: str = "ai_news",
                        platforms: str = "twitter,instagram") -> str:
    """Post YNAI5-branded content with automatic formatting and hashtags per content type.
    content_type: ai_news, crypto_signal, music, brand, announcement"""
    hashtag_map = {
        "ai_news":       ["AI", "ArtificialIntelligence", "OpenMindAI", "AINews", "Tech", "YNAI5"],
        "crypto_signal": ["Crypto", "BlockSyndicate", "YNAI5", "Bitcoin", "Trading", "CryptoSignals"],
        "music":         ["Symphony", "YNAI5", "AIMusic", "Suno", "TrapMusic", "MusicProduction"],
        "brand":         ["YNAI5", "AI", "Automation", "SoloOperator", "BuildInPublic"],
        "announcement":  ["YNAI5", "Announcement", "AI", "Community"]
    }
    hashtags = hashtag_map.get(content_type, ["YNAI5"])
    return post_to_platforms(content, platforms, ",".join(hashtags))

@mcp.tool()
def format_for_platform(content: str, platform: str, hashtags: str = "") -> str:
    """Format content correctly for a specific platform — returns ready-to-post text."""
    tags = [h.strip() for h in hashtags.split(",") if h.strip()]
    if platform.lower() == "twitter":
        return _format_twitter(content, tags)
    elif platform.lower() == "instagram":
        return _format_instagram(content, tags)
    elif platform.lower() == "linkedin":
        return _format_linkedin(content)
    elif platform.lower() == "tiktok":
        return _format_tiktok(content, tags)
    else:
        return content

@mcp.tool()
def create_cross_post_package(content: str, hashtags: str = "YNAI5,AI") -> str:
    """Format one piece of content for ALL platforms simultaneously — returns formatted versions."""
    tags = [h.strip() for h in hashtags.split(",") if h.strip()]
    return f"""═══ CROSS-POST PACKAGE ═══

📱 TWITTER (280 chars):
{_format_twitter(content, tags)}

📸 INSTAGRAM (caption):
{_format_instagram(content, tags[:30])}

💼 LINKEDIN:
{_format_linkedin(content)}

🎵 TIKTOK (caption):
{_format_tiktok(content, tags[:8])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Say 'post all' to publish, or specify platforms."""

@mcp.tool()
def get_analytics() -> str:
    """Get post analytics from Ayrshare — reach, engagement, impressions."""
    if not AYRSHARE_KEY:
        return "Ayrshare API key not set"
    result = _ayr("GET", "/analytics/social")
    return json.dumps(result, indent=2)

@mcp.tool()
def schedule_content_week(content_items: str) -> str:
    """Schedule multiple posts across a week. content_items = JSON array of {content, platform, schedule_date}"""
    if not AYRSHARE_KEY:
        return "Ayrshare API key not set. Add AYRSHARE_API_KEY to .env"
    try:
        items = json.loads(content_items)
        results = []
        for item in items:
            result = _ayr("POST", "/post", {
                "post": item["content"],
                "platforms": item.get("platforms", ["twitter"]),
                "scheduleDate": item["schedule_date"]
            })
            results.append(f"✅ Scheduled: {item['content'][:50]}... → {item['schedule_date']}")
        return "\n".join(results)
    except Exception as e:
        return f"Error scheduling: {e}"

@mcp.tool()
def get_best_posting_times(platform: str = "twitter") -> str:
    """Get optimal posting times for each platform for YNAI5's crypto/AI audience."""
    times = {
        "twitter":   "Best times: 8-9am EST, 12-1pm EST, 5-6pm EST. Crypto audience peaks 8pm-midnight EST.",
        "instagram": "Best times: 9-11am EST, 1-3pm EST. Reels perform best 9-10am and 6-8pm.",
        "tiktok":    "Best times: 7-9am EST, 12-3pm EST, 7-9pm EST. Post daily for algorithm boost.",
        "linkedin":  "Best times: Tue-Thu, 8-10am and 12-1pm EST. Avoid weekends.",
        "facebook":  "Best times: Wed 11am-1pm EST. Thu-Fri 1-4pm EST.",
        "telegram":  "Post anytime — Telegram channels don't have algorithm. Consistency matters more."
    }
    return times.get(platform.lower(), "Platform not found. Try: twitter, instagram, tiktok, linkedin, telegram")

if __name__ == "__main__":
    mcp.run()
