@echo off
cd /d "%~dp0"
start http://127.0.0.1:8000/
py -3 serveur.py
if errorlevel 1 python serveur.py
if errorlevel 1 python3 serveur.py
if errorlevel 1 python -m http.server 8000 --bind 0.0.0.0
pause
