@echo off
REM ============================================================
REM Process Emails with Qwen Code
REM ============================================================
REM This script processes all email files in Needs_Action folder
REM using Qwen Code
REM ============================================================

set VAULT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault

echo ============================================================
echo Email Processor - Qwen Code
echo ============================================================
echo.
echo Processing all files in /Needs_Action...
echo.

cd /d "%VAULT_PATH%"

qwen --prompt "Process all files in /Needs_Action. Read emails, draft replies based on Company_Handbook.md, and move completed items to /Done" --cwd "%VAULT_PATH%"

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Processing failed or Qwen Code not found
    echo ============================================================
    echo.
    echo Try the auto-processor instead:
    echo   cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
    echo   python auto_email_processor.py "%VAULT_PATH%"
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
