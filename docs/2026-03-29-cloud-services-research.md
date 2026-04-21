# Cloud Services Research — Automation Infrastructure
_Research date: 2026-03-29 | Purpose: Always-on hosting for Python bots + video processing + automation pipelines_
_Hardware constraint: HP Laptop, Ryzen 5, 8GB RAM, no dedicated GPU_

---

## 1. Cloud Compute — Always-On Python Hosting

### Quick Reference Table

| Service | Free Tier | Always-On | MCP Available | YNAI5 Fit |
|---------|-----------|-----------|---------------|-----------|
| Oracle Cloud (ARM) | 4 vCPU / 24GB RAM — truly free forever | YES — no sleep, no credits | No official MCP | ⭐⭐⭐⭐⭐ |
| Koyeb | 1 service, 512MB RAM, 0.1 vCPU — free forever | YES — no sleep guaranteed | No official MCP | ⭐⭐⭐⭐ |
| Railway | $5 credit — expires in 30 days (not permanent) | YES while credit lasts | No MCP, but MCP-hostable | ⭐⭐ |
| Render | 750 hrs/month — sleeps after 15min inactivity | PARTIAL — sleeps on web services | No official MCP | ⭐⭐ |
| Fly.io | No free tier — 2-hour trial only | PAID ONLY | No MCP | ⭐ |

---

### Service Breakdowns

#### Oracle Cloud Free Tier (WINNER — Compute)
- **Free forever:** 4 ARM OCPUs + 24GB RAM + 200GB block storage — no expiry, no credit limit
- **Platform:** Ampere A1 ARM compute — excellent for Docker, Python daemons, cron jobs
- **Gotcha:** Signup requires a credit card. In 2026, new free tier slots are limited by region — popular regions (US East) can be full. Try São Paulo or other less-saturated regions. Aruba has no dedicated OCI region but can select nearest (US or EU).
- **Python support:** Full. All SDKs available. Deploy via SSH, Docker, or bare scripts.
- **MCP:** No native MCP, but you can self-host any MCP server on the VM (including Activepieces).
- **Best use for YNAI5:** Host `price-alert.py`, `market-report.py`, `monitor-loop.py`, `telegram-claude-bridge.py` — all running 24/7 without touching local laptop.

#### Koyeb (RUNNER-UP — Compute)
- **Free forever:** 1 service (512MB RAM, 0.1 vCPU) — no sleep, no spin-down
- **Always-on guarantee:** Unlike Render, Koyeb explicitly does NOT spin down free services
- **Python support:** Full — Python, Node, Go, Ruby, Rust, Java all supported
- **Deployment:** Deploy via GitHub, Docker image, or CLI
- **Limitation:** Only 1 free service — use it for your most critical bot (e.g., `telegram-claude-bridge.py`)
- **Best use for YNAI5:** Single always-on Python bot (Telegram bridge or price alert). Upgrade to $8.90/mo to add more.

#### Railway
- **Free tier reality:** $5 one-time credit, expires in 30 days — NOT a permanent free tier
- **After trial:** Hobby plan at $5/month gives $5 credit/month (~500 CPU hours). **$5/mo is acceptable.**
- **Always-on:** Yes, no sleep/spin-down on paid plans
- **MCP hosting:** Railway is actually one of the best platforms to host custom MCP servers (recommended by MCP Playground in 2026)
- **Best use for YNAI5:** If budget allows $5/mo — good for hosting 1-2 Python bots + future MCP server. Not for "free" tier.

#### Render
- **Free tier:** 750 hrs/month — enough for one full-time service
- **Critical flaw:** Free web services spin down after 15 minutes of inactivity. Restarts take ~60 seconds.
- **Workaround:** Use an external ping service (UptimeRobot free) to hit the service every 14 minutes — keeps it alive
- **Best use for YNAI5:** Cron-style jobs (market-report.py that runs at fixed times, not continuously). Not ideal for the Telegram bridge.

#### Fly.io
- **Verdict: Skip.** No free tier in 2026. 2-hour trial only. Not relevant.

---

## 2. MCP Registry — Cloud/Infrastructure MCPs

The `mcp__mcp-registry__search_mcp_registry` tool was blocked by permissions this session. Based on web research:

### Confirmed Available MCPs (Cloud/Infra)

| MCP Server | What It Does | Cost | Status |
|-----------|-------------|------|--------|
| **Cloudflare MCP** (official) | Full Cloudflare API — DNS, Workers, R2, Zero Trust (2,500+ endpoints) | Free | LIVE — from Cloudflare |
| **Activepieces MCP** | 280+ automation MCPs in one — email, calendar, Telegram, HTTP, webhooks | Free (self-hosted) | LIVE |
| **fetch MCP** | HTTP requests from Claude | Free | Already in YNAI5 |
| **git MCP** | Git operations | Free | Already in YNAI5 |

### Key Finding — Cloudflare MCP
Cloudflare has an official MCP server that covers the entire Cloudflare API including R2 storage operations. This means Claude Code can directly interact with your R2 buckets, Workers, and DNS — no custom scripting needed.

Add it via:
```
claude mcp add cloudflare
```
Or connect via OAuth at: `https://mcp.cloudflare.com`

---

## 3. Automation Platforms

| Platform | Free Tier | Self-Host | MCP Available | YNAI5 Fit |
|---------|-----------|-----------|---------------|-----------|
| Activepieces | Free cloud (limited) + free self-host (unlimited) | YES (Docker) | YES — 280+ MCPs | ⭐⭐⭐⭐⭐ |
| n8n | Self-host free (Community Edition) — unlimited workflows | YES (Docker) | Via plugins | ⭐⭐⭐⭐ |
| Make.com | 1,000 operations/month free — 2 active workflows | NO | No | ⭐⭐ |

### Activepieces (WINNER — Automation)
- **Self-hosted = 100% free, unlimited workflows, unlimited executions**
- **MCP integration:** 280+ open-source MCP servers that work with Claude Code, Cursor, Windsurf
- **Deploy on:** Oracle Cloud free VM (Docker) — zero cost for both compute AND automation
- **Use cases for YNAI5:** Cross-platform signal distribution (Telegram + Reddit + Twitter/X + Discord), content scheduling, automated DCA alerts
- **Note:** Avoid version 0.78.1 (CPU spike bug) — use 0.77.8 for stability as of March 2026
- **GitHub:** https://github.com/activepieces/activepieces

### n8n (Community Edition)
- **Self-hosted:** Free forever, unlimited workflows
- **Requires:** Docker or Node.js — runs well on Oracle free VM
- **Best for:** Complex multi-step automation with many conditionals (more mature than Activepieces)
- **YNAI5 use case:** Market report distribution workflow, passive income channel post scheduler

### Make.com
- **Verdict:** Too limited for YNAI5. 1,000 ops/month disappears quickly with multi-step workflows. Skip.

---

## 4. Video/File Storage CDN

| Service | Free Tier | Python Integration | MCP Available | YNAI5 Fit |
|---------|-----------|-------------------|---------------|-----------|
| Cloudflare R2 | 10GB storage + 1M Class A ops + 10M Class B ops/month — **zero egress fees** | boto3 + custom endpoint | YES (Cloudflare MCP) | ⭐⭐⭐⭐⭐ |
| Backblaze B2 | 10GB storage free + 1GB/day download free | boto3 + custom endpoint | No | ⭐⭐⭐ |

### Cloudflare R2 (WINNER — Storage)
- **Free tier:** 10GB/month storage, 10M read ops, 1M write ops — **NO egress fees** (critical)
- **Python:** `boto3` with custom endpoint `https://<account_id>.r2.cloudflarestorage.com` — identical to S3 API
- **MCP:** Official Cloudflare MCP includes R2 operations — Claude can directly manage buckets
- **Best use for YNAI5:** Store generated audio (ElevenLabs MP3s), video queue files, B-roll downloads — accessible anywhere without paying download fees
- **Warning:** No spending cap available — set up usage alerts manually

### Backblaze B2
- **Free tier:** 10GB storage + 1GB/day download bandwidth free
- **Python:** `boto3` compatible (S3-compatible API)
- **Egress cost:** $0.01/GB after free tier — cheap but not zero like R2
- **Best use for YNAI5:** Long-term archive/backup only (crypto logs, session backups). Not for active delivery.

---

## Top 3 Recommendations for YNAI5

### #1 — Oracle Cloud Free Tier (Always-On Compute)
**Why:** 4 vCPU + 24GB RAM for free, forever. Run ALL Python bots simultaneously — price-alert.py, market-report.py, monitor-loop.py, telegram-claude-bridge.py. Nothing runs on your laptop. Deploy Docker containers for both Activepieces AND your scripts. This eliminates the hardware bottleneck completely for bots/automation.

**Action:** Sign up at oracle.com/cloud/free — select São Paulo or Europe region if US East is full. Requires credit card (not charged).

---

### #2 — Activepieces Self-Hosted (on Oracle VM)
**Why:** Free automation platform with 280+ MCP servers, deploy via Docker on Oracle's free ARM VM. Replaces Make.com/n8n. Connects to Telegram, Reddit, Twitter/X, Discord for multi-platform signal distribution. The MCP integration is a first-class feature — Claude can directly trigger workflows.

**Action:** Docker pull on Oracle VM → self-host Activepieces 0.77.8 → add to Claude Code via MCP.

---

### #3 — Cloudflare R2 + Cloudflare MCP (Storage + CDN)
**Why:** 10GB free storage with zero egress fees. Python boto3 integration is straightforward. The official Cloudflare MCP server gives Claude Code direct access to R2, Workers, and DNS — making it an extension of YNAI5's tool suite. Store generated audio/video assets here so the pipeline is cloud-first.

**Action:** Sign up at cloudflare.com → create R2 bucket → `claude mcp add cloudflare` for MCP access.

---

## Implementation Order (Priority)

1. **Oracle Cloud** — sign up, spin up ARM VM, migrate bots from local to cloud
2. **Cloudflare R2** — create bucket, add Cloudflare MCP to Claude Code
3. **Activepieces** — Docker deploy on Oracle VM, wire up distribution workflows
4. Koyeb as backup for 1 always-on service if Oracle setup is delayed

---

## Cost Summary

| Service | Cost |
|---------|------|
| Oracle Cloud ARM (4 vCPU / 24GB) | $0/month — forever |
| Cloudflare R2 (10GB) | $0/month — free tier |
| Activepieces self-hosted | $0/month — open source |
| Koyeb (1 service backup) | $0/month — free tier |
| **Total** | **$0/month** |

Optional if needed: Railway Hobby at $5/month for MCP server hosting.

---

_Sources:_
- [Railway Pricing Docs](https://docs.railway.com/pricing/plans)
- [Render Free Tier Docs](https://render.com/docs/free)
- [Fly.io Free Tier](https://fly.io/docs/about/free-trial/)
- [Oracle Cloud Always Free Resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)
- [Koyeb Free Tier](https://www.koyeb.com/pricing)
- [Activepieces MCP (GitHub)](https://github.com/activepieces/activepieces)
- [Cloudflare MCP Servers](https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/)
- [Cloudflare R2 vs Backblaze B2](https://themedev.net/blog/cloudflare-r2-vs-backblaze-b2/)
- [n8n vs Make 2026](https://softailed.com/blog/n8n-vs-make)
- [MCP Server Hosting Free Platforms](https://mcpplaygroundonline.com/blog/free-mcp-server-hosting-cloudflare-vercel-guide)
