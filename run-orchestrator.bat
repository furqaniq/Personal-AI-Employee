@echo off
REM ============================================================
REM Run Orchestrator
REM ============================================================
REM This batch file runs the Orchestrator with correct paths
REM ============================================================

set VAULT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault
set SCRIPT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts\orchestrator.py

echo ============================================================
echo Starting Orchestrator
echo ============================================================
echo.
echo Vault: %VAULT_PATH%
echo.
echo This will:
echo   1. Create approval requests for new emails
echo   2. Send emails from Approved/ folder via Email MCP
echo   3. Update Dashboard.md
echo.
echo Press Ctrl+C to stop the orchestrator
echo ============================================================
echo.

python "%SCRIPT_PATH%" "%VAULT_PATH%"

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Orchestrator stopped with error
    echo ============================================================
    echo.
)

pause
