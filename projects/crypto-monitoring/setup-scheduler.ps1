# YNAI5 — Price Alert Scheduler Setup
# Run this ONCE as Administrator to create twice-daily alert tasks.
# Right-click this file → Run with PowerShell (as Administrator)

$ScriptDir = "C:\Users\shema\OneDrive\Desktop\YNAI5-SU\projects\crypto-monitoring"
$BatchFile = "$ScriptDir\run_alerts.bat"
$Python    = (Get-Command python).Source

# ── Task 1: Morning Check (8:00 AM) ─────────────────────────────────────────
$ActionMorning  = New-ScheduledTaskAction -Execute $Python `
    -Argument "projects\crypto-monitoring\price-alert.py" `
    -WorkingDirectory "C:\Users\shema\OneDrive\Desktop\YNAI5-SU"

$TriggerMorning = New-ScheduledTaskTrigger -Daily -At "08:00AM"

$SettingsMorning = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 2) `
    -RunOnlyIfNetworkAvailable `
    -StartWhenAvailable

Register-ScheduledTask `
    -TaskName   "YNAI5-CryptoAlert-Morning" `
    -TaskPath   "\YNAI5\" `
    -Action     $ActionMorning `
    -Trigger    $TriggerMorning `
    -Settings   $SettingsMorning `
    -RunLevel   Limited `
    -Force

Write-Host "Morning task created: 08:00 AM daily" -ForegroundColor Green

# ── Task 2: Night Check (10:00 PM) ──────────────────────────────────────────
$ActionNight  = New-ScheduledTaskAction -Execute $Python `
    -Argument "projects\crypto-monitoring\price-alert.py" `
    -WorkingDirectory "C:\Users\shema\OneDrive\Desktop\YNAI5-SU"

$TriggerNight = New-ScheduledTaskTrigger -Daily -At "10:00PM"

Register-ScheduledTask `
    -TaskName   "YNAI5-CryptoAlert-Night" `
    -TaskPath   "\YNAI5\" `
    -Action     $ActionNight `
    -Trigger    $TriggerNight `
    -Settings   $SettingsMorning `
    -RunLevel   Limited `
    -Force

Write-Host "Night task created: 10:00 PM daily" -ForegroundColor Green

Write-Host ""
Write-Host "Both tasks registered. Check Task Scheduler -> YNAI5 folder to verify." -ForegroundColor Cyan
Write-Host "Logs will appear at: projects\crypto-monitoring\logs\" -ForegroundColor Cyan
