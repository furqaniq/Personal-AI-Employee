#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Base Watcher - Abstract base class for all AI Employee watchers.

Location: This file should be in the same scripts/ folder as the watcher scripts.
"""

import time
import logging
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any


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
