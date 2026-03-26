@echo off
REM ============================================================
REM Gmail Credentials Setup Script
REM ============================================================
REM This script sets up Gmail API credentials for AI Employee
REM ============================================================

echo ============================================================
echo Gmail Credentials Setup - AI Employee Silver Tier
echo ============================================================
echo.

REM Step 1: Define paths
set CREDENTIALS_SOURCE=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\credentials.json
set CREDENTIALS_DEST=C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json
set CREDENTIALS_FOLDER=C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail
set VAULT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault
set WATCHER_SCRIPT=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts\gmail_watcher.py

REM Step 2: Check if source credentials exist
echo [1/5] Checking for credentials file...
if not exist "%CREDENTIALS_SOURCE%" (
    echo.
    echo ERROR: credentials.json not found at:
    echo   %CREDENTIALS_SOURCE%
    echo.
    echo Please ensure the file exists and try again.
    echo.
    pause
    exit /b 1
)
echo   ✓ Found credentials.json
echo.

REM Step 3: Create secure credentials folder
echo [2/5] Creating secure credentials folder...
if not exist "%CREDENTIALS_FOLDER%" (
    mkdir "%CREDENTIALS_FOLDER%"
    echo   ✓ Created: %CREDENTIALS_FOLDER%
) else (
    echo   ✓ Folder already exists
)
echo.

REM Step 4: Copy credentials to secure location
echo [3/5] Copying credentials to secure location...
copy /Y "%CREDENTIALS_SOURCE%" "%CREDENTIALS_DEST%" > nul
if errorlevel 1 (
    echo   ✗ Failed to copy credentials
    echo.
    pause
    exit /b 1
)
echo   ✓ Credentials copied to secure location
echo.

REM Step 5: Check Python installation
echo [4/5] Checking Python and dependencies...
python --version > nul 2>&1
if errorlevel 1 (
    echo   ✗ Python not found in PATH
    echo.
    echo Please install Python 3.13+ and try again.
    echo.
    pause
    exit /b 1
)
echo   ✓ Python found

REM Check required packages
python -c "from google.oauth2.credentials import Credentials" > nul 2>&1
if errorlevel 1 (
    echo   ⚠ Gmail API packages not installed
    echo.
    echo Installing required packages...
    python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib --quiet
    if errorlevel 1 (
        echo   ✗ Failed to install packages
        echo.
        echo Please run manually:
        echo   python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
        echo.
        pause
        exit /b 1
    )
    echo   ✓ Packages installed
) else (
    echo   ✓ Gmail API packages found
)
echo.

REM Step 6: Run authentication
echo [5/5] Starting Gmail authentication...
echo.
echo ============================================================
echo AUTHENTICATION REQUIRED
echo ============================================================
echo.
echo A browser window will open with Google OAuth consent screen.
echo.
echo NEXT STEPS:
echo   1. Sign in to your Gmail account
echo   2. Click "Allow" to grant Gmail API access
echo   3. Browser will close automatically when done
echo   4. Watcher will start monitoring for new emails
echo.
echo ============================================================
echo.
pause

echo.
echo Opening browser for authentication...
echo.

cd /d "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts"
python gmail_watcher.py "%VAULT_PATH%" "%CREDENTIALS_DEST%"

if errorlevel 1 (
    echo.
    echo ============================================================
    echo SETUP COMPLETED WITH ISSUES
    echo ============================================================
    echo.
    echo Authentication may have failed. Please try again:
    echo   python gmail_watcher.py "%VAULT_PATH%" "%CREDENTIALS_DEST%"
    echo.
) else (
    echo.
    echo ============================================================
    echo SETUP COMPLETE!
    echo ============================================================
    echo.
    echo ✓ Credentials configured
    echo ✓ OAuth token saved
    echo ✓ Gmail Watcher is running
    echo.
    echo The watcher will:
    echo   • Check Gmail every 60 seconds
    echo   • Create action files for new emails
    echo   • Save files to: %VAULT_PATH%\Needs_Action\
    echo.
    echo To stop the watcher, press Ctrl+C
    echo.
    echo To set up auto-start with Task Scheduler, run:
    echo   cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\task-scheduler\scripts
    echo   python task_scheduler.py install-all --vault "%VAULT_PATH%" --credentials "%CREDENTIALS_DEST%"
    echo.
    echo ============================================================
)

pause
