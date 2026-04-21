import os, time, hmac, hashlib, base64, urllib.parse
import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("kraken")
API_KEY    = os.getenv("KRAKEN_API_KEY", "")
API_SECRET = os.getenv("KRAKEN_API_SECRET", "")
BASE       = "https://api.kraken.com"

def _sign(urlpath: str, data: dict, secret: str) -> str:
    postdata = urllib.parse.urlencode(data)
    encoded  = (str(data["nonce"]) + postdata).encode()
    message  = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    return base64.b64encode(mac.digest()).decode()

def _private(method: str, params: dict = {}) -> dict:
    path   = f"/0/private/{method}"
    nonce  = str(int(time.time() * 1000))
    data   = {"nonce": nonce, **params}
    sig    = _sign(path, data, API_SECRET)
    r = httpx.post(
        f"{BASE}{path}",
        headers={"API-Key": API_KEY, "API-Sign": sig},
        data=data, timeout=30
    )
    r.raise_for_status()
    j = r.json()
    if j.get("error"): raise ValueError(f"Kraken error: {j['error']}")
    return j["result"]

def _public(method: str, params: dict = {}) -> dict:
    r = httpx.get(f"{BASE}/0/public/{method}", params=params, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("error"): raise ValueError(f"Kraken error: {j['error']}")
    return j["result"]

@mcp.tool()
def get_balance() -> str:
    """Get all Kraken account balances."""
    result = _private("Balance")
    lines = []
    for asset, amount in result.items():
        if float(amount) > 0:
            lines.append(f"{asset}: {float(amount):.8f}")
    return "\n".join(lines) if lines else "No balances found"

@mcp.tool()
def get_ticker(pair: str) -> str:
    """Get current price data for a trading pair. Example: XBTUSD, ETHUSD, SOLUSD"""
    result = _public("Ticker", {"pair": pair})
    for k, v in result.items():
        return f"""Pair: {k}
Last Price: {v['c'][0]}
24h High: {v['h'][1]}
24h Low:  {v['l'][1]}
24h Volume: {v['v'][1]}
24h VWAP: {v['p'][1]}
Bid: {v['b'][0]} | Ask: {v['a'][0]}"""

@mcp.tool()
def get_ohlc(pair: str, interval: int = 60) -> str:
    """Get OHLC candle data. interval in minutes: 1,5,15,30,60,240,1440,10080"""
    result = _public("OHLC", {"pair": pair, "interval": interval})
    candles = list(result.values())[0][-10:]  # last 10 candles
    lines = ["Time | Open | High | Low | Close | Volume"]
    for c in candles:
        import datetime
        t = datetime.datetime.fromtimestamp(c[0]).strftime("%Y-%m-%d %H:%M")
        lines.append(f"{t} | {c[1]} | {c[2]} | {c[3]} | {c[4]} | {c[6]}")
    return "\n".join(lines)

@mcp.tool()
def get_order_book(pair: str, count: int = 5) -> str:
    """Get order book depth for a pair."""
    result = _public("Depth", {"pair": pair, "count": count})
    data = list(result.values())[0]
    asks = "\n".join([f"  ASK {a[0]} @ {a[1]}" for a in data["asks"][:count]])
    bids = "\n".join([f"  BID {b[0]} @ {b[1]}" for b in data["bids"][:count]])
    return f"ORDER BOOK — {pair}\n\n{asks}\n---\n{bids}"

@mcp.tool()
def get_open_orders() -> str:
    """Get all currently open orders."""
    result = _private("OpenOrders")
    orders = result.get("open", {})
    if not orders:
        return "No open orders"
    lines = []
    for oid, o in orders.items():
        d = o["descr"]
        lines.append(f"ID: {oid}\n  {d['order']} | Status: {o['status']} | Price: {o['price']}")
    return "\n\n".join(lines)

@mcp.tool()
def get_trade_history(count: int = 20) -> str:
    """Get recent trade history."""
    result = _private("TradesHistory", {"trades": True})
    trades = list(result.get("trades", {}).items())[:count]
    lines = []
    for tid, t in trades:
        import datetime
        ts = datetime.datetime.fromtimestamp(t["time"]).strftime("%Y-%m-%d %H:%M")
        lines.append(f"{ts} | {t['pair']} | {t['type'].upper()} {t['vol']} @ {t['price']} | PnL: {t.get('net', 'N/A')}")
    return "\n".join(lines) if lines else "No trade history"

@mcp.tool()
def place_order(pair: str, side: str, order_type: str, volume: str, price: str = "", validate: bool = True) -> str:
    """Place a Kraken order. side=buy/sell, order_type=limit/market, validate=True for dry run (SAFE)."""
    params = {
        "pair": pair,
        "type": side,
        "ordertype": order_type,
        "volume": volume,
        "validate": validate
    }
    if price:
        params["price"] = price
    result = _private("AddOrder", params)
    if validate:
        return f"VALIDATION ONLY (no real order placed):\n{result['descr']['order']}"
    return f"Order placed: {result.get('txid', ['unknown'])}"

@mcp.tool()
def cancel_order(txid: str) -> str:
    """Cancel an open order by transaction ID."""
    result = _private("CancelOrder", {"txid": txid})
    return f"Cancelled {result.get('count', 0)} order(s)"

@mcp.tool()
def get_portfolio_summary() -> str:
    """Get full portfolio with current USD values — ready for APEX risk analysis."""
    balances = _private("Balance")
    lines = ["KRAKEN PORTFOLIO\n" + "="*40]
    total_usd = 0
    for asset, amount in balances.items():
        amt = float(amount)
        if amt < 0.0001: continue
        if asset in ("ZUSD", "USD"):
            lines.append(f"USD:    ${amt:,.2f}")
            total_usd += amt
            continue
        # get USD price
        pair = f"XBT/USD" if asset in ("XBT","XXBT") else f"{asset.lstrip('X').lstrip('Z')}/USD"
        try:
            ticker_pair = f"X{asset}ZUSD" if not asset.startswith("Z") else f"{asset}ZUSD"
            t = _public("Ticker", {"pair": ticker_pair})
            price = float(list(t.values())[0]["c"][0])
            usd_val = amt * price
            total_usd += usd_val
            lines.append(f"{asset}: {amt:.6f} @ ${price:,.2f} = ${usd_val:,.2f}")
        except:
            lines.append(f"{asset}: {amt:.6f} (price unavailable)")
    lines.append("="*40)
    lines.append(f"TOTAL: ~${total_usd:,.2f} USD")
    return "\n".join(lines)

if __name__ == "__main__":
    mcp.run()
