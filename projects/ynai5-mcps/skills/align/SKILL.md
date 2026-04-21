---
name: align
description: >
  ALIGN — Activate this skill whenever Solo starts a new task, project, or request that involves building, creating, writing, planning, or executing something with multiple moving parts. Triggers on: "I want to", "help me build", "let's create", "I need to", "can you make", "help me with", any task that requires a deliverable, or any time Solo uploads files to inform a task. Also activates mid-conversation when Solo says things like "we're going in the wrong direction", "start over", "this isn't right", "we got sidetracked", or "reset". Core principle: DO NOT start executing until Solo and Claude are fully aligned through structured Q&A. Iterate through questions, not bad outputs.
---

# ALIGN — Task Alignment, Context Gathering & Skill Router

ALIGN does two things: locks in what Solo actually needs before any work starts, and routes to the right skill + MCP combination once aligned.

Question bank by task type → `references/question-bank.md`

---

## The YNAI5 Skill + MCP Map

ALIGN knows the full infrastructure. After gathering context, it routes to exactly the right combination:

| Task Type | Skill | MCPs Called |
|---|---|---|
| Crypto/stock analysis | APEX | hive-crypto + trading-signals + kraken |
| Trading signal for Block Syndicate | TRADING → DISTRIBUTION | kraken + hive-crypto + trading-signals + telegram |
| Stock deep dive | STOCKRESEARCH | research-mcp + perplexity |
| Music production | SYMPHONY | suno + genius + spotify |
| AI news / content research | RESEARCH | research-mcp + perplexity + opennews |
| Post / distribute content | DISTRIBUTION | telegram + distribution-mcp + playwright |
| Web scraping / browser task | PLAYWRIGHT | playwright MCP |
| Build / code / automate | Claude Code / Cowork | github + playwright |
| Complex multi-step task | ALIGN → route | depends on breakdown |

---

## MODE 1 — LAUNCH (New Task)

### Step 1 — Parse
Read Solo's input. Extract task + success condition. Read any uploaded files first.

**Do NOT start executing yet.**

### Step 2 — Identify Skill Route
Match the task to the skill map above. If it clearly maps to one skill — go directly there after 1 round of Q&A.

If it spans multiple skills (e.g. "research crypto + post the signal") — break into steps:
1. RESEARCH for intel
2. TRADING for signal format
3. DISTRIBUTION for posting

### Step 3 — Gather Context via Q&A

Use `ask_user_input_v0`. Pull from `references/question-bank.md` for the right questions per task type. Max 3 questions per round, max 2 rounds.

**YNAI5-specific context questions:**

For crypto/trading:
- "Which asset?" → [BTC | ETH | SOL | Custom ticker | My whole Kraken portfolio]
- "What do you need?" → [Signal for Block Syndicate | Personal analysis | Portfolio check | Quick price lookup]
- "Timeframe?" → [Day trade | Swing | Position | Long-term hold]

For content/distribution:
- "Which brand?" → [YNAI5 (main) | OpenMind AI (TikTok) | Block Syndicate | All]
- "Platform?" → [Telegram | TikTok | X/Twitter | Instagram | All platforms]
- "Content type?" → [AI news | Crypto signal | Music release | Brand post | Announcement]

For music:
- "Genre/vibe?" → [Trap | Melodic rap | R&B | Drill | Something new]
- "Artist reference?" → [YB | Gunna | Juice WRLD | Rod Wave | Drake | Original]
- "Topic?" → [Tell me | Loyalty | Pain | Flex | Street | Motivation]

For research:
- "Purpose?" → [Content post | Block Syndicate signal | Personal knowledge | Trading decision]
- "Depth?" → [Quick (1 min) | Medium (5 min) | Deep research (10+ min)]

### Step 4 — Confirm Plan + Route

State back in 3-5 bullets:
- What you're about to do
- Which skill + MCPs will be called
- Expected output format
- Any assumptions made

Then say: **"Ready — confirm or adjust."**

Once confirmed → execute fully without stopping.

---

## MODE 2 — RESET (Mid-Conversation)

When Solo says: "sidetracked", "start over", "wrong direction", "reset", "this isn't right"

### Reset Step 1 — Diagnose
```
Q: "What went wrong?"
Options: [Drifted from goal | Wrong format/style | Wrong context at start | Scope too big/small | Completely off base]

Q: "What to preserve?"
Options: [Nothing — full reset | Keep research/context | Keep structure | Keep most, fix specific part]
```

### Reset Step 2 — Re-align
One focused form targeting exactly what went wrong. Max 2 questions.

### Reset Step 3 — Reroute
Execute the corrected path with the right skill + MCP combination.

---

## MCP Availability Check

At the start of any task, ALIGN notes which MCPs are connected:

```
Connected MCPs → route accordingly:
✅ kraken → enable live portfolio + trading features
✅ hive-crypto → enable live crypto market data
✅ trading-signals → enable full technical analysis
✅ telegram → enable direct Block Syndicate distribution
✅ suno → enable direct music generation
✅ genius → enable lyrics research
✅ spotify → enable artist DNA research
✅ research-mcp → enable Perplexity-powered research
✅ opennews → enable crypto news signals
✅ distribution-mcp → enable multi-platform posting
✅ playwright → enable live browser automation
✅ perplexity → enable web search

If an MCP is NOT connected:
→ Tell Solo what would be automated if it were connected
→ Offer manual workaround (paste to Suno, post to Telegram manually, etc.)
```

---

## Output Rules

1. **Never execute before Step 4 confirmation** — alignment is non-negotiable
2. **Read uploaded files before asking questions** — files contain context
3. **Forms over free-text** — clickable options always via ask_user_input_v0
4. **Max 2 question rounds** — after that, make reasonable calls
5. **Always name the skill + MCPs** in the confirmation — Solo knows what's happening
6. **Reset is not failure** — it's the fastest path back on track
7. **Mid-execution: make calls** — don't stop to ask minor questions once aligned

---

## Pipeline Position

ALIGN is the **entry gate for every complex task** in the YNAI5 ecosystem.

```
Any complex request
       ↓
    ALIGN
  (scope + route)
       ↓
┌──────┬──────┬──────┬──────┬──────┐
APEX  TRADING SYMPHONY RESEARCH DISTRIBUTION
  ↓       ↓      ↓       ↓       ↓
MCPs   MCPs   MCPs    MCPs    MCPs
```
