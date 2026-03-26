# Email Processing - All Commands

## 🚀 Quick Start (Choose One)

### Option 1: Auto-Processor (Recommended - No Qwen Needed)

**Double-click:**
```
process-emails-auto.bat
```

**Or run:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python auto_email_processor.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

**What it does:**
- ✅ Reads all email files in `Needs_Action/`
- ✅ Categorizes emails (security, newsletters, etc.)
- ✅ Creates reply drafts for known contacts
- ✅ Creates approval requests for new contacts
- ✅ Moves processed files to `Done/`

---

### Option 2: Qwen Code (If Installed)

**Double-click:**
```
process-emails-qwen.bat
```

**Or run:**
```bash
qwen --prompt "Process all files in /Needs_Action. Read emails, draft replies based on Company_Handbook.md, and move completed items to /Done" --cwd "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

---

## Complete Workflow Commands

### Step 1: Start Gmail Watcher (Monitors Gmail)

**Terminal 1:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts

python gmail_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

**Output:**
```
📬 You have 7 unread email(s) in Gmail
✨ Found 1 NEW unread email(s) to process
Action file created: EMAIL_*.md
```

---

### Step 2: Start Orchestrator (Auto-Processes Emails)

**Terminal 2:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts

python orchestrator.py ..\AI_Employee_Vault
```

**Output:**
```
Found 15 pending item(s)
Processing emails automatically...
✓ Moved to Done: EMAIL_*.md
✓ Created approval request: REVIEW_EMAIL_*.md
Auto email processing complete!
```

---

### Step 3: Check Results

**View processed emails:**
```bash
dir AI_Employee_Vault\Done\EMAIL_*.md
```

**View pending approvals:**
```bash
dir AI_Employee_Vault\Pending_Approval\REVIEW_*.md
```

**View dashboard:**
```bash
type AI_Employee_Vault\Dashboard.md
```

---

## One-Click Batch Files

| File | Purpose | Location |
|------|---------|----------|
| `AUTHENTICATE-GMAIL.bat` | Authenticate with Gmail (first time) | Project root |
| `process-emails-auto.bat` | Auto-process emails (no Qwen) | Project root |
| `process-emails-qwen.bat` | Process with Qwen Code | Project root |

---

## Manual Processing Commands

### Process Specific Email File
```bash
qwen --prompt "Read EMAIL_Furqan_*.md in /Needs_Action and draft an appropriate reply" --cwd "AI_Employee_Vault"
```

### Process Only Security Emails
```bash
qwen --prompt "Process all security-related emails in /Needs_Action. Categorize and summarize them" --cwd "AI_Employee_Vault"
```

### Process Only New Contacts
```bash
qwen --prompt "Find emails from new contacts in /Needs_Action and create approval requests" --cwd "AI_Employee_Vault"
```

---

## Status Check Commands

### Check Pending Emails
```bash
dir AI_Employee_Vault\Needs_Action\*.md
```

### Check Completed Emails
```bash
dir AI_Employee_Vault\Done\*.md
```

### Check Approval Requests
```bash
dir AI_Employee_Vault\Pending_Approval\*.md
```

### Check Activity Logs
```bash
type AI_Employee_Vault\Logs\*.json
```

### Check Dashboard Status
```bash
type AI_Employee_Vault\Dashboard.md
```

---

## Troubleshooting Commands

### Restart Gmail Watcher
```bash
# Stop current (Ctrl+C)
# Then restart:
python gmail_watcher.py "VAULT_PATH" "CREDENTIALS_PATH"
```

### Restart Orchestrator
```bash
# Stop current (Ctrl+C)
# Then restart:
python orchestrator.py VAULT_PATH
```

### Re-process All Emails
```bash
# Delete processed tracking file
del AI_Employee_Vault\.creds\gmail\gmail_processed.json

# Restart Gmail Watcher
python gmail_watcher.py "VAULT_PATH" "CREDENTIALS_PATH"
```

### Check Gmail Connection
```bash
cd .qwen\skills\gmail-watcher\scripts
timeout /t 10 /nobreak & python gmail_watcher.py "VAULT" "CREDS"
```

---

## Auto-Start Setup (Task Scheduler)

### Install Auto-Start Tasks
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\task-scheduler\scripts

python task_scheduler.py install-all ^
  --vault "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" ^
  --credentials "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

**What it does:**
- Creates Windows Tasks for Gmail Watcher
- Creates Windows Tasks for Orchestrator
- Auto-starts at Windows logon
- Auto-restarts on failure

---

## Quick Reference Table

| Task | Command | Batch File |
|------|---------|------------|
| Authenticate Gmail | `AUTHENTICATE-GMAIL.bat` | ✅ |
| Start Gmail Watcher | `python gmail_watcher.py...` | ❌ |
| Start Orchestrator | `python orchestrator.py...` | ❌ |
| Auto-process emails | `python auto_email_processor.py...` | ✅ `process-emails-auto.bat` |
| Process with Qwen | `qwen --prompt...` | ✅ `process-emails-qwen.bat` |
| Check pending | `dir Needs_Action\*.md` | ❌ |
| Check completed | `dir Done\*.md` | ❌ |
| Install auto-start | `python task_scheduler.py install-all` | ❌ |

---

## Workflow Summary

```
1. Gmail Watcher (python gmail_watcher.py)
   ↓ Detects new emails
   ↓ Creates .md files in Needs_Action/
   
2. Orchestrator (python orchestrator.py)
   ↓ Detects .md files
   ↓ Runs Auto Email Processor
   
3. Auto Email Processor (auto_email_processor.py)
   ↓ Reads emails
   ↓ Categorizes (security, newsletters, etc.)
   ↓ Creates drafts/approvals
   ↓ Moves to Done/
   
4. Dashboard (auto-updated)
   ↓ Shows pending count
   ↓ Shows completed count
```

---

*Email Processing Commands Guide v1.0*  
*Created: 2026-03-27*  
*Silver Tier - AI Employee Hackathon*
