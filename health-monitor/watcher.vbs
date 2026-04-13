' YNAI5 Windows Health Monitor — Invisible Watchdog
' Runs main_win.py silently (no console window).
' If it crashes, restarts it after 5 seconds.
' Schedule this file with Task Scheduler for 24/7 persistence.

Dim objShell, objFSO, strDir, strCmd, intPID

Set objShell = CreateObject("WScript.Shell")
Set objFSO   = CreateObject("Scripting.FileSystemObject")

' Directory containing this script and main_win.py
strDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' pythonw.exe = Python with no console window
Dim strPython
strPython = "C:\Python314\pythonw.exe"

' Fallback: try common Python locations
If Not objFSO.FileExists(strPython) Then
    strPython = "C:\Python313\pythonw.exe"
End If
If Not objFSO.FileExists(strPython) Then
    strPython = "C:\Python312\pythonw.exe"
End If
If Not objFSO.FileExists(strPython) Then
    ' Last resort: just use pythonw from PATH
    strPython = "pythonw"
End If

strCmd = """" & strPython & """ """ & strDir & "\main_win.py"""

' Infinite restart loop — watcher never exits while Windows is on
Do While True
    ' Run silently (0 = hidden window, True = wait for exit)
    objShell.Run strCmd, 0, True
    ' If we get here, main_win.py has exited (crash or stop)
    WScript.Sleep 5000  ' Wait 5s before restarting
Loop
