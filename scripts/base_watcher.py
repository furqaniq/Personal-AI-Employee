#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Base Watcher - Abstract base class for all AI Employee watchers.

This module provides the common interface and functionality for:
- Gmail Watcher
- LinkedIn Watcher
- File System Watcher
- Future watchers (WhatsApp, Bank, etc.)

All watchers inherit from this base class to ensure consistent behavior.
"""

import time
import logging
import re
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseWatcher(ABC):
    """
    Abstract base class for all watchers.
    
    Provides common functionality:
    - Vault path management
    - Needs_Action folder creation
    - Logging setup
    - Filename sanitization
    - Action file creation pattern
    """

    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the base watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        
        # Vault folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.logs = self.vault_path / 'Logs'
        
        # Ensure all folders exist
        for folder in [self.needs_action, self.done, 
                       self.pending_approval, self.approved, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Track processed items (to be managed by subclasses)
        self.processed_items: set = set()

    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        """
        Check for new items to process.
        
        Returns:
            List of new items (emails, notifications, files, etc.)
        """
        pass

    @abstractmethod
    def create_action_file(self, item: Any) -> Path:
        """
        Create an action file for the item.
        
        Args:
            item: The item to process
            
        Returns:
            Path to the created action file
        """
        pass

    def sanitize_filename(self, name: str) -> str:
        """
        Sanitize a string for use in filenames.
        
        Args:
            name: The string to sanitize
            
        Returns:
            Sanitized filename-safe string
        """
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        
        # Remove leading/trailing spaces and dots
        name = name.strip().strip('.')
        
        # Limit length
        if len(name) > 100:
            name = name[:100]
        
        return name

    def is_file_ready(self, file_path: Path) -> bool:
        """
        Check if a file is fully written (not being copied).
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file is ready to read
        """
        try:
            with open(file_path, 'rb') as f:
                pass
            return True
        except (IOError, PermissionError):
            return False

    def run(self):
        """
        Main run loop for the watcher.
        
        This method:
        1. Logs startup information
        2. Enters infinite loop
        3. Checks for updates at intervals
        4. Creates action files for new items
        5. Handles errors gracefully
        """
        self.logger.info('=' * 60)
        self.logger.info(f'{self.__class__.__name__} - Silver Tier')
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
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise

    def log_activity(self, action_type: str, details: str, status: str = 'info'):
        """
        Log an activity to the logs folder.
        
        Args:
            action_type: Type of action (email, linkedin, file, etc.)
            details: Details of the action
            status: Status (info, success, warning, error)
        """
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.json'
        
        import json
        
        # Load existing logs
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text(encoding='utf-8'))
            except:
                logs = []
        else:
            logs = []
        
        # Add new log entry
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'details': details,
            'status': status,
            'watcher': self.__class__.__name__
        })
        
        # Save logs (keep last 1000 entries)
        logs = logs[-1000:]
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')

    def get_pending_items(self) -> List[Path]:
        """
        Get list of pending action files.
        
        Returns:
            List of Path objects for pending files
        """
        items = []
        if self.needs_action.exists():
            for file_path in self.needs_action.iterdir():
                if file_path.is_file() and file_path.suffix == '.md':
                    items.append(file_path)
        return items

    def get_approved_items(self) -> List[Path]:
        """
        Get list of approved action files.
        
        Returns:
            List of Path objects for approved files
        """
        items = []
        if self.approved.exists():
            for file_path in self.approved.iterdir():
                if file_path.is_file() and file_path.suffix == '.md':
                    items.append(file_path)
        return items

    def move_to_done(self, source: Path) -> Path:
        """
        Move a file to the Done folder.
        
        Args:
            source: Path to the source file
            
        Returns:
            Path to the destination file
        """
        if not source.exists():
            raise FileNotFoundError(f'Source file not found: {source}')
        
        dest = self.done / source.name
        
        # Handle duplicate names
        if dest.exists():
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            dest = self.done / f'{source.stem}_{timestamp}{source.suffix}'
        
        source.rename(dest)
        self.logger.info(f'Moved to Done: {dest.name}')
        return dest

    def create_approval_request(self, action_type: str, details: Dict[str, Any], 
                                reason: str = None) -> Path:
        """
        Create an approval request file.
        
        Args:
            action_type: Type of action (send_email, payment, etc.)
            details: Dictionary of action details
            reason: Reason approval is needed
            
        Returns:
            Path to created approval file
        """
        timestamp = datetime.now().isoformat()
        file_id = f"{action_type.upper()}_{int(datetime.now().timestamp())}"
        
        # Default reason if not provided
        if not reason:
            reason = "Action requires human review before execution"
        
        # Build details section
        details_text = '\n'.join([f'**{k.replace("_", " ").title()}:** {v}' 
                                   for k, v in details.items()])
        
        content = f"""---
type: approval_request
action: {action_type}
created: {timestamp}
status: pending
reason: {reason}
---

# Approval Required

**Action:** {action_type.replace('_', ' ').title()}  
**Created:** {timestamp}

## Details

{details_text}

## Why Approval is Needed

{reason}

## To Approve

Move this file to `/Approved` folder.

## To Reject

Move this file to `/Rejected` folder with reason.

---
*This file was created by {self.__class__.__name__} for human-in-the-loop approval*
"""
        
        filepath = self.pending_approval / f'{file_id}.md'
        filepath.write_text(content, encoding='utf-8')
        
        self.logger.info(f'Approval request created: {filepath.name}')
        return filepath


# Utility functions for watchers

def extract_email_domain(email: str) -> str:
    """Extract domain from email address."""
    if '@' not in email:
        return ''
    return email.split('@')[-1].lower()


def is_known_contact(email: str, known_domains: List[str] = None) -> bool:
    """
    Check if email is from a known contact.
    
    Args:
        email: Email address to check
        known_domains: List of known domains
        
    Returns:
        True if from known contact
    """
    if known_domains is None:
        known_domains = []
    
    domain = extract_email_domain(email)
    return any(known.lower() in domain for known in known_domains)


def determine_priority(content: str, keywords: Dict[str, str] = None) -> str:
    """
    Determine priority based on content keywords.
    
    Args:
        content: Text content to analyze
        keywords: Dictionary of keyword -> priority level
        
    Returns:
        Priority level (high, medium, low)
    """
    if keywords is None:
        keywords = {
            'urgent': 'high',
            'asap': 'high',
            'emergency': 'high',
            'invoice': 'high',
            'payment': 'high',
            'help': 'high',
            'opportunity': 'medium',
            'meeting': 'medium',
        }
    
    text = content.lower()
    
    for keyword, priority in keywords.items():
        if keyword in text:
            return priority
    
    return 'medium'
