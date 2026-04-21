import os, httpx, statistics
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("trading-signals")
CG = "https://api.coingecko.com/api/v3"

def _cg(path: str, params: dict = {}) -> dict:
    r = httpx.get(f"{CG}{path}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def _get_ohlc(coin_id: str, days: int = 30) -> list:
    return _cg(f"/coins/{coin_id}/ohlc", {"vs_currency": "usd", "days": days})

def _get_prices(coin_id: str, days: int = 90) -> list:
    data = _cg(f"/coins/{coin_id}/market_chart", {"vs_currency": "usd", "days": days})
    return [p[1] for p in data["prices"]]

def _sma(prices: list, period: int) -> float:
    if len(prices) < period: return 0
    return sum(prices[-period:]) / period

def _ema(prices: list, period: int) -> float:
    if len(prices) < period: return 0
    k = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema

def _rsi(prices: list, period: int = 14) -> float:
    if len(prices) < period + 1: return 50
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        gains.append(max(0, diff))
        losses.append(max(0, -diff))
    avg_g = sum(gains[-period:]) / period
    avg_l = sum(losses[-period:]) / period
    if avg_l == 0: return 100
    rs = avg_g / avg_l
    return 100 - (100 / (1 + rs))

def _macd(prices: list) -> tuple:
    if len(prices) < 26: return 0, 0, 0
    ema12 = _ema(prices, 12)
    ema26 = _ema(prices, 26)
    macd_line = ema12 - ema26
    # Signal line (9 EMA of MACD) — simplified
    signal = macd_line * 0.9
    histogram = macd_line - signal
    return macd_line, signal, histogram

def _bollinger(prices: list, period: int = 20) -> tuple:
    if len(prices) < period: return 0, 0, 0
    subset = prices[-period:]
    mid = sum(subset) / period
    std = statistics.stdev(subset)
    return mid + 2*std, mid, mid - 2*std

def _atr(ohlc: list, period: int = 14) -> float:
    if len(ohlc) < period + 1: return 0
    trs = []
    for i in range(1, len(ohlc)):
        high = ohlc[i][2]
        low  = ohlc[i][3]
        prev_close = ohlc[i-1][4]
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    return sum(trs[-period:]) / period

@mcp.tool()
def full_technical_analysis(coin_id: str) -> str:
    """Run complete technical analysis on a coin — RSI, MACD, Bollinger, EMA, ATR, support/resistance."""
    prices = _get_prices(coin_id, 90)
    ohlc   = _get_ohlc(coin_id, 30)
    current = prices[-1]

    rsi = _rsi(prices)
    macd_line, signal, hist = _macd(prices)
    bb_upper, bb_mid, bb_lower = _bollinger(prices)
    ema_50  = _ema(prices[-50:], 50) if len(prices) >= 50 else _ema(prices, len(prices))
    ema_200 = _ema(prices, min(200, len(prices)))
    sma_20  = _sma(prices, 20)
    atr     = _atr(ohlc)

    # Support/Resistance from 30d range
    highs  = [c[2] for c in ohlc]
    lows   = [c[3] for c in ohlc]
    r1     = max(highs[-10:]) if ohlc else current * 1.05
    s1     = min(lows[-10:])  if ohlc else current * 0.95
    r2     = max(highs)       if ohlc else current * 1.10
    s2     = min(lows)        if ohlc else current * 0.90

    # Signal scoring
    score = 0
    notes = []

    if rsi < 30:   score += 2; notes.append("RSI Oversold — strong buy signal")
    elif rsi < 45: score += 1; notes.append("RSI below 45 — mildly bullish")
    elif rsi > 70: score -= 2; notes.append("RSI Overbought — caution")
    elif rsi > 55: score -= 1; notes.append("RSI elevated")

    if macd_line > signal: score += 1; notes.append("MACD bullish crossover")
    else: score -= 1; notes.append("MACD bearish")

    if hist > 0: score += 1; notes.append("MACD histogram positive")

    if current > ema_50:  score += 1; notes.append("Above 50 EMA")
    else: score -= 1; notes.append("Below 50 EMA")

    if current > ema_200: score += 1; notes.append("Above 200 EMA — macro bullish")
    else: score -= 1; notes.append("Below 200 EMA — macro bearish")

    if current < bb_lower: score += 2; notes.append("Below Bollinger lower — oversold bounce zone")
    elif current > bb_upper: score -= 2; notes.append("Above Bollinger upper — extended")
    else: notes.append("Inside Bollinger bands")

    if current < sma_20: score -= 1; notes.append("Below 20 SMA")
    else: score += 1; notes.append("Above 20 SMA")

    direction = "🟢 LONG" if score >= 3 else "🔴 SHORT" if score <= -3 else "🟡 WATCH"
    confidence = "HIGH" if abs(score) >= 5 else "MEDIUM" if abs(score) >= 3 else "LOW"

    # Entry/Stop/Target
    entry = current
    stop  = current - (atr * 2)
    t1    = current + (atr * 3)
    t2    = current + (atr * 5)
    rr    = (t1 - entry) / (entry - stop) if entry != stop else 0

    return f"""═══ TECHNICAL ANALYSIS — {coin_id.upper()} ═══

📊 INDICATORS
Current Price: ${current:,.4f}
RSI (14):    {rsi:.1f} {'🔴 OB' if rsi>70 else '🟢 OS' if rsi<30 else '🟡 Neutral'}
MACD:        {macd_line:.4f} | Signal: {signal:.4f} | Hist: {hist:.4f}
EMA 50:      ${ema_50:,.4f} ({'Above' if current > ema_50 else 'Below'})
EMA 200:     ${ema_200:,.4f} ({'Above' if current > ema_200 else 'Below'})
Bollinger:   Upper ${bb_upper:,.4f} | Mid ${bb_mid:,.4f} | Lower ${bb_lower:,.4f}
ATR (14):    ${atr:,.4f}

📍 KEY LEVELS
Resistance 2: ${r2:,.4f}
Resistance 1: ${r1:,.4f}
Current:      ${current:,.4f}
Support 1:    ${s1:,.4f}
Support 2:    ${s2:,.4f}

🎯 TRADE PLAN
Direction: {direction} | Confidence: {confidence}
Entry:   ${entry:,.4f}
Stop:    ${stop:,.4f} (-{((entry-stop)/entry*100):.1f}%)
Target1: ${t1:,.4f} (+{((t1-entry)/entry*100):.1f}%)
Target2: ${t2:,.4f} (+{((t2-entry)/entry*100):.1f}%)
R:R Ratio: {rr:.1f}:1 {'✅' if rr >= 2 else '❌ Skip — R:R too low'}

📝 SIGNAL NOTES
{chr(10).join(['• ' + n for n in notes])}

Score: {score}/12"""

@mcp.tool()
def momentum_scan(coins: str = "bitcoin,ethereum,solana,avalanche-2,chainlink") -> str:
    """Scan multiple coins for momentum signals — returns ranked by signal strength."""
    coin_list = [c.strip() for c in coins.split(",")]
    results = []
    for coin in coin_list:
        try:
            prices = _get_prices(coin, 30)
            current = prices[-1]
            rsi = _rsi(prices)
            macd_l, sig, hist = _macd(prices)
            ema50 = _ema(prices[-50:] if len(prices) >= 50 else prices, min(50, len(prices)))
            score = 0
            if rsi < 35: score += 2
            elif rsi < 45: score += 1
            elif rsi > 65: score -= 1
            elif rsi > 75: score -= 2
            if macd_l > sig: score += 1
            if hist > 0: score += 1
            if current > ema50: score += 1
            else: score -= 1
            direction = "LONG 🟢" if score >= 2 else "SHORT 🔴" if score <= -2 else "WATCH 🟡"
            results.append((score, f"{coin.upper()}: {direction} | RSI:{rsi:.0f} | Score:{score} | ${current:,.4f}"))
        except Exception as e:
            results.append((0, f"{coin.upper()}: Error - {e}"))
    results.sort(key=lambda x: x[0], reverse=True)
    return "═══ MOMENTUM SCAN ═══\n" + "\n".join([r[1] for r in results])

@mcp.tool()
def volume_anomaly_detector(coins: str = "bitcoin,ethereum,solana") -> str:
    """Detect unusual volume spikes — early signal for big moves."""
    coin_list = [c.strip() for c in coins.split(",")]
    results = []
    for coin in coin_list:
        try:
            data = _cg(f"/coins/{coin}/market_chart", {"vs_currency": "usd", "days": 30})
            volumes = [v[1] for v in data["total_volumes"]]
            avg_vol = sum(volumes[:-1]) / len(volumes[:-1])
            recent_vol = volumes[-1]
            ratio = recent_vol / avg_vol if avg_vol > 0 else 1
            signal = "🚨 SPIKE" if ratio > 2 else "📈 High" if ratio > 1.5 else "📊 Normal" if ratio > 0.7 else "📉 Low"
            results.append(f"{coin.upper()}: {signal} ({ratio:.2f}x avg) | ${recent_vol:,.0f}")
        except Exception as e:
            results.append(f"{coin}: Error - {e}")
    return "═══ VOLUME ANOMALY DETECTOR ═══\n" + "\n".join(results)

@mcp.tool()
def correlation_analysis(base_coin: str = "bitcoin", compare_coins: str = "ethereum,solana,cardano") -> str:
    """Check how correlated other coins are to BTC — portfolio diversification check."""
    base_prices  = _get_prices(base_coin, 30)
    compare_list = [c.strip() for c in compare_coins.split(",")]
    results = [f"Correlation to {base_coin.upper()} (30d):"]
    for coin in compare_list:
        try:
            prices = _get_prices(coin, 30)
            n = min(len(base_prices), len(prices))
            bp = base_prices[-n:]
            cp = prices[-n:]
            # Pearson correlation
            mean_b = sum(bp) / n
            mean_c = sum(cp) / n
            num   = sum((bp[i] - mean_b) * (cp[i] - mean_c) for i in range(n))
            den_b = sum((x - mean_b) ** 2 for x in bp) ** 0.5
            den_c = sum((x - mean_c) ** 2 for x in cp) ** 0.5
            corr  = num / (den_b * den_c) if den_b * den_c != 0 else 0
            label = "Very High" if corr > 0.85 else "High" if corr > 0.65 else "Moderate" if corr > 0.4 else "Low"
            results.append(f"  {coin.upper()}: {corr:.3f} ({label})")
        except Exception as e:
            results.append(f"  {coin}: Error")
    return "\n".join(results)

if __name__ == "__main__":
    mcp.run()
