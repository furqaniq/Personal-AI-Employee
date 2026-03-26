@echo off
REM ============================================================
REM LinkedIn Poster Workflow - Quick Launch
REM ============================================================
REM Usage: linkedin-post.bat "Your post topic here"
REM Example: linkedin-post.bat "Test post from AI Employee"
REM ============================================================

set VAULT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault
set SCRIPTS_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\linkedin-poster\scripts

if "%~1"=="" (
    echo ============================================================
    echo LinkedIn Poster Workflow
    echo ============================================================
    echo.
    echo Usage: linkedin-post.bat "Your post topic here"
    echo.
    echo Example:
    echo   linkedin-post.bat "Test post from AI Employee Silver Tier"
    echo   linkedin-post.bat "New product launch"
    echo   linkedin-post.bat "Q1 revenue milestone"
    echo.
    echo ============================================================
    exit /b 1
)

cd /d "%SCRIPTS_PATH%"
python linkedin_poster_workflow.py "%~1" --vault "%VAULT_PATH%"
