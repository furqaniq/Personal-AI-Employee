# Gmail API Setup Guide

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it (e.g., "AI Employee Gmail")
4. Click "Create"

## Step 2: Enable Gmail API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and press "Enable"

## Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: AI Employee
   - User support email: Your email
   - Developer contact: Your email
4. Application type: Desktop app
5. Name: AI Employee Gmail
6. Click "Create"
7. Download the `client_secret.json` file

## Step 4: Secure Your Credentials

```bash
# Move to secure location
mkdir "%USERPROFILE%\.creds\gmail"
move client_secret.json "%USERPROFILE%\.creds\gmail\"
```

## Step 5: First-Time Authentication

```bash
python scripts/gmail_watcher.py "C:\path\to\AI_Employee_Vault" "%USERPROFILE%\.creds\gmail\client_secret.json"
```

This will open a browser window for OAuth consent.

## Troubleshooting

### 403 Forbidden Error

- Ensure Gmail API is enabled
- Check OAuth consent screen is published
- Verify scopes include `gmail.readonly`

### Token Expired

```bash
# Delete old token
del "%USERPROFILE%\.creds\gmail\token.json"

# Re-authenticate
python scripts/gmail_watcher.py --authenticate
```

## API Quotas

| Limit | Value |
|-------|-------|
| Daily send limit | 500 emails |
| Read quota | 1,000,000 units/day |
| Rate limit | 250 requests/second |

---

*Reference: Gmail API Setup for Silver Tier*
