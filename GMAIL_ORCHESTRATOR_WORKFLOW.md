# Gmail + Orchestrator Workflow - Complete Guide

## Overview

The complete email automation workflow with human-in-the-loop approval:

```
┌─────────────────────────────────────────────────────────────────┐
│                    EMAIL WORKFLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Gmail Watcher detects new email                             │
│     ↓ Creates EMAIL_*.md in Needs_Action/                       │
│                                                                  │
│  2. Orchestrator reads email                                    │
│     ↓ Creates APPROVAL_*.md with suggested reply                │
│     ↓ Saves to Pending_Approval/                                │
│                                                                  │
│  3. YOU review approval file                                    │
│     ↓ Edit reply if needed                                      │
│     ↓ Move to Approved/                                         │
│                                                                  │
│  4. Orchestrator detects approved file                          │
│     ↓ Uses Email MCP to send reply                              │
│     ↓ Moves file to Done/                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Process

### Step 1: Gmail Watcher Detects Email

**Command:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts

python gmail_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

**What happens:**
- Monitors Gmail every 60 seconds
- Detects new unread emails
- Creates `EMAIL_*.md` file in `Needs_Action/`

**Example file created:**
```
Needs_Action/EMAIL_Invoice_Request_19d2c1234567890a.md
```

---

### Step 2: Orchestrator Creates Approval Request

**Command (run in separate terminal):**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts

python orchestrator.py ..\AI_Employee_Vault
```

**What happens:**
- Detects new `EMAIL_*.md` file
- Reads email content
- Generates suggested reply
- Creates `APPROVAL_*.md` file in `Pending_Approval/`
- Moves original email to `Done/`

**Example approval file created:**
```
Pending_Approval/APPROVAL_EMAIL_Invoice_Request_19d2c1234567890a.md
```

**Approval file content:**
```markdown
---
type: approval_request
action: send_email
from: client@example.com
to: client@example.com
subject: Re: Invoice Request
created: 2026-03-27T01:00:00Z
status: pending
---

# Email Approval Required

**From:** client@example.com  
**Subject:** Invoice Request

## Original Email Content

Hi, can you send me the invoice for last month?

---

## Suggested Reply

**To:** client@example.com  
**Subject:** Re: Invoice Request

Dear Sender,

Thank you for your email regarding "Invoice Request".

We have received your request and will process it shortly. Our accounting team will review and respond with the necessary documentation.

Best regards,
AI Employee

---

## To Approve and Send

1. Review the suggested reply above
2. Edit if needed (modify the reply text)
3. Move this file to `/Approved` folder
4. The Email MCP will automatically send the reply
```

---

### Step 3: You Review and Approve

**What you do:**

1. **Check Pending_Approval folder:**
   ```bash
   dir AI_Employee_Vault\Pending_Approval\APPROVAL_*.md
   ```

2. **Open the approval file:**
   ```bash
   notepad AI_Employee_Vault\Pending_Approval\APPROVAL_*.md
   ```

3. **Review the suggested reply**

4. **Edit if needed** (modify the reply text in the "Suggested Reply" section)

5. **Save the file**

6. **Move to Approved folder:**
   ```bash
   move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Approved\
   ```

---

### Step 4: Orchestrator Sends Email via MCP

**What happens (automatic):**

Orchestrator (running every 60 seconds) detects the approved file:

```
2026-03-27 01:05:00 - Orchestrator - INFO - Processing approved item: APPROVAL_*.md
2026-03-27 01:05:00 - Orchestrator - INFO - Sending email to client@example.com...
2026-03-27 01:05:05 - Orchestrator - INFO - ✓ Email sent successfully
2026-03-27 01:05:05 - Orchestrator - INFO - ✓ Moved to Done: APPROVAL_*.md
```

**What Email MCP does:**
- Reads approval file
- Extracts: to, subject, body
- Authenticates with Gmail API
- Sends email
- Returns success/failure

---

### Step 5: File Moved to Done

After successful send:
```
Approved/APPROVAL_*.md  →  Done/APPROVAL_*.md
```

**Dashboard updated:**
```markdown
| Metric | Value |
|--------|-------|
| Pending Tasks | 0 |
| Awaiting Approval | 0 |
| Completed Today | 1 |
```

---

## Complete Commands Reference

### Start Gmail Watcher
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\gmail-watcher\scripts
python gmail_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault" "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json"
```

### Start Orchestrator
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python orchestrator.py ..\AI_Employee_Vault
```

### Check Pending Approvals
```bash
dir AI_Employee_Vault\Pending_Approval\APPROVAL_*.md
```

### Approve and Send (Manual)
```bash
# 1. Review file
notepad AI_Employee_Vault\Pending_Approval\APPROVAL_*.md

# 2. Edit reply if needed, save

# 3. Move to Approved
move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Approved\

# 4. Orchestrator will automatically send (within 60 seconds)
```

### Check Sent Emails
```bash
dir AI_Employee_Vault\Done\APPROVAL_*.md
```

### Check Activity Logs
```bash
type AI_Employee_Vault\Logs\*.json
```

---

## Folder Structure

```
AI_Employee_Vault/
├── Needs_Action/          # New emails from Gmail Watcher
│   └── EMAIL_*.md
├── Pending_Approval/      # Approval requests with suggested replies
│   └── APPROVAL_*.md
├── Approved/              # Approved, waiting to be sent
│   └── APPROVAL_*.md
├── Done/                  # Processed emails
│   ├── EMAIL_*.md         # Original emails
│   └── APPROVAL_*.md      # Sent replies
├── Logs/                  # Activity logs
│   └── YYYY-MM-DD.json
└── Dashboard.md           # Status dashboard
```

---

## Workflow States

| State | Location | What Happens |
|-------|----------|--------------|
| **New Email** | `Needs_Action/EMAIL_*.md` | Gmail Watcher creates file |
| **Pending Approval** | `Pending_Approval/APPROVAL_*.md` | Orchestrator creates approval with suggested reply |
| **Approved** | `Approved/APPROVAL_*.md` | You moved file here, waiting to send |
| **Sent** | `Done/APPROVAL_*.md` | Email MCP sent the reply |
| **Completed** | `Done/EMAIL_*.md` | Original email also moved here |

---

## Editing Suggested Replies

Before moving to Approved, you can edit the reply:

1. **Open approval file:**
   ```bash
   notepad AI_Employee_Vault\Pending_Approval\APPROVAL_*.md
   ```

2. **Find "Suggested Reply" section:**
   ```markdown
   ## Suggested Reply

   **To:** client@example.com  
   **Subject:** Re: Invoice Request

   Dear Sender,

   Thank you for your email...
   ```

3. **Edit the reply text** (keep the To/Subject lines)

4. **Save file**

5. **Move to Approved:**
   ```bash
   move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Approved\
   ```

---

## Troubleshooting

### "Email MCP not found"

**Error:**
```
Error: Credentials file not found
```

**Solution:**
```bash
# Run authentication first
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee
AUTHENTICATE-GMAIL.bat
```

### "Approval file not moving"

**Check:**
- File is in `Approved/` folder (not `Pending_Approval/`)
- Orchestrator is running
- Check logs for errors

### "Email not sending"

**Check:**
```bash
# View logs
type AI_Employee_Vault\Logs\*.json

# Check Gmail authentication
python scripts\email_mcp.py --help
```

### "Orchestrator not detecting files"

**Restart orchestrator:**
```bash
# Stop current (Ctrl+C)
# Then restart:
python orchestrator.py ..\AI_Employee_Vault
```

---

## Quick Reference Table

| Step | Component | Command | Location |
|------|-----------|---------|----------|
| 1 | Gmail Watcher | `python gmail_watcher.py...` | Terminal 1 |
| 2 | Orchestrator | `python orchestrator.py...` | Terminal 2 |
| 3 | Review | Open `APPROVAL_*.md` | Manual |
| 4 | Approve | Move to `Approved/` | Manual |
| 5 | Send | Automatic (Email MCP) | Automatic |
| 6 | Complete | Move to `Done/` | Automatic |

---

## Example Session

```bash
# Terminal 1 - Start Gmail Watcher
cd .qwen\skills\gmail-watcher\scripts
python gmail_watcher.py "C:\Users\...\AI_Employee_Vault" "C:\Users\...\client_secret.json"

# Output:
# 📬 You have 1 unread email(s) in Gmail
# ✨ Found 1 NEW unread email(s) to process
# Action file created: EMAIL_Client_Inquiry_*.md

# Terminal 2 - Start Orchestrator
cd ..\..\scripts
python orchestrator.py ..\AI_Employee_Vault

# Output:
# Processing email: EMAIL_Client_Inquiry_*.md
# ✓ Created approval request: APPROVAL_EMAIL_Client_Inquiry_*.md
# ✓ Moved to Done: EMAIL_Client_Inquiry_*.md

# Manual Step - Approve
# 1. Open: AI_Employee_Vault\Pending_Approval\APPROVAL_*.md
# 2. Review suggested reply
# 3. Move to Approved:
move AI_Employee_Vault\Pending_Approval\APPROVAL_*.md AI_Employee_Vault\Approved\

# Automatic - Email sent
# Output from Orchestrator:
# Processing approved item: APPROVAL_*.md
# Sending email to client@example.com...
# ✓ Email sent successfully
# ✓ Moved to Done: APPROVAL_*.md
```

---

*Gmail + Orchestrator Workflow Guide v1.0*  
*Created: 2026-03-27*  
*Silver Tier - AI Employee Hackathon*
