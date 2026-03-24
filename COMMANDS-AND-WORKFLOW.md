# AI Employee - Bronze Tier Commands & Workflow Guide

> **Your complete reference for running the AI Employee system**

---

## What is Bronze Tier?

**Bronze Tier** is the **foundation level** of the Personal AI Employee Hackathon. It provides the minimum viable deliverable for an autonomous AI employee system.

### Bronze Tier Deliverables ✅

- [x] **Obsidian Vault** with Dashboard.md and Company_Handbook.md
- [x] **One Working Watcher** - File System monitoring (detects copied/dropped files)
- [x] **Claude/Qwen Code Integration** - Reads from and writes to the vault
- [x] **Basic Folder Structure** - /Inbox, /Needs_Action, /Done
- [x] **Agent Skill** - File processing skill for AI

### What Bronze Tier Does

| Feature | Description |
|---------|-------------|
| **File Detection** | Automatically detects files dropped/copied into Inbox folder |
| **Action Creation** | Creates markdown action files in Needs_Action folder |
| **AI Processing** | Qwen Code reads and processes action files |
| **Approval Workflow** | Human-in-the-loop for sensitive actions |
| **Task Completion** | Moves completed items to Done folder |
| **Activity Logging** | Logs all actions to Logs folder |

### What Bronze Tier Does NOT Do (Yet)

| Feature | Available In |
|---------|--------------|
| Gmail monitoring | Silver Tier |
| WhatsApp monitoring | Silver Tier |
| Social media posting | Silver Tier |
| Email sending | Silver Tier |
| Scheduled tasks | Silver Tier |
| Accounting integration | Gold Tier |
| CEO Briefings | Gold Tier |
| Ralph Wiggum loop | Gold Tier |
| Cloud deployment | Platinum Tier |

---

## Quick Start (Copy-Paste Commands)

### Start the System

**Terminal 1 - Start File Watcher:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox
```

**Terminal 2 - Start Orchestrator:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python orchestrator.py ..\AI_Employee_Vault
```

**Terminal 3 - Process with Qwen Code:**
```bash
qwen --prompt "Process all files in Needs_Action folder using Company_Handbook.md rules" --cwd ..\AI_Employee_Vault
```

---

## Bronze Tier Setup Checklist

### Prerequisites

| Component | Required | Purpose |
|-----------|----------|---------|
| **Python** | 3.13+ | Watcher scripts & orchestration |
| **Qwen Code** | Active subscription | Primary reasoning engine |
| **Obsidian** | v1.10.6+ (free) | Knowledge base & dashboard |
| **Node.js** | v24+ LTS | Future MCP servers (Silver+) |

### Installation Steps

**Step 1: Install Python Dependencies**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
pip install -r requirements.txt
```

**Step 2: Verify Installation**
```bash
python test_bronze_tier.py ..\AI_Employee_Vault
```

**Expected Output:**
```
✓ PASS: Vault Structure
✓ PASS: Scripts
✓ PASS: Dependencies
! FAIL: Qwen Code (optional - can run manually)
✓ PASS: Sample File
```

**Step 3: Open Vault in Obsidian**
1. Open Obsidian
2. Click "Open folder as vault"
3. Select: `AI_Employee_Vault`
4. Verify you see `Dashboard.md` and `Company_Handbook.md`

**Step 4: Review Key Files**
- Open `Dashboard.md` - Your real-time status center
- Open `Company_Handbook.md` - Rules for AI behavior

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Employee Flow                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. You drop/copy a file → Inbox/                           │
│         ↓                                                    │
│  2. File System Watcher detects it (real-time)              │
│         ↓                                                    │
│  3. Creates action file → Needs_Action/                     │
│         ↓                                                    │
│  4. Orchestrator sees pending items (every 60s)             │
│         ↓                                                    │
│  5. Creates task file → Plans/ for Qwen Code                │
│         ↓                                                    │
│  6. Qwen Code processes task                                │
│         ↓                                                    │
│  7. Moves completed → Done/                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Bronze Tier Workflow Diagram

```
                    BRONZE TIER WORKFLOW
                         ════════════════

    ┌─────────────────────────────────────────────────────┐
    │  YOU: Drop/Copy file into Inbox/                    │
    │      • Any file type (PDF, TXT, DOCX, etc.)         │
    │      • Drag & drop or copy/paste                    │
    └──────────────────┬──────────────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────────────────────┐
    │  WATCHER: filesystem_watcher.py (running)           │
    │      • Detects new file in real-time                │
    │      • Creates action file → Needs_Action/          │
    │      • Prints: "✓ New file detected"                │
    └──────────────────┬──────────────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────────────────────┐
    │  ORCHESTRATOR: orchestrator.py (running)            │
    │      • Checks Needs_Action/ every 60 seconds        │
    │      • Creates task file → Plans/                   │
    │      • Triggers Qwen Code                           │
    └──────────────────┬──────────────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────────────────────┐
    │  QWEN CODE: Manual or automatic processing          │
    │      • Reads action file                            │
    │      • Consults Company_Handbook.md                 │
    │      • Creates plan if complex                      │
    │      • Requests approval if sensitive               │
    └──────────────────┬──────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
    ┌─────────────┐           ┌─────────────┐
    │  Simple     │           │  Requires   │
    │  Task       │           │  Approval   │
    └──────┬──────┘           └──────┬──────┘
           │                         │
           ▼                         ▼
    ┌─────────────┐           ┌─────────────┐
    │  Move to    │           │  Create     │
    │  Done/      │           │  file in    │
    │  ✓ Complete │           │  Pending_   │
    │             │           │  Approval/  │
    └─────────────┘           └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │  YOU:       │
                              │  Review &   │
                              │  Approve    │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │  Move to    │
                              │  Approved/  │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │  Qwen       │
                              │  Executes   │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │  Move to    │
                              │  Done/      │
                              │  ✓ Complete │
                              └─────────────┘
```

---

## Command Reference

### 1. File System Watcher

**Purpose:** Monitors the Inbox folder for new files and creates action files in Needs_Action.

**Command:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox
```

**Expected Output:**
```
✓ Watcher started
  Watching: ..\AI_Employee_Vault\Inbox
  Output: ..\AI_Employee_Vault\Needs_Action
  Press Ctrl+C to stop

Scanning for existing files...
Scan complete.

✓ New file detected: myfile.txt
✓ Action file created: FILE_myfile_1774305000.md
```

**Stop:** Press `Ctrl+C` in the terminal

**What it does:**
- Watches `Inbox/` folder in real-time
- Detects: copied files, dragged files, saved files
- Creates `.md` action files in `Needs_Action/`
- Skips `.md` files (already action files)

---

### 2. Orchestrator

**Purpose:** Coordinates the workflow by checking for pending items and triggering Qwen Code.

**Command:**
```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python orchestrator.py ..\AI_Employee_Vault
```

**With custom check interval (30 seconds):**
```bash
python orchestrator.py ..\AI_Employee_Vault 30
```

**Expected Output:**
```
2026-03-24 XX:XX:XX - Orchestrator - INFO - ============================================================
2026-03-24 XX:XX:XX - Orchestrator - INFO - AI Employee Orchestrator - Bronze Tier
2026-03-24 XX:XX:XX - Orchestrator - INFO - ============================================================
2026-03-24 XX:XX:XX - Orchestrator - INFO - Vault: ..\AI_Employee_Vault
2026-03-24 XX:XX:XX - Orchestrator - INFO - Check interval: 60s
2026-03-24 XX:XX:XX - Orchestrator - INFO - Press Ctrl+C to stop
2026-03-24 XX:XX:XX - Orchestrator - INFO - ============================================================
2026-03-24 XX:XX:XX - Orchestrator - INFO - Found 2 pending item(s)
2026-03-24 XX:XX:XX - Orchestrator - INFO - Triggering Qwen Code...
2026-03-24 XX:XX:XX - Orchestrator - INFO - State file created: ORCHESTRATOR_20260324_XXXXXX.md
```

**Stop:** Press `Ctrl+C` in the terminal

**What it does:**
- Checks `Needs_Action/` every 60 seconds (or custom interval)
- Creates task files in `Plans/` for Qwen Code
- Processes approved items from `Approved/`
- Updates `Dashboard.md` with status

---

### 3. Qwen Code (Manual Processing)

**Purpose:** Process pending files using AI reasoning.

**Command:**
```bash
qwen --prompt "Process all files in Needs_Action folder" --cwd ..\AI_Employee_Vault
```

**Detailed prompt:**
```bash
qwen --prompt "Read all files in Needs_Action. For each file: 1) Understand the task 2) Check Company_Handbook.md for rules 3) Create plans in Plans folder 4) Request approval for sensitive actions 5) Move completed items to Done" --cwd ..\AI_Employee_Vault
```

**What Qwen does:**
- Reads action files in `Needs_Action/`
- Consults `Company_Handbook.md` for rules
- Creates plans for complex tasks
- Requests approval for sensitive actions
- Moves completed items to `Done/`

---

## Complete Workflow Examples

### Example 1: Process a Document

**Step 1: Start the system**
```bash
# Terminal 1
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox
```

**Step 2: Drop a file**
- Copy any file to: `AI_Employee_Vault\Inbox\mydocument.pdf`

**Step 3: Watcher detects it**
```
✓ New file detected: mydocument.pdf
✓ Action file created: FILE_mydocument_1774305100.md
```

**Step 4: Process with Qwen**
```bash
# Terminal 3
qwen --prompt "Process FILE_mydocument_1774305100.md in Needs_Action - summarize the content and suggest actions" --cwd ..\AI_Employee_Vault
```

**Step 5: Check results**
```bash
dir ..\AI_Employee_Vault\Done
```

---

### Example 2: Email Invoice Request (Requires Approval)

**Step 1: Create email request file**
Copy a file or create: `Inbox\invoice_request.txt`

**Step 2: Watcher creates action file**
```
✓ New file detected: invoice_request.txt
✓ Action file created: FILE_invoice_request_1774305200.md
```

**Step 3: Qwen processes and creates approval request**
```bash
qwen --prompt "Process invoice request - check Company_Handbook.md for payment rules" --cwd ..\AI_Employee_Vault
```

**Step 4: Check Pending_Approval folder**
```bash
dir ..\AI_Employee_Vault\Pending_Approval
```

**Step 5: Review and approve**
- Open the approval file in `Pending_Approval/`
- If OK, move it to `Approved/`:
```bash
move ..\AI_Employee_Vault\Pending_Approval\EMAIL_*.md ..\AI_Employee_Vault\Approved\
```

**Step 6: Qwen executes approved action**
```bash
qwen --prompt "Process all approved items in Approved folder" --cwd ..\AI_Employee_Vault
```

---

## Folder Structure Reference

```
AI_Employee_Vault/
├── Dashboard.md              # Real-time status dashboard
├── Company_Handbook.md       # Rules and guidelines
│
├── Inbox/                    # ← DROP FILES HERE
│   └── (your files)
│
├── Needs_Action/             # ← Watcher creates action files here
│   ├── FILE_document_123.md
│   └── EMAIL_request_456.md
│
├── Plans/                    # ← Qwen creates plans here
│   ├── PLAN_task_789.md
│   └── ORCHESTRATOR_20260324_XXXXXX.md
│
├── Pending_Approval/         # ← Awaiting your approval
│   └── EMAIL_send_XXX.md
│
├── Approved/                 # ← Move approved files here
│   └── (approved actions)
│
├── Rejected/                 # ← Move rejected files here
│   └── (rejected actions)
│
├── Done/                     # ← Completed tasks
│   └── (finished work)
│
├── Logs/                     # ← Activity logs
│   └── 2026-03-24.json
│
└── Accounting/               # ← Financial records (future)
```

---

## Common Tasks

### Check System Status

```bash
# View dashboard
type ..\AI_Employee_Vault\Dashboard.md

# Check pending items
dir ..\AI_Employee_Vault\Needs_Action

# Check running processes
tasklist | findstr "python"
```

### Stop All Processes

```bash
# Stop Python watchers
taskkill /F /FI "WINDOWTITLE eq *python*" /T 2>nul

# Or press Ctrl+C in each terminal
```

### Test the System

```bash
# Create a test file
echo "Test at %time%" > ..\AI_Employee_Vault\Inbox\test_%random%.txt

# Wait 3 seconds
timeout /t 3 /nobreak

# Check if action file was created
dir ..\AI_Employee_Vault\Needs_Action\FILE_test_*.md
```

### View Logs

```bash
# Today's activity log
type ..\AI_Employee_Vault\Logs\2026-03-24.json

# List all logs
dir ..\AI_Employee_Vault\Logs
```

---

## Troubleshooting

### Watcher Not Detecting Files

**Check if watcher is running:**
```bash
tasklist | findstr "filesystem_watcher"
```

**Restart watcher:**
```bash
# Stop existing
taskkill /F /FI "WINDOWTITLE eq *python*" /T 2>nul

# Start fresh
python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox
```

**Test with simple file:**
```bash
echo "test" > ..\AI_Employee_Vault\Inbox\test.txt
```

### Orchestrator Not Creating Tasks

**Check orchestrator output:**
```bash
python orchestrator.py ..\AI_Employee_Vault
```

**Manually create task:**
```bash
# Check Needs_Action
dir ..\AI_Employee_Vault\Needs_Action

# Manually trigger Qwen
qwen --prompt "Process all files in Needs_Action" --cwd ..\AI_Employee_Vault
```

### Qwen Code Not Found

**Install Qwen Code:**
```bash
npm install -g qwen
```

**Verify installation:**
```bash
qwen --version
```

**Use manual mode (no Qwen CLI needed):**
- Open files in `Needs_Action/` manually
- Process them yourself
- Move to `Done/` when complete

### Files Not Being Processed

**Check file type:**
- `.md` files are skipped (already action files)
- Hidden files (starting with `.`) are skipped

**Check file is fully copied:**
- Wait for copy to complete
- Watcher waits for file to be ready

**Check Company_Handbook.md rules:**
- Some actions require approval
- Check `Pending_Approval/` folder

---

## Daily Workflow

### Morning (Start System)

1. **Open Terminal 1** - Start Watcher
   ```bash
   cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
   python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox
   ```

2. **Open Terminal 2** - Start Orchestrator
   ```bash
   cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
   python orchestrator.py ..\AI_Employee_Vault
   ```

3. **Check Dashboard**
   ```bash
   type ..\AI_Employee_Vault\Dashboard.md
   ```

### During Day (Working)

- **Drop files** into `Inbox/` as needed
- **Watch terminal** for detection confirmations
- **Review approvals** in `Pending_Approval/`
- **Move approved** to `Approved/`

### Evening (Shutdown)

1. **Check completed work**
   ```bash
   dir ..\AI_Employee_Vault\Done
   ```

2. **Review logs**
   ```bash
   type ..\AI_Employee_Vault\Logs\2026-03-24.json
   ```

3. **Stop processes**
   - Press `Ctrl+C` in Terminal 1 (Watcher)
   - Press `Ctrl+C` in Terminal 2 (Orchestrator)

---

## Quick Reference Card

| Task | Command |
|------|---------|
| **Start Watcher** | `python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox` |
| **Start Orchestrator** | `python orchestrator.py ..\AI_Employee_Vault` |
| **Process with Qwen** | `qwen --prompt "Process all files in Needs_Action" --cwd ..\AI_Employee_Vault` |
| **Check Pending** | `dir ..\AI_Employee_Vault\Needs_Action` |
| **Check Approved** | `dir ..\AI_Employee_Vault\Approved` |
| **View Dashboard** | `type ..\AI_Employee_Vault\Dashboard.md` |
| **View Logs** | `type ..\AI_Employee_Vault\Logs\2026-03-24.json` |
| **Stop All** | Press `Ctrl+C` in each terminal |

---

## Approval Workflow

### When Approval is Needed

Qwen creates a file in `Pending_Approval/`:

```markdown
---
type: approval_request
action: send_email
created: 2026-03-24T10:00:00Z
status: pending
---

# Approval Required

**Action:** Send email to client@example.com
**Subject:** Invoice #123

Move to /Approved to proceed.
```

### To Approve

```bash
move ..\AI_Employee_Vault\Pending_Approval\EMAIL_*.md ..\AI_Employee_Vault\Approved\
```

### To Reject

```bash
move ..\AI_Employee_Vault\Pending_Approval\EMAIL_*.md ..\AI_Employee_Vault\Rejected\
```

---

## Best Practices

1. **Keep terminals open** - Watcher and Orchestrator need to run continuously
2. **Check Dashboard daily** - Stay informed of pending items
3. **Review approvals promptly** - Don't let items sit in `Pending_Approval/`
4. **Clean up Done folder** - Archive completed items weekly
5. **Review logs** - Check `Logs/` for audit trail
6. **Backup vault** - Use Git or cloud sync for `AI_Employee_Vault/`

---

## Bronze Tier Example Scenarios

### Scenario 1: Process a Meeting Notes File

**Use Case:** You have meeting notes you want summarized and action items extracted.

**Files:**
- Input: `meeting_notes.txt` in `Inbox/`
- Output: Summary and action items in `Done/`

**Steps:**

1. **Start the system**
   ```bash
   # Terminal 1
   python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox
   ```

2. **Copy your file**
   ```bash
   copy "C:\Users\...\Documents\meeting_notes.txt" "..\AI_Employee_Vault\Inbox\"
   ```

3. **Watcher detects it**
   ```
   ✓ New file detected: meeting_notes.txt
   ✓ Action file created: FILE_meeting_notes_1774305000.md
   ```

4. **Process with Qwen**
   ```bash
   qwen --prompt "Read FILE_meeting_notes_1774305000.md in Needs_Action. Summarize the meeting notes and extract action items. Create a plan if there are follow-up tasks. Move to Done when complete." --cwd ..\AI_Employee_Vault
   ```

5. **Check results**
   ```bash
   # View the processed file
   type ..\AI_Employee_Vault\Done\FILE_meeting_notes_1774305000.md
   ```

---

### Scenario 2: Invoice Request (Approval Required)

**Use Case:** Client requests an invoice via email/text.

**Files:**
- Input: `invoice_request.txt` in `Inbox/`
- Output: Invoice sent, logged in `Done/`

**Steps:**

1. **Create request file**
   ```
   Copy to Inbox/invoice_request.txt:
   
   "Client ABC Corp is requesting an invoice for Project X.
    Amount: $2,500
    Email: billing@abccorp.com
    Due: Net 15 days"
   ```

2. **Watcher creates action file**
   ```
   ✓ New file detected: invoice_request.txt
   ✓ Action file created: FILE_invoice_request_1774305100.md
   ```

3. **Qwen processes and requests approval**
   ```bash
   qwen --prompt "Process invoice request. Check Company_Handbook.md for invoicing rules. Create invoice and request approval before sending." --cwd ..\AI_Employee_Vault
   ```

4. **Check Pending_Approval**
   ```bash
   dir ..\AI_Employee_Vault\Pending_Approval
   # You'll see: EMAIL_send_invoice_XXX.md
   ```

5. **Review and approve**
   ```bash
   # Read the approval request
   type ..\AI_Employee_Vault\Pending_Approval\EMAIL_send_invoice_XXX.md
   
   # If OK, approve it
   move ..\AI_Employee_Vault\Pending_Approval\EMAIL_*.md ..\AI_Employee_Vault\Approved\
   ```

6. **Qwen executes**
   ```bash
   qwen --prompt "Process approved items in Approved folder. Send the invoice email and log the action." --cwd ..\AI_Employee_Vault
   ```

7. **Verify completion**
   ```bash
   dir ..\AI_Employee_Vault\Done
   ```

---

### Scenario 3: Document Categorization

**Use Case:** You have multiple documents to categorize and file.

**Files:**
- Input: Multiple files in `Inbox/`
- Output: Categorized and summarized in `Done/`

**Steps:**

1. **Drop multiple files**
   ```bash
   copy "C:\docs\*.pdf" "..\AI_Employee_Vault\Inbox\"
   ```

2. **Watcher processes all**
   ```
   ✓ New file detected: report.pdf
   ✓ Action file created: FILE_report_1774305200.md
   
   ✓ New file detected: contract.pdf
   ✓ Action file created: FILE_contract_1774305201.md
   ```

3. **Batch process with Qwen**
   ```bash
   qwen --prompt "Process all files in Needs_Action. For each document: 1) Identify document type 2) Summarize content 3) Suggest category 4) Move to Done with notes" --cwd ..\AI_Employee_Vault
   ```

4. **Check Dashboard**
   ```bash
   type ..\AI_Employee_Vault\Dashboard.md
   # Should show updated "Completed Today" count
   ```

---

### Scenario 4: Daily Task Processing Routine

**Use Case:** Establish a daily workflow for processing items.

**Morning (9:00 AM):**
```bash
# Start watcher
python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox

# Start orchestrator
python orchestrator.py ..\AI_Employee_Vault

# Check overnight activity
type ..\AI_Employee_Vault\Logs\2026-03-24.json
```

**Midday (1:00 PM):**
```bash
# Check pending items
dir ..\AI_Employee_Vault\Needs_Action

# Process with Qwen
qwen --prompt "Process all pending files in Needs_Action" --cwd ..\AI_Employee_Vault

# Check for approvals needed
dir ..\AI_Employee_Vault\Pending_Approval
```

**Evening (5:00 PM):**
```bash
# Review completed work
dir ..\AI_Employee_Vault\Done

# Update dashboard
type ..\AI_Employee_Vault\Dashboard.md

# Stop processes (Ctrl+C in each terminal)
```

---

## Bronze Tier Completion Checklist

Use this to verify you've completed Bronze Tier:

### Setup ✅
- [ ] Python 3.13+ installed
- [ ] Watchdog package installed (`pip install watchdog`)
- [ ] AI_Employee_Vault folder exists
- [ ] Dashboard.md created and readable
- [ ] Company_Handbook.md created with rules

### Functionality ✅
- [ ] Watcher detects copied files
- [ ] Watcher detects dragged files
- [ ] Action files created in Needs_Action/
- [ ] Orchestrator creates task files in Plans/
- [ ] Qwen Code can read and process files
- [ ] Approval workflow works (Pending_Approval → Approved → Done)
- [ ] Completed files moved to Done/

### Testing ✅
- [ ] Test with .txt file
- [ ] Test with .pdf file
- [ ] Test with copied file
- [ ] Test with dragged file
- [ ] Test approval workflow
- [ ] Verify logs are created

### Documentation ✅
- [ ] Can start system from memory
- [ ] Know how to stop processes
- [ ] Understand folder structure
- [ ] Know when approval is needed
- [ ] Can troubleshoot common issues

---

## Next Steps (After Bronze)

Once you've completed Bronze Tier and are comfortable with the workflow, consider adding:

### Silver Tier (20-30 hours)
- [ ] Gmail Watcher - Monitor Gmail for new emails
- [ ] WhatsApp Watcher - Monitor WhatsApp messages
- [ ] MCP Server for email sending - Send emails automatically
- [ ] Scheduled tasks via Task Scheduler - Run at specific times
- [ ] Human-in-the-loop approval workflow - Enhanced approvals

### Gold Tier (40+ hours)
- [ ] Ralph Wiggum persistence loop - Keep Qwen working until done
- [ ] CEO Briefing generation - Weekly business summaries
- [ ] Full cross-domain integration - Personal + Business
- [ ] Error recovery and graceful degradation
- [ ] Comprehensive audit logging

### Platinum Tier (60+ hours)
- [ ] Cloud deployment - Run 24/7 on cloud VM
- [ ] Work-zone specialization - Cloud vs Local tasks
- [ ] Vault sync - Multi-agent coordination
- [ ] Odoo integration - Full accounting system

---

*Generated for AI Employee Bronze Tier - Personal AI Employee Hackathon*
*Last Updated: 2026-03-24*

**Ready to start? Run these commands:**

```bash
# Terminal 1 - Start Watcher
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python filesystem_watcher.py ..\AI_Employee_Vault ..\AI_Employee_Vault\Inbox

# Terminal 2 - Start Orchestrator
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\scripts
python orchestrator.py ..\AI_Employee_Vault

# Terminal 3 - Test it!
echo "Hello AI Employee!" > ..\AI_Employee_Vault\Inbox\hello.txt
```
