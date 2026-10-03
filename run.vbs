Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "poetry run pythonw run.py", 0, False
