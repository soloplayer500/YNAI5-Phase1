#!/usr/bin/env python3
"""Install YNAI5 startup.bat into Windows Startup folder. Run once."""
import os, shutil
from pathlib import Path

bat = Path(r"C:\Users\shema\OneDrive\Desktop\YNAI5-SU\projects\system-health\startup.bat")
startup = Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs/Startup"
dest = startup / "YNAI5-Startup.bat"

if not bat.exists():
    print(f"ERROR: startup.bat not found at {bat}")
    exit(1)

shutil.copy2(bat, dest)
print(f"Installed: {dest}")
print("Runs automatically on every Windows login.")
print(f"Starts: price-alert.py + telegram-claude-bridge.py + quick health check")
