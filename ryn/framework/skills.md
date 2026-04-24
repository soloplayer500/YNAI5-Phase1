# skills.md — Skill Registry & Trigger Guide
_What skill to invoke and when. All skills live in .claude/skills/._

---

## Skill Index

### System & Infrastructure
| Skill | Trigger | When to Use |
|-------|---------|-------------|
| `/health-check` | "check system", "VM status", "is everything up" | Quick VM + local health |
| `/vm-repair` | "service down", "SSH fix", "repair", "restart failed" | SSH diagnostic + fix loop |
| `/log-audit` | "check logs", "audit logs", "log size", "log errors" | VM log analysis |
| `/telegram-ops` | "test bot", "Telegram command", "check commander" | Bot health + manual ops |
| `/github-snapshot` | "snapshot", "save state", "brain update", "commit state" | Push brain state to GitHub |

### Trading & Finance
| Skill | Trigger | When to Use |
|-------|---------|-------------|
| `/market-scan` | "morning scan", "market check", "what's moving" | Daily market brief |
| `/trading-analysis` | "analyze [ticker]", "trade setup", "entry/stop/target" | Full trade setup |
| `/crypto-screen` | "screen crypto", "find setups", "best crypto" | Signal screening |
| `/crypto-portfolio` | "portfolio", "my positions", "P&L" | Kraken portfolio check |
| `/technical-analysis` | "TA [ticker]", "chart analysis", "support/resistance" | Chart + indicators |
| `/risk-analyze` | "risk check", "portfolio risk", "exposure" | Risk assessment |
| `/market-check` | "price [ticker]", "news", "sentiment" | Quick price + news |
| `/macro-impact` | "macro", "Fed", "inflation impact" | Macro → portfolio |

### Content & Research
| Skill | Trigger | When to Use |
|-------|---------|-------------|
| `/research [topic]` | "research X", "find info on" | Web research → docs/ |
| `/trend-check` | "trending", "viral topics", "what's hot" | Top 5 trends |
| `/gemini [task]` | "ask Gemini", "use Gemini for" | Gemini sub-agent |
| `/kimi [task]` | "ask Kimi", "parallel research" | Kimi K2.5 sub-agent |

### Memory & Session
| Skill | Trigger | When to Use |
|-------|---------|-------------|
| `/remember [pref]` | "remember I prefer", "always do X" | Save to preferences.md |
| `/session-close` | "end session", "wrap up", "close" | Session summary + commit |
| `/md-update` | "update docs", "refresh markdown" | Stale doc review |

---

## Domain Routing

```
User input → keyword scan → domain match → skill invoked

TRADING  → market-scan | trading-analysis | crypto-screen | technical-analysis
VM-OPS   → vm-repair | log-audit | health-check
TELEGRAM → telegram-ops
GITHUB   → github-snapshot
MEMORY   → remember | md-update | session-close
```

---

## Creating New Skills

All skills follow the format in `.claude/skills/[name]/SKILL.md`:
```markdown
---
name: skill-name
description: One-line trigger description
---
# Skill Name
[Step-by-step instructions Claude follows exactly]
```

After creating: add to `CLAUDE.md` Skills section + rebuild RAG index.
