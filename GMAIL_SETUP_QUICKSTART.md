# Gmail Setup - Quick Start Guide

## Automated Setup (Recommended)

### Step 1: Run Setup Script

**Double-click:**
```
setup-gmail-credentials.bat
```

**Or run from Command Prompt:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee
setup-gmail-credentials.bat
```

### Step 2: Follow Prompts

The script will:
1. ✅ Check for credentials file
2. ✅ Create secure folder
3. ✅ Copy credentials
4. ✅ Check Python & dependencies
5. ✅ Open browser for authentication

### Step 3: Authenticate

When browser opens:
1. Sign in to your Gmail account
2. Click "Allow" on OAuth consent screen
3. Browser closes automatically
4. Watcher starts monitoring

**Done!** ✅

---

## Manual Setup (Alternative)

If you prefer manual steps:

### Step 1: Create Secure Folder
```bash
mkdir "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail"
```

### Step 2: Copy Credentials
```bash
copy "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\credentials.json" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

### Step 3: Authenticate
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts

python gmail_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

---

## Verify Setup

### Check Token Created
```bash
dir "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\token.json"
```

### Test with Email
1. Send yourself an email from another account
2. Wait 60 seconds
3. Check for action file:
```bash
dir "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault\Needs_Action\EMAIL_*.md"
```

---

## Auto-Start with Task Scheduler

To have Gmail Watcher start automatically at logon:

```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\task-scheduler\scripts

python task_scheduler.py install-all ^
  --vault "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" ^
  --credentials "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

---

## Troubleshooting

### "credentials.json not found"
- Ensure file exists at: `C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\credentials.json`

### "Python not found"
- Install Python 3.13+ from python.org
- Add to PATH during installation

### "Packages not installed"
- Script will auto-install
- Or manually: `python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib`

### "Authentication failed"
- Delete token and retry:
  ```bash
  del "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\token.json"
  ```
- Run setup script again

---

## Files Created

| File | Purpose |
|------|---------|
| `setup-gmail-credentials.bat` | Automated setup script |
| `GMAIL_SETUP_QUICKSTART.md` | This guide |
| `creds/gmail/client_secret.json` | Your credentials (secure) |
| `creds/gmail/token.json` | OAuth token (auto-generated) |

---

*Gmail Setup Quick Start v1.0*  
*Created: 2026-03-26*
