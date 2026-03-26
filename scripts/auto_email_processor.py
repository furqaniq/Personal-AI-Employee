#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Auto Email Processor - Automatically processes emails without Qwen Code.

This script:
1. Reads all email action files in Needs_Action/
2. Analyzes content and determines actions
3. Creates reply drafts or approval requests
4. Moves processed files to Done/

Usage:
    python auto_email_processor.py /path/to/vault
"""

import sys
import logging
from pathlib import Path
from datetime import datetime
import shutil
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class AutoEmailProcessor:
    """Automatically processes email action files."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        
        # Ensure folders exist
        for folder in [self.pending_approval, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger('AutoEmailProcessor')
        
        # Known contact domains (auto-reply)
        self.known_domains = ['client.com', 'partner.com', 'yourcompany.com']
        
        # Priority keywords
        self.priority_keywords = ['urgent', 'asap', 'invoice', 'payment', 'emergency']

    def process_all(self):
        """Process all email files in Needs_Action/."""
        if not self.needs_action.exists():
            self.logger.warning('Needs_Action folder not found')
            return
        
        email_files = list(self.needs_action.glob('EMAIL_*.md'))
        
        if not email_files:
            self.logger.info('No email files to process')
            return
        
        self.logger.info(f'Found {len(email_files)} email file(s) to process')
        
        processed = 0
        for file_path in email_files:
            try:
                self.process_email(file_path)
                processed += 1
            except Exception as e:
                self.logger.error(f'Error processing {file_path.name}: {e}')
        
        self.logger.info(f'Processed {processed}/{len(email_files)} email(s)')

    def process_email(self, file_path: Path):
        """Process a single email file."""
        content = file_path.read_text(encoding='utf-8')
        
        # Extract email info from frontmatter
        email_info = self.extract_email_info(content)
        
        # Determine action based on content
        action = self.determine_action(email_info, content)
        
        if action['type'] == 'auto_reply':
            self.create_auto_reply(file_path, email_info, action)
        elif action['type'] == 'approval_required':
            self.create_approval_request(file_path, email_info, action)
        elif action['type'] == 'categorize':
            self.categorize_email(file_path, email_info)
        
        # Move to Done
        dest = self.done / file_path.name
        shutil.move(str(file_path), str(dest))
        self.logger.info(f'✓ Moved to Done: {file_path.name}')

    def extract_email_info(self, content: str) -> dict:
        """Extract email information from frontmatter."""
        info = {
            'from': '',
            'to': '',
            'subject': '',
            'priority': 'medium'
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
                        if key in info:
                            info[key] = value
        
        # Check for priority keywords in content
        content_lower = content.lower()
        for keyword in self.priority_keywords:
            if keyword in content_lower:
                info['priority'] = 'high'
                break
        
        return info

    def determine_action(self, email_info: dict, content: str) -> dict:
        """Determine what action to take for this email."""
        from_addr = email_info.get('from', '').lower()
        subject = email_info.get('subject', '').lower()
        
        # Check if from known contact
        is_known = any(domain in from_addr for domain in self.known_domains)
        
        # Check content type
        is_pin_code = any(word in content.lower() for word in ['pin', 'verification code', 'otp'])
        is_security_alert = 'security alert' in subject or 'security alert' in content.lower()
        is_newsletter = any(word in subject for word in ['newsletter', 'digest', 'update'])
        
        if is_pin_code or is_security_alert:
            return {'type': 'categorize', 'category': 'security'}
        elif is_newsletter:
            return {'type': 'categorize', 'category': 'newsletter'}
        elif is_known:
            return {'type': 'auto_reply', 'template': 'known_contact'}
        else:
            return {'type': 'approval_required', 'reason': 'New contact - requires review'}

    def create_auto_reply(self, file_path: Path, email_info: dict, action: dict):
        """Create an auto-reply draft."""
        reply_content = f"""---
type: email_draft
in_reply_to: {file_path.name}
created: {datetime.now().isoformat()}
status: draft
---

# Email Draft - Auto Reply

**To:** {email_info.get('from', '')}  
**Subject:** Re: {email_info.get('subject', '')}

## Draft Content

Thank you for your email. We have received your message and will respond shortly.

Best regards,  
AI Employee

---
*This draft was auto-generated. Review before sending.*
"""
        draft_path = self.vault_path / 'Drafts' / f'REPLY_{file_path.name}'
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(reply_content, encoding='utf-8')
        self.logger.info(f'  → Created reply draft: {draft_path.name}')

    def create_approval_request(self, file_path: Path, email_info: dict, action: dict):
        """Create an approval request for new contacts."""
        content = file_path.read_text(encoding='utf-8')
        
        approval_content = f"""---
type: approval_request
action: review_email
from: {email_info.get('from', '')}
subject: {email_info.get('subject', '')}
created: {datetime.now().isoformat()}
status: pending
reason: {action.get('reason', 'Review required')}
---

# Email Review Required

**From:** {email_info.get('from', '')}  
**Subject:** {email_info.get('subject', '')}  
**Priority:** {email_info.get('priority', 'medium')}

## Reason for Review

{action.get('reason', 'This email requires human review before action')}

## Email Content

{content.split('##')[0]}

## Suggested Actions

- [ ] Review email content
- [ ] Determine appropriate response
- [ ] Reply manually or approve auto-reply
- [ ] Archive after processing

## To Approve

Move this file to `/Approved` folder to mark as reviewed.

## To Reject

Move this file to `/Rejected` folder with reason.

---
*This file was created by Auto Email Processor*
"""
        approval_path = self.pending_approval / f'REVIEW_{file_path.name}'
        approval_path.write_text(approval_content, encoding='utf-8')
        self.logger.info(f'  → Created approval request: {approval_path.name}')

    def categorize_email(self, file_path: Path, email_info: dict):
        """Categorize security/newsletter emails."""
        # Just log for now - these are informational
        self.logger.info(f'  → Categorized: {email_info.get("subject", "Unknown")[:50]}')

    def log_activity(self, action: str, details: str):
        """Log activity to Logs folder."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}-email-processor.json'
        
        import json
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_email_processor.py /path/to/vault")
        print("\nExample:")
        print('  python auto_email_processor.py "C:\\Users\\...\\AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    processor = AutoEmailProcessor(vault_path)
    processor.process_all()
    
    print("\n✓ Email processing complete!")
    print(f"  Check {vault_path}\\Done\\ for processed emails")
    print(f"  Check {vault_path}\\Pending_Approval\\ for items needing review")


if __name__ == '__main__':
    main()
