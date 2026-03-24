# AI Employee - Bronze Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

This is the **Bronze Tier** implementation of the Personal AI Employee Hackathon. It provides the foundational layer for an autonomous AI agent that processes files and tasks using Claude Code and Obsidian.

## What You Get

✅ **Obsidian Vault** with Dashboard.md and Company_Handbook.md
✅ **File System Watcher** - Monitors a drop folder for new files
✅ **Orchestrator** - Triggers Claude Code to process pending items
✅ **Agent Skill** - File processing skill for Claude Code
✅ **Basic folder structure** - /Inbox, /Needs_Action, /Done, /Plans, /Pending_Approval

## Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| [Claude Code](https://claude.com/product/claude-code) | Active subscription | Primary reasoning engine |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ (free) | Knowledge base & dashboard |
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts & orchestration |
| [Node.js](https://nodejs.org/) | v24+ LTS | Future MCP servers |

## Quick Start

### 1. Install Python Dependencies

```bash
pip install watchdog
```

### 2. Set Up Your Vault

The vault is already created at `AI_Employee_Vault/`. Open it in Obsidian:

```bash
# Open Obsidian and load the vault
# File → Open Folder → Select AI_Employee_Vault
```

### 3. Start the File System Watcher

```bash
cd scripts
python filesystem_watcher.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

### 4. Start the Orchestrator (in a new terminal)

```bash
cd scripts
python orchestrator.py "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

### 5. Test the System

1. Drop any file into the `Inbox/` folder
2. Watcher will create an action file in `Needs_Action/`
3. Orchestrator triggers Claude Code
4. Claude processes the file and moves it to `Done/`

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Employee - Bronze Tier                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Perception: File System Watcher                             │
│    • Monitors Inbox/ for new files                          │
│    • Creates action files in Needs_Action/                  │
│                                                              │
│  Reasoning: Claude Code                                      │
│    • Reads Company_Handbook.md for rules                    │
│    • Processes action files                                 │
│    • Creates plans for complex tasks                        │
│    • Requests approval for sensitive actions                │
│                                                              │
│  Memory: Obsidian Vault                                      │
│    • Dashboard.md - Real-time status                        │
│    • Company_Handbook.md - Rules of engagement              │
│    • /Needs_Action - Pending tasks                          │
│    • /Done - Completed tasks                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Folder Structure

```
AI_Employee_Vault/
├── Dashboard.md           # Real-time status dashboard
├── Company_Handbook.md    # Rules and guidelines
├── Inbox/                 # Drop folder for new files
├── Needs_Action/          # Pending tasks (created by watcher)
├── Done/                  # Completed tasks
├── Plans/                 # Task plans (created by Claude)
├── Pending_Approval/      # Awaiting human approval
├── Approved/              # Approved actions ready to execute
├── Rejected/              # Rejected actions
├── Logs/                  # Activity logs
├── Briefings/             # CEO briefings (future)
├── Invoices/              # Generated invoices (future)
└── Accounting/            # Financial records (future)
```

## Usage Examples

### Process a Dropped File

1. Save any file (PDF, TXT, DOCX) to `Inbox/`
2. Watcher automatically creates action file in `Needs_Action/`
3. Orchestrator triggers Claude Code
4. Claude reads and processes the file
5. File moves to `Done/` when complete

### Manual Processing

```bash
# Trigger Qwen manually
qwen --prompt "Process all files in Needs_Action" \
  --cwd "C:\Users\...\AI_Employee_Vault"
```

### Check System Status

```bash
# View dashboard
cat AI_Employee_Vault/Dashboard.md

# View pending items
ls AI_Employee_Vault/Needs_Action/

# View logs
cat AI_Employee_Vault/Logs/2026-03-24.json
```

## Scripts Reference

### filesystem_watcher.py

Monitors a folder for new files and creates action files.

```bash
python filesystem_watcher.py <vault_path> [drop_folder]
```

### orchestrator.py

Triggers Claude Code and manages workflow.

```bash
python orchestrator.py <vault_path> [check_interval]
```

### base_watcher.py

Base class for building custom watchers.

```bash
python base_watcher.py <vault_path> [drop_folder]
```

## Approval Workflow

For sensitive actions, Claude creates an approval request:

1. Claude creates file in `Pending_Approval/`
2. You review the file
3. Move to `Approved/` to proceed
4. Move to `Rejected/` to cancel

Example approval file:

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

## Troubleshooting

### Claude Code not found

```bash
# Install Qwen Code (if using Qwen)
npm install -g qwen

# Verify installation
qwen --version
```

### Watcher not detecting files

```bash
# Check if watchdog is installed
pip install watchdog

# Verify folder permissions
# Ensure the script has read/write access to the vault
```

### Orchestrator not triggering Qwen

The Bronze tier creates state files in `Plans/` for Qwen to process. Run Qwen manually:

```bash
qwen --prompt "Check Plans/ folder for new tasks" --cwd <vault_path>
```

## Next Steps (Silver Tier)

After mastering Bronze, add:

- [ ] Gmail Watcher
- [ ] WhatsApp Watcher  
- [ ] MCP Server for email sending
- [ ] Human-in-the-loop approval workflow
- [ ] Scheduled tasks via cron/Task Scheduler

## Security Notes

- **Never** store credentials in the vault
- Use environment variables for API keys
- Keep `.env` files in `.gitignore`
- Review all approval requests carefully

## Hackathon Submission

This Bronze Tier implementation includes:

- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script (File System)
- ✅ Claude Code integration for reading/writing to vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ Agent Skill for file processing

---

*Built for Personal AI Employee Hackathon 0 - Building Autonomous FTEs in 2026*
