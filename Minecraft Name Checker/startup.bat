@echo off
title Minecraft Name Checker
cd /d "P:\Minecraft Name Checker"

echo ================================
echo  MINECRAFT NAME CHECKER
echo ================================
echo.

echo Checking Python...
python --version 2>nul
if errorlevel 1 (
    echo Python not found! Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo.
echo Checking dependencies...
python -c "import PySide6, aiohttp" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting Minecraft Name Checker...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo Error occurred. Check the output above.
    pause
)