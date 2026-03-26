# Silver Tier Setup Guide

**Personal AI Employee - Silver Tier**  
*Complete setup guide for Gmail + LinkedIn integration with Qwen Code*

**Last Updated:** 2026-03-25  
**Version:** 1.1

---

## Quick Start Checklist

- [ ] Step 0: Setup environment (fix PATH warning)
- [ ] Step 1: Install Python packages
- [ ] Step 2: Verify credentials
- [ ] Step 3: Set up Gmail Watcher
- [ ] Step 4: Set up LinkedIn Watcher
- [ ] Step 5: Test watchers
- [ ] Step 6: Install Task Scheduler
- [ ] Step 7: Run Qwen Code integration

---

## Step 0: Setup Environment (Fix PATH Warning)

**Problem:** You see warnings like:
```
WARNING: The script google-oauthlib-tool.exe is installed in 
'C:\Users\Lenovo\AppData\Local\Python\pythoncore-3.14-64\Scripts' 
which is not on PATH.
```

**Solution Option 1: Use Setup Script (Recommended for testing)**

```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
setup-env.bat
```

This adds Python Scripts to PATH for the current session only.

**Solution Option 2: Add to PATH Permanently**

1. Press `Win + R`
2. Type: `sysdm.cpl`
3. Click "Advanced" tab
4. Click "Environment Variables"
5. Under "User variables", select `Path`
6. Click "Edit"
7. Click "New"
8. Add: `C:\Users\Lenovo\AppData\Local\Python\pythoncore-3.14-64\Scripts`
9. Click "OK" on all dialogs
10. **Restart Command Prompt**

**Verify PATH is set:**
```bash
python -c "import googleapiclient; print('OK')"
playwright --version
```

## Prerequisites

| Component | Required | Installed |
|-----------|----------|-----------|
| Python 3.13+ | ✅ | ✅ Python 3.14 |
| Obsidian | ✅ | ✅ |
| Qwen Code | ✅ | ✅ |
| Node.js | ✅ | ✅ |
| Gmail API credentials | ✅ | ✅ credentials.json |
| LinkedIn account | ✅ | ✅ |

---

## Step 1: Install Python Packages

All required packages have been installed:

```bash
# Gmail API packages
✅ google-api-python-client 2.193.0
✅ google-auth 2.49.1
✅ google-auth-httplib2 0.3.0
✅ google-auth-oauthlib 1.3.0

# Automation packages
✅ playwright (with Chromium browser)
✅ watchdog
```

**Verify installation:**
```bash
python -m pip list | findstr "google playwright watchdog"
```

---

## Step 2: Verify Credentials

Your Gmail API credentials are located at:

```
Project Root: credentials.json
Secure Location: C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json
```

**Credentials Info:**
- **Project ID:** hackathon-0-fte-491317
- **Client ID:** 795983673793-4co75v1f811i2ivdm9hjpk1rg5vsecvt.apps.googleusercontent.com
- **Redirect URI:** http://localhost

---

## Step 3: Set Up Gmail Watcher

### Location
```
.qwen/skills/gmail-watcher/
├── SKILL.md
├── scripts/
│   ├── gmail_watcher.py
│   └── base_watcher.py
└── references/
    └── gmail-api-setup.md
```

### First-Time Authentication

1. Open Command Prompt
2. Navigate to Gmail Watcher scripts:
   ```bash
   cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts
   ```

3. Run the watcher:
   ```bash
   python gmail_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
   ```

4. **Browser will open** - Sign in to your Google account
5. **Grant permissions** - Allow Gmail API access
6. **Token saved** to: `C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\token.json`

### Running Gmail Watcher

```bash
# Start watcher (checks every 60 seconds)
python gmail_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"

# With custom interval (every 2 minutes)
python gmail_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json" 120
```

### What It Does

- Monitors Gmail every 60 seconds
- Filters: Unread + Important emails only
- Creates action files in `Needs_Action/` folder
- Format: `EMAIL_<subject>_<gmail_id>.md`

---

## Step 4: Set Up LinkedIn Watcher

### Location
```
.qwen/skills/linkedin-watcher/
├── SKILL.md
├── scripts/
│   ├── linkedin_watcher.py
│   └── base_watcher.py
└── references/
    └── playwright-setup.md
```

### First-Time Session Setup

1. **Open Command Prompt** (run `setup-env.bat` first if PATH warning appears)

2. Navigate to LinkedIn Watcher scripts:
   ```bash
   cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\linkedin-watcher\scripts
   ```

3. Run session setup:
   ```bash
   python linkedin_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" --setup-session
   ```

4. **What happens next:**
   ```
   ============================================================
   LinkedIn Session Setup
   ============================================================
   
   A browser window will open in 3 seconds...
   
   Instructions:
     1. Wait for browser to open
     2. Navigate to: https://www.linkedin.com/feed/
     3. Log in to your LinkedIn account
     4. Wait for your feed to fully load
     5. Verify you see your LinkedIn homepage
     6. Press Ctrl+C to save session and exit
   ============================================================
   ```

5. **Browser opens automatically** - Wait for it

6. **Check login status:**
   - If you see `✅ SUCCESS: You are logged in to LinkedIn!` - You're good!
   - If you see `⚠️  NOT LOGGED IN` - Log in to LinkedIn in the browser

7. **Wait for feed to load** - Verify you see your LinkedIn homepage

8. **Press Ctrl+C** - Session will be saved automatically

9. **Confirmation message:**
   ```
   ============================================================
   Saving LinkedIn session...
   ✅ Session saved successfully!
      Location: C:\...\AI_Employee_Vault\.creds\linkedin_session
   
   Next time, run without --setup-session:
      python linkedin_watcher.py "VAULT_PATH" --headless
   ============================================================
   ```

### Running LinkedIn Watcher

```bash
# Start watcher (headless, checks every 5 minutes)
python linkedin_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" --headless --interval 300

# With browser visible (for debugging)
python linkedin_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" --interval 300
```

### What It Monitors

- Connection requests
- LinkedIn messages
- Notifications (job alerts, post interactions)
- Keyword mentions

### Creates Files

Format: `LINKEDIN_<type>_<id>.md` in `Needs_Action/`

---

## Step 5: Test Watchers

### Test Gmail Watcher

```bash
cd .qwen\skills\gmail-watcher\scripts

# Run for 30 seconds to test
timeout /t 30 /nobreak & python gmail_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

**Expected Output:**
```
============================================================
GmailWatcher - Silver Tier
============================================================
Vault path: C:\...\AI_Employee_Vault
Check interval: 60s
Press Ctrl+C to stop
============================================================
Gmail API service initialized
Watching for new emails...
```

### Test LinkedIn Watcher

```bash
cd .qwen\skills\linkedin-watcher\scripts

# Run for 30 seconds to test
timeout /t 30 /nobreak & python linkedin_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" --headless
```

**Expected Output:**
```
============================================================
LinkedInWatcher - Silver Tier
============================================================
Vault path: C:\...\AI_Employee_Vault
Check interval: 300s
Headless: True
Press Ctrl+C to stop
============================================================
```

---

## Step 6: Install Task Scheduler

### Location
```
.qwen/skills/task-scheduler/
├── SKILL.md
├── scripts/
│   └── task_scheduler.py
└── references/
    └── windows-task-setup.md
```

### Install All Tasks

```bash
cd .qwen\skills\task-scheduler\scripts

python task_scheduler.py install-all ^
  --vault "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" ^
  --credentials "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

### Pre-configured Tasks

| Task | Trigger | Purpose |
|------|---------|---------|
| GmailWatcher | At log on | Monitor Gmail |
| LinkedInWatcher | At log on | Monitor LinkedIn |
| Orchestrator | At log on | Process pending items |
| FileSystemWatcher | At log on | Monitor drop folder |
| DailyBriefing | Daily 8 AM | Generate briefing |

### Verify Installation

```bash
# List all AI Employee tasks
python task_scheduler.py list

# Check specific task status
python task_scheduler.py status --name "GmailWatcher"
```

### Open Task Scheduler

1. Press `Win + R`
2. Type: `taskschd.msc`
3. Navigate to: Task Scheduler Library → AI_Employee

---

## Step 7: Qwen Code Integration

### Process All Pending Items

```bash
qwen --prompt "Process all files in /Needs_Action" ^
  --cwd "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

### Create Plan for Complex Task

```bash
qwen --prompt "Create a plan for processing EMAIL_invoice_request.md" ^
  --cwd "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

### Generate LinkedIn Post

```bash
qwen --prompt "Create a LinkedIn post about our Q1 revenue growth from Business_Goals.md" ^
  --cwd "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

### Check Approved Actions

```bash
qwen --prompt "Check /Approved folder and process pending actions" ^
  --cwd "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

---

## Vault Structure

```
AI_Employee_Vault/
├── Inbox/                    # Raw incoming files
├── Needs_Action/             # Pending tasks (auto-created by watchers)
├── Plans/                    # Task plans created by Qwen
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved actions (ready to execute)
├── Rejected/                 # Rejected actions
├── Done/                     # Completed tasks
├── Logs/                     # Activity logs
├── Briefings/                # CEO briefings
├── Dashboard.md              # Main dashboard
├── Company_Handbook.md       # Rules and guidelines
└── .creds/                   # Credentials (gitignored)
    ├── gmail_token.json
    ├── linkedin_session/
    └── linkedin_poster_session/
```

---

## Troubleshooting

### Gmail Watcher Issues

| Issue | Solution |
|-------|----------|
| Authentication fails | Delete `token.json`, re-run watcher |
| No emails detected | Check Gmail API enabled, labels correct |
| API quota exceeded | Wait 24 hours or request increase |
| "Google API libraries not installed" | Run: `python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib` |

### LinkedIn Watcher Issues

| Issue | Solution |
|-------|----------|
| Not logged in | Run with `--setup-session` |
| Session expired | Clear session folder, re-login |
| Browser won't open | Run `playwright install chromium` |
| LinkedIn blocks requests | Increase check interval (min 5 min) |

### Task Scheduler Issues

| Issue | Solution |
|-------|----------|
| Task won't start | Check "Run with highest privileges" |
| Python not found | Use full path to python.exe |
| Script not found | Use full path to script |
| Task fails immediately | Check credentials and vault path |

---

## Security Best Practices

1. **Never commit credentials** - Add `.creds/` to `.gitignore`
2. **Use secure storage** - Credentials in `C:\Users\Lenovo\AppData\Local\AI_Employee\creds\`
3. **Rotate OAuth credentials** monthly
4. **Enable 2FA** on Google and LinkedIn accounts
5. **Review approval files** before approving
6. **Audit logs regularly** in `Logs/` folder

---

## Next Steps

1. **Send yourself a test email** - Watcher will detect it
2. **Check Needs_Action folder** - Email action file created
3. **Run Qwen Code** - Process the email
4. **Create approval workflow** - Test HITL pattern
5. **Schedule daily briefing** - Set up automated reports

---

## Support

| Resource | Location |
|----------|----------|
| Skill Documentation | `.qwen/skills/*/SKILL.md` |
| Setup Guides | `.qwen/skills/*/references/` |
| Main README | `SILVER_TIER_README.md` |
| Architecture Doc | `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md` |

---

*Silver Tier Setup Guide v1.0 - For use with AI Employee Hackathon*
