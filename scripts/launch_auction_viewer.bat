@echo off
echo Starting Python HTTP server on port 8000...
start "" http://localhost:8000/frontend/auction_viewer.html
python -m http.server 8000
echo Server stopped.
pause
