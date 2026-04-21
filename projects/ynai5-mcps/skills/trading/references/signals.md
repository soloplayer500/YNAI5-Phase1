# TRADING — Signal Logic Reference

## Signal Quality Ratings
| Score | Criteria Met | Action |
|---|---|---|
| 5-6 | STRONG | Publish VIP + Public immediately |
| 4 | GOOD | Publish VIP + Public |
| 3 | MODERATE | VIP only, developing setup |
| 1-2 | WEAK | Watch only — do not publish |

## Position Sizing Rule
Risk per trade = Portfolio × 1-2% max
Position size = Risk ÷ (Entry price - Stop price)

## Kraken Pairs Reference
BTC=XBTUSD | ETH=ETHUSD | SOL=SOLUSD | ADA=ADAUSD | LINK=LINKUSD | DOT=DOTUSD | AVAX=AVAXUSD | MATIC=MATICUSD

## MCP Call Reference
kraken.get_balance() — holdings
kraken.get_ticker(pair) — live price
kraken.get_ohlc(pair, interval) — candles (interval=60,240,1440)
kraken.place_order(..., validate=True) — ALWAYS validate first
trading_signals.full_technical_analysis(coin_id) — RSI/MACD/BB/EMA/ATR/levels
hive_crypto.run_signal_scan(coins) — multi-coin scan
opennews.get_fear_greed() — market sentiment
