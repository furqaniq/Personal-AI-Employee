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

Location: This file should be in the same scripts/ folder as the watcher scripts.
"""

import time
import logging
import re
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseWatcher(ABC):
    """Abstract base class for all watchers."""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.logs = self.vault_path / 'Logs'
        
        for folder in [self.needs_action, self.done, 
                       self.pending_approval, self.approved, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.processed_items: set = set()

    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        pass

    @abstractmethod
    def create_action_file(self, item: Any) -> Path:
        pass

    def sanitize_filename(self, name: str) -> str:
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip().strip('.')[:100]

    def is_file_ready(self, file_path: Path) -> bool:
        try:
            with open(file_path, 'rb') as f:
                pass
            return True
        except (IOError, PermissionError):
            return False

    def run(self):
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
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise

    def log_activity(self, action_type: str, details: str, status: str = 'info'):
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.json'
        import json
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
            'status': status,
            'watcher': self.__class__.__name__
        })
        logs = logs[-1000:]
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')

    def get_pending_items(self) -> List[Path]:
        items = []
        if self.needs_action.exists():
            for file_path in self.needs_action.iterdir():
                if file_path.is_file() and file_path.suffix == '.md':
                    items.append(file_path)
        return items

    def get_approved_items(self) -> List[Path]:
        items = []
        if self.approved.exists():
            for file_path in self.approved.iterdir():
                if file_path.is_file() and file_path.suffix == '.md':
                    items.append(file_path)
        return items

    def move_to_done(self, source: Path) -> Path:
        if not source.exists():
            raise FileNotFoundError(f'Source file not found: {source}')
        dest = self.done / source.name
        if dest.exists():
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            dest = self.done / f'{source.stem}_{timestamp}{source.suffix}'
        source.rename(dest)
        self.logger.info(f'Moved to Done: {dest.name}')
        return dest


def extract_email_domain(email: str) -> str:
    if '@' not in email:
        return ''
    return email.split('@')[-1].lower()


def is_known_contact(email: str, known_domains: List[str] = None) -> bool:
    if known_domains is None:
        known_domains = []
    domain = extract_email_domain(email)
    return any(known.lower() in domain for known in known_domains)


def determine_priority(content: str, keywords: Dict[str, str] = None) -> str:
    if keywords is None:
        keywords = {
            'urgent': 'high', 'asap': 'high', 'emergency': 'high',
            'invoice': 'high', 'payment': 'high', 'help': 'high',
            'opportunity': 'medium', 'meeting': 'medium',
        }
    text = content.lower()
    for keyword, priority in keywords.items():
        if keyword in text:
            return priority
    return 'medium'
