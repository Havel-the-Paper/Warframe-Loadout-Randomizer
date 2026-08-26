# ==============================================================================
# Windows PowerShell Launcher for Warframe EDA Web Dashboard
# Starts the local server and automatically launches your default web browser.
# ==============================================================================

Set-Location -Path $PSScriptRoot
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " Starting Warframe EDA Web Server..." -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

if (Get-Command python -ErrorAction SilentlyContinue) {
    & python run_web.py
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 run_web.py
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 run_web.py
} else {
    Write-Host "`n[ERROR] Python was not found in your PATH." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org" -ForegroundColor White
    Pause
}
