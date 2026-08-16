#!/bin/sh
cd "$(dirname "$0")"
python3 -m http.server 8000 &
sleep 0.4
open "http://127.0.0.1:8000/" 2>/dev/null || xdg-open "http://127.0.0.1:8000/" 2>/dev/null
wait
