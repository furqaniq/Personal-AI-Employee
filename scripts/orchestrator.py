#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Orchestrator - Master process for AI Employee Silver Tier.

This script:
1. Watches Needs_Action folder for new items
2. Reads emails and creates approval requests with suggested replies
3. Watches Approved folder for approved actions
4. Uses Email MCP to send approved emails
5. Moves completed items to Done/
6. Updates Dashboard.md

Usage:
    python orchestrator.py /path/to/vault

Example:
    python orchestrator.py "C:/Users/.../AI_Employee_Vault"
"""

import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import time
import json
import re
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Orchestrator:
    """Main orchestrator for AI Employee Silver Tier."""

    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the orchestrator.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.logger = logging.getLogger('Orchestrator')

        # Vault folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'

        # Ensure all folders exist
        for folder in [self.needs_action, self.done, self.plans,
                       self.pending_approval, self.approved, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

        # Track processed files to avoid duplicates
        self.processed_files: set = set()
        
        # Track sent emails to prevent duplicate sends
        self.sent_emails_file = self.vault_path / '.creds' / 'sent_emails.json'
        self.sent_emails = self._load_sent_emails()
        
        # Credentials path for Email MCP
        self.credentials_path = Path.home() / 'AppData' / 'Local' / 'AI_Employee' / 'creds' / 'gmail' / 'client_secret.json'

        self.logger.info(f'Orchestrator initialized for vault: {vault_path}')
    
    def _load_sent_emails(self) -> set:
        """Load list of sent email IDs."""
        import json
        if self.sent_emails_file.exists():
            try:
                data = json.loads(self.sent_emails_file.read_text(encoding='utf-8'))
                return set(data.get('sent_ids', []))
            except:
                pass
        return set()
    
    def _save_sent_email(self, email_id: str):
        """Save sent email ID to prevent duplicate sends."""
        import json
        self.sent_emails.add(email_id)
        # Keep only last 1000 sent emails
        sent_list = list(self.sent_emails)[-1000:]
        self.sent_emails_file.write_text(
            json.dumps({'sent_ids': sent_list, 'updated': datetime.now().isoformat()}, indent=2),
            encoding='utf-8'
        )
    
    def _was_already_sent(self, email_id: str) -> bool:
        """Check if email was already sent."""
        return email_id in self.sent_emails

    def get_pending_items(self) -> List[Path]:
        """Get list of pending email action files."""
        items = []
        if self.needs_action.exists():
            for file_path in self.needs_action.iterdir():
                if file_path.is_file() and file_path.suffix == '.md' and file_path.name.startswith('EMAIL_'):
                    if file_path.name not in self.processed_files:
                        items.append(file_path)
        return items

    def get_approved_items(self) -> List[Path]:
        """Get list of approved action files."""
        items = []
        if self.approved.exists():
            for file_path in self.approved.iterdir():
                if file_path.is_file() and file_path.suffix == '.md':
                    items.append(file_path)
        return items

    def read_email_file(self, file_path: Path) -> dict:
        """Read and parse email action file."""
        content = file_path.read_text(encoding='utf-8')
        
        email_info = {
            'from': '',
            'to': '',
            'subject': '',
            'date': '',
            'content': '',
            'gmail_id': ''
        }
        
        # Parse frontmatter
        if content.startswith('---'):
            end_idx = content.find('---', 3)
            if end_idx > 0:
                frontmatter = content[4:end_idx]
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in email_info:
                            email_info[key] = value
        
        # Extract email content from body
        if '## Content' in content:
            email_info['content'] = content.split('## Content')[1].split('##')[0].strip()
        elif '## Email Content' in content:
            email_info['content'] = content.split('## Email Content')[1].split('##')[0].strip()
        
        return email_info

    def generate_suggested_reply(self, email_info: dict) -> str:
        """Generate a suggested reply based on email content."""
        subject = email_info.get('subject', '')
        content = email_info.get('content', '').lower()
        
        # Check for common patterns
        if any(word in content for word in ['invoice', 'payment', 'bill']):
            return f"""Dear Sender,

Thank you for your email regarding "{subject}".

We have received your request and will process it shortly. Our accounting team will review and respond with the necessary documentation.

Best regards,
AI Employee"""
        
        elif any(word in content for word in ['pin', 'verification', 'code', 'otp']):
            return f"""Dear Sender,

Thank you for your message regarding verification code.

For security reasons, we do not respond to verification code requests via email. Please use the official application or website for verification.

Best regards,
AI Employee"""
        
        elif any(word in content for word in ['security alert', 'login', 'device']):
            return f"""Dear Sender,

Thank you for the security notification.

We have reviewed this security alert and confirmed it is legitimate. No further action is required at this time.

Best regards,
AI Employee"""
        
        elif any(word in content for word in ['hello', 'hi', 'greetings', 'regards']):
            return f"""Dear Sender,

Thank you for reaching out!

We have received your email and appreciate you contacting us. A team member will review your message and respond within 24 hours.

Best regards,
AI Employee"""
        
        else:
            # Generic reply
            return f"""Dear Sender,

Thank you for your email regarding "{subject}".

We have received your message and will respond shortly.

Best regards,
AI Employee"""

    def create_approval_request(self, email_file: Path, email_info: dict):
        """Create approval request file with suggested reply."""
        timestamp = datetime.now().isoformat()
        file_id = email_file.stem
        
        suggested_reply = self.generate_suggested_reply(email_info)
        
        approval_content = f"""---
type: approval_request
action: send_email
from: {email_info.get('from', '')}
to: {email_info.get('from', '')}
subject: Re: {email_info.get('subject', '')}
original_file: {email_file.name}
gmail_id: {email_info.get('gmail_id', '')}
created: {timestamp}
status: pending
priority: {email_info.get('priority', 'medium')}
---

# Email Approval Required

**From:** {email_info.get('from', '')}  
**Subject:** {email_info.get('subject', '')}  
**Date:** {email_info.get('date', '')}  
**Created:** {timestamp}

## Original Email Content

{email_info.get('content', '')}

---

## Suggested Reply

**To:** {email_info.get('from', '')}  
**Subject:** Re: {email_info.get('subject', '')}

{suggested_reply}

---

## To Approve and Send

1. Review the suggested reply above
2. Edit if needed (modify the reply text)
3. Move this file to `/Approved` folder
4. The Email MCP will automatically send the reply

## To Reject

1. Move this file to `/Rejected` folder
2. Add a comment explaining the rejection

## To Edit Reply

1. Modify the "Suggested Reply" section above
2. Save the file
3. Move to `/Approved` when ready to send

---
*This file was created by Orchestrator for human-in-the-loop approval*
*File ID: {file_id}*
"""
        
        approval_path = self.pending_approval / f'APPROVAL_{file_id}.md'
        approval_path.write_text(approval_content, encoding='utf-8')
        
        self.logger.info(f'✓ Created approval request: {approval_path.name}')
        return approval_path

    def send_approved_email(self, approval_file: Path) -> bool:
        """Send email using Email MCP for approved approval file."""
        content = approval_file.read_text(encoding='utf-8')
        
        # Parse approval file
        email_data = {
            'to': '',
            'subject': '',
            'body': '',
            'gmail_id': ''
        }
        
        # Extract frontmatter
        if content.startswith('---'):
            end_idx = content.find('---', 3)
            if end_idx > 0:
                frontmatter = content[4:end_idx]
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in email_data:
                            email_data[key] = value
        
        # Extract reply body from "Suggested Reply" section
        if '## Suggested Reply' in content:
            reply_section = content.split('## Suggested Reply')[1]
            # Remove the To/Subject lines and get the body
            lines = reply_section.split('\n')
            body_lines = []
            skip_next = False
            for line in lines:
                if line.strip().startswith('**To:**') or line.strip().startswith('**Subject:**'):
                    skip_next = True
                    continue
                if skip_next and line.strip():
                    skip_next = False
                    continue
                if line.strip() and not line.startswith('---'):
                    body_lines.append(line)
            email_data['body'] = '\n'.join(body_lines).strip()
        
        if not email_data['to'] or not email_data['body']:
            self.logger.error(f'Cannot send email - missing to or body: {approval_file.name}')
            return False
        
        self.logger.info(f'Sending email to {email_data["to"]} via Email MCP...')
        
        try:
            # Run Email MCP - handle both cases: running from scripts/ folder or root
            if Path('email_mcp.py').exists():
                email_mcp_path = Path('email_mcp.py').resolve()
            else:
                email_mcp_path = self.vault_path.parent.parent / 'scripts' / 'email_mcp.py'
            
            cmd = [
                sys.executable,
                str(email_mcp_path),
                '--to', email_data['to'],
                '--subject', email_data['subject'],
                '--body', email_data['body'],
                '--vault', str(self.vault_path)
            ]
            
            if self.credentials_path.exists():
                cmd.extend(['--credentials', str(self.credentials_path)])
            
            self.logger.info(f'Running Email MCP: {email_mcp_path}')
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Check for success (Email MCP outputs success to stdout)
            combined_output = result.stdout + result.stderr
            if result.returncode == 0 or '✅ Email sent' in combined_output or 'Email sent successfully' in combined_output:
                self.logger.info(f'✓ Email sent successfully to {email_data["to"]}')
                
                # Log the sent email
                self.log_activity('email_sent', f'To: {email_data["to"]}, Subject: {email_data["subject"]}')
                
                return True
            else:
                self.logger.error(f'Email MCP failed: {result.stderr}')
                self.log_activity('email_failed', f'To: {email_data["to"]}, Error: {result.stderr}')
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error('Email MCP timed out (60s limit)')
            return False
        except FileNotFoundError:
            self.logger.error(f'Email MCP not found at: {email_mcp_path}')
            return False
        except Exception as e:
            self.logger.error(f'Error sending email: {e}')
            return False
    
    def log_activity(self, action: str, details: str):
        """Log activity to Logs folder."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}-orchestrator.json'
        
        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text(encoding='utf-8'))
            except:
                pass
        
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        })
        
        logs = logs[-500:]
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')

    def process_pending_emails(self):
        """Process pending emails - create approval requests."""
        pending_items = self.get_pending_items()
        
        for item in pending_items:
            self.logger.info(f'Processing email: {item.name}')
            
            # Read email
            email_info = self.read_email_file(item)
            
            # Create approval request with suggested reply
            self.create_approval_request(item, email_info)
            
            # Mark as processed and move to Done (approval file is in Pending_Approval)
            dest = self.done / item.name
            shutil.move(str(item), str(dest))
            self.processed_files.add(item.name)
            
            self.logger.info(f'✓ Moved to Done: {item.name}')

    def process_approved_items(self):
        """Process approved items - send emails via MCP."""
        approved_items = self.get_approved_items()
        
        for item in approved_items:
            self.logger.info(f'Processing approved item: {item.name}')
            
            # Check if file still exists (might have been processed by another instance)
            if not item.exists():
                self.logger.warning(f'File no longer exists (already processed?): {item.name}')
                continue
            
            # Check if already sent (prevent duplicates)
            if self._was_already_sent(item.name):
                self.logger.info(f'✓ Email already sent (skipping): {item.name}')
                # Move to Done since it was already sent
                try:
                    dest = self.done / item.name
                    if dest.exists():
                        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                        dest = self.done / f'{item.stem}_{timestamp}{item.suffix}'
                    shutil.move(str(item), str(dest))
                except:
                    pass
                continue
            
            # Send email
            success = self.send_approved_email(item)
            
            if success:
                # Mark as sent to prevent duplicates
                self._save_sent_email(item.name)
                
                # Move to Done
                try:
                    dest = self.done / item.name
                    # Check if destination already exists
                    if dest.exists():
                        # Add timestamp to avoid conflict
                        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                        dest = self.done / f'{item.stem}_{timestamp}{item.suffix}'
                    
                    shutil.move(str(item), str(dest))
                    self.logger.info(f'✅ SUCCESS: Email sent and moved to Done: {dest.name}')
                    self.logger.info('=' * 60)
                except FileNotFoundError:
                    # File was moved by another process - that's ok
                    self.logger.info(f'✓ Email sent successfully (file already moved)')
                except Exception as e:
                    self.logger.error(f'Warning: Could not move file to Done: {e}')
                    self.logger.info('✓ But email WAS sent successfully!')
            else:
                self.logger.error(f'✗ Failed to send email: {item.name}')
                self.logger.info('File remains in Approved/ for retry')

    def update_dashboard(self, pending_count: int, approved_count: int, completed_count: int):
        """Update the Dashboard.md with current status."""
        if not self.dashboard.exists():
            self.logger.warning('Dashboard.md not found')
            return

        try:
            content = self.dashboard.read_text(encoding='utf-8')

            # Update timestamp
            content = re.sub(
                r'last_updated: \d{4}-\d{2}-\d{2}T[\d:.]+',
                f'last_updated: {datetime.now().isoformat()}',
                content
            )

            # Update pending count
            content = re.sub(
                r'\| Pending Tasks\s*\| \d+\s*\|',
                f'| Pending Tasks | {pending_count} |',
                content
            )

            # Update awaiting approval
            content = re.sub(
                r'\| Awaiting Approval\s*\| \d+\s*\|',
                f'| Awaiting Approval | {approved_count} |',
                content
            )

            # Update completed today
            content = re.sub(
                r'\| Completed Today\s*\| \d+\s*\|',
                f'| Completed Today | {completed_count} |',
                content
            )

            self.dashboard.write_text(content, encoding='utf-8')
            self.logger.info(f'Dashboard updated: {pending_count} pending, {approved_count} awaiting approval, {completed_count} completed')

        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}')

    def run(self):
        """Main run loop."""
        self.logger.info('=' * 60)
        self.logger.info('AI Employee Orchestrator - Silver Tier')
        self.logger.info('=' * 60)
        self.logger.info(f'Vault: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        self.logger.info('Press Ctrl+C to stop')
        self.logger.info('=' * 60)

        try:
            while True:
                # Process pending emails (create approval requests)
                self.process_pending_emails()
                
                # Process approved items (send emails)
                self.process_approved_items()
                
                # Update dashboard
                pending_count = len(self.get_pending_items())
                approved_count = len(self.get_approved_items())
                completed_count = len(list(self.done.glob('EMAIL_*.md')))
                
                self.update_dashboard(pending_count, approved_count, completed_count)
                
                # Wait for next check
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("=" * 60)
        print("AI Employee Orchestrator - Silver Tier")
        print("=" * 60)
        print()
        print("Usage:")
        print("  python orchestrator.py <vault_path> [check_interval]")
        print()
        print("Arguments:")
        print("  vault_path      - Path to your Obsidian vault")
        print("  check_interval  - Seconds between checks (default: 60)")
        print()
        print("Workflow:")
        print("  1. Gmail Watcher creates EMAIL_*.md in /Needs_Action")
        print("  2. Orchestrator creates APPROVAL_*.md with suggested reply in /Pending_Approval")
        print("  3. You review and move to /Approved")
        print("  4. Orchestrator sends email via Email MCP")
        print("  5. File moved to /Done")
        print()
        sys.exit(1)

    vault_path = sys.argv[1]
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60

    # Validate vault path
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)

    orchestrator = Orchestrator(vault_path, check_interval)
    orchestrator.run()
