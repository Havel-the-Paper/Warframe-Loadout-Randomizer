@echo off
rem ==============================================================================
rem Windows Launcher for Warframe EDA Web Dashboard
rem Starts the local server and automatically launches your default web browser.
rem ==============================================================================

title Warframe EDA Loadout Generator
cd /d "%~dp0"

echo ==================================================
echo  Starting Warframe EDA Web Server...
echo ==================================================

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python run_web.py
    goto :eof
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py -3 run_web.py
    goto :eof
)

where python3 >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python3 run_web.py
    goto :eof
)

echo.
echo [ERROR] Python 3 was not found on your system PATH.
echo Please install Python from https://www.python.org or the Microsoft Store.
echo.
pause
