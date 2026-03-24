@echo off
REM Setup script for AI Employee Bronze Tier
REM Run this script to install dependencies and verify setup

echo ============================================================
echo AI Employee - Bronze Tier Setup
echo ============================================================
echo.

REM Check Python installation
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.13+
    echo Download from: https://www.python.org/downloads/
    exit /b 1
)
python --version
echo.

REM Check Claude Code installation
echo [2/4] Checking Claude Code installation...
where claude >nul 2>&1
if errorlevel 1 (
    echo WARNING: Claude Code not found in PATH
    echo Install with: npm install -g @anthropic/claude-code
    echo Or download from: https://claude.com/product/claude-code
) else (
    claude --version
)
echo.

REM Install Python dependencies
echo [3/4] Installing Python dependencies...
cd /d "%~dp0scripts"
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo.

REM Verify vault structure
echo [4/4] Verifying vault structure...
cd /d "%~dp0AI_Employee_Vault"
if not exist "Dashboard.md" (
    echo ERROR: Dashboard.md not found
    exit /b 1
)
if not exist "Company_Handbook.md" (
    echo ERROR: Company_Handbook.md not found
    exit /b 1
)
if not exist "Needs_Action" (
    echo ERROR: Needs_Action folder not found
    exit /b 1
)
if not exist "Done" (
    echo ERROR: Done folder not found
    exit /b 1
)
echo Vault structure verified.
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Open Obsidian and load the AI_Employee_Vault folder
echo 2. Review Dashboard.md and Company_Handbook.md
echo 3. Start the watcher:
echo    cd scripts
echo    python filesystem_watcher.py "..\AI_Employee_Vault"
echo.
echo 4. In a new terminal, start the orchestrator:
echo    cd scripts
echo    python orchestrator.py "..\AI_Employee_Vault"
echo.
echo 5. Test by dropping a file into AI_Employee_Vault\Inbox\
echo.
