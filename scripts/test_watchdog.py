#!/usr/bin/env python3
"""Simple watchdog test to verify file detection is working."""

import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TestHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        print("✓ TestHandler initialized")
    
    def on_created(self, event):
        if event.is_directory:
            return
        print(f"\n{'='*60}")
        print(f"✓ FILE DETECTED: {event.src_path}")
        print(f"{'='*60}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python test_watchdog.py <folder_to_watch>")
        sys.exit(1)
    
    folder = Path(sys.argv[1])
    
    if not folder.exists():
        print(f"ERROR: Folder does not exist: {folder}")
        sys.exit(1)
    
    print(f"Watching folder: {folder}")
    print("Press Ctrl+C to stop")
    print("Drop a file in the folder to test...")
    print()
    
    observer = Observer()
    observer.schedule(TestHandler(), str(folder), recursive=False)
    observer.start()
    print("✓ Observer started - waiting for files...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        observer.stop()
    observer.join()
