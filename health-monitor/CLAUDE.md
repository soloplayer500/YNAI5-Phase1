# Health Monitor

Phase 1 Ubuntu system health daemon.
Root: health-monitor/
Entry: python main.py
Config: config.yaml
Logs: logs/system.log (events) + logs/monitor.log (failures)
DB: state/monitor.db
Credentials: .env.local → TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
