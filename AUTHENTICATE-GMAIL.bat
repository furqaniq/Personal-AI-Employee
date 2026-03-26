@echo off
REM ============================================================
REM Gmail One-Click Authentication - FINAL FIXED VERSION
REM ============================================================
REM This script handles everything automatically
REM ============================================================

echo.
echo ============================================================
echo  GMAIL AUTHENTICATION - SUPER SIMPLE
echo ============================================================
echo.

REM Setup paths
set CREDENTIALS_SOURCE=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\credentials.json
set CREDENTIALS_DEST=C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json
set SCRIPTS=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts

REM Create folder and copy credentials
if not exist "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail" mkdir "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail"
copy /Y "%CREDENTIALS_SOURCE%" "%CREDENTIALS_DEST%" > nul

echo [1/3] Setting up credentials... Done!
echo.

REM Check Python
echo [2/3] Checking Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.13+ from python.org
    pause
    exit /b 1
)
echo   Python found!
echo.

REM Install required packages using python -m pip (works even if pip not in PATH)
echo [3/3] Installing Gmail API packages...
echo   (This may take a minute...)
echo.
python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib --quiet

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages!
    echo Please run manually:
    echo   python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
    echo.
    pause
    exit /b 1
)

echo   Packages installed!
echo.

REM Run authentication
cd /d "%SCRIPTS%"
python authenticate.py

if errorlevel 1 (
    echo.
    echo Authentication failed.
    pause
    exit /b 1
)

echo.
echo Authentication complete!
pause
