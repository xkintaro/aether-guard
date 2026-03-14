Set WshShell = CreateObject("WScript.Shell")

WshShell.Run "cmd /c cd C:\aether-guard && python app.py", 0, False