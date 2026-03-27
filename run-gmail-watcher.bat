@echo off
REM ============================================================
REM Run Gmail Watcher
REM ============================================================
REM This batch file runs the Gmail Watcher with correct paths
REM ============================================================

set VAULT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault
set CREDENTIALS_PATH=C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json
set SCRIPT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts\gmail_watcher.py

echo ============================================================
echo Starting Gmail Watcher
echo ============================================================
echo.
echo Vault: %VAULT_PATH%
echo Credentials: %CREDENTIALS_PATH%
echo.
echo Press Ctrl+C to stop the watcher
echo ============================================================
echo.

python "%SCRIPT_PATH%" "%VAULT_PATH%" "%CREDENTIALS_PATH%"

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Gmail Watcher stopped with error
    echo ============================================================
    echo.
    echo Troubleshooting:
    echo   1. Check if credentials file exists
    echo   2. Run AUTHENTICATE-GMAIL.bat first
    echo   3. Check vault path exists
    echo.
)

pause
