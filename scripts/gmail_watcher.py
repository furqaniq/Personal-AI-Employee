#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Gmail Watcher - Monitors Gmail for new emails and creates action files.

Silver Tier implementation for AI Employee Hackathon.

Usage:
    python gmail_watcher.py /path/to/vault /path/to/client_secret.json

Example:
    python gmail_watcher.py "C:/Users/.../AI_Employee_Vault" "C:/Users/.../client_secret.json"
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import base64
from email import message_from_bytes

# Google API imports
try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import flow
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Google API libraries not installed.")
    print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

# Import base class
from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Priority keywords
PRIORITY_KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency', 'important']


class GmailWatcher(BaseWatcher):
    """
    Gmail Watcher using Google Gmail API.
    
    Monitors Gmail for new, unread, important emails and creates
    action files in the Obsidian vault Needs_Action folder.
    """

    def __init__(self, vault_path: str, credentials_path: str, check_interval: int = 60):
        """
        Initialize the Gmail Watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            credentials_path: Path to OAuth credentials JSON file
            check_interval: Seconds between checks (default: 60)
        """
        super().__init__(vault_path, check_interval)
        
        self.credentials_path = Path(credentials_path)
        self.token_path = self.vault_path / '.creds' / 'gmail_token.json'
        
        # Ensure credentials folder exists
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Gmail API service
        self.service = None
        
        # Track processed message IDs (persisted across sessions)
        self.processed_ids_file = self.vault_path / '.creds' / 'gmail_processed.json'
        self.processed_ids = self._load_processed_ids()
        
        # Authenticate
        self._authenticate()

    def _load_processed_ids(self) -> set:
        """Load previously processed message IDs."""
        if self.processed_ids_file.exists():
            import json
            try:
                data = json.loads(self.processed_ids_file.read_text(encoding='utf-8'))
                return set(data.get('processed_ids', []))
            except:
                pass
        return set()

    def _save_processed_ids(self):
        """Save processed message IDs to disk."""
        import json
        # Keep only last 1000 IDs to prevent unbounded growth
        ids_list = list(self.processed_ids)[-1000:]
        self.processed_ids_file.write_text(
            json.dumps({'processed_ids': ids_list, 'updated': datetime.now().isoformat()}, indent=2),
            encoding='utf-8'
        )

    def _authenticate(self):
        """Authenticate with Gmail API."""
        creds = None
        
        # Load existing token
        if self.token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                self.logger.warning(f'Failed to load token: {e}')
                creds = None
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    self.logger.warning(f'Token refresh failed: {e}')
                    creds = None
            
            if not creds:
                self.logger.info('Starting OAuth flow...')
                try:
                    app_flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES
                    )
                    creds = app_flow.run_local_server(host='localhost', port=8080)
                    
                    # Save credentials
                    self.token_path.write_text(creds.to_json(), encoding='utf-8')
                    self.logger.info('Authentication successful!')
                except Exception as e:
                    self.logger.error(f'Authentication failed: {e}')
                    sys.exit(1)
        
        # Build Gmail API service
        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info('Gmail API service initialized')

    def check_for_updates(self) -> List[Dict]:
        """
        Check for new unread, important emails.
        
        Returns:
            List of message dictionaries
        """
        if not self.service:
            return []
        
        try:
            # Query: unread + important
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()
            
            messages = results.get('messages', [])
            
            # Filter out already processed
            new_messages = []
            for msg in messages:
                if msg['id'] not in self.processed_ids:
                    new_messages.append(msg)
            
            if new_messages:
                self.logger.info(f'Found {len(new_messages)} new email(s)')
            
            return new_messages
            
        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            # Try to re-authenticate on auth errors
            if error.resp.status in [401, 403]:
                self._authenticate()
            return []
        except Exception as e:
            self.logger.error(f'Error checking Gmail: {e}')
            return []

    def create_action_file(self, message: Dict) -> Path:
        """
        Create an action file for the email.
        
        Args:
            message: Gmail message dictionary
            
        Returns:
            Path to created action file
        """
        # Get full message details
        msg = self.service.users().messages().get(
            userId='me',
            id=message['id'],
            format='full'
        ).execute()
        
        # Extract headers
        headers = msg.get('payload', {}).get('headers', [])
        header_dict = {h['name']: h['value'] for h in headers}
        
        from_addr = header_dict.get('From', 'Unknown')
        to_addr = header_dict.get('To', '')
        subject = header_dict.get('Subject', 'No Subject')
        date = header_dict.get('Date', '')
        
        # Get email body
        body = self._extract_body(msg)
        
        # Determine priority
        priority = self._determine_priority(subject, body, from_addr)
        
        # Create timestamp
        timestamp = datetime.now().isoformat()
        
        # Sanitize filename
        safe_subject = self._sanitize_filename(subject[:50])
        file_id = f"{safe_subject}_{message['id']}"
        
        # Build action file content
        content = f"""---
type: email
from: {from_addr}
to: {to_addr}
subject: {subject}
received: {timestamp}
date: {date}
priority: {priority}
status: pending
gmail_id: {message['id']}
---

# Email Received

**From:** {from_addr}  
**To:** {to_addr}  
**Subject:** {subject}  
**Date:** {date}  
**Received:** {timestamp}

## Content

{body}

## Suggested Actions

- [ ] Read and understand email content
- [ ] Determine required response
- [ ] Reply to sender (if appropriate)
- [ ] Forward to relevant party (if needed)
- [ ] Archive after processing

## Notes

*This file was automatically created by Gmail Watcher*
*Original Gmail ID: {message['id']}*
"""
        
        # Write action file
        filepath = self.needs_action / f'EMAIL_{file_id}.md'
        filepath.write_text(content, encoding='utf-8')
        
        # Mark as processed
        self.processed_ids.add(message['id'])
        self._save_processed_ids()
        
        self.logger.info(f'Action file created: {filepath.name}')
        return filepath

    def _extract_body(self, msg: Dict) -> str:
        """Extract plain text body from Gmail message."""
        def get_payload(msg):
            payload = msg.get('payload', {})
            parts = payload.get('parts', [])
            
            if parts:
                for part in parts:
                    mime_type = part.get('mimeType', '')
                    if mime_type == 'text/plain':
                        data = part.get('body', {}).get('data', '')
                        if data:
                            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    elif mime_type == 'multipart/alternative':
                        return get_payload(part)
                # Fallback to first part
                if parts:
                    data = parts[0].get('body', {}).get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            else:
                # No parts, check body directly
                data = payload.get('body', {}).get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            
            return '[No text content available]'
        
        body = get_payload(msg)
        
        # Truncate if too long
        if len(body) > 5000:
            body = body[:5000] + '\n\n... [Content truncated, view in Gmail for full message]'
        
        return body

    def _determine_priority(self, subject: str, body: str, from_addr: str) -> str:
        """Determine email priority based on content."""
        text = (subject + ' ' + body).lower()
        
        # Check for priority keywords
        for keyword in PRIORITY_KEYWORDS:
            if keyword in text:
                return 'high'
        
        # Check if from known contact (you can extend this)
        known_domains = ['client.com', 'partner.com']  # Add your known contacts
        for domain in known_domains:
            if domain in from_addr.lower():
                return 'medium'
        
        return 'medium'

    def run(self):
        """Run the Gmail watcher."""
        self.logger.info('=' * 60)
        self.logger.info('Gmail Watcher - Silver Tier')
        self.logger.info('=' * 60)
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        self.logger.info('Press Ctrl+C to stop')
        self.logger.info('=' * 60)

        try:
            while True:
                items = self.check_for_updates()
                
                for item in items:
                    self.create_action_file(item)
                
                # Wait for next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Gmail Watcher stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("=" * 60)
        print("Gmail Watcher - AI Employee Silver Tier")
        print("=" * 60)
        print()
        print("Usage:")
        print("  python gmail_watcher.py <vault_path> <credentials_path> [interval]")
        print()
        print("Arguments:")
        print("  vault_path       - Path to your Obsidian vault")
        print("  credentials_path - Path to OAuth client_secret.json")
        print("  interval         - Check interval in seconds (default: 60)")
        print()
        print("First-time setup:")
        print("  1. Enable Gmail API in Google Cloud Console")
        print("  2. Create OAuth 2.0 credentials")
        print("  3. Download client_secret.json")
        print("  4. Run watcher - it will open browser for authentication")
        print()
        sys.exit(1)

    vault_path = sys.argv[1]
    credentials_path = sys.argv[2]
    check_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 60

    # Validate paths
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)

    if not Path(credentials_path).exists():
        print(f"Error: Credentials file not found: {credentials_path}")
        sys.exit(1)

    watcher = GmailWatcher(vault_path, credentials_path, check_interval)
    watcher.run()
