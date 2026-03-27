#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Authenticate Gmail for Sending Emails

This script authenticates with Gmail API with FULL permissions including:
- gmail.send - Send emails
- gmail.readonly - Read emails
- gmail.modify - Modify email labels

Run this script to re-authenticate with send permissions.
"""

import sys
import os
from pathlib import Path

# Google API imports
try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("ERROR: Google API packages not installed!")
    print("Run: python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    input("Press Enter to exit...")
    sys.exit(1)

# Configuration - FULL PERMISSIONS for sending emails
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',      # Send emails
    'https://www.googleapis.com/auth/gmail.readonly',  # Read emails
    'https://www.googleapis.com/auth/gmail.modify',    # Modify labels
]

# Paths
CREDENTIALS_FILE = Path.home() / 'AppData' / 'Local' / 'AI_Employee' / 'creds' / 'gmail' / 'client_secret.json'
TOKEN_FILE = Path.home() / 'AppData' / 'Local' / 'AI_Employee' / 'creds' / 'gmail' / 'token.json'

print("=" * 70)
print("GMAIL AUTHENTICATION FOR EMAIL SENDING")
print("=" * 70)
print()

# Check credentials file exists
if not CREDENTIALS_FILE.exists():
    print(f"ERROR: Credentials file not found at:")
    print(f"  {CREDENTIALS_FILE}")
    print()
    print("Please run AUTHENTICATE-GMAIL.bat first!")
    input("Press Enter to exit...")
    sys.exit(1)

print("✓ Credentials file found")
print()

# Delete old token if exists (to force re-authentication with new scopes)
if TOKEN_FILE.exists():
    print("⚠ Found existing token with read-only permissions")
    print()
    response = input("Delete old token and re-authenticate with SEND permissions? (y/n): ").strip().lower()
    if response == 'y':
        try:
            TOKEN_FILE.unlink()
            print("✓ Old token deleted")
        except Exception as e:
            print(f"✗ Could not delete old token: {e}")
            input("Press Enter to exit...")
            sys.exit(1)
    else:
        print("Authentication cancelled.")
        input("Press Enter to exit...")
        sys.exit(0)

print()
print("=" * 70)
print("OPENING BROWSER FOR AUTHENTICATION")
print("=" * 70)
print()
print("PERMISSIONS REQUESTED:")
print("  ✓ Send emails (gmail.send)")
print("  ✓ Read emails (gmail.readonly)")
print("  ✓ Modify labels (gmail.modify)")
print()
print("INSTRUCTIONS:")
print("  1. Browser will open with Google sign-in")
print("  2. Sign in with your Gmail account")
print("  3. Click 'Advanced' then 'Go to hackathon-0-fte-491317 (unsafe)'")
print("  4. Click 'Allow' to grant ALL permissions")
print("  5. Come back here when you see 'Authentication successful'")
print()
print("=" * 70)
print()
print("Opening browser in 3 seconds...")
print()

# Start the OAuth flow
try:
    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        SCOPES
    )
    
    # This will open the browser automatically
    creds = flow.run_local_server(
        host='localhost',
        port=8081,
        open_browser=True,
        bind_addr='127.0.0.1'
    )
    
    # Save token
    TOKEN_FILE.write_text(creds.to_json(), encoding='utf-8')
    
    print()
    print("=" * 70)
    print("✅ AUTHENTICATION SUCCESSFUL!")
    print("=" * 70)
    print()
    print(f"✓ Token saved to: {TOKEN_FILE}")
    print()
    print("PERMISSIONS GRANTED:")
    print("  ✓ Send emails via Gmail API")
    print("  ✓ Read emails from Gmail")
    print("  ✓ Modify email labels")
    print()
    print("You can now:")
    print("  1. Run orchestrator.py to auto-send approved emails")
    print("  2. Move APPROVAL_*.md files to Approved/ folder")
    print("  3. Emails will be sent automatically via Email MCP")
    print()
    print("=" * 70)
    print()
    
    input("Press Enter to exit...")
    
except Exception as e:
    print()
    print("=" * 70)
    print("❌ AUTHENTICATION FAILED")
    print("=" * 70)
    print()
    print(f"Error: {e}")
    print()
    print("Troubleshooting:")
    print("  1. Check your internet connection")
    print("  2. Make sure credentials.json is valid")
    print("  3. Try running as Administrator")
    print()
    input("Press Enter to exit...")
    sys.exit(1)
