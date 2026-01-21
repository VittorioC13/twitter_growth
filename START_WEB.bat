@echo off
title Twitter Content Generator - Web Interface
echo.
echo ============================================
echo   Twitter Content Generator
echo   Web Interface Starting...
echo ============================================
echo.
echo Starting web server...
echo.
echo Your browser should open automatically.
echo If not, go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================
echo.

start http://localhost:5000
python web_interface.py

pause
