# Playwright Setup Guide

## Step 1: Install Node.js

Download and install from [nodejs.org](https://nodejs.org/)

Verify installation:
```bash
node --version
npm --version
```

## Step 2: Install Playwright MCP Server

```bash
npm install -g @playwright/mcp
```

## Step 3: Install Browser Binaries

```bash
# Install Chromium (required for LinkedIn automation)
playwright install chromium

# Install all browsers (optional)
playwright install
```

## Step 4: Install Python Playwright

```bash
pip install playwright
playwright install chromium
```

## Step 5: Verify Installation

```bash
# Check Playwright is installed
playwright --version

# Test browser launch
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

## LinkedIn Session Setup

```bash
# First-time setup (opens browser for login)
python scripts/linkedin_watcher.py "C:\path\to\AI_Employee_Vault" --setup-session
```

1. Browser opens
2. Log in to LinkedIn
3. Wait for feed to load
4. Press Ctrl+C to save session

## Troubleshooting

### Browser Won't Launch

```bash
# Reinstall browser binaries
playwright install chromium --force
```

### Session Expired

```bash
# Clear session and re-login
rmdir /s /q "C:\path\to\AI_Employee_Vault\.creds\linkedin_session"
python scripts/linkedin_watcher.py --setup-session
```

### LinkedIn Blocks Requests

- Increase check interval (minimum 5 minutes)
- Use headful mode occasionally
- Ensure session is valid

## Ethical Usage Guidelines

⚠️ **Important**: This tool automates LinkedIn access. Please:

1. **Respect ToS** - Review LinkedIn's Terms of Service
2. **Rate Limits** - Use 5+ minute check intervals
3. **Personal Use** - Don't scrape or harvest data
4. **No Spam** - Don't send bulk automated messages

## Playwright Commands Reference

| Command | Description |
|---------|-------------|
| `playwright install` | Install all browser binaries |
| `playwright install chromium` | Install Chromium only |
| `playwright codegen` | Generate Playwright code |
| `playwright show-report` | Show test report |

---

*Reference: Playwright Setup for Silver Tier*
