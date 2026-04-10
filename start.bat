@echo off
title VirtualDJ Rich Presence
echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1
echo.
echo ========================================
echo   VirtualDJ Discord Rich Presence
echo ========================================
echo.
python main.py
pause
