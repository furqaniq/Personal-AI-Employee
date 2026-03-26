#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Gmail Authentication - Opens browser automatically
Run this script to authenticate with Gmail API
Auto-installs required packages if missing
"""

import sys
import os
import subprocess
from pathlib import Path

# Try to import Gmail API, install if missing
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("=" * 70)
    print("INSTALLING GMAIL API PACKAGES...")
    print("=" * 70)
    print()
    
    # Install packages using python -m pip (works even if pip not in PATH)
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "google-api-python-client", 
                          "google-auth-httplib2", 
                          "google-auth-oauthlib",
                          "--quiet"])
    
    print()
    print("✓ Packages installed!")
    print()
    
    # Try importing again
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

# Configuration
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = Path.home() / 'AppData' / 'Local' / 'AI_Employee' / 'creds' / 'gmail' / 'client_secret.json'
TOKEN_FILE = Path.home() / 'AppData' / 'Local' / 'AI_Employee' / 'creds' / 'gmail' / 'token.json'

print("=" * 70)
print("GMAIL AUTHENTICATION")
print("=" * 70)
print()

# Check credentials file exists
if not CREDENTIALS_FILE.exists():
    print(f"ERROR: Credentials file not found at:")
    print(f"  {CREDENTIALS_FILE}")
    print()
    print("Please run AUTHENTICATE-GMAIL.bat instead!")
    input("Press Enter to exit...")
    sys.exit(1)

print("✓ Credentials file found")
print()

# Check if token already exists
if TOKEN_FILE.exists():
    print("⚠ Token already exists!")
    print()
    response = input("Delete existing token and re-authenticate? (y/n): ").strip().lower()
    if response != 'y':
        print("Authentication cancelled.")
        input("Press Enter to exit...")
        sys.exit(0)
    
    try:
        TOKEN_FILE.unlink()
        print("✓ Old token deleted")
    except:
        print("✗ Could not delete old token")
        input("Press Enter to exit...")
        sys.exit(1)

print()
print("=" * 70)
print("OPENING BROWSER FOR AUTHENTICATION")
print("=" * 70)
print()
print("INSTRUCTIONS:")
print("  1. Browser will open with Google sign-in")
print("  2. Sign in with your Gmail account")
print("  3. Click 'Advanced' then 'Go to hackathon-0-fte-491317 (unsafe)'")
print("  4. Click 'Allow' to grant permissions")
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
    print("🌐 Browser opened - please complete sign-in...")
    print()
    
    creds = flow.run_local_server(
        host='localhost',
        port=8080,
        open_browser=True,
        bind_addr='127.0.0.1'
    )
    
    print()
    print("=" * 70)
    print("✅ AUTHENTICATION SUCCESSFUL!")
    print("=" * 70)
    print()
    print(f"✓ Token saved to: {TOKEN_FILE}")
    print()
    print("You can now use Gmail Watcher!")
    print()
    print("To start monitoring Gmail, run:")
    vault_path = Path.home().parent.parent / "OneDrive" / "Documents" / "GitHub" / "Personal-AI-Employee" / "AI_Employee_Vault"
    print(f'  python gmail_watcher.py "{vault_path}" "{CREDENTIALS_FILE}"')
    print()
    
    # Keep window open so user can see success message
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
