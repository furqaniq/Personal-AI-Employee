#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
LinkedIn Watcher - Monitors LinkedIn for notifications using Playwright.

Silver Tier implementation for AI Employee Hackathon.

⚠️ WARNING: Respect LinkedIn's Terms of Service. Use responsibly.

Usage:
    python linkedin_watcher.py /path/to/vault [options]

Example:
    python linkedin_watcher.py "C:/Users/.../AI_Employee_Vault" --interval 300
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Playwright imports
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: Playwright not installed.")
    print("Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# Import base class
from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Keywords for priority detection
PRIORITY_KEYWORDS = ['hiring', 'opportunity', 'job', 'position', 'interview', 'role', 'urgent']

# Target companies (add your own)
TARGET_COMPANIES = []


class LinkedInWatcher(BaseWatcher):
    """
    LinkedIn Watcher using Playwright browser automation.
    
    Monitors LinkedIn for new notifications, connection requests,
    and messages.
    """

    def __init__(self, vault_path: str, check_interval: int = 300, headless: bool = True):
        """
        Initialize the LinkedIn Watcher.
        
        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 300 = 5 min)
            headless: Run browser in headless mode (default: True)
        """
        super().__init__(vault_path, check_interval)
        
        self.headless = headless
        self.session_path = self.vault_path / '.creds' / 'linkedin_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Track processed notifications
        self.processed_file = self.vault_path / '.creds' / 'linkedin_processed.json'
        self.processed = self._load_processed()
        
        # Browser context
        self.context = None
        self.page = None

    def _load_processed(self) -> set:
        """Load previously processed notification IDs."""
        import json
        if self.processed_file.exists():
            try:
                data = json.loads(self.processed_file.read_text(encoding='utf-8'))
                return set(data.get('processed_ids', []))
            except:
                pass
        return set()

    def _save_processed(self):
        """Save processed notification IDs to disk."""
        import json
        # Keep only last 500 IDs
        ids_list = list(self.processed)[-500:]
        self.processed_file.write_text(
            json.dumps({'processed_ids': ids_list, 'updated': datetime.now().isoformat()}, indent=2),
            encoding='utf-8'
        )

    def _setup_browser(self):
        """Set up Playwright browser with persistent context."""
        playwright = sync_playwright().start()
        
        # Launch browser with persistent context
        self.context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.session_path),
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        self.page = self.context.pages[0]
        
        # Set viewport
        self.page.set_viewport_size({'width': 1280, 'height': 720})

    def _is_logged_in(self) -> bool:
        """Check if logged into LinkedIn."""
        try:
            # Navigate to LinkedIn
            self.page.goto('https://www.linkedin.com/feed/', timeout=30000)
            self.page.wait_for_load_state('networkidle')
            
            # Check if we're on feed page (logged in) vs login page
            current_url = self.page.url
            return 'feed' in current_url or 'mynetwork' in current_url
            
        except Exception as e:
            self.logger.warning(f'Error checking login status: {e}')
            return False

    def setup_session(self):
        """Interactive session setup - user logs in manually."""
        print("=" * 60)
        print("LinkedIn Session Setup")
        print("=" * 60)
        print()
        print("A browser window will open.")
        print("1. Navigate to linkedin.com if needed")
        print("2. Log in to your account")
        print("3. Wait for the feed to load")
        print("4. Close this script (Ctrl+C) when done")
        print()
        input("Press Enter to open browser...")
        
        self._setup_browser()
        
        # Navigate to LinkedIn
        self.page.goto('https://www.linkedin.com/')
        
        try:
            # Keep browser open until user interrupts
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSession saved!")
            self.context.close()

    def check_for_updates(self) -> List[Dict]:
        """
        Check for new LinkedIn notifications.
        
        Returns:
            List of notification dictionaries
        """
        notifications = []
        
        try:
            # Ensure browser is set up
            if not self.page:
                self._setup_browser()
            
            # Check if still logged in
            if not self._is_logged_in():
                self.logger.warning('Not logged in to LinkedIn. Please re-authenticate.')
                self.context.close()
                self.context = None
                self.page = None
                return []
            
            # Check notifications
            notifications.extend(self._check_notifications())
            
            # Check connection requests
            notifications.extend(self._check_connections())
            
            # Check messages
            notifications.extend(self._check_messages())
            
            # Filter processed
            new_notifications = []
            for notif in notifications:
                notif_id = notif.get('id')
                if notif_id and notif_id not in self.processed:
                    new_notifications.append(notif)
                    self.processed.add(notif_id)
            
            if new_notifications:
                self._save_processed()
                self.logger.info(f'Found {len(new_notifications)} new notification(s)')
            
            return new_notifications
            
        except Exception as e:
            self.logger.error(f'Error checking LinkedIn: {e}')
            # Try to recover
            if self.context:
                try:
                    self.context.close()
                except:
                    pass
            self.context = None
            self.page = None
            return []

    def _check_notifications(self) -> List[Dict]:
        """Check LinkedIn notifications."""
        results = []
        
        try:
            # Go to notifications page
            self.page.goto('https://www.linkedin.com/notifications/', timeout=30000)
            self.page.wait_for_timeout(3000)  # Wait for content to load
            
            # Find notification elements
            notification_elements = self.page.query_selector_all(
                'div.notification-item, div.scaffold-finite-scroll__content > div'
            )
            
            for i, elem in enumerate(notification_elements[:10]):  # Limit to 10
                try:
                    text = elem.inner_text()
                    if text.strip():
                        results.append({
                            'id': f'notif_{datetime.now().strftime("%Y%m%d%H%M")}_{i}',
                            'type': 'notification',
                            'content': text[:500],
                            'priority': self._determine_priority(text)
                        })
                except:
                    continue
                    
        except Exception as e:
            self.logger.debug(f'Error checking notifications: {e}')
        
        return results

    def _check_connections(self) -> List[Dict]:
        """Check LinkedIn connection requests."""
        results = []
        
        try:
            # Go to my network page
            self.page.goto('https://www.linkedin.com/mynetwork/', timeout=30000)
            self.page.wait_for_timeout(3000)
            
            # Look for pending invitations
            invitations = self.page.query_selector_all(
                'div.invitation-card, button:has-text("Accept")'
            )
            
            for i, elem in enumerate(invitations[:5]):  # Limit to 5
                try:
                    text = elem.inner_text()
                    if text.strip() and 'pending' in text.lower():
                        results.append({
                            'id': f'connect_{datetime.now().strftime("%Y%m%d%H%M")}_{i}',
                            'type': 'connection_request',
                            'content': text[:500],
                            'priority': 'high'
                        })
                except:
                    continue
                    
        except Exception as e:
            self.logger.debug(f'Error checking connections: {e}')
        
        return results

    def _check_messages(self) -> List[Dict]:
        """Check LinkedIn messages."""
        results = []
        
        try:
            # Go to messaging page
            self.page.goto('https://www.linkedin.com/messaging/', timeout=30000)
            self.page.wait_for_timeout(3000)
            
            # Look for unread messages
            unread = self.page.query_selector_all(
                'div.msg-conversations-container__conversation--unread'
            )
            
            for i, elem in enumerate(unread[:5]):  # Limit to 5
                try:
                    text = elem.inner_text()
                    if text.strip():
                        results.append({
                            'id': f'msg_{datetime.now().strftime("%Y%m%d%H%M")}_{i}',
                            'type': 'message',
                            'content': text[:500],
                            'priority': 'high'
                        })
                except:
                    continue
                    
        except Exception as e:
            self.logger.debug(f'Error checking messages: {e}')
        
        return results

    def _determine_priority(self, content: str) -> str:
        """Determine notification priority based on content."""
        text = content.lower()
        
        # Check for priority keywords
        for keyword in PRIORITY_KEYWORDS:
            if keyword in text:
                return 'high'
        
        # Check for target companies
        for company in TARGET_COMPANIES:
            if company.lower() in text:
                return 'high'
        
        return 'medium'

    def create_action_file(self, notification: Dict) -> Path:
        """
        Create an action file for the notification.
        
        Args:
            notification: Notification dictionary
            
        Returns:
            Path to created action file
        """
        timestamp = datetime.now().isoformat()
        notif_type = notification.get('type', 'unknown')
        content = notification.get('content', 'No content')
        priority = notification.get('priority', 'medium')
        
        # Build action file content
        content_text = f"""---
type: linkedin_{notif_type}
received: {timestamp}
priority: {priority}
status: pending
---

# LinkedIn {notif_type.replace('_', ' ').title()}

**Received:** {timestamp}  
**Priority:** {priority}

## Content

{content}

## Suggested Actions

- [ ] Review notification
- [ ] Determine required action
- [ ] Respond if necessary
- [ ] Archive after processing

## Notes

*This file was automatically created by LinkedIn Watcher*
*⚠️ Remember to respect LinkedIn's Terms of Service*
"""
        
        # Write action file
        filepath = self.needs_action / f'LINKEDIN_{notification["id"]}.md'
        filepath.write_text(content_text, encoding='utf-8')
        
        self.logger.info(f'Action file created: {filepath.name}')
        return filepath

    def run(self):
        """Run the LinkedIn watcher."""
        self.logger.info('=' * 60)
        self.logger.info('LinkedIn Watcher - Silver Tier')
        self.logger.info('=' * 60)
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval}s')
        self.logger.info(f'Headless: {self.headless}')
        self.logger.info('Press Ctrl+C to stop')
        self.logger.info('=' * 60)
        
        # Initial browser setup
        self._setup_browser()
        
        try:
            while True:
                items = self.check_for_updates()
                
                for item in items:
                    self.create_action_file(item)
                
                # Wait for next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('LinkedIn Watcher stopped by user')
            if self.context:
                self.context.close()
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            if self.context:
                self.context.close()
            raise


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='LinkedIn Watcher - AI Employee Silver Tier')
    parser.add_argument('vault_path', help='Path to your Obsidian vault')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds (default: 300)')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--setup-session', action='store_true', help='Run interactive session setup')
    
    args = parser.parse_args()
    
    # Validate vault path
    if not Path(args.vault_path).exists():
        print(f"Error: Vault path does not exist: {args.vault_path}")
        sys.exit(1)
    
    if args.setup_session:
        # Interactive session setup
        watcher = LinkedInWatcher(args.vault_path, args.interval, headless=False)
        watcher.setup_session()
    else:
        watcher = LinkedInWatcher(args.vault_path, args.interval, headless=args.headless)
        watcher.run()
