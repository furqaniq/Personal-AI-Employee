# Windows Task Scheduler Setup Guide

## Overview

Windows Task Scheduler allows you to automate the execution of programs or scripts at specified times or in response to specific events.

---

## Prerequisites

- Windows 10/11
- Python 3.13+ installed
- Administrator access (for creating tasks)
- All watcher scripts tested and working manually

---

## Task Scheduler Basics

### Opening Task Scheduler

1. Press `Win + R`
2. Type `taskschd.msc`
3. Press Enter

### Task Scheduler Interface

```
Task Scheduler (Local)
├── Task Scheduler Library
│   └── AI_Employee/          ← Our tasks folder
├── Task Scheduler History
└── Create Basic Task...      ← Wizard for simple tasks
```

---

## Creating Tasks Manually

### Step 1: Create Task Folder

1. Right-click "Task Scheduler Library"
2. Select "Create Folder"
3. Name: `AI_Employee`

### Step 2: Create Basic Task

1. Right-click "AI_Employee" folder
2. Select "Create Basic Task..."
3. Follow the wizard:
   - **Name:** GmailWatcher
   - **Description:** Monitor Gmail for new emails
   - **Trigger:** When I log on
   - **Action:** Start a program
   - **Program/script:** `C:\path\to\python.exe`
   - **Arguments:** `"C:\path\to\gmail_watcher.py" "C:\path\to\vault" "C:\path\to\client_secret.json"`
   - **Start in:** `C:\path\to\scripts`

### Step 3: Configure Advanced Settings

1. Right-click the task → Properties
2. **General tab:**
   - ✅ Run with highest privileges
   - Configure for: Windows 10/11
3. **Conditions tab:**
   - ❌ Uncheck "Start only if computer is on AC power"
4. **Settings tab:**
   - ✅ Allow task to be run on demand
   - ✅ Run task as soon as possible after scheduled start is missed
   - ✅ Restart every: 1 minute
   - ✅ Attempt to restart up to: 3 times
   - ✅ Stop task if it runs longer than: 24 hours

---

## Task Configuration Examples

### Gmail Watcher

| Setting | Value |
|---------|-------|
| **Program** | `C:\Python313\python.exe` |
| **Arguments** | `"C:\...\gmail_watcher.py" "C:\...\AI_Employee_Vault" "C:\...\client_secret.json"` |
| **Start in** | `C:\...\gmail-watcher\scripts` |
| **Trigger** | At log on |
| **Run as** | Your user account |

### LinkedIn Watcher

| Setting | Value |
|---------|-------|
| **Program** | `C:\Python313\python.exe` |
| **Arguments** | `"C:\...\linkedin_watcher.py" "C:\...\AI_Employee_Vault" --headless` |
| **Start in** | `C:\...\linkedin-watcher\scripts` |
| **Trigger** | At log on |
| **Run as** | Your user account |

### Orchestrator

| Setting | Value |
|---------|-------|
| **Program** | `C:\Python313\python.exe` |
| **Arguments** | `"C:\...\orchestrator.py" "C:\...\AI_Employee_Vault"` |
| **Start in** | `C:\...\scripts` |
| **Trigger** | At log on |
| **Run as** | Your user account |

### Daily Briefing (8 AM)

| Setting | Value |
|---------|-------|
| **Program** | `C:\Python313\python.exe` |
| **Arguments** | `"C:\...\daily_briefing.py" "C:\...\AI_Employee_Vault"` |
| **Start in** | `C:\...\scripts` |
| **Trigger** | Daily at 8:00 AM |
| **Run as** | Your user account |

---

## Using schtasks Command

### Create Task

```cmd
schtasks /Create /TN "AI_Employee\GmailWatcher" ^
  /TR "\"C:\Python313\python.exe\" \"C:\...\gmail_watcher.py\"" ^
  /SC ONLOGON ^
  /RL HIGHEST ^
  /F
```

### Delete Task

```cmd
schtasks /Delete /TN "AI_Employee\GmailWatcher" /F
```

### Query Task

```cmd
schtasks /Query /TN "AI_Employee\GmailWatcher" /V /FO LIST
```

### Run Task Manually

```cmd
schtasks /Run /TN "AI_Employee\GmailWatcher"
```

### Export Task to XML

```cmd
schtasks /Query /TN "AI_Employee\GmailWatcher" /XML > GmailWatcher.xml
```

---

## Troubleshooting

### Task Won't Start

**Check:**
1. Task is enabled
2. "Run with highest privileges" is checked
3. User account has correct permissions
4. Python path is correct

**Solution:**
```cmd
# Test command manually
"C:\Python313\python.exe" "C:\...\script.py" --test
```

### Python Not Found

**Problem:** Task fails with error 0x2

**Solution:** Use full path to python.exe:
```
C:\Python313\python.exe
```

Find Python path:
```python
import sys
print(sys.executable)
```

### Script Not Found

**Problem:** Task fails with error 0x1

**Solution:**
1. Use full path to script
2. Set "Start in" directory
3. Quote paths with spaces

### Task Runs But Exits Immediately

**Check:**
1. Script has no syntax errors
2. All dependencies installed
3. Credentials are valid
4. Vault path exists

**Solution:** Add logging to script:
```python
import logging
logging.basicConfig(filename='C:/path/to/debug.log', level=logging.INFO)
```

### Multiple Instances Running

**Problem:** Task starts new instance while previous is still running

**Solution:** In task Properties → Settings:
- Select "Do not start a new instance"

---

## Best Practices

1. **Use full paths** - Always specify complete paths
2. **Quote arguments** - Wrap paths with spaces in quotes
3. **Set "Start in"** - Working directory matters
4. **Enable logging** - Track task execution
5. **Test manually first** - Verify script works before scheduling
6. **Use task folder** - Organize tasks in AI_Employee folder
7. **Set restart policy** - Auto-restart on failure
8. **Limit execution time** - Prevent runaway tasks

---

## Security Considerations

1. **Run as user** - Not SYSTEM unless necessary
2. **Limit permissions** - Only what's needed
3. **Secure credentials** - Don't store passwords in tasks
4. **Audit execution** - Review task history
5. **Use encrypted storage** - For sensitive data

---

## Monitoring

### View Task History

1. Open Task Scheduler
2. Click "Enable All Tasks History" (right panel)
3. Select task → History tab

### Check Last Result

```cmd
schtasks /Query /TN "AI_Employee\GmailWatcher" /V /FO LIST | findstr "Last Result"
```

Result codes:
- `0x0` - Success
- `0x1` - Incorrect function
- `0x2` - File not found
- `0x41301` - Task is running
- `0x41303` - Task hasn't run yet

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `taskschd.msc` | Open Task Scheduler |
| `schtasks /Create` | Create task |
| `schtasks /Delete` | Delete task |
| `schtasks /Query` | View task info |
| `schtasks /Run` | Run task now |
| `schtasks /End` | Stop running task |

---

*Reference: Windows Task Scheduler Setup for Silver Tier*
