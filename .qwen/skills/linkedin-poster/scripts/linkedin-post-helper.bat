@echo off
REM ============================================================
REM LinkedIn Post Helper - Semi-Automated Posting
REM ============================================================
REM This script opens LinkedIn and copies post content to clipboard
REM You manually paste and click Post (more reliable than automation)
REM ============================================================

set VAULT_PATH=C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault

echo ============================================================
echo LinkedIn Post Helper - Semi-Automated
echo ============================================================
echo.
echo This will:
echo   1. Find the latest approved post in Approved/ folder
echo   2. Copy post content to clipboard
echo   3. Open LinkedIn in your default browser
echo   4. You paste and click Post manually
echo.
echo ============================================================
echo.

cd /d "%VAULT_PATH%\Approved"

if not exist "*.md" (
    echo No approved posts found in Approved/ folder.
    echo.
    echo To approve a post:
    echo   1. Run: python linkedin_poster_workflow.py "topic" --vault "VAULT_PATH"
    echo   2. Type 'yes' when prompted
    echo   3. Then run this script again
    echo.
    pause
    exit /b 1
)

echo Finding latest approved post...
for /f "tokens=*" %%f in ('dir /b /o-d *.md') do (
    set "LATEST_FILE=%%f"
    goto :found
)

:found
if "%LATEST_FILE%"=="" (
    echo No .md files found.
    pause
    exit /b 1
)

echo Found: %LATEST_FILE%
echo.

REM Extract post content and copy to clipboard
echo Extracting post content...
powershell -Command "Get-Content '%LATEST_FILE%' -Raw | Select-String -Pattern '(?s)## Post Content\s+(.*?)(?=##|$)' | ForEach-Object { $_.Matches.Groups[1].Value } | Set-Clipboard"

if errorlevel 1 (
    echo Failed to extract content. Opening file instead...
    notepad "%LATEST_FILE%"
) else (
    echo.
    echo ============================================================
    echo ✅ Post content copied to clipboard!
    echo ============================================================
    echo.
    echo Opening LinkedIn...
    start https://www.linkedin.com/feed/
    echo.
    echo Next steps:
    echo   1. Click "Start a post" on LinkedIn
    echo   2. Press Ctrl+V to paste the content
    echo   3. Click "Post" button
    echo   4. Come back here and press any key when done
    echo.
    echo ============================================================
    pause
)

echo.
echo Moving file to Done/ folder...
move "%LATEST_FILE%" "%VAULT_PATH%\Done\"
if errorlevel 1 (
    echo Failed to move file. Please move manually:
    echo   From: %VAULT_PATH%\Approved\%LATEST_FILE%
    echo   To:   %VAULT_PATH%\Done\%LATEST_FILE%
) else (
    echo ✅ File moved to Done/ folder
)

echo.
echo ============================================================
echo Done! Your post should be live on LinkedIn.
echo ============================================================
echo.
pause
