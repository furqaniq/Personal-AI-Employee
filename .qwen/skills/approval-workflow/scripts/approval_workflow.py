#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Approval Workflow - Manages human-in-the-loop approval for sensitive actions.

Silver Tier implementation for AI Employee Hackathon.

Usage:
    python approval_workflow.py create --action "send_email" --details '{"to": "..."}' --vault "/path/to/vault"
    python approval_workflow.py pending --vault "/path/to/vault"
    python approval_workflow.py process --vault "/path/to/vault"
    python approval_workflow.py stats --vault "/path/to/vault"
    python approval_workflow.py cleanup --vault "/path/to/vault"
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Action types that require approval
ACTION_TYPES = {
    'send_email': {
        'auto_approve_conditions': ['known_contact', 'routine_reply'],
        'always_require_approval': ['new_contact', 'bulk_send', 'has_attachment']
    },
    'linkedin_post': {
        'auto_approve_conditions': [],
        'always_require_approval': ['all']
    },
    'linkedin_connect': {
        'auto_approve_conditions': ['known_company'],
        'always_require_approval': ['unknown_company']
    },
    'payment': {
        'auto_approve_conditions': ['recurring', 'under_50'],
        'always_require_approval': ['new_payee', 'over_50']
    },
    'file_delete': {
        'auto_approve_conditions': [],
        'always_require_approval': ['all']
    },
    'file_move': {
        'auto_approve_conditions': ['within_vault'],
        'always_require_approval': ['outside_vault']
    }
}

# Approval templates by action type
APPROVAL_TEMPLATES = {
    'send_email': """
## Email Details

**To:** {to}  
**Subject:** {subject}  
**Body:**

{body}
""",
    'linkedin_post': """
## Post Content

{content}
""",
    'linkedin_connect': """
## Connection Details

**Profile:** {profile_name}  
**Company:** {company}  
**Note:** {note}
""",
    'payment': """
## Payment Details

**Payee:** {payee}  
**Amount:** ${amount}  
**Reference:** {reference}  
**Due Date:** {due_date}
""",
    'file_delete': """
## File Details

**File:** {file_path}  
**Size:** {file_size}  
**Reason:** {reason}
"""
}


class ApprovalWorkflow:
    """
    Approval Workflow for managing human-in-the-loop approvals.
    """

    def __init__(self, vault_path: str):
        """
        Initialize Approval Workflow.
        
        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = logging.getLogger('ApprovalWorkflow')
        
        # Vault folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        
        # Ensure folders exist
        for folder in [self.pending_approval, self.approved, 
                       self.rejected, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

    def requires_approval(self, action_type: str, details: Dict) -> tuple:
        """
        Check if action requires approval.
        
        Args:
            action_type: Type of action
            details: Action details
            
        Returns:
            Tuple of (requires_approval: bool, reason: str)
        """
        config = ACTION_TYPES.get(action_type)
        if not config:
            return True, f"Unknown action type: {action_type}"
        
        # Check if all actions of this type require approval
        if 'all' in config['always_require_approval']:
            return True, f"All {action_type} actions require approval"
        
        # Check auto-approve conditions
        for condition in config['auto_approve_conditions']:
            if self._check_condition(condition, details):
                return False, f"Auto-approved: {condition}"
        
        # Check require approval conditions
        for condition in config['always_require_approval']:
            if self._check_condition(condition, details):
                return True, f"Approval required: {condition}"
        
        # Default to requiring approval
        return True, "Default: approval required for safety"

    def _check_condition(self, condition: str, details: Dict) -> bool:
        """Check if a condition is met."""
        if condition == 'known_contact':
            to = details.get('to', '')
            known_domains = ['client.com', 'partner.com']  # From Company Handbook
            return any(d in to for d in known_domains)
        
        elif condition == 'new_contact':
            to = details.get('to', '')
            known_domains = ['client.com', 'partner.com']
            return not any(d in to for d in known_domains)
        
        elif condition == 'bulk_send':
            return details.get('bulk', False)
        
        elif condition == 'has_attachment':
            return bool(details.get('attachments', []))
        
        elif condition == 'routine_reply':
            subject = details.get('subject', '')
            return subject.lower().startswith('re:')
        
        elif condition == 'recurring':
            return details.get('recurring', False)
        
        elif condition == 'under_50':
            amount = float(details.get('amount', 0))
            return amount < 50
        
        elif condition == 'over_50':
            amount = float(details.get('amount', 0))
            return amount >= 50
        
        elif condition == 'new_payee':
            return details.get('new_payee', True)
        
        elif condition == 'known_company':
            company = details.get('company', '')
            known_companies = ['Google', 'Microsoft', 'Amazon']
            return any(c in company for c in known_companies)
        
        elif condition == 'unknown_company':
            company = details.get('company', '')
            known_companies = ['Google', 'Microsoft', 'Amazon']
            return not any(c in company for c in known_companies)
        
        elif condition == 'within_vault':
            path = details.get('path', '')
            return str(self.vault_path) in path
        
        elif condition == 'outside_vault':
            path = details.get('path', '')
            return str(self.vault_path) not in path
        
        return False

    def create_approval_request(self, action_type: str, details: Dict,
                                reason: str = None, priority: str = 'medium',
                                expires_hours: int = 24) -> Path:
        """
        Create an approval request file.
        
        Args:
            action_type: Type of action
            details: Action details dictionary
            reason: Reason approval is needed
            priority: Request priority (low, medium, high)
            expires_hours: Hours until expiry
            
        Returns:
            Path to created approval file
        """
        # Check if approval is actually needed
        needs_approval, auto_reason = self.requires_approval(action_type, details)
        
        if not needs_approval:
            self.logger.info(f'Action auto-approved: {auto_reason}')
            return None
        
        # Use provided reason or auto-generated
        if not reason:
            reason = auto_reason
        
        timestamp = datetime.now().isoformat()
        expires = (datetime.now() + timedelta(hours=expires_hours)).isoformat()
        file_id = f"{action_type.upper()}_{int(datetime.now().timestamp())}"
        
        # Get template content
        template = APPROVAL_TEMPLATES.get(action_type, "")
        try:
            details_content = template.format(**details)
        except KeyError as e:
            details_content = f"\n**Details:** {json.dumps(details, indent=2)}\n"
        
        # Risk assessment
        risk_level = self._assess_risk(action_type, details)
        
        content = f"""---
type: approval_request
action: {action_type}
created: {timestamp}
status: pending
priority: {priority}
expires: {expires}
reason: {reason}
risk_level: {risk_level}
---

# Approval Required: {action_type.replace('_', ' ').title()}

**Action:** {action_type.replace('_', ' ').title()}  
**Created:** {timestamp}  
**Priority:** {priority.title()}  
**Expires:** {expires}  
**Risk Level:** {risk_level.title()}

{details_content}

## Why Approval is Needed

{reason}

## Risk Assessment

| Factor | Level |
|--------|-------|
| Reversibility | {self._get_reversibility(action_type)} |
| Financial Impact | {self._get_financial_impact(details)} |
| External Communication | {self._is_external(action_type)} |

## To Approve

1. Review the action details above
2. Move this file to `/Approved` folder
3. The system will automatically execute the action

## To Reject

1. Move this file to `/Rejected` folder
2. Add a comment explaining the rejection

## To Request Changes

1. Add comments to this file
2. Move back to `/Needs_Action` for revision

---
*This file was created by Approval Workflow for human-in-the-loop approval*
*File ID: {file_id}*
"""
        
        filepath = self.pending_approval / f'{file_id}.md'
        filepath.write_text(content, encoding='utf-8')
        
        self.logger.info(f'Approval request created: {filepath.name}')
        self._log_action('approval_created', str(filepath), action_type, 'pending')
        
        return filepath

    def _assess_risk(self, action_type: str, details: Dict) -> str:
        """Assess risk level of action."""
        high_risk_actions = ['payment', 'file_delete']
        medium_risk_actions = ['send_email', 'linkedin_post']
        
        if action_type in high_risk_actions:
            return 'high'
        elif action_type in medium_risk_actions:
            return 'medium'
        return 'low'

    def _get_reversibility(self, action_type: str) -> str:
        """Get reversibility status."""
        reversible = ['send_email', 'linkedin_post', 'linkedin_connect']
        irreversible = ['file_delete', 'payment']
        
        if action_type in reversible:
            return 'Reversible'
        elif action_type in irreversible:
            return 'Irreversible'
        return 'Unknown'

    def _get_financial_impact(self, details: Dict) -> str:
        """Get financial impact level."""
        amount = float(details.get('amount', 0))
        
        if amount == 0:
            return 'None'
        elif amount < 100:
            return 'Low (< $100)'
        elif amount < 1000:
            return 'Medium ($100-$1000)'
        return 'High (> $1000)'

    def _is_external(self, action_type: str) -> str:
        """Check if action is external communication."""
        external = ['send_email', 'linkedin_post', 'linkedin_connect']
        return 'Yes' if action_type in external else 'No'

    def get_pending_approvals(self) -> List[Dict]:
        """Get list of pending approvals."""
        pending = []
        
        if not self.pending_approval.exists():
            return pending
        
        for file_path in self.pending_approval.iterdir():
            if file_path.is_file() and file_path.suffix == '.md':
                content = file_path.read_text(encoding='utf-8')
                
                # Parse frontmatter
                info = {
                    'file': file_path.name,
                    'path': str(file_path),
                    'action': '',
                    'created': '',
                    'priority': 'medium',
                    'status': 'pending'
                }
                
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
                
                # Check if expired
                if info.get('expires'):
                    try:
                        expires = datetime.fromisoformat(info['expires'])
                        if datetime.now() > expires:
                            info['status'] = 'expired'
                    except:
                        pass
                
                pending.append(info)
        
        # Sort by priority and expiry
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        pending.sort(key=lambda x: (
            priority_order.get(x.get('priority', 'medium'), 1),
            x.get('expires', '9999')
        ))
        
        return pending

    def process_approved_actions(self) -> List[Dict]:
        """
        Process actions that have been approved.
        
        Returns:
            List of processed action info
        """
        processed = []
        
        if not self.approved.exists():
            return processed
        
        for file_path in self.approved.iterdir():
            if file_path.is_file() and file_path.suffix == '.md':
                self.logger.info(f'Processing approved action: {file_path.name}')
                
                # Read the approval file
                content = file_path.read_text(encoding='utf-8')
                
                # Parse action type
                action_type = ''
                for line in content.split('\n'):
                    if line.startswith('action:'):
                        action_type = line.split(':', 1)[1].strip()
                        break
                
                # Log the processing
                self._log_action('approval_processed', str(file_path), action_type, 'success')
                
                # Move to Done
                dest = self.done / file_path.name
                file_path.rename(dest)
                
                processed.append({
                    'file': file_path.name,
                    'action_type': action_type,
                    'destination': str(dest)
                })
                
                self.logger.info(f'Moved to Done: {dest.name}')
        
        return processed

    def get_statistics(self) -> Dict:
        """Get approval workflow statistics."""
        stats = {
            'pending': 0,
            'approved_today': 0,
            'rejected_today': 0,
            'expired': 0,
            'by_action_type': {}
        }
        
        # Count pending
        pending = self.get_pending_approvals()
        stats['pending'] = len(pending)
        stats['expired'] = sum(1 for p in pending if p.get('status') == 'expired')
        
        # Count by action type
        for p in pending:
            action = p.get('action', 'unknown')
            stats['by_action_type'][action] = stats['by_action_type'].get(action, 0) + 1
        
        # Count today's decisions
        today = datetime.now().strftime('%Y-%m-%d')
        
        if self.approved.exists():
            for f in self.approved.iterdir():
                if f.is_file() and f.suffix == '.md':
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime)
                        if mtime.strftime('%Y-%m-%d') == today:
                            stats['approved_today'] += 1
                    except:
                        pass
        
        if self.rejected.exists():
            for f in self.rejected.iterdir():
                if f.is_file() and f.suffix == '.md':
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime)
                        if mtime.strftime('%Y-%m-%d') == today:
                            stats['rejected_today'] += 1
                    except:
                        pass
        
        return stats

    def cleanup_expired(self, days: int = 7) -> List[Path]:
        """
        Clean up expired approval requests.
        
        Args:
            days: Move files older than this many days
            
        Returns:
            List of moved file paths
        """
        moved = []
        cutoff = datetime.now() - timedelta(days=days)
        
        if not self.pending_approval.exists():
            return moved
        
        for file_path in self.pending_approval.iterdir():
            if file_path.is_file() and file_path.suffix == '.md':
                try:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff:
                        # Move to Rejected as expired
                        dest = self.rejected / f'EXPIRED_{file_path.name}'
                        file_path.rename(dest)
                        moved.append(dest)
                        self.logger.info(f'Moved expired file: {file_path.name}')
                except Exception as e:
                    self.logger.error(f'Error processing {file_path.name}: {e}')
        
        return moved

    def _log_action(self, action_type: str, details: str, 
                    approval_action: str, status: str):
        """Log an approval action."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}-approvals.json'
        
        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text(encoding='utf-8'))
            except:
                pass
        
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'details': details,
            'approval_action': approval_action,
            'status': status
        })
        
        logs = logs[-1000:]
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Approval Workflow - AI Employee Silver Tier')
    parser.add_argument('action', 
                       choices=['create', 'pending', 'process', 'stats', 'cleanup'],
                       help='Action to perform')
    parser.add_argument('--type', dest='action_type', help='Action type (for create)')
    parser.add_argument('--details', help='Action details as JSON (for create)')
    parser.add_argument('--reason', help='Reason for approval (for create)')
    parser.add_argument('--priority', default='medium',
                       choices=['low', 'medium', 'high'],
                       help='Priority level (for create)')
    parser.add_argument('--vault', help='Path to Obsidian vault')
    parser.add_argument('--days', type=int, default=7,
                       help='Days for cleanup (for cleanup)')
    
    args = parser.parse_args()
    
    if not args.vault:
        parser.error("--vault is required")
    
    workflow = ApprovalWorkflow(args.vault)
    
    if args.action == 'create':
        if not args.action_type or not args.details:
            parser.error("--type and --details are required for create")
        
        try:
            details = json.loads(args.details)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON for --details: {e}")
            sys.exit(1)
        
        filepath = workflow.create_approval_request(
            args.action_type,
            details,
            reason=args.reason,
            priority=args.priority
        )
        
        if filepath:
            print(f"Approval request created: {filepath}")
            print(f"Location: {filepath}")
            print("\nTo approve: Move file to /Approved folder")
            print("To reject: Move file to /Rejected folder")
        else:
            print("Action was auto-approved, no approval request needed")
    
    elif args.action == 'pending':
        pending = workflow.get_pending_approvals()
        
        print("=" * 60)
        print("Pending Approvals")
        print("=" * 60)
        
        if not pending:
            print("No pending approvals.")
        else:
            for item in pending:
                status_icon = '⚠️' if item.get('status') == 'expired' else '⏳'
                print(f"\n{status_icon} {item.get('file', 'Unknown')}")
                print(f"   Action: {item.get('action', 'N/A')}")
                print(f"   Priority: {item.get('priority', 'medium')}")
                print(f"   Status: {item.get('status', 'pending')}")
                if item.get('expires'):
                    print(f"   Expires: {item['expires']}")
    
    elif args.action == 'process':
        print("Processing approved actions...")
        processed = workflow.process_approved_actions()
        
        if processed:
            print(f"Processed {len(processed)} approved action(s):")
            for p in processed:
                print(f"  - {p['file']} ({p['action_type']})")
        else:
            print("No approved actions to process.")
    
    elif args.action == 'stats':
        stats = workflow.get_statistics()
        
        print("=" * 60)
        print("Approval Workflow Statistics")
        print("=" * 60)
        print(f"\nPending: {stats['pending']}")
        print(f"Expired: {stats['expired']}")
        print(f"Approved Today: {stats['approved_today']}")
        print(f"Rejected Today: {stats['rejected_today']}")
        
        if stats['by_action_type']:
            print("\nBy Action Type:")
            for action, count in stats['by_action_type'].items():
                print(f"  {action}: {count}")
    
    elif args.action == 'cleanup':
        print(f"Cleaning up approvals older than {args.days} days...")
        moved = workflow.cleanup_expired(args.days)
        
        if moved:
            print(f"Moved {len(moved)} expired file(s) to /Rejected:")
            for f in moved:
                print(f"  - {f.name}")
        else:
            print("No expired files to clean up.")


if __name__ == '__main__':
    main()
