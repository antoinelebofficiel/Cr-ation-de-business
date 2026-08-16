@echo off
cd /d "%~dp0"
start http://127.0.0.1:8000/
python -m http.server 8000
if errorlevel 1 py -m http.server 8000
pause
