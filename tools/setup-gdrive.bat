@echo off
:: YNAI5-Phase1 — Google Drive Setup Script
:: Run this ONCE to configure rclone + create Drive folders + upload files
:: Requires: rclone installed (done) + browser for Google OAuth

SET RCLONE=C:\Users\shema\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.73.3-windows-amd64\rclone.exe
SET WORKSPACE=C:\Users\shema\OneDrive\Desktop\YNAI5-Phase1

echo ============================================
echo  YNAI5-Phase1 Google Drive Setup
echo ============================================
echo.

:: Step 1: Configure Google Drive remote
echo [1/4] Configuring Google Drive remote...
echo  - A browser window will open for Google OAuth
echo  - Sign in with your Google account
echo  - Allow rclone access to Google Drive
echo.
"%RCLONE%" config create gdrive drive scope drive
if errorlevel 1 (
    echo ERROR: rclone config failed. Try running: rclone config
    pause
    exit /b 1
)
echo gdrive remote configured!
echo.

:: Step 2: Create Drive folder structure
echo [2/4] Creating YNAI5_AI_CORE folder structure on Google Drive...
"%RCLONE%" mkdir gdrive:/YNAI5_AI_CORE
"%RCLONE%" mkdir gdrive:/YNAI5_AI_CORE/SYSTEM
"%RCLONE%" mkdir gdrive:/YNAI5_AI_CORE/SKILLS_LIBRARY
"%RCLONE%" mkdir gdrive:/YNAI5_AI_CORE/SYNC
"%RCLONE%" mkdir gdrive:/YNAI5_AI_CORE/PROJECTS
"%RCLONE%" mkdir gdrive:/YNAI5_AI_CORE/TRADING
"%RCLONE%" mkdir gdrive:/YNAI5_AI_CORE/CONTEXT
"%RCLONE%" mkdir gdrive:/YNAI5_AI_CORE/SESSIONS
echo Folder structure created!
echo.

:: Step 3: Upload drive-sync core files
echo [3/4] Uploading core files to Google Drive...
"%RCLONE%" copy "%WORKSPACE%\drive-sync" gdrive:/YNAI5_AI_CORE --progress
echo Core files uploaded!
echo.

:: Step 4: Sync workspace content
echo [4/4] Syncing workspace context + memory + skills...
"%RCLONE%" copy "%WORKSPACE%\context" gdrive:/YNAI5_AI_CORE/CONTEXT --progress
"%RCLONE%" copy "%WORKSPACE%\memory" gdrive:/YNAI5_AI_CORE/CONTEXT/memory --progress
"%RCLONE%" copy "%WORKSPACE%\.claude\skills" gdrive:/YNAI5_AI_CORE/SKILLS_LIBRARY --include "*.md" --progress
"%RCLONE%" copy "%WORKSPACE%\projects" gdrive:/YNAI5_AI_CORE/PROJECTS --include "*.md" --include "*.json" --include "*.py" --exclude "social-media-automation/footage/**" --exclude "social-media-automation/audio/**" --progress
echo Workspace synced!
echo.

echo ============================================
echo  SETUP COMPLETE!
echo  Google Drive: gdrive:/YNAI5_AI_CORE
echo  Check: https://drive.google.com
echo ============================================
pause
