---
name: email-mcp
description: |
  Silver Tier Email MCP skill for Qwen Code.
  Send, draft, and manage emails via Gmail API.
  
  Prerequisites:
  - Google Cloud Project with Gmail API enabled
  - OAuth 2.0 credentials (same as Gmail Watcher)
  - Python 3.13+ with google-api-python-client
  
  Use this skill when:
  - You need to send emails from your AI Employee
  - You want to draft emails for human approval
  - You need to search or organize Gmail
  
  ⚠️ Human-in-the-Loop: All emails to new contacts require approval.
---

# Email MCP Skill

This skill enables Qwen Code to send and manage emails via Gmail API.

## Architecture

```
Qwen Code → Email MCP → Gmail API → Send/Draft Email
                ↓
        Pending_Approval/ (for HITL)
```

## Setup Instructions

### Step 1: Enable Gmail API

Same credentials as Gmail Watcher:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Gmail API
3. Create OAuth 2.0 credentials
4. Download `client_secret.json`

### Step 2: Install Dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 3: First-Time Authentication

```bash
python email_mcp.py --authenticate
```

## Usage

### Send Email (Direct)

```bash
python email_mcp.py send \
  --to "recipient@example.com" \
  --subject "Meeting Follow-up" \
  --body "Hi, Thanks for the meeting today..."
```

### Draft Email (for approval)

```bash
python email_mcp.py draft \
  --to "recipient@example.com" \
  --subject "Invoice #123" \
  --body "Please find attached..." \
  --vault "/path/to/vault"
```

### Search Emails

```bash
python email_mcp.py search \
  --query "from:boss@company.com is:unread"
```

## Human-in-the-Loop Pattern

For sensitive actions, the MCP creates an approval request:

```markdown
---
type: approval_request
action: send_email
to: newcontact@example.com
subject: Project Proposal
created: 2026-03-24T22:30:00Z
status: pending
---

# Email Approval Required

**To:** newcontact@example.com  
**Subject:** Project Proposal

## Content

Dear...,

[Email body]

## Why Approval is Needed

- Recipient is not in known contacts list
- First-time communication

## To Approve

Move this file to `/Approved` folder.

## To Reject

Move to `/Rejected` with reason.
```

## Qwen Code Integration

### Send Routine Email

```bash
qwen --prompt "Send a reply to john@example.com thanking him for the meeting" \
  --cwd /path/to/vault
```

### Draft for Approval

```bash
qwen --prompt "Draft an email to new client with project proposal" \
  --cwd /path/to/vault
```

## Email Templates

### Reply Template

```markdown
**To:** {{to}}
**Subject:** Re: {{original_subject}}

Hi {{name}},

Thank you for your email. [Your response here]

Best regards,
[Your name]
```

### Invoice Template

```markdown
**To:** {{to}}
**Subject:** Invoice #{{number}} - {{amount}}

Hi {{name}},

Please find attached invoice #{{number}} for {{amount}}.

Payment is due within {{days}} days.

Best regards,
[Your name]
```

## Company Handbook Rules

| Rule | Behavior |
|------|----------|
| Known contacts | Auto-send routine emails |
| New contacts | Require approval |
| Attachments | Require approval |
| Bulk sends (>5) | Require approval |
| Payments/Contracts | Always require approval |

## API Reference

### send_email(to, subject, body, attachments=[])

Send an email immediately.

### draft_email(to, subject, body, vault_path)

Create approval request file in vault.

### search_emails(query, max_results=10)

Search Gmail and return results.

### mark_read(message_id)

Mark email as read.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication fails | Re-run `--authenticate` |
| Email not sent | Check Gmail API quota |
| Approval not working | Verify vault path |

## Security Notes

- **Never commit** credentials to git
- Store `client_secret.json` securely
- Use environment variables for sensitive data
- Rotate credentials periodically

---

*Silver Tier Skill v0.1 - For use with AI Employee Hackathon*
