import os, httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("hive-crypto")
CG  = "https://api.coingecko.com/api/v3"
CMC = "https://pro-api.coinmarketcap.com/v1"
CMC_KEY = os.getenv("CMC_API_KEY", "")
LC_KEY  = os.getenv("LUNARCRUSH_API_KEY", "")
LC_BASE = "https://lunarcrush.com/api4/public"

def _cg(path: str, params: dict = {}) -> dict:
    r = httpx.get(f"{CG}{path}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def _lc(path: str, params: dict = {}) -> dict:
    h = {"Authorization": f"Bearer {LC_KEY}"} if LC_KEY else {}
    r = httpx.get(f"{LC_BASE}{path}", headers=h, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

# ── PRICE & MARKET DATA ──────────────────────────────────────────

@mcp.tool()
def get_price(coins: str, vs: str = "usd") -> str:
    """Get current price for one or more coins. coins = comma-separated IDs like 'bitcoin,ethereum,solana'"""
    data = _cg("/simple/price", {
        "ids": coins, "vs_currencies": vs,
        "include_24hr_change": True, "include_market_cap": True, "include_24hr_vol": True
    })
    lines = []
    for coin, info in data.items():
        lines.append(
            f"{coin.upper()}: ${info.get(vs, 0):,.4f} | "
            f"24h: {info.get(f'{vs}_24h_change', 0):.2f}% | "
            f"Vol: ${info.get(f'{vs}_24h_vol', 0):,.0f} | "
            f"MCap: ${info.get(f'{vs}_market_cap', 0):,.0f}"
        )
    return "\n".join(lines)

@mcp.tool()
def get_market_data(coin_id: str) -> str:
    """Full market data for one coin — price, ATH, ATL, supply, rank, sentiment."""
    data = _cg(f"/coins/{coin_id}", {
        "localization": False, "tickers": False,
        "market_data": True, "community_data": True
    })
    md = data["market_data"]
    return f"""═══ {data['name']} ({data['symbol'].upper()}) ═══
Rank: #{data.get('market_cap_rank', 'N/A')}
Price: ${md['current_price']['usd']:,.6f}
24h Change: {md['price_change_percentage_24h']:.2f}%
7d Change:  {md['price_change_percentage_7d']:.2f}%
30d Change: {md['price_change_percentage_30d']:.2f}%
Market Cap: ${md['market_cap']['usd']:,.0f}
Volume 24h: ${md['total_volume']['usd']:,.0f}
ATH: ${md['ath']['usd']:,.6f} ({md['ath_change_percentage']['usd']:.1f}% from ATH)
ATL: ${md['atl']['usd']:,.6f}
Circulating Supply: {md.get('circulating_supply', 0):,.0f}
Total Supply: {md.get('total_supply', 0) or 'N/A'}
Sentiment Positive: {data.get('sentiment_votes_up_percentage', 0):.1f}%"""

@mcp.tool()
def get_top_coins(limit: int = 25, category: str = "") -> str:
    """Get top coins by market cap. Optional category filter: defi, nft, layer-1, layer-2"""
    params = {"vs_currency": "usd", "order": "market_cap_desc",
              "per_page": limit, "page": 1, "price_change_percentage": "1h,24h,7d"}
    if category:
        params["category"] = category
    data = _cg("/coins/markets", params)
    lines = ["# | Symbol | Price | 1h% | 24h% | 7d% | Volume"]
    for c in data:
        lines.append(
            f"#{c['market_cap_rank']} {c['symbol'].upper()} "
            f"${c['current_price']:,.4f} | "
            f"1h:{c.get('price_change_percentage_1h_in_currency', 0):.1f}% | "
            f"24h:{c.get('price_change_percentage_24h_in_currency', 0):.1f}% | "
            f"7d:{c.get('price_change_percentage_7d_in_currency', 0):.1f}% | "
            f"${c['total_volume']:,.0f}"
        )
    return "\n".join(lines)

@mcp.tool()
def get_trending_coins() -> str:
    """Get trending coins on CoinGecko — early signal intelligence."""
    data = _cg("/search/trending")
    lines = ["TRENDING COINS:"]
    for c in data.get("coins", []):
        item = c["item"]
        lines.append(f"#{item.get('market_cap_rank','?')} {item['name']} ({item['symbol']}) — Score: {item.get('score',0)}")
    nfts = data.get("nfts", [])
    if nfts:
        lines.append("\nTRENDING NFTs:")
        for n in nfts[:3]:
            lines.append(f"  {n['name']} — Floor: {n.get('floor_price_in_native_currency', 'N/A')}")
    return "\n".join(lines)

@mcp.tool()
def get_global_market() -> str:
    """Get global crypto market overview — total mcap, BTC dominance, fear & greed."""
    data = _cg("/global")["data"]
    fg = httpx.get("https://api.alternative.me/fng/", timeout=10).json()["data"][0]
    return f"""═══ GLOBAL CRYPTO MARKET ═══
Total Market Cap: ${data['total_market_cap']['usd']:,.0f}
24h Volume: ${data['total_volume']['usd']:,.0f}
BTC Dominance: {data['market_cap_percentage'].get('btc', 0):.1f}%
ETH Dominance: {data['market_cap_percentage'].get('eth', 0):.1f}%
Active Coins: {data['active_cryptocurrencies']:,}
Markets: {data['markets']:,}
24h Change: {data['market_cap_change_percentage_24h_usd']:.2f}%

Fear & Greed: {fg['value']} — {fg['value_classification']}"""

# ── TECHNICAL ANALYSIS ───────────────────────────────────────────

@mcp.tool()
def get_ohlc_data(coin_id: str, days: int = 14, vs: str = "usd") -> str:
    """Get OHLC candle data for technical analysis. days: 1,7,14,30,90,180,365"""
    data = _cg(f"/coins/{coin_id}/ohlc", {"vs_currency": vs, "days": days})
    if not data:
        return "No OHLC data available"
    # Compute basic TA from OHLC
    closes = [c[4] for c in data]
    highs  = [c[2] for c in data]
    lows   = [c[3] for c in data]
    current = closes[-1]
    high_period = max(highs)
    low_period  = min(lows)
    avg = sum(closes) / len(closes)
    # RSI approximation
    gains = [max(0, closes[i] - closes[i-1]) for i in range(1, len(closes))]
    losses = [max(0, closes[i-1] - closes[i]) for i in range(1, len(closes))]
    avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else sum(gains) / max(len(gains), 1)
    avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else sum(losses) / max(len(losses), 1)
    rsi = 100 - (100 / (1 + avg_gain / avg_loss)) if avg_loss != 0 else 100
    return f"""═══ OHLC ANALYSIS — {coin_id.upper()} ({days}d) ═══
Current: ${current:,.4f}
{days}d High: ${high_period:,.4f} ({((current/high_period)-1)*100:.1f}% from high)
{days}d Low:  ${low_period:,.4f} ({((current/low_period)-1)*100:.1f}% from low)
{days}d Avg:  ${avg:,.4f}
RSI (14): {rsi:.1f} {'🔴 Overbought' if rsi > 70 else '🟢 Oversold' if rsi < 30 else '🟡 Neutral'}
Position in range: {((current-low_period)/(high_period-low_period)*100):.1f}%"""

@mcp.tool()
def get_price_history(coin_id: str, days: int = 30, vs: str = "usd") -> str:
    """Get price history with key levels — support, resistance, trend."""
    data = _cg(f"/coins/{coin_id}/market_chart", {"vs_currency": vs, "days": days})
    prices = [p[1] for p in data["prices"]]
    volumes = [v[1] for v in data["total_volumes"]]
    current = prices[-1]
    high = max(prices)
    low  = min(prices)
    # Simple trend
    mid = len(prices) // 2
    first_half_avg  = sum(prices[:mid]) / mid
    second_half_avg = sum(prices[mid:]) / max(len(prices[mid:]), 1)
    trend = "📈 Uptrend" if second_half_avg > first_half_avg else "📉 Downtrend"
    avg_vol = sum(volumes) / len(volumes)
    recent_vol = sum(volumes[-3:]) / 3
    vol_signal = "📊 Rising volume" if recent_vol > avg_vol else "📊 Declining volume"
    return f"""═══ PRICE ANALYSIS — {coin_id.upper()} ({days}d) ═══
Current: ${current:,.4f}
Trend: {trend}
{days}d High (Resistance): ${high:,.4f}
{days}d Low (Support): ${low:,.4f}
Range Size: {((high-low)/low*100):.1f}%
{vol_signal} (recent vs avg: {recent_vol/avg_vol:.2f}x)"""

# ── SOCIAL & SENTIMENT ───────────────────────────────────────────

@mcp.tool()
def get_social_sentiment(coin_slug: str) -> str:
    """Get social sentiment data via LunarCrush. coin_slug: bitcoin, ethereum, solana etc."""
    try:
        data = _lc(f"/coins/{coin_slug}/v1")
        c = data.get("data", {})
        return f"""═══ SOCIAL SENTIMENT — {coin_slug.upper()} ═══
Galaxy Score: {c.get('galaxy_score', 'N/A')} / 100
Alt Rank: #{c.get('alt_rank', 'N/A')}
Social Volume (24h): {c.get('social_volume_24h', 'N/A'):,}
Social Score: {c.get('social_score', 'N/A')}
Social Dominance: {c.get('social_dominance', 'N/A')}%
Sentiment: {c.get('sentiment', 'N/A')}
News Volume: {c.get('news', 'N/A')}
Reddit Posts: {c.get('reddit_posts', 'N/A')}
Tweets: {c.get('tweets', 'N/A')}"""
    except:
        return f"LunarCrush data unavailable. Set LUNARCRUSH_API_KEY in .env for social sentiment."

@mcp.tool()
def get_fear_greed() -> str:
    """Get Fear & Greed Index — key Block Syndicate signal input."""
    r = httpx.get("https://api.alternative.me/fng/?limit=7", timeout=30)
    data = r.json()["data"]
    lines = ["FEAR & GREED INDEX (7 days)"]
    for d in data:
        import datetime
        ts = datetime.datetime.fromtimestamp(int(d["timestamp"])).strftime("%Y-%m-%d")
        bar = "🟢" if int(d["value"]) > 60 else "🔴" if int(d["value"]) < 40 else "🟡"
        lines.append(f"{ts}: {bar} {d['value']} — {d['value_classification']}")
    return "\n".join(lines)

# ── ON-CHAIN DATA ────────────────────────────────────────────────

@mcp.tool()
def get_defi_stats() -> str:
    """Get global DeFi stats — TVL, volume, top protocols."""
    try:
        r = httpx.get("https://api.llama.fi/global", timeout=30)
        data = r.json()
        chains_r = httpx.get("https://api.llama.fi/v2/chains", timeout=30)
        chains = chains_r.json()[:5]
        chain_lines = "\n".join([f"  {c['name']}: ${c.get('tvl', 0):,.0f}" for c in chains])
        return f"""═══ DEFI GLOBAL STATS ═══
Total TVL: ${data.get('totalLiquidityUSD', 0):,.0f}
24h Change: {data.get('change_1d', 0):.2f}%
7d Change: {data.get('change_7d', 0):.2f}%

Top Chains by TVL:
{chain_lines}"""
    except Exception as e:
        return f"DeFi data error: {e}"

@mcp.tool()
def get_exchange_volumes() -> str:
    """Get top crypto exchange volumes — whale activity indicator."""
    data = _cg("/exchanges", {"per_page": 10})
    lines = ["TOP EXCHANGES BY VOLUME (24h BTC normalized)"]
    for e in data:
        lines.append(f"{e.get('trust_score_rank','?')}. {e['name']}: {e.get('trade_volume_24h_btc', 0):.0f} BTC")
    return "\n".join(lines)

# ── BLOCK SYNDICATE SIGNAL BUILDER ──────────────────────────────

@mcp.tool()
def run_signal_scan(coins: str = "bitcoin,ethereum,solana,cardano,polkadot") -> str:
    """Run a multi-coin signal scan — outputs signal strength for each. coins = comma-separated IDs"""
    coin_list = [c.strip() for c in coins.split(",")]
    results = []
    fg_r = httpx.get("https://api.alternative.me/fng/", timeout=10).json()["data"][0]
    fg_val = int(fg_r["value"])
    market_bias = "🟢 Bullish market" if fg_val > 60 else "🔴 Bearish market" if fg_val < 40 else "🟡 Neutral market"

    for coin in coin_list:
        try:
            data = _cg(f"/coins/{coin}", {"localization": False, "tickers": False, "market_data": True})
            md = data["market_data"]
            change_24h = md["price_change_percentage_24h"]
            change_7d  = md["price_change_percentage_7d"]
            change_30d = md["price_change_percentage_30d"]
            vol_24h    = md["total_volume"]["usd"]
            mcap       = md["market_cap"]["usd"]
            price      = md["current_price"]["usd"]
            vol_mcap   = vol_24h / mcap if mcap > 0 else 0

            # Signal scoring
            score = 0
            signals = []
            if change_24h > 5:  score += 2; signals.append("Strong 24h pump")
            elif change_24h > 2: score += 1; signals.append("Positive 24h")
            elif change_24h < -10: score -= 2; signals.append("Heavy 24h dump")
            elif change_24h < -5:  score -= 1; signals.append("Negative 24h")

            if change_7d > 15: score += 2; signals.append("Strong weekly trend")
            elif change_7d > 5: score += 1; signals.append("Positive weekly")
            elif change_7d < -20: score -= 2; signals.append("Bearish weekly")

            if vol_mcap > 0.15: score += 1; signals.append("High volume activity")
            if fg_val > 70: score += 1; signals.append("Greed market")
            elif fg_val < 30: score -= 1; signals.append("Fear market")

            rating = "⭐⭐⭐⭐⭐ STRONG" if score >= 4 else \
                     "⭐⭐⭐⭐ GOOD" if score >= 2 else \
                     "⭐⭐⭐ NEUTRAL" if score >= 0 else \
                     "⭐⭐ WEAK" if score >= -2 else \
                     "⭐ BEARISH"

            direction = "LONG" if score >= 2 else "SHORT" if score <= -2 else "WATCH"

            results.append(f"{rating}\n{data['symbol'].upper()} — {direction}\n${price:,.4f} | 24h:{change_24h:+.1f}% | 7d:{change_7d:+.1f}%\nSignals: {', '.join(signals) if signals else 'No clear signal'}")
        except Exception as e:
            results.append(f"❌ {coin}: {e}")

    header = f"═══ BLOCK SYNDICATE SCANNER ═══\n{market_bias} (F&G: {fg_val})\n"
    return header + "\n\n".join(results)

if __name__ == "__main__":
    mcp.run()
