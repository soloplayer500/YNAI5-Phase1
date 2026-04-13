@echo off
:: YNAI5 Windows Health Monitor — Task Scheduler Installer
:: Run this ONCE as Administrator to register the 24/7 background monitor.
:: After install, the monitor starts automatically every time you log in.

setlocal

set TASK_NAME=YNAI5-WinHealthMonitor
set SCRIPT_DIR=%~dp0
set WATCHER=%SCRIPT_DIR%watcher.vbs

echo.
echo ========================================
echo  YNAI5 Windows Health Monitor Installer
echo ========================================
echo.
echo Script dir : %SCRIPT_DIR%
echo Watcher    : %WATCHER%
echo Task name  : %TASK_NAME%
echo.

:: Verify watcher.vbs exists
if not exist "%WATCHER%" (
    echo ERROR: watcher.vbs not found at %WATCHER%
    echo Make sure you are running this from the health-monitor folder.
    pause
    exit /b 1
)

:: Remove existing task (ignore error if not found)
schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1

:: Create Task Scheduler entry
:: - Trigger: At logon (fires when you sign into Windows)
:: - Action: wscript.exe runs watcher.vbs (invisible)
:: - Priority: High, runs with highest privileges
:: - Restart on fail: every 2 minutes, up to 999 times
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "wscript.exe \"%WATCHER%\"" ^
  /sc ONLOGON ^
  /rl HIGHEST ^
  /f ^
  >nul 2>&1

if %errorlevel% neq 0 (
    echo ERROR: Failed to create task. Try running as Administrator.
    pause
    exit /b 1
)

echo [OK] Task created: %TASK_NAME%
echo.

:: Start it immediately (don't wait for next logon)
schtasks /run /tn "%TASK_NAME%" >nul 2>&1

if %errorlevel% equ 0 (
    echo [OK] Monitor started now.
) else (
    echo [WARN] Could not start immediately — will start on next logon.
)

echo.
echo Done. The health monitor now runs silently in the background.
echo Logs: %SCRIPT_DIR%logs\win_monitor.log
echo.
echo To stop:  schtasks /end /tn "%TASK_NAME%"
echo To remove: schtasks /delete /tn "%TASK_NAME%" /f
echo.
pause
