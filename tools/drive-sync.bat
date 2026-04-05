@echo off
:: YNAI5-Phase1 — Scheduled Drive Sync (runs every 2 hours via Task Scheduler)
SET RCLONE=C:\Users\shema\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.73.3-windows-amd64\rclone.exe
SET WORKSPACE=C:\Users\shema\OneDrive\Desktop\YNAI5-Phase1
SET LOGFILE=%WORKSPACE%\projects\system-health\logs\drive-sync.log

echo [%DATE% %TIME%] Drive sync started >> "%LOGFILE%"

:: Sync context (priorities, profile, goals)
"%RCLONE%" sync "%WORKSPACE%\context" gdrive:/YNAI5_AI_CORE/CONTEXT --include "*.md" --log-file="%LOGFILE%" --log-level INFO

:: Sync memory (MEMORY.md, preferences, patterns, decisions)
"%RCLONE%" sync "%WORKSPACE%\memory" gdrive:/YNAI5_AI_CORE/CONTEXT/memory --include "*.md" --log-file="%LOGFILE%" --log-level INFO

:: Sync HEARTBEAT (two-way: Drive → local first, then local → Drive)
"%RCLONE%" sync gdrive:/YNAI5_AI_CORE/SYNC "%WORKSPACE%\drive-sync\SYNC" --log-file="%LOGFILE%" --log-level INFO
"%RCLONE%" sync "%WORKSPACE%\drive-sync\SYNC" gdrive:/YNAI5_AI_CORE/SYNC --log-file="%LOGFILE%" --log-level INFO

echo [%DATE% %TIME%] Drive sync complete >> "%LOGFILE%"
