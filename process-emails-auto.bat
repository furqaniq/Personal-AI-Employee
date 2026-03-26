@echo off
REM ============================================================
REM Auto Email Processor (No Qwen Code Required)
REM ============================================================
REM Automatically processes emails without needing Qwen Code
REM ============================================================

set SCRIPTS_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
set VAULT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault

echo ============================================================
echo Auto Email Processor
echo ============================================================
echo.
echo Processing all emails in Needs_Action folder...
echo (No Qwen Code required - fully automatic)
echo.

cd /d "%SCRIPTS_PATH%"

python auto_email_processor.py "%VAULT_PATH%"

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Processing failed
    echo ============================================================
    echo.
) else (
    echo.
    echo ============================================================
    echo Processing complete!
    echo ============================================================
    echo.
    echo Check the following folders:
    echo   Done/              - Processed emails
    echo   Pending_Approval/  - Items needing your review
    echo   Drafts/            - Email drafts created
    echo.
)

pause
