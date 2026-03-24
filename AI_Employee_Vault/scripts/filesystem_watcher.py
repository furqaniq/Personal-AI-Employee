#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File System Watcher - Monitors a drop folder for new files.

This is the Bronze Tier watcher - simple, reliable, and easy to test.
When you drop any file into the Inbox folder, this watcher will:
1. Detect the new file
2. Create an action file in Needs_Action
3. Trigger Claude Code to process it

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop_folder

Example:
    python filesystem_watcher.py "C:\Users\...\AI_Employee_Vault" "C:\Users\...\Inbox"
"""

import time
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

# Import base class
from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class FileDropHandler(FileSystemEventHandler):
    """Handles file system events for the drop folder."""
    
    def __init__(self, vault_path: str, logger: logging.Logger):
        super().__init__()
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logger = logger
        self.processed_files: set = set()
    
    def sanitize_filename(self, name: str) -> str:
        """Sanitize string for use in filenames."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name.strip()
    
    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Skip markdown files (they're already action files)
        if file_path.suffix == '.md':
            return
        
        # Skip hidden files
        if file_path.name.startswith('.'):
            return
        
        self.logger.info(f'New file detected: {file_path.name}')
        self.create_action_file(file_path)
    
    def create_action_file(self, file_path: Path) -> Path:
        """Create an action file for the dropped file."""
        timestamp = datetime.now().isoformat()
        file_id = self.sanitize_filename(f"{file_path.stem}_{int(time.time())}")
        
        # Get file info
        try:
            file_size = file_path.stat().st_size
        except Exception:
            file_size = 0
        
        content = f"""---
type: file_drop
original_name: {file_path.name}
size: {file_size}
received: {timestamp}
status: pending
priority: medium
---

# File Drop for Processing

**Original File:** `{file_path.name}`
**Size:** {file_size} bytes
**Received:** {timestamp}

## Content

A new file has been dropped for AI processing.

## Suggested Actions

- [ ] Review file content
- [ ] Determine required action
- [ ] Execute action or create plan
- [ ] Move to /Done when complete

## Notes

*This file was automatically created by File System Watcher*
"""
        
        filepath = self.needs_action / f'FILE_{file_id}.md'
        filepath.write_text(content)
        self.logger.info(f'Action file created: {filepath.name}')
        return filepath


class FileSystemWatcher(BaseWatcher):
    """
    File System Watcher using watchdog library.
    
    Monitors a folder for new files and creates action files in the vault.
    """
    
    def __init__(self, vault_path: str, drop_folder: str, check_interval: int = 30):
        super().__init__(vault_path, check_interval)
        self.drop_folder = Path(drop_folder)
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        self.handler = FileDropHandler(vault_path, self.logger)
        self.observer = None
    
    def check_for_updates(self) -> list:
        """
        Check for existing unprocessed files (fallback method).
        The main detection is done via event handler.
        """
        # This is a fallback - real-time detection is via watchdog events
        items = []
        for file_path in self.drop_folder.iterdir():
            if file_path.is_file() and file_path.suffix not in ['.md', '.tmp']:
                file_id = f"{file_path.stem}_{int(file_path.stat().st_mtime)}"
                if file_id not in self.handler.processed_files:
                    items.append(file_path)
                    self.handler.processed_files.add(file_id)
        return items
    
    def create_action_file(self, item) -> Path:
        """Delegate to handler."""
        return self.handler.create_action_file(item)
    
    def run(self):
        """Run the watcher with real-time event monitoring."""
        self.logger.info(f'Starting FileSystemWatcher')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Drop folder: {self.drop_folder}')
        
        # Set up the observer
        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.drop_folder), recursive=False)
        self.observer.start()
        self.logger.info('Watching for new files... (Press Ctrl+C to stop)')
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info('Stopping watcher...')
            self.observer.stop()
        except Exception as e:
            self.logger.error(f'Error: {e}')
            self.observer.stop()
        
        self.observer.join()
        self.logger.info('Watcher stopped')


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("File System Watcher - AI Employee Bronze Tier")
        print("=" * 60)
        print()
        print("Usage:")
        print("  python filesystem_watcher.py <vault_path> [drop_folder]")
        print()
        print("Arguments:")
        print("  vault_path   - Path to your Obsidian vault")
        print("  drop_folder  - Path to folder to watch (default: vault/Inbox)")
        print()
        print("Examples:")
        print('  python filesystem_watcher.py "C:\\Users\\...\\AI_Employee_Vault"')
        print('  python filesystem_watcher.py "C:\\Users\\...\\AI_Employee_Vault" "C:\\Users\\...\\Inbox"')
        print()
        print("How it works:")
        print("  1. Drop any file into the drop folder")
        print("  2. Watcher creates an action file in Needs_Action/")
        print("  3. Claude Code processes the action file")
        print("  4. Task is moved to Done/ when complete")
        print()
        sys.exit(1)
    
    vault_path = sys.argv[1]
    drop_folder = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Validate vault path
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    watcher = FileSystemWatcher(vault_path, drop_folder)
    watcher.run()
