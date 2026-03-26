@echo off
REM ============================================================
REM Silver Tier Environment Setup
REM ============================================================
REM Adds Python Scripts directory to PATH for current session
REM This fixes the "script not on PATH" warning
REM ============================================================

echo ============================================================
echo Silver Tier Environment Setup
echo ============================================================
echo.

REM Get Python Scripts directory
set PYTHON_SCRIPTS=C:\Users\Lenovo\AppData\Local\Python\pythoncore-3.14-64\Scripts

REM Add to PATH for current session
set PATH=%PYTHON_SCRIPTS%;%PATH%

echo Added to PATH:
echo   %PYTHON_SCRIPTS%
echo.

REM Verify installations
echo Checking installations...
echo.

python -c "import googleapiclient; print('✓ Google API: OK')" 2>nul || echo "✗ Google API: Not installed"
python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright: OK')" 2>nul || echo "✗ Playwright: Not installed"
python -c "import watchdog; print('✓ Watchdog: OK')" 2>nul || echo "✗ Watchdog: Not installed"

echo.
echo ============================================================
echo Available commands:
echo   - python
echo   - pip
echo   - playwright
echo   - google-oauthlib-tool
echo ============================================================
echo.
echo You can now run:
echo   1. Gmail Watcher:
echo      cd .qwen\skills\gmail-watcher\scripts
echo      python gmail_watcher.py "VAULT_PATH" "CREDENTIALS_PATH"
echo.
echo   2. LinkedIn Watcher:
echo      cd .qwen\skills\linkedin-watcher\scripts
echo      python linkedin_watcher.py "VAULT_PATH" --setup-session
echo.
echo   3. Task Scheduler:
echo      cd .qwen\skills\task-scheduler\scripts
echo      python task_scheduler.py install-all --vault "VAULT_PATH"
echo ============================================================
echo.
pause
