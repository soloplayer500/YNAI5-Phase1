# YNAI5 Universal AI Guide
_Read this after CORE_IDENTITY.md. This governs how all AI agents operate in this system._

## Startup Protocol (Required for Any AI)
1. Read `/SYSTEM/CORE_IDENTITY.md` — understand who you're working for
2. Read `/SYNC/HEARTBEAT.json` — check current system state
3. Check `task_queue` for pending tasks assigned to you
4. Execute your tasks and write results back to HEARTBEAT.json
5. **Never restart system logic — always continue from current state**

## Task Queue Format
```json
{
  "id": "short-uuid",
  "type": "claude_skill | gemini_analysis | python_script | research",
  "command": "the full command or prompt to execute",
  "priority": 1,
  "created_at": "ISO-8601 timestamp",
  "assigned_to": "claude | gemini | system",
  "context": "optional background context string"
}
```

## Cross-AI Execution Rules
- **Claude → Gemini:** Set `"assigned_to": "gemini"` for analysis, research, large-context tasks
- **Gemini → Claude:** Set `"assigned_to": "claude"` for code execution, skill commands, file edits
- **VM watcher:** Polls HEARTBEAT.json every 30 seconds, picks up matching tasks

## YNAI5 Skill Commands (Claude)
Invoke skills using: `/skill-name [args]`

### Finance Skills
- `/crypto-screen [risk] [focus] [budget]` — Goldman Sachs-style crypto screener
- `/crypto-portfolio [--predict] [--stats]` — Kraken portfolio + predictions
- `/technical-analysis [ticker] [timeframe]` — Citadel-grade TA
- `/market-check [ticker]` — price + news + sentiment
- `/macro-impact [holdings]` — McKinsey macro impact

### Content Skills
- `/trend-check [platform]` — top 5 trends with virality scores
- `/content-gen [topic] [platform]` — full script + captions + B-roll
- `/content-batch [niche]` — parallel daily content dispatch
- `/voice-gen [text]` — ElevenLabs TTS → MP3

### Research Skills
- `/research [topic]` — web research → docs/
- `/niche-finder [seed]` — BRAINAI5 V3 deep niche analysis

## Priority Order for Decisions
1. Revenue first (crypto/content/passive income)
2. System stability (infrastructure uptime)
3. Research and learning
4. Optimization and refactoring

## Communication Style
- Professional but friendly, no filler, high signal
- Structured outputs with headings
- MVP first, challenge weak reasoning
- Always save outputs to files — never chat-only
