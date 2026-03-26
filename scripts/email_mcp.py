#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Email MCP - Send and manage emails via Gmail API.

Silver Tier implementation for AI Employee Hackathon.

Usage:
    python email_mcp.py send --to "recipient@example.com" --subject "Subject" --body "Body"
    python email_mcp.py draft --to "recipient@example.com" --subject "Subject" --body "Body" --vault "/path/to/vault"
    python email_mcp.py search --query "from:boss@company.com"
"""

import os
import sys
import base64
import logging
import argparse
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Google API imports
try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Google API libraries not installed.")
    print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.draft',
          'https://www.googleapis.com/auth/gmail.modify']

# Known contacts (add your known contacts here)
KNOWN_CONTACTS = ['client.com', 'partner.com', 'yourcompany.com']


class EmailMCP:
    """
    Email MCP for sending and managing emails via Gmail API.
    """

    def __init__(self, credentials_path: str = None, vault_path: str = None):
        """
        Initialize Email MCP.
        
        Args:
            credentials_path: Path to OAuth credentials JSON file
            vault_path: Path to Obsidian vault (for approval workflow)
        """
        self.logger = logging.getLogger('EmailMCP')
        
        # Find credentials
        if credentials_path:
            self.credentials_path = Path(credentials_path)
        else:
            # Default location
            self.credentials_path = Path.home() / '.creds' / 'gmail' / 'client_secret.json'
        
        self.vault_path = Path(vault_path) if vault_path else None
        self.token_path = Path.home() / '.creds' / 'gmail' / 'token.json'
        
        # Ensure directories exist
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Gmail API service
        self.service = None
        
        # Authenticate
        self._authenticate()

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
                if not self.credentials_path.exists():
                    self.logger.error(f'Credentials file not found: {self.credentials_path}')
                    self.logger.error('Please provide --credentials path or run --authenticate')
                    sys.exit(1)
                
                self.logger.info('Starting OAuth flow...')
                try:
                    app_flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES
                    )
                    creds = app_flow.run_local_server(host='localhost', port=8081)
                    
                    # Save credentials
                    self.token_path.write_text(creds.to_json(), encoding='utf-8')
                    self.logger.info('Authentication successful!')
                except Exception as e:
                    self.logger.error(f'Authentication failed: {e}')
                    sys.exit(1)
        
        # Build Gmail API service
        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info('Gmail API service initialized')

    def send_email(self, to: str, subject: str, body: str, 
                   html: bool = False, attachments: list = None) -> dict:
        """
        Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
            html: Whether body is HTML (default: False)
            attachments: List of file paths to attach
            
        Returns:
            Message ID if successful
        """
        try:
            # Create message
            message = MIMEMultipart() if attachments else MIMEText('')
            message['to'] = to
            message['subject'] = subject
            
            # Add body
            message_type = 'html' if html else 'plain'
            message.attach(MIMEText(body, message_type))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    self._attach_file(message, file_path)
            
            # Encode and send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            sent_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            self.logger.info(f'Email sent to {to}, message ID: {sent_message["id"]}')
            return sent_message
            
        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            raise
        except Exception as e:
            self.logger.error(f'Error sending email: {e}')
            raise

    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Attach a file to the message."""
        try:
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{Path(file_path).name}"'
                )
                message.attach(part)
        except Exception as e:
            self.logger.error(f'Error attaching file {file_path}: {e}')
            raise

    def create_draft(self, to: str, subject: str, body: str, 
                     html: bool = False, attachments: list = None) -> dict:
        """
        Create a draft email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
            html: Whether body is HTML (default: False)
            attachments: List of file paths to attach
            
        Returns:
            Draft ID if successful
        """
        try:
            # Create message
            message = MIMEMultipart() if attachments else MIMEText('')
            message['to'] = to
            message['subject'] = subject
            
            # Add body
            message_type = 'html' if html else 'plain'
            message.attach(MIMEText(body, message_type))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    self._attach_file(message, file_path)
            
            # Encode and create draft
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw_message}}
            ).execute()
            
            self.logger.info(f'Draft created, ID: {draft["id"]}')
            return draft
            
        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            raise
        except Exception as e:
            self.logger.error(f'Error creating draft: {e}')
            raise

    def create_approval_request(self, to: str, subject: str, body: str, 
                                reason: str = None) -> Path:
        """
        Create an approval request file in the vault.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
            reason: Reason approval is needed
            
        Returns:
            Path to created approval file
        """
        if not self.vault_path:
            raise ValueError("Vault path required for approval workflow")
        
        pending_approval = self.vault_path / 'Pending_Approval'
        pending_approval.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().isoformat()
        file_id = f"EMAIL_{int(datetime.now().timestamp())}"
        
        # Determine reason if not provided
        if not reason:
            domain = to.split('@')[-1] if '@' in to else ''
            is_known = any(known in domain for known in KNOWN_CONTACTS)
            
            if not is_known:
                reason = "Recipient is not in known contacts list"
            else:
                reason = "Email requires human review before sending"
        
        content = f"""---
type: approval_request
action: send_email
to: {to}
subject: {subject}
created: {timestamp}
status: pending
reason: {reason}
---

# Email Approval Required

**To:** {to}  
**Subject:** {subject}  
**Created:** {timestamp}

## Email Content

{body}

## Why Approval is Needed

{reason}

## To Approve

1. Review the email content above
2. Move this file to `/Approved` folder to send
3. The Email MCP will automatically send the email

## To Reject

1. Move this file to `/Rejected` folder
2. Add a comment explaining the rejection

---
*This file was created by Email MCP for human-in-the-loop approval*
"""
        
        filepath = pending_approval / f'{file_id}.md'
        filepath.write_text(content, encoding='utf-8')
        
        self.logger.info(f'Approval request created: {filepath.name}')
        return filepath

    def search_emails(self, query: str, max_results: int = 10) -> list:
        """
        Search Gmail for emails.
        
        Args:
            query: Gmail search query
            max_results: Maximum results to return
            
        Returns:
            List of message dictionaries
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            # Get full details for each message
            email_list = []
            for msg in messages:
                details = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'To', 'Subject', 'Date']
                ).execute()
                
                headers = {h['name']: h['value'] for h in details.get('payload', {}).get('headers', [])}
                email_list.append({
                    'id': msg['id'],
                    'from': headers.get('From', ''),
                    'to': headers.get('To', ''),
                    'subject': headers.get('Subject', ''),
                    'date': headers.get('Date', '')
                })
            
            return email_list
            
        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            return []
        except Exception as e:
            self.logger.error(f'Error searching emails: {e}')
            return []

    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark an email as read.
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            True if successful
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            self.logger.info(f'Message {message_id} marked as read')
            return True
            
        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            return False
        except Exception as e:
            self.logger.error(f'Error marking as read: {e}')
            return False

    def is_known_contact(self, email: str) -> bool:
        """Check if email is from a known contact."""
        if '@' not in email:
            return False
        
        domain = email.split('@')[-1].lower()
        return any(known.lower() in domain for known in KNOWN_CONTACTS)


def main():
    parser = argparse.ArgumentParser(description='Email MCP - Send and manage emails')
    parser.add_argument('action', choices=['send', 'draft', 'search', 'authenticate'],
                       help='Action to perform')
    parser.add_argument('--to', help='Recipient email address')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body text')
    parser.add_argument('--html', action='store_true', help='Body is HTML')
    parser.add_argument('--query', help='Search query (for search action)')
    parser.add_argument('--vault', help='Path to Obsidian vault')
    parser.add_argument('--credentials', help='Path to OAuth credentials JSON')
    parser.add_argument('--attachments', nargs='+', help='Files to attach')
    
    args = parser.parse_args()
    
    # Initialize MCP
    mcp = EmailMCP(credentials_path=args.credentials, vault_path=args.vault)
    
    if args.action == 'authenticate':
        print("Authentication successful!")
        return
    
    if args.action == 'send':
        if not args.to or not args.subject or not args.body:
            parser.error("send requires --to, --subject, and --body")
        
        # Check if approval needed
        if not mcp.is_known_contact(args.to):
            print(f"Recipient {args.to} is not a known contact.")
            print("Creating approval request...")
            filepath = mcp.create_approval_request(args.to, args.subject, args.body)
            print(f"Approval request created: {filepath}")
            return
        
        # Send directly
        result = mcp.send_email(args.to, args.subject, args.body, 
                               html=args.html, attachments=args.attachments)
        print(f"Email sent! Message ID: {result['id']}")
    
    elif args.action == 'draft':
        if not args.to or not args.subject or not args.body:
            parser.error("draft requires --to, --subject, and --body")
        
        if not args.vault:
            parser.error("draft requires --vault path")
        
        filepath = mcp.create_approval_request(args.to, args.subject, args.body)
        print(f"Approval request created: {filepath}")
    
    elif args.action == 'search':
        if not args.query:
            parser.error("search requires --query")
        
        results = mcp.search_emails(args.query)
        print(f"Found {len(results)} emails:")
        for email in results:
            print(f"  From: {email['from']}")
            print(f"  Subject: {email['subject']}")
            print(f"  Date: {email['date']}")
            print()


if __name__ == '__main__':
    main()
