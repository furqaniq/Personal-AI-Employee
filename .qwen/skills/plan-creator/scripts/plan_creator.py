#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Plan Creator - Creates and manages Plan.md files for complex tasks.

Silver Tier implementation for AI Employee Hackathon.
Implements the "Qwen Reasoning Loop" pattern.

Usage:
    python plan_creator.py create --source "file.md" --vault "/path/to/vault"
    python plan_creator.py update --plan "PLAN_xxx.md" --step 3 --status complete
    python plan_creator.py status --plan "PLAN_xxx.md" --vault "/path/to/vault"
    python plan_creator.py report --vault "/path/to/vault"
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Plan templates by type
PLAN_TEMPLATES = {
    'email_response': {
        'steps': [
            'Read email content',
            'Identify sender and context',
            'Determine response type',
            'Draft response',
            'Request approval (if new contact)',
            'Send email',
            'Log activity'
        ]
    },
    'file_processing': {
        'steps': [
            'Read file content',
            'Identify file type',
            'Extract relevant information',
            'Determine required actions',
            'Execute actions',
            'Create summary report',
            'Move to Done'
        ]
    },
    'invoice_generation': {
        'steps': [
            'Read client information',
            'Calculate invoice amount',
            'Generate invoice PDF',
            'Create email draft',
            'Request approval',
            'Send email after approval',
            'Log transaction',
            'Move to Done'
        ]
    },
    'general': {
        'steps': [
            'Understand task requirements',
            'Gather necessary information',
            'Identify required actions',
            'Execute actions',
            'Verify completion',
            'Document results',
            'Move to Done'
        ]
    }
}

# Keywords to detect plan type
PLAN_TYPE_KEYWORDS = {
    'email_response': ['email', 'reply', 'respond', 'message'],
    'file_processing': ['file', 'document', 'process', 'analyze'],
    'invoice_generation': ['invoice', 'payment', 'bill', 'receipt']
}


class PlanCreator:
    """
    Plan Creator for managing complex task plans.
    """

    def __init__(self, vault_path: str):
        """
        Initialize Plan Creator.
        
        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = logging.getLogger('PlanCreator')
        
        # Vault folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.logs = self.vault_path / 'Logs'
        
        # Ensure folders exist
        for folder in [self.needs_action, self.done, self.plans, 
                       self.pending_approval, self.approved, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

    def detect_plan_type(self, source_content: str) -> str:
        """
        Detect plan type from source content.
        
        Args:
            source_content: Content of the source file
            
        Returns:
            Plan type string
        """
        content_lower = source_content.lower()
        
        for plan_type, keywords in PLAN_TYPE_KEYWORDS.items():
            if any(kw in content_lower for kw in keywords):
                return plan_type
        
        return 'general'

    def create_plan(self, source_file: str, objective: str = None, 
                    priority: str = 'medium') -> Path:
        """
        Create a new plan from a source file.
        
        Args:
            source_file: Name of source file in Needs_Action
            objective: Plan objective (auto-detected if not provided)
            priority: Plan priority (low, medium, high)
            
        Returns:
            Path to created plan file
        """
        source_path = self.needs_action / source_file
        
        if not source_path.exists():
            # Try Plans folder
            source_path = self.plans / source_file
        
        if not source_path.exists():
            raise FileNotFoundError(f'Source file not found: {source_file}')
        
        # Read source content
        content = source_path.read_text(encoding='utf-8')
        
        # Detect plan type
        plan_type = self.detect_plan_type(content)
        
        # Get template
        template = PLAN_TEMPLATES.get(plan_type, PLAN_TEMPLATES['general'])
        
        # Auto-detect objective if not provided
        if not objective:
            # Use first line or file name
            first_line = content.split('\n')[0].strip()
            if first_line.startswith('#'):
                objective = first_line[1:].strip()
            else:
                objective = f"Process {source_file}"
        
        # Generate steps markdown
        steps_md = '\n'.join([f'- [ ] {step}' for step in template['steps']])
        
        # Create approval table if needed
        approval_steps = self._identify_approval_steps(plan_type, content)
        approval_md = ''
        if approval_steps:
            approval_md = '| Step | Action | Status |\n|------|--------|--------|\n'
            for step in approval_steps:
                approval_md += f'| {step["num"]} | {step["action"]} | Pending |\n'
        
        timestamp = datetime.now().isoformat()
        plan_id = f"PLAN_{int(datetime.now().timestamp())}"
        
        plan_content = f"""---
type: plan
created: {timestamp}
status: in_progress
priority: {priority}
objective: {objective}
source_file: {source_file}
plan_type: {plan_type}
---

# Plan: {objective}

## Objective

{objective}

## Context

Plan created from source file: {source_file}

## Steps

{steps_md}

## Approval Required

{approval_md if approval_md else 'No approval required for this plan.'}

## Notes

*Plan created by Plan Creator skill*
*Update progress as steps are completed*

## Progress

| Timestamp | Step | Status | Notes |
|-----------|------|--------|-------|
| {timestamp} | 0 | Started | Plan created |
"""
        
        filepath = self.plans / f'{plan_id}.md'
        filepath.write_text(plan_content, encoding='utf-8')
        
        self.logger.info(f'Plan created: {filepath.name}')
        return filepath

    def _identify_approval_steps(self, plan_type: str, content: str) -> List[Dict]:
        """Identify steps that require approval."""
        approvals = []
        
        # Common approval triggers
        if plan_type == 'email_response':
            if 'new contact' in content.lower() or 'unknown' in content.lower():
                approvals.append({'num': 5, 'action': 'Email send (new contact)'})
        
        elif plan_type == 'invoice_generation':
            approvals.append({'num': 5, 'action': 'Email send'})
        
        elif plan_type == 'file_processing':
            if 'delete' in content.lower() or 'remove' in content.lower():
                approvals.append({'num': 5, 'action': 'File deletion'})
        
        return approvals

    def update_progress(self, plan_file: str, step: int, status: str,
                       notes: str = '') -> Path:
        """
        Update plan progress.
        
        Args:
            plan_file: Name of plan file
            step: Step number to update
            status: Step status (complete, in_progress, blocked)
            notes: Optional notes
            
        Returns:
            Path to updated plan file
        """
        plan_path = self.plans / plan_file
        
        if not plan_path.exists():
            raise FileNotFoundError(f'Plan not found: {plan_file}')
        
        content = plan_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Update step checkbox
        timestamp = datetime.now().isoformat()
        
        # Find and update the step in ## Steps section
        in_steps = False
        step_count = 0
        for i, line in enumerate(lines):
            if line.strip() == '## Steps':
                in_steps = True
                continue
            if in_steps and line.startswith('##'):
                in_steps = False
            if in_steps and line.strip().startswith('- [ ]'):
                step_count += 1
                if step_count == step:
                    if status == 'complete':
                        lines[i] = line.replace('- [ ]', '- [x]')
                    elif status == 'in_progress':
                        lines[i] = line.replace('- [ ]', '- [>]')
                    break
        
        # Add progress entry
        in_progress = False
        for i, line in enumerate(lines):
            if line.strip() == '## Progress':
                in_progress = True
                # Find the table end
                j = i + 1
                while j < len(lines) and (lines[j].startswith('|') or lines[j].strip() == ''):
                    j += 1
                # Insert new row
                status_emoji = {'complete': '✅', 'in_progress': '🔄', 'blocked': '🚫'}.get(status, '⏳')
                new_row = f'| {timestamp} | {step} | {status_emoji} {status} | {notes} |'
                lines.insert(j, new_row)
                break
        
        # Update status in frontmatter if all steps complete
        if self._all_steps_complete('\n'.join(lines)):
            content_str = '\n'.join(lines)
            content_str = content_str.replace('status: in_progress', 'status: complete')
            lines = content_str.split('\n')
        
        # Write updated content
        updated_content = '\n'.join(lines)
        plan_path.write_text(updated_content, encoding='utf-8')
        
        self.logger.info(f'Plan progress updated: {plan_file}, step {step} = {status}')
        return plan_path

    def _all_steps_complete(self, content: str) -> bool:
        """Check if all steps are complete."""
        incomplete = content.count('- [ ]')
        in_progress = content.count('- [>]')
        return incomplete == 0 and in_progress == 0

    def get_plan_status(self, plan_file: str) -> Dict:
        """
        Get plan status summary.
        
        Args:
            plan_file: Name of plan file
            
        Returns:
            Dictionary with plan status
        """
        plan_path = self.plans / plan_file
        
        if not plan_path.exists():
            return {'error': f'Plan not found: {plan_file}'}
        
        content = plan_path.read_text(encoding='utf-8')
        
        # Parse frontmatter
        status = {
            'file': plan_file,
            'objective': '',
            'status': '',
            'priority': '',
            'total_steps': 0,
            'completed_steps': 0,
            'pending_steps': 0
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
                        if key in status:
                            status[key] = value
        
        # Count steps
        status['completed_steps'] = content.count('- [x]')
        status['in_progress_steps'] = content.count('- [>]')
        status['pending_steps'] = content.count('- [ ]')
        status['total_steps'] = status['completed_steps'] + status['in_progress_steps'] + status['pending_steps']
        
        # Calculate completion percentage
        if status['total_steps'] > 0:
            status['completion_pct'] = round(
                (status['completed_steps'] / status['total_steps']) * 100, 1
            )
        else:
            status['completion_pct'] = 0
        
        return status

    def get_all_plans(self) -> List[Dict]:
        """Get status of all plans."""
        plans = []
        
        if self.plans.exists():
            for file_path in self.plans.iterdir():
                if file_path.is_file() and file_path.suffix == '.md':
                    status = self.get_plan_status(file_path.name)
                    status['path'] = str(file_path)
                    plans.append(status)
        
        # Sort by priority and completion
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        plans.sort(key=lambda x: (
            priority_order.get(x.get('priority', 'medium'), 1),
            -x.get('completion_pct', 0)
        ))
        
        return plans

    def complete_plan(self, plan_file: str) -> Path:
        """
        Mark plan as complete and move to Done.
        
        Args:
            plan_file: Name of plan file
            
        Returns:
            Path to plan in Done folder
        """
        plan_path = self.plans / plan_file
        
        if not plan_path.exists():
            raise FileNotFoundError(f'Plan not found: {plan_file}')
        
        # Update status to complete
        content = plan_path.read_text(encoding='utf-8')
        content = content.replace('status: in_progress', 'status: complete')
        
        # Add completion timestamp
        timestamp = datetime.now().isoformat()
        if '## Progress' in content:
            content = content.replace(
                '## Progress',
                f'## Progress\n\n**Completed:** {timestamp}\n'
            )
        
        plan_path.write_text(content, encoding='utf-8')
        
        # Move to Done
        dest = self.done / plan_file
        plan_path.rename(dest)
        
        self.logger.info(f'Plan completed: {dest.name}')
        return dest

    def log_activity(self, action: str, details: str, status: str = 'info'):
        """Log an activity."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.json'
        
        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text(encoding='utf-8'))
            except:
                pass
        
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'action_type': action,
            'details': details,
            'status': status,
            'component': 'plan_creator'
        })
        
        logs = logs[-500:]
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Plan Creator - AI Employee Silver Tier')
    parser.add_argument('action', 
                       choices=['create', 'update', 'status', 'report', 'complete'],
                       help='Action to perform')
    parser.add_argument('--source', help='Source file name (for create)')
    parser.add_argument('--plan', help='Plan file name')
    parser.add_argument('--step', type=int, help='Step number (for update)')
    parser.add_argument('--status', help='Step status (for update)')
    parser.add_argument('--notes', help='Notes (for update)')
    parser.add_argument('--objective', help='Plan objective (for create)')
    parser.add_argument('--priority', default='medium', 
                       choices=['low', 'medium', 'high'],
                       help='Plan priority (for create)')
    parser.add_argument('--vault', help='Path to Obsidian vault')
    
    args = parser.parse_args()
    
    if not args.vault:
        parser.error("--vault is required")
    
    creator = PlanCreator(args.vault)
    
    if args.action == 'create':
        if not args.source:
            parser.error("--source is required for create action")
        
        filepath = creator.create_plan(
            args.source,
            objective=args.objective,
            priority=args.priority
        )
        print(f"Plan created: {filepath}")
        print(f"Location: {filepath}")
    
    elif args.action == 'update':
        if not args.plan or args.step is None or not args.status:
            parser.error("--plan, --step, and --status are required for update")
        
        filepath = creator.update_progress(
            args.plan,
            args.step,
            args.status,
            notes=args.notes or ''
        )
        print(f"Plan updated: {filepath}")
    
    elif args.action == 'status':
        if not args.plan:
            parser.error("--plan is required for status")
        
        status = creator.get_plan_status(args.plan)
        
        print("=" * 60)
        print(f"Plan: {status.get('file', 'Unknown')}")
        print("=" * 60)
        print(f"Objective: {status.get('objective', 'N/A')}")
        print(f"Status: {status.get('status', 'N/A')}")
        print(f"Priority: {status.get('priority', 'N/A')}")
        print(f"Progress: {status.get('completed_steps', 0)}/{status.get('total_steps', 0)} ({status.get('completion_pct', 0)}%)")
        
        if status.get('completed_steps') == status.get('total_steps'):
            print("\n✅ Plan complete!")
    
    elif args.action == 'report':
        plans = creator.get_all_plans()
        
        print("=" * 60)
        print("All Plans Status Report")
        print("=" * 60)
        
        if not plans:
            print("No plans found.")
        else:
            for plan in plans:
                status_icon = {'complete': '✅', 'in_progress': '🔄', 'blocked': '🚫'}.get(
                    plan.get('status', 'in_progress'), '📋'
                )
                print(f"\n{status_icon} {plan.get('file', 'Unknown')}")
                print(f"   Objective: {plan.get('objective', 'N/A')}")
                print(f"   Priority: {plan.get('priority', 'N/A')}")
                print(f"   Progress: {plan.get('completed_steps', 0)}/{plan.get('total_steps', 0)} ({plan.get('completion_pct', 0)}%)")
    
    elif args.action == 'complete':
        if not args.plan:
            parser.error("--plan is required for complete")
        
        filepath = creator.complete_plan(args.plan)
        print(f"Plan completed and moved to Done: {filepath}")


if __name__ == '__main__':
    main()
