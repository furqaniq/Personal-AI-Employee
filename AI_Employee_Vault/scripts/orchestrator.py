#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator - Master process for AI Employee Bronze Tier.

This script:
1. Watches the Needs_Action folder for new items
2. Triggers Claude Code to process pending items
3. Updates the Dashboard.md with recent activity
4. Manages the overall workflow

Usage:
    python orchestrator.py /path/to/vault

Example:
    python orchestrator.py "C:\Users\...\AI_Employee_Vault"
"""

import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List
import time
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Orchestrator:
    """Main orchestrator for AI Employee Bronze Tier."""
    
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
        
        self.logger.info(f'Orchestrator initialized for vault: {vault_path}')
    
    def get_pending_items(self) -> List[Path]:
        """Get list of pending action files."""
        items = []
        if self.needs_action.exists():
            for file_path in self.needs_action.iterdir():
                if file_path.is_file() and file_path.suffix == '.md':
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
    
    def trigger_claude(self, prompt: str) -> bool:
        """
        Trigger Claude Code to process items.
        
        Args:
            prompt: The prompt to send to Claude
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info('Triggering Claude Code...')
        
        try:
            # Build the claude command
            # Note: This assumes claude is in PATH and configured
            cmd = [
                'claude',
                '--prompt', prompt,
                '--cwd', str(self.vault_path)
            ]
            
            # For Bronze tier, we'll use a simpler approach
            # Just log what Claude should do
            self.logger.info(f'Would run: {" ".join(cmd)}')
            self.logger.info(f'Prompt: {prompt}')
            
            # In Bronze tier, we create a state file for Claude
            state_file = self.plans / f'ORCHESTRATOR_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            state_file.write_text(f"""---
type: orchestrator_state
created: {datetime.now().isoformat()}
status: pending
---

# Claude Code Task

**Prompt:** {prompt}

**Instructions:**
1. Read all files in /Needs_Action
2. Process each item according to Company_Handbook.md
3. Create plans in /Plans as needed
4. Request approval for sensitive actions
5. Move completed items to /Done
6. Update Dashboard.md with activity

**Status:** Ready for Claude Code to process

---

*This file was created by Orchestrator to track Claude Code tasks*
""")
            
            self.logger.info(f'State file created: {state_file.name}')
            return True
            
        except FileNotFoundError:
            self.logger.warning('Claude Code not found in PATH. Running in manual mode.')
            self.logger.info('To process items manually, run:')
            self.logger.info(f'  claude --prompt "Process all files in {self.needs_action}" --cwd {self.vault_path}')
            return False
        except Exception as e:
            self.logger.error(f'Error triggering Claude Code: {e}')
            return False
    
    def update_dashboard(self, pending_count: int, completed_count: int):
        """Update the Dashboard.md with current status."""
        if not self.dashboard.exists():
            self.logger.warning('Dashboard.md not found')
            return
        
        try:
            content = self.dashboard.read_text()
            
            # Update timestamp
            content = content.replace(
                'last_updated: 2026-03-24T00:00:00Z',
                f'last_updated: {datetime.now().isoformat()}'
            )
            
            # Update pending count
            if 'Pending Tasks | 0' in content:
                content = content.replace(
                    'Pending Tasks | 0',
                    f'Pending Tasks | {pending_count}'
                )
            
            # Update completed today
            if 'Completed Today | 0' in content:
                content = content.replace(
                    'Completed Today | 0',
                    f'Completed Today | {completed_count}'
                )
            
            self.dashboard.write_text(content)
            self.logger.info('Dashboard updated')
            
        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}')
    
    def log_activity(self, action: str, details: str, status: str = 'info'):
        """Log an activity to the logs folder."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.json'
        
        # Load existing logs or create new
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []
        else:
            logs = []
        
        # Add new log entry
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'action_type': action,
            'details': details,
            'status': status
        })
        
        # Save logs
        log_file.write_text(json.dumps(logs, indent=2))
    
    def process_approved_items(self):
        """Process items that have been approved by human."""
        approved_items = self.get_approved_items()
        
        for item in approved_items:
            self.logger.info(f'Processing approved item: {item.name}')
            
            # Read the approval file
            content = item.read_text()
            
            # Log the approval
            self.log_activity('approval_processed', f'File: {item.name}', 'success')
            
            # Move to Done
            dest = self.done / item.name
            item.rename(dest)
            self.logger.info(f'Moved to Done: {dest.name}')
    
    def run(self):
        """Main run loop."""
        self.logger.info('=' * 60)
        self.logger.info('AI Employee Orchestrator - Bronze Tier')
        self.logger.info('=' * 60)
        self.logger.info(f'Vault: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        self.logger.info('Press Ctrl+C to stop')
        self.logger.info('=' * 60)
        
        try:
            while True:
                # Check for pending items
                pending_items = self.get_pending_items()
                
                if pending_items:
                    self.logger.info(f'Found {len(pending_items)} pending item(s)')
                    
                    # Trigger Claude to process
                    prompt = f"""Process all {len(pending_items)} file(s) in /Needs_Action folder.

For each file:
1. Read and understand the content
2. Determine required actions based on Company_Handbook.md
3. Execute simple actions or create approval requests for sensitive actions
4. Move completed items to /Done

Files to process:
{', '.join([f.name for f in pending_items])}
"""
                    self.trigger_claude(prompt)
                    
                    # Mark as processed
                    for item in pending_items:
                        self.processed_files.add(item.name)
                
                # Process approved items
                self.process_approved_items()
                
                # Update dashboard
                self.update_dashboard(len(pending_items), len(self.processed_files))
                
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
        print("AI Employee Orchestrator - Bronze Tier")
        print("=" * 60)
        print()
        print("Usage:")
        print("  python orchestrator.py <vault_path> [check_interval]")
        print()
        print("Arguments:")
        print("  vault_path      - Path to your Obsidian vault")
        print("  check_interval  - Seconds between checks (default: 60)")
        print()
        print("Examples:")
        print('  python orchestrator.py "C:\\Users\\...\\AI_Employee_Vault"')
        print('  python orchestrator.py "C:\\Users\\...\\AI_Employee_Vault" 30')
        print()
        print("What it does:")
        print("  1. Watches /Needs_Action for new items")
        print("  2. Triggers Claude Code to process items")
        print("  3. Processes approved items")
        print("  4. Updates Dashboard.md")
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
