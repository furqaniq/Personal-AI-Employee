# Gmail OAuth Setup for Email MCP

## Overview

The Email MCP uses the same OAuth credentials as the Gmail Watcher. If you've already set up the Gmail Watcher, you can reuse those credentials.

## Quick Setup

### If Gmail Watcher is Already Configured

```bash
# Credentials should be at:
%USERPROFILE%\.creds\gmail\client_secret.json

# Run Email MCP authentication
python scripts/email_mcp.py --authenticate
```

### Fresh Setup

1. Follow the [Gmail API Setup Guide](../gmail-watcher/references/gmail-api-setup.md)
2. Download `client_secret.json`
3. Place in `%USERPROFILE%\.creds\gmail\`
4. Run authentication

## OAuth Scopes

The Email MCP requires these scopes:

```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',      # Send emails
    'https://www.googleapis.com/auth/gmail.readonly',  # Read emails
    'https://www.googleapis.com/auth/gmail.draft',     # Create drafts
    'https://www.googleapis.com/auth/gmail.modify'     # Modify labels
]
```

## Usage Examples

### Send Email to Known Contact

```bash
python scripts/email_mcp.py send \
  --to "client@known-domain.com" \
  --subject "Meeting Follow-up" \
  --body "Hi, Thanks for the meeting..."
```

### Create Approval Request (New Contact)

```bash
python scripts/email_mcp.py draft \
  --to "newcontact@example.com" \
  --subject "Project Proposal" \
  --body "Dear..., We would like to..." \
  --vault "C:\path\to\AI_Employee_Vault"
```

### Search Emails

```bash
python scripts/email_mcp.py search \
  --query "is:unread from:boss@company.com"
```

## Human-in-the-Loop Workflow

1. **Email MCP creates** approval file in `Pending_Approval/`
2. **Human reviews** the email content
3. **Move to** `Approved/` to send
4. **Email MCP sends** the email automatically
5. **File moved to** `Done/`

## Security Best Practices

| Practice | Implementation |
|----------|----------------|
| Credential storage | `%USERPROFILE%\.creds\gmail\` |
| Token storage | Same folder, auto-generated |
| Git ignore | Add `.creds/` to `.gitignore` |
| Rotation | Re-authenticate monthly |

## Troubleshooting

### Authentication Fails

```bash
# Delete token and re-authenticate
del "%USERPROFILE%\.creds\gmail\token.json"
python scripts/email_mcp.py --authenticate
```

### Send Fails with 403

- Check Gmail API is enabled
- Verify OAuth scopes include `gmail.send`
- Ensure account hasn't exceeded daily quota

---

*Reference: Gmail OAuth for Email MCP - Silver Tier*
