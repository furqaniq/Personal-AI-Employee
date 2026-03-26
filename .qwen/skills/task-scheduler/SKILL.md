---
name: task-scheduler
description: |
  Silver Tier Task Scheduler skill for Qwen Code.
  Manages Windows Task Scheduler integration for automating
  watcher scripts and scheduled AI Employee tasks.
  
  Prerequisites:
  - Windows 10/11
  - Python 3.13+ installed
  - All watcher scripts tested and working
  - Administrator access for task creation
  
  Use this skill when:
  - You need watchers to run automatically at startup
  - You want scheduled tasks (daily briefings, etc.)
  - You need automatic restart on failure
  - You want centralized task management
  
  This skill implements the basic scheduling requirement for Silver Tier.
---

# Task Scheduler Skill

This skill enables automated scheduling of AI Employee tasks on Windows.

## Architecture

```
Windows Task Scheduler
        ↓
    Triggers
        ↓
┌───────┴───────┬───────────────┬───────────────┐
│               │               │               │
▼               ▼               ▼               ▼
Gmail        LinkedIn      Orchestrator   Custom Tasks
Watcher      Watcher
```

## Quick Start

### 1. Install All Watchers

```bash
# Verify all scripts work manually first
cd .qwen/skills/gmail-watcher/scripts
python gmail_watcher.py "C:\path\to\vault" "C:\path\to\client_secret.json"
```

### 2. Create Scheduled Tasks

```bash
cd .qwen/skills/task-scheduler/scripts

# Create all tasks
python task_scheduler.py install-all --vault "C:\path\to\vault"

# Or create individual tasks
python task_scheduler.py create --name "GmailWatcher" --script "gmail_watcher.py"
```

### 3. Verify Tasks

```bash
# List all AI Employee tasks
python task_scheduler.py list

# Check task status
python task_scheduler.py status --name "GmailWatcher"
```

## Usage

### Create Single Task

```bash
python task_scheduler.py create \
  --name "GmailWatcher" \
  --script "gmail_watcher.py" \
  --skill "gmail-watcher" \
  --trigger "atlogon" \
  --vault "C:\path\to\vault" \
  --credentials "C:\path\to\client_secret.json"
```

### Create All Watcher Tasks

```bash
python task_scheduler.py install-all \
  --vault "C:\path\to\vault" \
  --credentials "C:\path\to\client_secret.json"
```

### Remove Tasks

```bash
# Remove single task
python task_scheduler.py remove --name "GmailWatcher"

# Remove all AI Employee tasks
python task_scheduler.py remove-all
```

### Export Task Configuration

```bash
python task_scheduler.py export \
  --name "GmailWatcher" \
  --output "GmailWatcher.xml"
```

### Import Task Configuration

```bash
python task_scheduler.py import \
  --file "GmailWatcher.xml"
```

## Trigger Types

| Trigger | Description | Example |
|---------|-------------|---------|
| `atlogon` | When user logs on | Start watchers at startup |
| `atstartup` | When system starts | Background services |
| `daily` | Every day at specific time | Daily briefing at 8 AM |
| `weekly` | Specific day every week | Weekly review on Monday |
| `idle` | When system is idle | Background processing |

## Pre-configured Tasks

### Gmail Watcher Task

- **Trigger:** At log on
- **Action:** Run gmail_watcher.py
- **Restart:** On failure (every 1 minute, up to 3 times)
- **Stop:** If running longer than 24 hours

### LinkedIn Watcher Task

- **Trigger:** At log on
- **Action:** Run linkedin_watcher.py
- **Restart:** On failure (every 1 minute, up to 3 times)
- **Stop:** If running longer than 24 hours

### Orchestrator Task

- **Trigger:** At log on
- **Action:** Run orchestrator.py
- **Restart:** On failure (every 1 minute, up to 3 times)
- **Stop:** If running longer than 24 hours

### Daily Briefing Task

- **Trigger:** Daily at 8:00 AM
- **Action:** Run daily_briefing.py
- **Restart:** On failure (every 15 minutes, up to 2 times)

## Task Configuration

### Basic Settings

```json
{
  "name": "GmailWatcher",
  "description": "Monitor Gmail for new emails",
  "trigger": "atlogon",
  "script": "gmail_watcher.py",
  "skill": "gmail-watcher",
  "arguments": ["--vault", "--credentials"],
  "restart_on_failure": true,
  "restart_interval": 60,
  "restart_count": 3,
  "stop_if_running": 86400
}
```

### Advanced Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `allow_demand_start` | true | Can start manually |
| `stop_on_idle_end` | false | Continue if user logs off |
| `execution_time_limit` | 24 hours | Max run time |
| `priority` | 7 | Task priority (1-10) |
| `multiple_instances` | stop_new | Handle multiple instances |

## Qwen Code Integration

### Create Task via Qwen

```bash
qwen --prompt "Create a scheduled task for Gmail Watcher to run at startup" \
  --cwd "C:\path\to\vault"
```

### Check Task Status

```bash
qwen --prompt "Check if all AI Employee tasks are running" \
  --cwd "C:\path\to\vault"
```

### Generate Task Report

```bash
qwen --prompt "Generate a report of all scheduled tasks and their status" \
  --cwd "C:\path\to\vault"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task won't start | Check "Run with highest privileges" |
| Python not found | Use full path to python.exe |
| Script not found | Use full path to script |
| Task fails immediately | Check credentials and vault path |
| Multiple instances | Set "Do not start new instance" |

## Security Notes

- **Run as your user account** - Not SYSTEM or Admin unless needed
- **Store credentials securely** - Use encrypted credentials
- **Limit task permissions** - Only what's necessary
- **Audit task execution** - Check history regularly

## File Structure

```
.qwen/skills/task-scheduler/
├── SKILL.md (this file)
├── scripts/
│   ├── task_scheduler.py
│   └── templates/
│       └── task_template.xml
└── references/
    ├── windows-task-setup.md
    └── troubleshooting-guide.md
```

---

*Silver Tier Skill v0.1 - For use with AI Employee Hackathon*
