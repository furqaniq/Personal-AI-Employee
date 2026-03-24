#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Base Watcher - Abstract template for all AI Employee watchers.

All watchers inherit from this base class and implement:
- check_for_updates(): Return list of new items to process
- create_action_file(item): Create .md file in Needs_Action folder

Usage:
    class MyWatcher(BaseWatcher):
        def check_for_updates(self) -> list:
            # Your implementation
            return [item1, item2]
        
        def create_action_file(self, item) -> Path:
            # Your implementation
            return filepath
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseWatcher(ABC):
    """Abstract base class for all watchers."""
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        self.processed_ids: set = set()
        
        # Ensure Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process.
        
        Returns:
            List of new items that need action
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create a markdown action file for an item.
        
        Args:
            item: The item to process
            
        Returns:
            Path to the created file
        """
        pass
    
    def sanitize_filename(self, name: str) -> str:
        """Sanitize string for use in filenames."""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()
    
    def run(self):
        """Main run loop - continuously checks for updates."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    if items:
                        self.logger.info(f'Found {len(items)} new item(s)')
                        for item in items:
                            try:
                                filepath = self.create_action_file(item)
                                self.logger.info(f'Created action file: {filepath.name}')
                            except Exception as e:
                                self.logger.error(f'Error creating action file: {e}')
                except Exception as e:
                    self.logger.error(f'Error in check loop: {e}')
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise


class SimpleWatcher(BaseWatcher):
    """
    A simple concrete implementation for testing.
    Watches a drop folder for new files.
    """
    
    def __init__(self, vault_path: str, drop_folder: Optional[str] = None, check_interval: int = 30):
        super().__init__(vault_path, check_interval)
        self.drop_folder = Path(drop_folder) if drop_folder else self.vault_path / 'Inbox'
        self.drop_folder.mkdir(parents=True, exist_ok=True)
    
    def check_for_updates(self) -> list:
        """Check drop folder for new files."""
        items = []
        for file_path in self.drop_folder.iterdir():
            if file_path.is_file() and file_path.suffix not in ['.md']:
                file_id = f"{file_path.stem}_{int(file_path.stat().st_mtime)}"
                if file_id not in self.processed_ids:
                    items.append(file_path)
                    self.processed_ids.add(file_id)
        return items
    
    def create_action_file(self, file_path: Path) -> Path:
        """Create action file for dropped file."""
        timestamp = datetime.now().isoformat()
        file_id = self.sanitize_filename(f"{file_path.stem}_{int(file_path.stat().st_mtime)}")
        
        content = f"""---
type: file_drop
original_name: {file_path.name}
size: {file_path.stat().st_size}
received: {timestamp}
status: pending
---

# File Drop for Processing

**Original File:** `{file_path.name}`
**Size:** {file_path.stat().st_size} bytes
**Received:** {timestamp}

## Content

File is ready for AI processing.

## Suggested Actions

- [ ] Review file content
- [ ] Process as needed
- [ ] Move to /Done when complete
"""
        
        filepath = self.needs_action / f'FILE_{file_id}.md'
        filepath.write_text(content)
        return filepath


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python base_watcher.py <vault_path> [drop_folder]")
        print("\nExample:")
        print("  python base_watcher.py /path/to/vault")
        print("  python base_watcher.py /path/to/vault /path/to/drop_folder")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    drop_folder = sys.argv[2] if len(sys.argv) > 2 else None
    
    watcher = SimpleWatcher(vault_path, drop_folder)
    watcher.run()
