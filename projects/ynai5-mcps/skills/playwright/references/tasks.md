# PLAYWRIGHT — Task Patterns & Execution Guide

---

## Crypto Data Scraping Patterns

### CoinGecko — Price + Market Data
```
Navigate: https://www.coingecko.com/en/coins/{coin-id}
Extract:
  - Current price (USD)
  - 24h change %
  - Market cap
  - 24h volume
  - All-time high / low
Wait for: .no-wrap price elements to populate (dynamic)
Output: structured table
```

### CoinMarketCap — Rankings + Signals
```
Navigate: https://coinmarketcap.com/currencies/{coin-slug}/
Extract:
  - Price, rank, dominance %
  - Fear & Greed Index (homepage widget)
  - Trending coins sidebar
Output: signal brief for Block Syndicate
```

### TradingView — Chart Data
```
Navigate: https://www.tradingview.com/symbols/{PAIR}/
Extract:
  - Current price
  - RSI reading (if visible in summary)
  - Analyst ratings
  - Technical summary (buy/sell/neutral)
Output: TA brief for APEX Lens #6
```

### Kraken Web UI — Portfolio Snapshot
```
Navigate: https://www.kraken.com/u/trade/balance
Requires: authenticated session
Extract:
  - All asset balances
  - USD value per asset
  - Total portfolio value
Output: holdings table → feed to APEX Lens #3 (Bridgewater Risk)
```

---

## News & Trend Monitoring Patterns

### X (Twitter) — AI Trending
```
Navigate: https://x.com/explore
Tab: Trending
Filter: Technology / AI
Extract: top 10 trending topics + tweet counts
Time filter: past 24 hours
Output: trend brief for OpenMind AI content
```

### Reddit — r/artificial Intelligence
```
Navigate: https://www.reddit.com/r/artificial/hot/
Extract:
  - Top 10 posts (title, upvotes, comment count)
  - Flair/category if present
Output: news brief ranked by engagement
```

### YouTube — AI Trending Videos
```
Navigate: https://www.youtube.com/results?search_query=AI+news+today&sp=CAI%3D
Extract:
  - Top 5 video titles
  - Channel names
  - View counts
  - Upload time
Output: video brief for content inspiration
```

### TikTok Discover — AI Trends
```
Navigate: https://www.tiktok.com/discover
Search: "AI" or "artificial intelligence"
Extract:
  - Trending hashtags
  - Top sounds related to AI content
Output: trend brief for OpenMind AI TikTok strategy
```

---

## Content Posting Patterns

### Twitter/X — Post Content
```
Navigate: https://x.com/compose/tweet
Action sequence:
  1. Click compose area
  2. Type content (280 char limit enforced)
  3. If thread: click "+" for each additional tweet
  4. If media: click media icon → upload
  5. CONFIRM with Solo before clicking Post
```

### Instagram — Caption Draft
```
Note: Instagram web has limited posting capability
Navigate: https://www.instagram.com/
Action: Use Creator Studio or Meta Business Suite instead
Redirect: https://business.facebook.com/creatorstudio
```

### LinkedIn — Post
```
Navigate: https://www.linkedin.com/
Action sequence:
  1. Click "Start a post"
  2. Type or paste content
  3. Add hashtags at end
  4. CONFIRM before posting
```

---

## Web Build Debug Patterns

### Full Page Screenshot + Audit
```
Navigate: [localhost URL or deployed URL]
Actions:
  1. Screenshot full page (scroll capture)
  2. Evaluate: window.console.errors (capture JS errors)
  3. Evaluate: document.querySelectorAll('[style*="overflow"]') (check layout)
  4. Evaluate: performance.timing (load time metrics)
Report:
  - Visual issues observed
  - JS errors found
  - Performance metrics
  - Specific elements to fix with location
```

### Mobile Viewport Test
```
Set viewport: 375x812 (iPhone 14)
Navigate: [URL]
Screenshot: capture mobile render
Check: nav, CTAs, text readability, image sizing
Report: mobile-specific issues
```

---

## Research Patterns

### Site-Specific Data Extraction
```
1. Navigate to URL
2. Wait for content to fully load (look for loading spinners to disappear)
3. Identify target data location (headline, table, card)
4. Evaluate JS to extract text: document.querySelector('[selector]').textContent
5. Clean and format output
6. Note: URL + timestamp of extraction for reference
```

### Multi-Page Scraping
```
1. Start at index/listing page
2. Extract all item links
3. Loop: navigate to each → extract detail → return to list
4. Aggregate into single structured output
Note: Add 1-2 second delays between pages
```
