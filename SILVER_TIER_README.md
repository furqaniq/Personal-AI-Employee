# Silver Tier - Personal AI Employee (Qwen Code)

**Tagline:** *Functional Assistant with Gmail + LinkedIn Integration + Auto-Posting*

Complete Silver Tier implementation using **Qwen Code** as the reasoning engine.

**📖 Setup Guide:** See `SILVER_TIER_SETUP.md` for step-by-step setup instructions with screenshots.

**✅ Packages Installed:** All required Python packages are installed and ready to use.

**🔑 Credentials:** Your Gmail API credentials are at `credentials.json` (project root) and copied to `C:\Users\Lenovo\AppData\Local\AI_Employee\creds\gmail\client_secret.json`

---

## Silver Tier Requirements ✅

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| All Bronze requirements | ✅ Complete | File System Watcher, Orchestrator, Qwen integration |
| Two or more Watcher scripts | ✅ Complete | Gmail, LinkedIn, File System |
| Auto-post on LinkedIn | ✅ Complete | `linkedin-poster` skill |
| Qwen reasoning loop with Plan.md | ✅ Complete | `plan-creator` skill |
| One working MCP server | ✅ Complete | Email MCP |
| HITL approval workflow | ✅ Complete | `approval-workflow` skill |
| Basic scheduling | ✅ Complete | `task-scheduler` skill + Windows Task Scheduler |

---

## Skills Architecture

```
.qwen/skills/
├── browsing-with-playwright/    # Bronze (existing)
├── gmail-watcher/               # Silver - Monitor Gmail
├── linkedin-watcher/            # Silver - Monitor LinkedIn
├── email-mcp/                   # Silver - Send emails
├── linkedin-poster/             # Silver - Auto-post to LinkedIn
├── plan-creator/                # Silver - Create Plan.md files
├── approval-workflow/           # Silver - HITL approvals
└── task-scheduler/              # Silver - Windows Task Scheduler integration
```

---

## Quick Start

### 1. Install Dependencies

```bash
# For Gmail Watcher and Email MCP
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# For LinkedIn Watcher and Poster
pip install playwright
playwright install chromium

# For File System Watcher
pip install watchdog
```

### 2. Set Up Google Cloud (Gmail API)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Gmail API
3. Create OAuth credentials → Download `client_secret.json`
4. Store securely: `mkdir "%USERPROFILE%\.creds\gmail"` → move file there

### 3. First-Time Authentication

```bash
# Gmail authentication
cd .qwen/skills/gmail-watcher/scripts
python gmail_watcher.py "C:\path\to\AI_Employee_Vault" "%USERPROFILE%\.creds\gmail\client_secret.json"

# LinkedIn session setup
cd .qwen/skills/linkedin-watcher/scripts
python linkedin_watcher.py "C:\path\to\AI_Employee_Vault" --setup-session
```

---

## Skills Reference

### 1. Gmail Watcher

**Location:** `.qwen/skills/gmail-watcher/`

**Purpose:** Monitor Gmail for new, unread, important emails

**Usage:**
```bash
cd .qwen/skills/gmail-watcher/scripts

# Run watcher
python gmail_watcher.py "C:\path\to\AI_Employee_Vault" "C:\path\to\client_secret.json"

# With custom interval (check every 2 minutes)
python gmail_watcher.py "C:\path\to\AI_Employee_Vault" "C:\path\to\client_secret.json" 120
```

**Creates:** `EMAIL_<subject>_<gmail_id>.md` in `Needs_Action/`

**Dependencies:** `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`

---

### 2. LinkedIn Watcher

**Location:** `.qwen/skills/linkedin-watcher/`

**Purpose:** Monitor LinkedIn for notifications, connection requests, messages

**Usage:**
```bash
cd .qwen/skills/linkedin-watcher/scripts

# First-time setup (opens browser for login)
python linkedin_watcher.py "C:\path\to\AI_Employee_Vault" --setup-session

# Run watcher (headless, 5-minute intervals)
python linkedin_watcher.py "C:\path\to\AI_Employee_Vault" --headless --interval 300
```

**Creates:** `LINKEDIN_<type>_<id>.md` in `Needs_Action/`

**Dependencies:** `playwright`

---

### 3. Email MCP

**Location:** `.qwen/skills/email-mcp/`

**Purpose:** Send and manage emails via Gmail API with HITL approval

**Usage:**
```bash
cd .qwen/skills/email-mcp/scripts

# Send email (known contact)
python email_mcp.py send \
  --to "client@known-domain.com" \
  --subject "Meeting Follow-up" \
  --body "Hi, Thanks for the meeting..."

# Create approval request (new contact)
python email_mcp.py draft \
  --to "newcontact@example.com" \
  --subject "Project Proposal" \
  --body "Dear..., We would like to..." \
  --vault "C:\path\to\AI_Employee_Vault"

# Search emails
python email_mcp.py search \
  --query "from:boss@company.com is:unread"
```

**Dependencies:** `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`

---

### 4. LinkedIn Poster

**Location:** `.qwen/skills/linkedin-poster/`

**Purpose:** Automatically post business content to LinkedIn to generate sales

**Usage:**
```bash
cd .qwen/skills/linkedin-poster/scripts

# Create post (draft for approval)
python linkedin_poster.py create \
  --topic "New product launch" \
  --type "product_update" \
  --vault "C:\path\to\AI_Employee_Vault"

# Post approved content
python linkedin_poster.py post-approved \
  --vault "C:\path\to\AI_Employee_Vault"

# First-time session setup
python linkedin_poster.py setup-session
```

**Dependencies:** `playwright`

**Content Types:** `product_update`, `milestone`, `insight`, `promotion`, `testimonial`

---

### 5. Plan Creator

**Location:** `.qwen/skills/plan-creator/`

**Purpose:** Create structured Plan.md files for complex tasks (Qwen reasoning loop)

**Usage:**
```bash
cd .qwen/skills/plan-creator/scripts

# Create plan from source file
python plan_creator.py create \
  --source "EMAIL_invoice_request.md" \
  --vault "C:\path\to\AI_Employee_Vault"

# Update plan progress
python plan_creator.py update \
  --plan "PLAN_1234567890.md" \
  --step 3 \
  --status complete \
  --notes "Invoice generated" \
  --vault "C:\path\to\AI_Employee_Vault"

# Get all plans status
python plan_creator.py report \
  --vault "C:\path\to\AI_Employee_Vault"
```

**Dependencies:** None (pure Python)

---

### 6. Approval Workflow

**Location:** `.qwen/skills/approval-workflow/`

**Purpose:** Manage human-in-the-loop approval for sensitive actions

**Usage:**
```bash
cd .qwen/skills/approval-workflow/scripts

# Create approval request
python approval_workflow.py create \
  --type "send_email" \
  --details '{"to": "user@example.com", "subject": "Hello"}' \
  --reason "New contact" \
  --vault "C:\path\to\AI_Employee_Vault"

# Check pending approvals
python approval_workflow.py pending \
  --vault "C:\path\to\AI_Employee_Vault"

# Process approved actions
python approval_workflow.py process \
  --vault "C:\path\to\AI_Employee_Vault"

# Get statistics
python approval_workflow.py stats \
  --vault "C:\path\to\AI_Employee_Vault"
```

**Dependencies:** None (pure Python)

---

### 7. Task Scheduler

**Location:** `.qwen/skills/task-scheduler/`

**Purpose:** Windows Task Scheduler integration for automating watchers and scheduled tasks

**Usage:**
```bash
cd .qwen/skills/task-scheduler/scripts

# Install all AI Employee tasks
python task_scheduler.py install-all \
  --vault "C:\path\to\AI_Employee_Vault" \
  --credentials "C:\path\to\client_secret.json"

# List all tasks
python task_scheduler.py list

# Check task status
python task_scheduler.py status --name "GmailWatcher"

# Run task manually
python task_scheduler.py run --name "GmailWatcher"

# Remove single task
python task_scheduler.py remove --name "GmailWatcher"

# Remove all tasks
python task_scheduler.py remove-all
```

**Pre-configured Tasks:**
- `GmailWatcher` - Starts at logon
- `LinkedInWatcher` - Starts at logon
- `Orchestrator` - Starts at logon
- `FileSystemWatcher` - Starts at logon
- `DailyBriefing` - Daily at 8:00 AM

**Dependencies:** None (pure Python, uses Windows schtasks API)

**Auto-restart:** Configured to restart on failure (every 1 minute, up to 3 times)

**Execution Limit:** 24 hours per task (prevents runaway processes)

---

## Vault Structure

```
AI_Employee_Vault/
├── Inbox/                    # Raw incoming files
├── Needs_Action/             # Pending tasks
├── Plans/                    # Task plans
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved actions
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

## Human-in-the-Loop Workflow

```
┌─────────────────┐
│  Action Needed  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create Approval │
│ Request File    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pending_Approval│ ← Human reviews here
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│ Approved│ │ Rejected │
└────┬────┘ └──────────┘
     │
     ▼
┌─────────┐
│ Execute │
│ Action  │
└────┬────┘
     │
     ▼
┌─────────┐
│  Done   │
└─────────┘
```

---

## Qwen Code Integration

### Process All Pending Items

```bash
qwen --prompt "Process all files in /Needs_Action" \
  --cwd "C:\path\to\AI_Employee_Vault"
```

### Create Plan for Complex Task

```bash
qwen --prompt "Create a plan for processing EMAIL_invoice_request.md" \
  --cwd "C:\path\to\AI_Employee_Vault"
```

### Generate LinkedIn Post

```bash
qwen --prompt "Create a LinkedIn post about our Q1 revenue growth from Business_Goals.md" \
  --cwd "C:\path\to\AI_Employee_Vault"
```

### Check Approved Actions

```bash
qwen --prompt "Check /Approved folder and process pending actions" \
  --cwd "C:\path\to\AI_Employee_Vault"
```

---

## Scheduling

### Windows Task Scheduler (Recommended)

Use the Task Scheduler skill to automatically install all tasks:

```bash
cd .qwen/skills/task-scheduler/scripts

# Install all AI Employee tasks
python task_scheduler.py install-all \
  --vault "C:\path\to\AI_Employee_Vault" \
  --credentials "C:\path\to\client_secret.json"

# List installed tasks
python task_scheduler.py list

# Check status of specific task
python task_scheduler.py status --name "GmailWatcher"
```

**Pre-configured Tasks:**

| Task | Trigger | Purpose |
|------|---------|---------|
| GmailWatcher | At log on | Monitor Gmail |
| LinkedInWatcher | At log on | Monitor LinkedIn |
| Orchestrator | At log on | Process pending items |
| FileSystemWatcher | At log on | Monitor drop folder |
| DailyBriefing | Daily 8 AM | Generate briefing |

**Features:**
- Auto-restart on failure (every 1 minute, up to 3 times)
- Execution time limit (24 hours max)
- Run with highest privileges
- Organized in AI_Employee task folder

### Manual Task Scheduler Setup

1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create folder: `AI_Employee`
3. Create basic task for each watcher
4. Configure:
   - Trigger: At log on
   - Action: Run Python script
   - Settings: Restart on failure, 24h limit

See `.qwen/skills/task-scheduler/references/windows-task-setup.md` for detailed guide.

### Linux/Mac (cron)

```bash
crontab -e

# Add entries
@reboot cd /path/to/Personal-AI-Employee && \
  python .qwen/skills/gmail-watcher/scripts/gmail_watcher.py ... &
@reboot cd /path/to/Personal-AI-Employee && \
  python .qwen/skills/linkedin-watcher/scripts/linkedin_watcher.py ... &
@reboot cd /path/to/Personal-AI-Employee && \
  python scripts/orchestrator.py ... &
0 8 * * * cd /path/to/Personal-AI-Employee && \
  python scripts/daily_briefing.py ...
```

---

## Troubleshooting

### Gmail Watcher Issues

| Issue | Solution |
|-------|----------|
| Authentication fails | Delete `token.json`, re-run watcher |
| No emails detected | Check Gmail API enabled, labels correct |
| API quota exceeded | Wait 24 hours or request increase |

### LinkedIn Watcher Issues

| Issue | Solution |
|-------|----------|
| Not logged in | Run with `--setup-session` |
| Session expired | Clear session folder, re-login |
| Browser won't open | Run `playwright install chromium` |

### Email MCP Issues

| Issue | Solution |
|-------|----------|
| Email not sent | Check Gmail API scopes include `.send` |
| Approval not working | Verify vault path is correct |

### LinkedIn Poster Issues

| Issue | Solution |
|-------|----------|
| Post fails | Check session is valid |
| Content rejected | Review LinkedIn community guidelines |
| Rate limited | Reduce posting frequency (max 2/day) |

---

## Security Best Practices

1. **Never commit credentials** - Add `.creds/` to `.gitignore`
2. **Use environment variables** for sensitive data
3. **Rotate OAuth credentials** monthly
4. **Enable 2FA** on all connected accounts
5. **Review approval files** before approving
6. **Audit logs regularly** in `Logs/` folder

---

## Company Handbook Integration

All skills respect rules in `Company_Handbook.md`:

| Rule | Behavior |
|------|----------|
| Known contacts | Auto-reply to routine emails |
| New contacts | Require approval before reply |
| LinkedIn posts | All require approval |
| Payments > $50 | Require approval |
| File deletions | Require approval |

---

## Next Steps (Gold Tier)

To upgrade to Gold Tier, add:

1. **Odoo ERP Integration** - Accounting via MCP
2. **Facebook/Instagram Integration** - Auto-posting
3. **Twitter (X) Integration** - Auto-posting
4. **Weekly CEO Briefing** - Autonomous audit
5. **Multiple MCP Servers** - Calendar, Slack, etc.
6. **Ralph Wiggum Loop** - Autonomous multi-step completion

---

## Skills Location Reference

All skills are installed in `.qwen/skills/` with self-contained scripts:

```
.qwen/skills/<skill-name>/
├── SKILL.md              # Skill documentation
├── scripts/
│   ├── <skill>.py        # Main script
│   └── base_watcher.py   # Base class (where needed)
└── references/
    └── <reference>.md    # Setup guides, templates
```

**Shared scripts** (orchestrator, file watcher) remain in `scripts/` folder at project root.

---

*Silver Tier v0.3 - For use with AI Employee Hackathon*
*Last updated: 2026-03-25*
