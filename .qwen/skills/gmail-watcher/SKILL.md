---
name: gmail-watcher
description: |
  Silver Tier Gmail Watcher skill for Qwen Code.
  Monitors Gmail for new, unread, important emails and creates
  action files in the Obsidian vault Needs_Action folder.
  
  Prerequisites:
  - Google Cloud Project with Gmail API enabled
  - OAuth 2.0 credentials (client_secret.json)
  - Python 3.13+ with google-api-python-client
  
  Use this skill when:
  - You need to monitor Gmail for new emails
  - You want to auto-triage incoming messages
  - You need email notifications in your Obsidian vault
---

# Gmail Watcher Skill

This skill enables Qwen Code to monitor Gmail and create action files for new emails.

## Architecture

```
Gmail API → Gmail Watcher (Python) → Needs_Action/ → Qwen Code → Action
```

## Setup Instructions

### Step 1: Enable Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API: `APIs & Services > Library > Gmail API > Enable`
4. Go to `APIs & Services > Credentials`
5. Click `Create Credentials > OAuth client ID`
6. Download `client_secret.json`

### Step 2: Install Dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 3: First-Time Authentication

Run the watcher once to authenticate:

```bash
python scripts/gmail_watcher.py --authenticate
```

This will open a browser window for OAuth consent.

## Usage

### Start the Watcher

```bash
# Basic usage
python scripts/gmail_watcher.py /path/to/vault /path/to/client_secret.json

# With custom check interval (seconds)
python scripts/gmail_watcher.py /path/to/vault /path/to/client_secret.json --interval 60
```

### What It Does

1. **Monitors Gmail** every 60 seconds (configurable)
2. **Filters emails**: Unread + Important only
3. **Creates action files** in `Needs_Action/` folder
4. **Tracks processed emails** to avoid duplicates

## Action File Format

Each email creates a file like:

```markdown
---
type: email
from: John Doe <john@example.com>
subject: Invoice Request
received: 2026-03-24T21:30:00Z
priority: high
status: pending
gmail_id: 18e4a1b2c3d4e5f6
---

# Email Content

**From:** John Doe <john@example.com>
**To:** you@yourdomain.com
**Subject:** Invoice Request
**Date:** March 24, 2026 at 9:30 PM

## Body

Hi,

Could you please send me the invoice for last month's services?

Thanks,
John

## Suggested Actions

- [ ] Reply to sender
- [ ] Forward to accounting
- [ ] Archive after processing
```

## Company Handbook Integration

The watcher respects rules in `Company_Handbook.md`:

| Rule | Behavior |
|------|----------|
| Known contacts | Auto-categorize as routine |
| Keywords: urgent, asap | Mark as high priority |
| Keywords: invoice, payment | Flag for immediate attention |
| New contacts | Require approval before reply |

## Qwen Code Integration

After the watcher creates action files, trigger Qwen:

```bash
# Process all pending emails
qwen --prompt "Process all files in /Needs_Action" --cwd /path/to/vault
```

## Advanced Configuration

### Custom Filters

Edit `scripts/gmail_watcher.py` to customize the Gmail query:

```python
# Default: unread + important
query = 'is:unread is:important'

# All unread emails
query = 'is:unread'

# From specific sender
query = 'is:unread from:boss@company.com'

# With specific label
query = 'is:unread label:Work'
```

### Keyword Alerts

Add custom keywords for priority flagging:

```python
PRIORITY_KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency']
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication fails | Re-run `--authenticate` flag |
| No emails detected | Check Gmail labels, ensure API is enabled |
| Duplicate action files | Check `processed_ids` set in watcher |
| Token expired | Delete `token.json`, re-authenticate |

## Security Notes

- **Never commit** `client_secret.json` or `token.json` to git
- Add to `.gitignore` immediately
- Store credentials in secure location
- Rotate OAuth credentials periodically

## File Structure

```
.qwen/skills/gmail-watcher/
├── SKILL.md (this file)
├── scripts/
│   └── gmail_watcher.py (linked from /scripts/)
└── references/
    └── gmail-api-setup.md
```

---

*Silver Tier Skill v0.1 - For use with AI Employee Hackathon*
