---
name: distribution
description: >
  DISTRIBUTION — Activate this skill for any content posting, scheduling, cross-platform publishing, Telegram channel management, or social media distribution task. Triggers on: "post this", "publish to", "send to Telegram", "schedule", "cross-post", "put this on", "share to", "push to my channels", "OpenMind AI post", "Block Syndicate alert", "YNAI5 content", or any task where content needs to go out to one or more platforms. Handles Telegram (Block Syndicate + Openclaw), X/Twitter, TikTok, Instagram, YouTube, and LinkedIn. Formats content per platform automatically. Uses Telegram MCP (60+ tools), Ayrshare MCP (13+ platforms), and PLAYWRIGHT as fallback for platforms without MCP coverage.
---

# DISTRIBUTION — Multi-Platform Content Publishing

DISTRIBUTION is the last mile of every YNAI5 pipeline. Content comes in → formats per platform → routes to the right MCP → confirms delivery.

Platform specs → `references/platforms.md`

---

## Full Pipeline — How It Runs

```
[Content arrives from TRADING/SYMPHONY/RESEARCH/Solo]
         ↓
DISTRIBUTION Step 1: Identify destination
  → Which channels? (Block Syndicate / OpenMind AI / YNAI5 brand / all)
  → Content type? (signal / AI news / music / brand / announcement)
         ↓
DISTRIBUTION Step 2: Format per platform
  → Load references/platforms.md specs
  → Twitter: ≤280 chars, 3-5 hashtags
  → Instagram: 125 char hook, hashtags in first comment
  → Telegram: markdown, bold for signals
  → TikTok: 150 chars ideal, 5-8 hashtags
         ↓
DISTRIBUTION Step 3: Show preview + confirm
  → Display formatted content per platform
  → "Confirm to publish or say 'edit [platform]'"
  → Wait for Solo's green light
         ↓
DISTRIBUTION Step 4: Route to MCPs
  → Telegram signals: telegram.send_block_syndicate_signal()
  → Telegram general: telegram.send_message()
  → Multi-platform: distribution-mcp.post_ynai5_content()
  → TikTok (no Ayrshare): playwright → navigate → post
         ↓
DISTRIBUTION Step 5: Confirm
  → "Posted to [platforms] at [time]"
  → Log what went where
```

---

## MCP Routing Map

| Content Type | Destination | MCP to Call |
|---|---|---|
| Block Syndicate signal | Telegram (public + VIP) | `telegram.send_block_syndicate_signal()` |
| Openclaw announcement | Telegram (Openclaw channel) | `telegram.send_message()` |
| YNAI5 brand post | X + IG + LinkedIn | `distribution.post_ynai5_content(type="brand")` |
| OpenMind AI content | TikTok | `playwright` → navigate suno.ai or TikTok |
| AI news post | X + IG | `distribution.post_ynai5_content(type="ai_news")` |
| Music release | All platforms | `distribution.post_ynai5_content(type="music")` |
| Cross-post all | All | `distribution.create_cross_post_package()` then post |
| Schedule content | Future date | `distribution.post_to_platforms(schedule_date=...)` |

---

## MCP Call Reference

```python
# Signal to Telegram
telegram.send_block_syndicate_signal(
    channel="@BlockSyndicate",
    asset="BTC", direction="LONG",
    entry_low="95000", entry_high="96000",
    target1="102000", target2="110000",
    stop_loss="91000", thesis="RSI oversold + MACD crossover",
    vip=False
)

# VIP signal
telegram.send_block_syndicate_signal(channel=VIP_CHANNEL_ID, ..., vip=True)
telegram.pin_message(channel=VIP_CHANNEL_ID, message_id=last_id)

# Multi-platform brand post
distribution.post_ynai5_content(
    content="[post text]",
    content_type="ai_news",
    platforms="twitter,instagram"
)

# Get best times
distribution.get_best_posting_times("tiktok")

# Schedule for later
distribution.post_to_platforms(
    content="[text]",
    platforms="twitter,instagram",
    hashtags="AI,YNAI5",
    schedule_date="2024-12-25T10:00:00Z"
)

# Playwright fallback for TikTok
playwright.navigate("https://www.tiktok.com")
playwright.type("[caption + hashtags]")
playwright.confirm_with_solo_before_submit()
```

---

## Content Type Hashtag Sets

| Type | Auto-hashtags |
|---|---|
| ai_news | #AI #ArtificialIntelligence #OpenMindAI #AINews #Tech #YNAI5 |
| crypto_signal | #Crypto #BlockSyndicate #YNAI5 #Bitcoin #Trading #CryptoSignals |
| music | #Symphony #YNAI5 #AIMusic #Suno #TrapMusic #MusicProduction |
| brand | #YNAI5 #AI #Automation #SoloOperator #BuildInPublic |
| announcement | #YNAI5 #Announcement #AI #Community |

---

## Output Rules

1. **Always preview before publishing** — never auto-post without confirmation
2. **Always format per platform** — one size never fits all
3. **Signals bypass preview** for public channel — VIP signals need confirm
4. **Track delivery** — confirm back what went where + timestamp
5. **Playwright fallback** for any platform without MCP (TikTok, emerging platforms)
6. **Never exceed hashtag limits** — Twitter 5, TikTok 8, Instagram 30

---

## Pipeline Connections

- **← TRADING**: Signal formatted → DISTRIBUTION routes to Telegram channels
- **← SYMPHONY**: Track released → DISTRIBUTION posts to music channels + all socials
- **← RESEARCH**: Content brief angles → DISTRIBUTION formats + schedules
- **← ALIGN**: Any content task scoped through ALIGN first
- **→ TELEGRAM MCP**: Primary distribution channel
- **→ DISTRIBUTION MCP**: Multi-platform via Ayrshare
- **→ PLAYWRIGHT**: TikTok + any platform without native MCP support
