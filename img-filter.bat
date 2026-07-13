@echo off
title Image Filter CLI
:: Set the working directory to the folder where this .bat file is located
cd /d "%~dp0"

:: Check if the virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo Looked for: "%~dp0.venv\Scripts\python.exe"
    echo.
    echo Please make sure your virtual environment is named ".venv"
    echo and is located in the same folder as this script.
    pause
    exit /b 1
)

:: Launch the script directly using the virtual environment's Python
".venv\Scripts\python.exe" main.py

:: Keep the window open if the script crashes or the user quits
echo.
pause