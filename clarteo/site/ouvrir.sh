#!/bin/sh
cd "$(dirname "$0")"
python3 serveur.py &
sleep 0.5
open "http://127.0.0.1:8000/" 2>/dev/null || xdg-open "http://127.0.0.1:8000/" 2>/dev/null
wait
