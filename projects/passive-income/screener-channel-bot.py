#!/usr/bin/env python3
"""
Block Syndicate — Daily Signals Bot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Runs daily at 8AM AST via GitHub Actions.
Posts top crypto + stock setups to Telegram channels.

FREE channel (@BlockSyndicate_bot):   teaser cards only
VIP channel (@BlockSyndicatevip_bot): full signals with entry/stop/target

Data sources: CoinGecko (free), Yahoo Finance (free), stdlib only
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ── UTF-8 fix ─────────────────────────────────────────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ── Config ─────────────────────────────────────────────────────────────────────
HERE        = Path(__file__).resolve().parent
ENV_PATH    = HERE.parent.parent / ".env.local"
LOG_DIR     = HERE / "logs"
LOG_DIR.mkdir(exist_ok=True)

FREE_CHANNEL  = "@BlockSyndicate_bot"    # public discovery channel
VIP_CHANNEL   = "@BlockSyndicatevip_bot" # paid premium channel

SEP = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Watchlist: always check these stocks (free Yahoo Finance)
STOCK_WATCHLIST = ["NVDA", "TSLA", "META", "MSFT", "AAPL", "AMD", "PLTR", "COIN"]

# Crypto: top candidates (CoinGecko IDs)
CRYPTO_UNIVERSE = [
    "bitcoin", "ethereum", "solana", "sui", "avalanche-2",
    "chainlink", "injective-protocol", "render-token", "fetch-ai",
    "aptos", "arbitrum", "optimism", "pepe", "dogecoin", "shiba-inu"
]


# ── Env loader ────────────────────────────────────────────────────────────────
def load_env() -> dict:
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"')
    return env


ENV = load_env()
BOT_TOKEN        = ENV.get("TELEGRAM_BOT_TOKEN", "")
COINGECKO_KEY    = ENV.get("COINGECKO_API_KEY", "")
GEMINI_KEY       = ENV.get("GEMINI_API_KEY", "")


# ── HTTP helpers ───────────────────────────────────────────────────────────────
def http_get(url: str, headers: dict = None, timeout: int = 12) -> dict | list | None:
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "YNAI5/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"[HTTP] GET failed: {url[:60]}... → {e}")
        return None


def tg_send(chat_id: str, text: str) -> bool:
    """Send a Telegram message to a channel."""
    if not BOT_TOKEN:
        print("[TG] No bot token — skipping send")
        return False
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id":    chat_id,
        "text":       text,
        "parse_mode": "HTML"
    }).encode()
    req = urllib.request.Request(url, data=data,
                                  headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read())
            if result.get("ok"):
                return True
            print(f"[TG] Error: {result.get('description')}")
            return False
    except Exception as e:
        print(f"[TG] Send failed to {chat_id}: {e}")
        return False


# ── CoinGecko data ────────────────────────────────────────────────────────────
def fetch_crypto_data() -> list[dict]:
    """Fetch price, volume, and momentum data for screener universe."""
    ids = ",".join(CRYPTO_UNIVERSE)
    url = (
        f"https://api.coingecko.com/api/v3/coins/markets"
        f"?vs_currency=usd&ids={ids}"
        f"&order=volume_desc&per_page=50&page=1"
        f"&price_change_percentage=24h,7d"
    )
    headers = {"User-Agent": "YNAI5/1.0"}
    if COINGECKO_KEY:
        headers["x-cg-demo-api-key"] = COINGECKO_KEY
    time.sleep(1)
    return http_get(url, headers) or []


def fetch_market_overview() -> dict:
    """Fetch global crypto market data (BTC dominance, total cap)."""
    time.sleep(1)
    data = http_get("https://api.coingecko.com/api/v3/global") or {}
    g = data.get("data", {})
    return {
        "btc_dominance": round(g.get("market_cap_percentage", {}).get("btc", 0), 1),
        "total_mcap_b":  round((g.get("total_market_cap", {}).get("usd", 0)) / 1e9, 0),
        "market_cap_change_24h": round(g.get("market_cap_change_percentage_24h_usd", 0), 2),
    }


# ── Scoring engine ────────────────────────────────────────────────────────────
def score_crypto(coin: dict) -> float:
    """
    Score each coin 0–10 based on:
    - Momentum (24h + 7d change direction) — 35%
    - Volume/MCap ratio (activity signal) — 25%
    - RSI proxy (magnitude of recent move) — 25%
    - Price vs ATH (room to run) — 15%
    """
    score = 0.0
    ch24  = coin.get("price_change_percentage_24h") or 0
    ch7d  = coin.get("price_change_percentage_7d_in_currency") or 0
    vol   = coin.get("total_volume") or 0
    mcap  = coin.get("market_cap") or 1
    ath   = coin.get("ath") or 1
    price = coin.get("current_price") or 0

    # Momentum score (both timeframes positive = strong)
    if ch24 > 0 and ch7d > 0:   score += 3.5
    elif ch24 > 0 and ch7d < 0: score += 2.0   # reversal candidate
    elif ch24 < -5 and ch7d < -10: score += 1.5  # oversold bounce candidate

    # Volume/MCap ratio (higher = more active)
    vol_ratio = vol / mcap
    if vol_ratio > 0.25:   score += 2.5
    elif vol_ratio > 0.10: score += 1.5
    elif vol_ratio > 0.05: score += 0.5

    # RSI proxy: extreme 24h move = oversold/overbought signal
    if -20 < ch24 < -8:  score += 2.0   # oversold bounce setup
    elif 5 < ch24 < 15:  score += 1.5   # momentum continuation
    elif ch24 > 15:      score += 1.0   # breakout (riskier)
    elif -5 < ch24 < 5:  score += 0.5   # consolidation

    # Distance from ATH (room to run)
    if price > 0 and ath > 0:
        pct_from_ath = ((ath - price) / ath) * 100
        if 30 < pct_from_ath < 70:  score += 1.5   # good upside potential
        elif pct_from_ath > 70:     score += 0.5   # too beaten down

    return round(min(score, 10.0), 1)


def determine_signal(coin: dict) -> tuple[str, str, str, str]:
    """Return (signal_type, entry, target, stop) based on price data."""
    price = coin.get("current_price") or 0
    ch24  = coin.get("price_change_percentage_24h") or 0
    ch7d  = coin.get("price_change_percentage_7d_in_currency") or 0
    ath   = coin.get("ath") or price * 3

    def fmt(p):
        if p >= 1000: return f"${p:,.0f}"
        elif p >= 1:  return f"${p:.2f}"
        else:         return f"${p:.4f}"

    if ch24 < -8 and ch7d < -15:
        # Oversold bounce play
        signal = "🟢 OVERSOLD BOUNCE"
        entry  = fmt(price * 0.98)
        target = fmt(price * 1.18)
        stop   = fmt(price * 0.90)
    elif ch24 > 5 and ch7d > 10:
        # Momentum play
        signal = "🚀 MOMENTUM"
        entry  = fmt(price * 1.01)
        target = fmt(price * 1.15)
        stop   = fmt(price * 0.93)
    elif -5 < ch24 < 3 and ch7d > 5:
        # Pullback into uptrend
        signal = "📉 PULLBACK ENTRY"
        entry  = fmt(price * 0.97)
        target = fmt(price * 1.20)
        stop   = fmt(price * 0.89)
    else:
        # Consolidation breakout watch
        signal = "👁 WATCH"
        entry  = fmt(price * 0.99)
        target = fmt(price * 1.12)
        stop   = fmt(price * 0.92)

    return signal, entry, target, stop


def screen_crypto(coins: list[dict], top_n: int = 3) -> list[dict]:
    """Score and rank coins, return top N setups."""
    scored = []
    for coin in coins:
        if not coin.get("current_price"):
            continue
        score = score_crypto(coin)
        signal, entry, target, stop = determine_signal(coin)
        scored.append({
            "symbol":  coin["symbol"].upper(),
            "name":    coin["name"],
            "price":   coin.get("current_price", 0),
            "ch24":    coin.get("price_change_percentage_24h") or 0,
            "ch7d":    coin.get("price_change_percentage_7d_in_currency") or 0,
            "vol":     coin.get("total_volume") or 0,
            "score":   score,
            "signal":  signal,
            "entry":   entry,
            "target":  target,
            "stop":    stop,
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


# ── Yahoo Finance stock data ───────────────────────────────────────────────────
def fetch_stock(ticker: str) -> dict | None:
    """Fetch stock quote from Yahoo Finance (free, no auth)."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
    data = http_get(url, timeout=8)
    if not data:
        return None
    try:
        meta   = data["chart"]["result"][0]["meta"]
        price  = meta.get("regularMarketPrice", 0)
        prev   = meta.get("chartPreviousClose", price)
        ch24   = ((price - prev) / prev * 100) if prev else 0
        return {
            "ticker": ticker,
            "price":  price,
            "ch24":   round(ch24, 2),
            "52wHigh": meta.get("fiftyTwoWeekHigh", price * 1.3),
            "52wLow":  meta.get("fiftyTwoWeekLow",  price * 0.7),
        }
    except Exception:
        return None


def screen_stocks(tickers: list[str], top_n: int = 2) -> list[dict]:
    """Fetch and rank stocks from watchlist."""
    results = []
    for ticker in tickers:
        s = fetch_stock(ticker)
        if not s or s["price"] == 0:
            continue
        ch = s["ch24"]
        # Simple score: absolute 24h move + distance from 52w high
        dist_from_high = ((s["52wHigh"] - s["price"]) / s["52wHigh"]) * 100
        score = 0.0
        if -8 < ch < -3:   score += 4.0   # healthy pullback
        elif 2 < ch < 8:   score += 3.5   # momentum
        elif ch > 8:        score += 2.0   # breakout risk
        if 20 < dist_from_high < 50: score += 3.0
        elif dist_from_high < 20:    score += 1.0

        entry  = f"${s['price'] * 0.99:.2f}"
        target = f"${s['price'] * 1.12:.2f}"
        stop   = f"${s['price'] * 0.93:.2f}"

        if ch < -3:   sig = "📉 PULLBACK BUY"
        elif ch > 3:  sig = "🚀 MOMENTUM"
        else:         sig = "👁 WATCH"

        results.append({
            "ticker": ticker,
            "price":  s["price"],
            "ch24":   ch,
            "score":  round(score, 1),
            "signal": sig,
            "entry":  entry,
            "target": target,
            "stop":   stop,
        })
        time.sleep(0.3)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


# ── Message builders ───────────────────────────────────────────────────────────
def build_vip_crypto_card(coin: dict, rank: int) -> str:
    ch24_arrow = "▲" if coin["ch24"] >= 0 else "▼"
    ch24_str   = f"{ch24_arrow} {abs(coin['ch24']):.1f}%"
    ch7d_arrow = "▲" if coin["ch7d"] >= 0 else "▼"
    ch7d_str   = f"{ch7d_arrow} {abs(coin['ch7d']):.1f}%"

    price = coin["price"]
    if price >= 1000:   price_str = f"${price:,.0f}"
    elif price >= 1:    price_str = f"${price:.2f}"
    else:               price_str = f"${price:.4f}"

    return (
        f"<b>#{rank} {coin['symbol']} — {coin['signal']}</b>\n"
        f"💰 Price:  {price_str}\n"
        f"📊 24h: {ch24_str}  |  7d: {ch7d_str}\n"
        f"🎯 Entry:  {coin['entry']}\n"
        f"🚀 Target: {coin['target']}\n"
        f"🛑 Stop:   {coin['stop']}\n"
        f"⭐ Score:  {coin['score']}/10"
    )


def build_vip_stock_card(s: dict, rank: int) -> str:
    arrow = "▲" if s["ch24"] >= 0 else "▼"
    return (
        f"<b>#{rank} {s['ticker']} — {s['signal']}</b>\n"
        f"💰 Price:  ${s['price']:.2f}\n"
        f"📊 24h: {arrow} {abs(s['ch24']):.1f}%\n"
        f"🎯 Entry:  {s['entry']}\n"
        f"🚀 Target: {s['target']}\n"
        f"🛑 Stop:   {s['stop']}\n"
        f"⭐ Score:  {s['score']}/10"
    )


def build_vip_message(date_str: str, overview: dict,
                       crypto: list[dict], stocks: list[dict]) -> str:
    dom = overview.get("btc_dominance", 0)
    mcap_chg = overview.get("market_cap_change_24h", 0)
    mood_arrow = "▲" if mcap_chg >= 0 else "▼"
    btc_regime = "Risk-OFF (alts weak)" if dom > 57 else "Risk-ON (alts active)" if dom < 50 else "Neutral"

    header = (
        f"{SEP}\n"
        f"🔐 <b>BLOCK SYNDICATE VIP</b>\n"
        f"📅 Daily Signals — {date_str}\n"
        f"{SEP}\n\n"
        f"<b>🌍 MARKET OVERVIEW</b>\n"
        f"BTC Dominance: {dom}%  →  {btc_regime}\n"
        f"Total MCap: {mood_arrow} {abs(mcap_chg):.1f}% (24h)\n\n"
    )

    crypto_section = "<b>⚡ CRYPTO SETUPS</b>\n\n"
    for i, c in enumerate(crypto, 1):
        crypto_section += build_vip_crypto_card(c, i) + "\n\n"

    stock_section = "<b>📈 STOCK SETUPS</b>\n\n"
    for i, s in enumerate(stocks, 1):
        stock_section += build_vip_stock_card(s, i) + "\n\n"

    footer = (
        f"{SEP}\n"
        f"⚠️ <i>Educational only. Not financial advice.\n"
        f"Always use your own risk management.</i>\n"
        f"{SEP}"
    )
    return header + crypto_section + stock_section + footer


def build_free_message(date_str: str, crypto: list[dict], stocks: list[dict]) -> str:
    """Teaser only — tickers and direction, no entry/stop/target."""
    lines = [
        f"{SEP}",
        f"📡 <b>BLOCK SYNDICATE</b> — Daily Signals",
        f"📅 {date_str}",
        f"{SEP}\n",
        f"<b>Today's Top Setups:</b>\n",
    ]
    for c in crypto:
        arrow = "🟢" if "BOUNCE" in c["signal"] or "MOMENTUM" in c["signal"] else "👁"
        lines.append(f"{arrow} <b>{c['symbol']}</b> — {c['signal'].split(' ', 1)[-1]}")

    for s in stocks:
        arrow = "🟢" if "BUY" in s["signal"] or "MOMENTUM" in s["signal"] else "👁"
        lines.append(f"{arrow} <b>${s['ticker']}</b> — {s['signal'].split(' ', 1)[-1]}")

    lines += [
        "",
        "🔐 <b>Full signals (entry / stop / target) →</b>",
        "Join VIP: <i>see pinned message for link</i>",
        "",
        f"{SEP}",
        f"<i>Educational only. Not financial advice.</i>",
        f"{SEP}",
    ]
    return "\n".join(lines)


# ── AI analyst (optional) ─────────────────────────────────────────────────────
def ai_market_take(overview: dict, crypto: list[dict]) -> str:
    """Get a 2-sentence market take from Gemini (optional, skipped if no key)."""
    if not GEMINI_KEY:
        return ""
    dom = overview.get("btc_dominance", 0)
    top = crypto[0]["symbol"] if crypto else "BTC"
    prompt = (
        f"BTC dominance is {dom}%. Top signal today: {top}. "
        f"Give me a 2-sentence crypto market outlook for today. Be direct and specific. "
        f"No fluff. End with one actionable insight."
    )
    url  = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    req  = urllib.request.Request(url, data=body,
                                   headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return ""


# ── Logger ────────────────────────────────────────────────────────────────────
def log_run(date_str: str, crypto: list[dict], stocks: list[dict], success: bool):
    log_file = LOG_DIR / f"screener-{date_str[:7]}.log"
    entry = {
        "date":    date_str,
        "success": success,
        "crypto":  [{"symbol": c["symbol"], "score": c["score"], "signal": c["signal"]} for c in crypto],
        "stocks":  [{"ticker": s["ticker"], "score": s["score"], "signal": s["signal"]} for s in stocks],
    }
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    now      = datetime.now(timezone.utc)
    date_str = now.strftime("%B %d, %Y")
    print(f"\n{SEP}")
    print(f"  Block Syndicate Screener — {date_str}")
    print(f"{SEP}")

    # 1. Fetch data
    print("[1/4] Fetching market overview...")
    overview = fetch_market_overview()
    print(f"      BTC Dom: {overview.get('btc_dominance')}%  |  MCap chg: {overview.get('market_cap_change_24h')}%")

    print("[2/4] Fetching crypto data...")
    raw_coins = fetch_crypto_data()
    print(f"      Got {len(raw_coins)} coins")

    print("[3/4] Screening stocks...")
    stocks = screen_stocks(STOCK_WATCHLIST, top_n=2)
    print(f"      Top stocks: {[s['ticker'] for s in stocks]}")

    # 2. Screen
    crypto = screen_crypto(raw_coins, top_n=3)
    print(f"      Top crypto: {[c['symbol'] for c in crypto]}")

    # 3. Build messages
    print("[4/4] Sending to Telegram...")
    ai_take = ai_market_take(overview, crypto)

    vip_msg  = build_vip_message(date_str, overview, crypto, stocks)
    if ai_take:
        vip_msg += f"\n\n💡 <b>AI Take:</b>\n<i>{ai_take}</i>"

    free_msg = build_free_message(date_str, crypto, stocks)

    # 4. Send
    ok_vip  = tg_send(VIP_CHANNEL,  vip_msg)
    time.sleep(1)
    ok_free = tg_send(FREE_CHANNEL, free_msg)

    status = "✅" if ok_vip and ok_free else "⚠️ partial"
    print(f"      VIP channel: {'✅' if ok_vip else '❌'}")
    print(f"      Free channel: {'✅' if ok_free else '❌'}")

    # 5. Log
    log_run(date_str, crypto, stocks, ok_vip and ok_free)

    print(f"\n{SEP}")
    print(f"  Done — {status}")
    print(f"{SEP}\n")

    return 0 if (ok_vip and ok_free) else 1


if __name__ == "__main__":
    sys.exit(main())
