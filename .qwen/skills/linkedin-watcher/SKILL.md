---
name: linkedin-watcher
description: |
  Silver Tier LinkedIn Watcher skill for Qwen Code.
  Monitors LinkedIn for new notifications, connection requests,
  and messages using Playwright browser automation.
  
  Prerequisites:
  - LinkedIn account
  - Playwright installed (npm install -g @playwright/mcp)
  - Browser session folder for persistent login
  
  Use this skill when:
  - You need to monitor LinkedIn for new activity
  - You want to track connection requests and messages
  - You need LinkedIn notifications in your Obsidian vault
  
  ⚠️ WARNING: Respect LinkedIn's Terms of Service. Use responsibly.
---

# LinkedIn Watcher Skill

This skill enables Qwen Code to monitor LinkedIn activity using browser automation.

## Architecture

```
LinkedIn → Playwright Browser → LinkedIn Watcher (Python) → Needs_Action/ → Qwen Code
```

## Setup Instructions

### Step 1: Install Playwright

```bash
# Install Playwright MCP server
npm install -g @playwright/mcp

# Install browser binaries
playwright install chromium
```

### Step 2: Install Python Dependencies

```bash
pip install playwright
playwright install chromium
```

### Step 3: First-Time Login

Run the watcher once to set up your LinkedIn session:

```bash
python scripts/linkedin_watcher.py /path/to/vault --setup-session
```

This will:
1. Open a browser window
2. Navigate to LinkedIn
3. You log in manually
4. Session is saved for future runs

## Usage

### Start the Watcher

```bash
# Basic usage
python scripts/linkedin_watcher.py /path/to/vault

# With custom check interval (seconds)
python scripts/linkedin_watcher.py /path/to/vault --interval 300

# Headless mode (after session is set up)
python scripts/linkedin_watcher.py /path/to/vault --headless
```

### What It Monitors

1. **Connection Requests** - New pending connections
2. **Messages** - New LinkedIn messages
3. **Notifications** - Job alerts, post interactions
4. **Keywords** - Mentions of your specified keywords

## Action File Format

Each notification creates a file like:

```markdown
---
type: linkedin_notification
category: connection_request
from: John Doe
title: Senior Manager at Tech Corp
received: 2026-03-24T22:00:00Z
priority: medium
status: pending
---

# LinkedIn Connection Request

**From:** John Doe  
**Title:** Senior Manager at Tech Corp  
**Location:** San Francisco Bay Area  
**Received:** March 24, 2026

## Message

Hi, I'd like to join your professional network.

## Suggested Actions

- [ ] Review profile
- [ ] Accept connection
- [ ] Send welcome message
- [ ] Archive after processing
```

## Company Handbook Integration

The watcher respects rules in `Company_Handbook.md`:

| Rule | Behavior |
|------|----------|
| Connection from known company | Auto-accept candidate |
| Message with keywords | Flag for immediate attention |
| Job opportunity notification | Create follow-up task |
| Recruiter from target company | High priority |

## Qwen Code Integration

After the watcher creates action files, trigger Qwen:

```bash
# Process all LinkedIn notifications
qwen --prompt "Process all LinkedIn files in /Needs_Action" --cwd /path/to/vault
```

## Advanced Configuration

### Custom Keywords

Add keywords for priority flagging:

```python
KEYWORDS = ['hiring', 'opportunity', 'job', 'position', 'interview', 'role']
```

### Target Companies

Track notifications from specific companies:

```python
TARGET_COMPANIES = ['Google', 'Microsoft', 'Amazon', 'Meta']
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login required | Run with `--setup-session` flag |
| Session expired | Clear session folder, re-login |
| Browser won't open | Check Playwright installation |
| LinkedIn blocks requests | Increase check interval |

## Security Notes

- **Never share** your session folder
- Add session path to `.gitignore`
- Use reasonable check intervals (avoid rate limiting)
- Respect LinkedIn's Terms of Service

## File Structure

```
.qwen/skills/linkedin-watcher/
├── SKILL.md (this file)
├── scripts/
│   └── linkedin_watcher.py (linked from /scripts/)
└── references/
    └── playwright-setup.md
```

## Ethical Usage

⚠️ **Important**: This tool uses browser automation to access LinkedIn. Please:

1. **Use responsibly** - Don't spam or abuse the platform
2. **Respect rate limits** - Use reasonable check intervals (5+ minutes)
3. **Follow ToS** - Review LinkedIn's Terms of Service
4. **Personal use only** - Don't use for scraping or data harvesting

---

*Silver Tier Skill v0.1 - For use with AI Employee Hackathon*
