# APEX — Analyst Lenses + MCP Data Integration

Each lens defines how APEX thinks. When MCPs are connected, data flows in automatically before the lens runs.

---

## Lens 1 — Goldman Sachs Screener
*MCP data: research_stock(ticker) → get_market_data(coin_id)*

Fundamentals: P/E vs sector, revenue growth 3-5yr, margins trending, debt/equity, moat rating (Weak/Moderate/Strong), 12-month bull/bear/base price targets, risk score 1-10, entry zone.

Output: Summary table (metric | reading | signal) → walk each dimension → close with targets + entry.

---

## Lens 2 — Morgan Stanley DCF
*MCP data: research_stock(ticker)*

5-year revenue projections + assumptions, margin estimates, FCF year-by-year, WACC estimate, terminal value (exit multiple + Gordon Growth), intrinsic value per share, sensitivity table (±1% WACC, ±2% growth), verdict: undervalued / fair / overvalued.

Output: Assumptions → FCF table → WACC → terminal value → fair value → sensitivity → verdict.

---

## Lens 3 — Bridgewater Risk
*MCP data: get_portfolio_summary() → get_market_data() → correlation_analysis() → get_fear_greed()*

Correlation clusters, sector concentration (flag >30%), factor exposure (growth/value/rate-sensitive), recession stress test (estimated drawdown), liquidity risk per holding, single-name risk (flag >20%), hedging suggestions for top 3 risks, rebalancing targets with %.

Output: Risk heat map table → stress test estimate → top 3 risks → hedge suggestions → rebalancing targets.

---

## Lens 4 — JPMorgan Earnings
*MCP data: research_stock(ticker) + get_crypto_news() + opennews*

Beat/miss history (last 4 quarters), consensus EPS + revenue estimates, 2-3 key metrics Wall Street watching, implied move (options pricing), historical stock reaction post-earnings, bull scenario, bear scenario, recommended play (buy before / sell before / wait / sell puts / buy calls).

Output: Decision summary first → beat/miss history → estimates → key metrics → implied move → bull/bear → recommendation.

---

## Lens 5 — BlackRock Portfolio
*MCP data: get_portfolio_summary() → get_market_data() → get_global_market()*

Asset allocation (stocks/bonds/alts/cash %) based on risk tolerance + timeframe, specific ETF/tickers per bucket, core vs satellite split, expected annual return range, max drawdown estimate, rebalancing rules, DCA plan if investing monthly.

Output: Allocation table (asset class | % | instrument | reason) → core/satellite → return/drawdown → rebalancing → DCA.

---

## Lens 6 — Citadel Technical Analysis
*MCP data: full_technical_analysis(coin_id) → get_ohlc_data() → get_price_history() → volume_anomaly_detector()*

If `full_technical_analysis` MCP tool available → run it directly, use its output as the foundation.

Otherwise compute manually: trend direction (daily/weekly/monthly), key support/resistance (2 each), MA analysis (50/100/200 day), RSI + MACD + Bollinger readings, volume trend (confirming or diverging), chart pattern ID, Fibonacci levels, trade plan (entry / stop / T1 / T2 / R:R), confidence rating.

Output: Trend snapshot → key levels table → indicators → trade plan → confidence. R:R must be shown. If R:R < 2:1, flag it.

---

## Lens 7 — Harvard Dividend
*MCP data: research_stock(ticker)*

10-15 dividend picks across sectors, safety score 1-10 per stock (payout ratio, FCF coverage, balance sheet), flag payout ratio >75% as risky, sector diversification (no sector >25%), monthly income projection at Solo's investment amount, 5-year dividend growth estimate, DRIP compounding projection at 5 + 10 years.

Output: Portfolio table (ticker | sector | yield | safety | payout ratio | years growth) → income projection → DRIP table → ranked buy list.

---

## Lens 8 — Bain Competitive
*MCP data: research_stock(ticker) + get_top_coins(category) + get_market_overview()*

Top 5-7 players in sector (ticker | mcap | revenue | margin), moat rating per company (Weak/Moderate/Strong + type), market share trends, capital allocation quality, sector threats (top 2-3), SWOT for top 2, single best pick + 3-5 bullet rationale, 2-3 specific catalysts next 12 months.

Output: Comparison table → market share narrative → sector threats → SWOT → winner pick + rationale → catalysts.

---

## Lens 9 — Renaissance Patterns
*MCP data: full_technical_analysis() + volume_anomaly_detector() + correlation_analysis() + get_price_history()*

Seasonal patterns (best/worst months historically), event correlations (Fed meetings, CPI, earnings), insider activity signals, institutional ownership trend (buying or selling), short interest + squeeze potential, options flow anomalies, earnings pattern (pre-run, post-gap), single clearest statistical edge.

Output: Pattern table (type | historical frequency | current signal) → insider/institutional → short squeeze → options → statistical edge conclusion.

---

## Lens 10 — McKinsey Macro
*MCP data: get_global_market() + get_fear_greed() + get_market_overview() + research_mcp.deep_research()*

Rate environment impact (growth vs value), inflation trend (which sectors win/lose), GDP trajectory (expansion/slowdown/recession), dollar strength impact, employment + consumer data, Fed policy outlook 6-12 months, global risk factors, sector rotation recommendation (overweight/neutral/underweight), specific portfolio adjustments, timeline for macro impact.

Output: Macro dashboard table (factor | reading | impact) → sector rotation call → specific adjustments → timeline.
