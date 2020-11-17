@echo off
D:\OneDrive\PycharmProjects\ScriptGame\venv\Scripts\pyinstaller.exe -F GameOnmyoji2.py
xcopy dist\GameOnmyoji2.exe .\ /Y
rd /s /q build
rd /s /q dist
del /q GameOnmyoji2.spec
pause