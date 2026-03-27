@echo off
REM ============================================================
REM Authenticate Gmail for Sending Emails
REM ============================================================
REM This script re-authenticates with FULL permissions including
REM the ability to SEND emails via Gmail API
REM ============================================================

echo ============================================================
echo Gmail Authentication for Email Sending
echo ============================================================
echo.
echo This will:
echo   1. Delete old read-only token
echo   2. Open browser for authentication
echo   3. Request SEND permissions
echo   4. Save new token with full permissions
echo.
echo After authentication:
echo   - Orchestrator can send emails from Approved/ folder
echo   - Email MCP can send replies automatically
echo.
echo ============================================================
echo.
pause

cd /d "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts"

python authenticate-gmail-send.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Authentication failed
    echo ============================================================
    echo.
) else (
    echo.
    echo ============================================================
    echo Authentication complete!
    echo ============================================================
    echo.
    echo Next steps:
    echo   1. Move APPROVAL_*.md files to Approved/ folder
    echo   2. Run orchestrator.py
    echo   3. Emails will be sent automatically
    echo.
)

pause
