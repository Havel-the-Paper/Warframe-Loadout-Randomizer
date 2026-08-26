#!/usr/bin/env python3
"""
Launcher for Warframe EDA Web Dashboard
Serves the pre-built web UI locally and automatically opens your default browser.
Zero external dependencies required.
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "web", "dist")
PORT = 5173

if not os.path.exists(DIST_DIR):
    print("Building web production bundle...")
    os.system(f"cd {os.path.join(BASE_DIR, 'web')} && npm run build")

class DualHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def log_message(self, format, *args):
        # Quiet logger for clean terminal experience
        pass

def open_browser():
    """Waits for server to start listening, then opens default browser."""
    time.sleep(0.6)
    url = f"http://localhost:{PORT}"
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Note: Could not automatically open browser: {e}")

def main():
    print("==================================================================")
    print("  🚀 WARFRAME EDA / ETA LOADOUT GENERATOR")
    print("  Sanctum Anatomica • 3 Choices Per Category")
    print("==================================================================")
    print(f"\n🌐 Local Server: http://localhost:{PORT}")
    print(f"🔗 Official Wiki: wiki.warframe.com")
    print(f"✨ Launching default web browser...\n")
    print("Press Ctrl+C in this terminal to stop the server.\n")

    # Start browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), DualHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped. Good hunting, Tenno!")
    except OSError as e:
        if "Address already in use" in str(e) or e.errno == 98 or e.errno == 10048:
            print(f"\n[Notice] Port {PORT} is already in use. Opening browser to existing instance...")
            webbrowser.open(f"http://localhost:{PORT}")
        else:
            print(f"\nServer error: {e}")

if __name__ == "__main__":
    main()
