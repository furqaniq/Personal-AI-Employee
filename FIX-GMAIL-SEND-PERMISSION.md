# ✅ GMAIL SEND PERMISSION - QUICK FIX

## Problem
```
Error: Insufficient Permission
Request had insufficient authentication scopes for gmail.send
```

## Solution

### Step 1: Delete Old Token
```bash
del "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault\.creds\gmail_token.json"
del "C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\token.json"
```

### Step 2: Re-Authenticate with Send Permissions

**Double-click:**
```
AUTHENTICATE-GMAIL-SEND.bat
```

**Or run:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python authenticate-gmail-send.py
```

### Step 3: Complete Browser Authentication

1. Browser opens automatically
2. Sign in to Gmail
3. Click "Advanced" → "Go to hackathon-0-fte-491317 (unsafe)"
4. Click "Allow" on permissions (gmail.send, gmail.readonly, gmail.modify)
5. Wait for "Authentication successful!"

### Step 4: Test Email Sending

```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python orchestrator.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

Move an approval file to Approved/ folder and watch it send automatically!

---

## What Changed

**Before:** Token had only `gmail.readonly` scope
**After:** Token has `gmail.send`, `gmail.readonly`, `gmail.modify` scopes

---

## Verify It Works

Check your Gmail "Sent" folder after the orchestrator sends an email!

---

*Gmail Send Permission Fix v1.0*
*Created: 2026-03-27*
