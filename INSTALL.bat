@echo off
title Install Twitter Content Generator
echo.
echo ============================================
echo   Installing Twitter Content Generator
echo ============================================
echo.
echo This will install all required packages...
echo.
pause
echo.
echo Installing Python packages...
echo.

pip install -r requirements.txt

echo.
echo ============================================
echo   Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Add your DeepSeek API key to .env
echo 3. Run START_GENERATOR.bat to test
echo.
pause
