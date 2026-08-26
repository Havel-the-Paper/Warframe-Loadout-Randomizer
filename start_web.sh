#!/usr/bin/env bash
# ==============================================================================
# Linux & macOS Launcher for Warframe EDA Web Dashboard
# Starts the local server and automatically launches your default web browser.
# ==============================================================================

set -e

# Change directory to the script's folder
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$SCRIPT_DIR"

echo "=================================================="
echo " Starting Warframe EDA Web Server..."
echo "=================================================="

# Check for Python
if command -v python3 &>/dev/null; then
    exec python3 run_web.py
elif command -v python &>/dev/null; then
    exec python run_web.py
else
    echo "[ERROR] Python 3 was not found on your system."
    echo "Please install Python 3 (e.g., sudo apt install python3) to run this tool."
    exit 1
fi
