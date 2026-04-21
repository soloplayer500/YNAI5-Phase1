import os, httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("opennews")
# Uses CryptoPanic API (free tier available)
API_KEY  = os.getenv("CRYPTOPANIC_API_KEY", "")
CGNEWS   = "https://api.coingecko.com/api/v3"
CP_BASE  = "https://cryptopanic.com/api/v1"

def _cg(endpoint: str, params: dict = {}) -> dict:
    r = httpx.get(f"{CGNEWS}{endpoint}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def _cp(endpoint: str, params: dict = {}) -> dict:
    p = {"auth_token": API_KEY, **params} if API_KEY else params
    r = httpx.get(f"{CP_BASE}{endpoint}", params=p, timeout=30)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def get_crypto_news(currencies: str = "BTC,ETH", kind: str = "news", limit: int = 10) -> str:
    """Get latest crypto news and signals. currencies: comma-separated tickers. kind: news or media"""
    try:
        data = _cp("/posts/", {"currencies": currencies, "kind": kind, "public": True})
        results = data.get("results", [])[:limit]
        lines = []
        for n in results:
            sentiment = ""
            if n.get("votes"):
                pos = n["votes"].get("positive", 0)
                neg = n["votes"].get("negative", 0)
                if pos > neg: sentiment = "🟢 Bullish"
                elif neg > pos: sentiment = "🔴 Bearish"
                else: sentiment = "🟡 Neutral"
            lines.append(f"{sentiment} [{n.get('published_at', '')[:10]}] {n['title']}\n  Source: {n.get('domain', 'N/A')}")
        return "\n\n".join(lines) if lines else "No news found"
    except Exception as e:
        # Fallback to CoinGecko news
        return get_coingecko_news(currencies.split(",")[0].lower())

@mcp.tool()
def get_coingecko_news(coin_id: str = "bitcoin", count: int = 10) -> str:
    """Get latest news from CoinGecko for a specific coin."""
    try:
        data = _cg(f"/coins/{coin_id}", {"localization": False, "tickers": False, "community_data": True})
        info = []
        info.append(f"Coin: {data.get('name')} ({data.get('symbol', '').upper()})")
        info.append(f"Current Price: ${data['market_data']['current_price']['usd']:,.2f}")
        info.append(f"24h Change: {data['market_data']['price_change_percentage_24h']:.2f}%")
        info.append(f"7d Change: {data['market_data']['price_change_percentage_7d']:.2f}%")
        info.append(f"Market Cap Rank: #{data.get('market_cap_rank', 'N/A')}")
        info.append(f"Sentiment: Positive={data['sentiment_votes_up_percentage']:.1f}% Negative={data['sentiment_votes_down_percentage']:.1f}%")
        return "\n".join(info)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def get_trending_coins() -> str:
    """Get trending crypto coins on CoinGecko right now — signal intelligence."""
    data = _cg("/search/trending")
    coins = data.get("coins", [])
    lines = []
    for c in coins[:10]:
        coin = c["item"]
        lines.append(f"#{coin.get('market_cap_rank', '?')} {coin['name']} ({coin['symbol']}) — Score: {coin.get('score', 'N/A')}")
    return "\n".join(lines) if lines else "No trending data"

@mcp.tool()
def get_market_overview(vs_currency: str = "usd", top: int = 20) -> str:
    """Get top crypto market overview — price, volume, and change data."""
    data = _cg("/coins/markets", {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": top,
        "page": 1,
        "price_change_percentage": "24h,7d"
    })
    lines = ["Rank | Coin | Price | 24h% | 7d%"]
    for c in data:
        lines.append(f"#{c['market_cap_rank']} {c['symbol'].upper()} ${c['current_price']:,.4f} | 24h: {c.get('price_change_percentage_24h', 0):.2f}% | 7d: {c.get('price_change_percentage_7d_in_currency', 0):.2f}%")
    return "\n".join(lines)

@mcp.tool()
def get_fear_greed() -> str:
    """Get the Crypto Fear & Greed Index — key sentiment signal for Block Syndicate."""
    r = httpx.get("https://api.alternative.me/fng/?limit=3", timeout=30)
    r.raise_for_status()
    data = r.json()["data"]
    lines = []
    for d in data:
        lines.append(f"Date: {d.get('timestamp', 'N/A')} | Index: {d['value']} | Sentiment: {d['value_classification']}")
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run()
