#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Email MCP - Send emails via Gmail API.

Silver Tier implementation for AI Employee Hackathon.

Usage:
    python email_mcp.py send --to "recipient@example.com" --subject "Subject" --body "Body"
    python email_mcp.py --help
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

# Google API imports
try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Google API libraries not installed.")
    print("Run: python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class EmailMCP:
    """
    Email MCP for sending emails via Gmail API.
    """

    def __init__(self, credentials_path: str = None, vault_path: str = None):
        """
        Initialize Email MCP.
        
        Args:
            credentials_path: Path to OAuth credentials JSON file
            vault_path: Path to Obsidian vault (for token storage)
        """
        self.logger = logging.getLogger('EmailMCP')
        
        # Find credentials
        if credentials_path:
            self.credentials_path = Path(credentials_path)
        else:
            # Default location
            self.credentials_path = Path.home() / '.creds' / 'gmail' / 'client_secret.json'
        
        # Token path
        if vault_path:
            self.token_path = Path(vault_path) / '.creds' / 'gmail_token.json'
        else:
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
                    self.logger.error('Please run AUTHENTICATE-GMAIL.bat first')
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
                   html: bool = False, in_reply_to: str = None) -> dict:
        """
        Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
            html: Whether body is HTML (default: False)
            in_reply_to: Message ID to reply to (optional)
            
        Returns:
            Message dict if successful
        """
        try:
            # Create message
            message = MIMEMultipart() if not html else MIMEText(body, 'html')
            message['to'] = to
            message['subject'] = subject
            
            if not html:
                message.attach(MIMEText(body, 'plain'))
            
            # Add In-Reply-To header if replying
            if in_reply_to:
                message['In-Reply-To'] = in_reply_to
                message['References'] = in_reply_to
            
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


def main():
    parser = argparse.ArgumentParser(description='Email MCP - Send emails via Gmail API')
    parser.add_argument('--to', help='Recipient email address')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body text')
    parser.add_argument('--html', action='store_true', help='Body is HTML')
    parser.add_argument('--in-reply-to', help='Message ID to reply to')
    parser.add_argument('--credentials', help='Path to OAuth credentials JSON')
    parser.add_argument('--vault', help='Path to Obsidian vault')
    
    args = parser.parse_args()
    
    if not args.to or not args.subject or not args.body:
        parser.print_help()
        print("\nError: --to, --subject, and --body are required")
        sys.exit(1)
    
    # Initialize MCP
    mcp = EmailMCP(credentials_path=args.credentials, vault_path=args.vault)
    
    # Send email
    try:
        result = mcp.send_email(
            to=args.to,
            subject=args.subject,
            body=args.body,
            html=args.html,
            in_reply_to=getattr(args, 'in_reply_to', None)
        )
        print(f"\n✅ Email sent successfully!")
        print(f"   To: {args.to}")
        print(f"   Subject: {args.subject}")
        print(f"   Message ID: {result['id']}")
    except Exception as e:
        print(f"\n❌ Failed to send email: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
