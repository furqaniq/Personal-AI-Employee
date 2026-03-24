#!/usr/bin/env python3
"""Simple file watcher - runs in foreground with immediate output."""

import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SimpleFileHandler(FileSystemEventHandler):
    def __init__(self, vault_path):
        super().__init__()
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        print(f"✓ Handler initialized")
        print(f"  Vault: {self.vault_path}")
        print(f"  Output: {self.needs_action}")
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Skip markdown files
        if file_path.suffix == '.md':
            print(f"⊘ Skipped (markdown): {file_path.name}")
            return
        
        # Skip hidden files
        if file_path.name.startswith('.'):
            return
        
        print(f"\n{'='*60}")
        print(f"✓ NEW FILE DETECTED: {file_path.name}")
        
        # Create action file
        try:
            timestamp = time.strftime('%Y-%m-%dT%H:%M:%S')
            file_id = f"{file_path.stem}_{int(time.time())}"
            
            content = f"""---
type: file_drop
original_name: {file_path.name}
size: {file_path.stat().st_size}
received: {timestamp}
status: pending
---

# File Drop for Processing

**File:** `{file_path.name}`
**Size:** {file_path.stat().st_size} bytes

## Actions
- [ ] Review and process
- [ ] Move to /Done when complete
"""
            
            action_file = self.needs_action / f'FILE_{file_id}.md'
            action_file.write_text(content)
            print(f"✓ ACTION FILE CREATED: {action_file.name}")
        except Exception as e:
            print(f"✗ ERROR: {e}")
        
        print(f"{'='*60}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python simple_watcher.py <vault_path> [drop_folder]")
        sys.exit(1)
    
    vault_path = Path(sys.argv[1])
    drop_folder = Path(sys.argv[2]) if len(sys.argv) > 2 else vault_path / 'Inbox'
    
    if not vault_path.exists():
        print(f"ERROR: Vault not found: {vault_path}")
        sys.exit(1)
    
    if not drop_folder.exists():
        drop_folder.mkdir(parents=True, exist_ok=True)
    
    print("="*60)
    print("Simple File Watcher - AI Employee Bronze Tier")
    print("="*60)
    print(f"Watching: {drop_folder}")
    print(f"Output: {vault_path}/Needs_Action/")
    print("Press Ctrl+C to stop")
    print("="*60)
    print()
    
    handler = SimpleFileHandler(vault_path)
    observer = Observer()
    observer.schedule(handler, str(drop_folder), recursive=False)
    observer.start()
    print("✓ Observer started - waiting for files...\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        observer.stop()
    observer.join()
    print("Done")
