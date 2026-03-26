#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
LinkedIn Poster - Creates and posts business content to LinkedIn.

Silver Tier implementation for AI Employee Hackathon.

⚠️ WARNING: Respect LinkedIn's Terms of Service. Use responsibly.

Usage:
    python linkedin_poster.py create --topic "Product launch" --vault "/path/to/vault"
    python linkedin_poster.py post-approved --vault "/path/to/vault"
    python linkedin_poster.py schedule --frequency daily --time "09:00"
"""

import os
import sys
import time
import random
import logging
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Playwright imports
try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: Playwright not installed.")
    print("Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Content templates
CONTENT_TEMPLATES = {
    'product_update': """🚀 Exciting Update!

{content}

Key highlights:
{highlights}

Learn more: {link}

#ProductUpdate #Innovation #{hashtag}
""",
    
    'milestone': """📈 Milestone Alert!

{content}

This achievement is thanks to:
{highlights}

Thank you for being part of our journey!

#Milestone #Growth #{hashtag}
""",
    
    'insight': """💡 Industry Insight

{content}

Key observations:
{highlights}

What's your take on this?

#IndustryInsights #ThoughtLeadership #{hashtag}
""",
    
    'promotion': """🎯 Special Offer

{content}

Details:
{highlights}

Act now: {link}

#SpecialOffer #Deal #{hashtag}
""",
    
    'testimonial': """⭐ Customer Success

{content}

Results achieved:
{highlights}

Ready for similar results? {link}

#CustomerSuccess #Testimonial #{hashtag}
"""
}

# Hashtag suggestions by industry
HASHTAGS = {
    'tech': ['Technology', 'AI', 'Automation', 'Innovation', 'SaaS'],
    'business': ['Business', 'Entrepreneurship', 'Growth', 'Strategy', 'Leadership'],
    'marketing': ['Marketing', 'DigitalMarketing', 'ContentMarketing', 'SEO', 'SocialMedia'],
    'general': ['Business', 'Innovation', 'Success', 'Motivation', 'Networking']
}


class LinkedInPoster:
    """
    LinkedIn Poster for creating and posting business content.
    """

    def __init__(self, vault_path: str):
        """
        Initialize LinkedIn Poster.
        
        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = logging.getLogger('LinkedInPoster')
        
        # Vault folders
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.logs = self.vault_path / 'Logs'
        
        # Ensure folders exist
        for folder in [self.pending_approval, self.approved, self.done, self.plans, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Session path
        self.session_path = self.vault_path / '.creds' / 'linkedin_poster_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Browser context
        self.context = None
        self.page = None

    def _setup_browser(self):
        """Set up Playwright browser with persistent context."""
        playwright = sync_playwright().start()
        
        self.context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.session_path),
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        self.page = self.context.pages[0]
        self.page.set_viewport_size({'width': 1280, 'height': 720})

    def _is_logged_in(self) -> bool:
        """Check if logged into LinkedIn."""
        try:
            self.page.goto('https://www.linkedin.com/feed/', timeout=30000)
            self.page.wait_for_load_state('networkidle')
            current_url = self.page.url
            return 'feed' in current_url
        except Exception as e:
            self.logger.warning(f'Error checking login status: {e}')
            return False

    def setup_session(self):
        """Interactive session setup - user logs in manually."""
        print("=" * 60)
        print("LinkedIn Poster Session Setup")
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
        self.page.goto('https://www.linkedin.com/')
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nSession saved!")
            self.context.close()

    def create_post_content(self, topic: str, content_type: str = None) -> Dict:
        """
        Create LinkedIn post content.
        
        Args:
            topic: Main topic/theme for the post
            content_type: Type of content (product_update, milestone, etc.)
            
        Returns:
            Dictionary with post content and metadata
        """
        # Auto-detect content type from topic keywords if not specified
        if not content_type:
            topic_lower = topic.lower()
            if any(w in topic_lower for w in ['launch', 'update', 'feature', 'new']):
                content_type = 'product_update'
            elif any(w in topic_lower for w in ['milestone', 'achievement', 'reached', 'growth']):
                content_type = 'milestone'
            elif any(w in topic_lower for w in ['insight', 'trend', 'industry', 'analysis']):
                content_type = 'insight'
            elif any(w in topic_lower for w in ['offer', 'deal', 'discount', 'promo']):
                content_type = 'promotion'
            else:
                content_type = 'product_update'
        
        # Get template
        template = CONTENT_TEMPLATES.get(content_type, CONTENT_TEMPLATES['product_update'])
        
        # Generate content using Qwen-style reasoning
        highlights = self._generate_highlights(topic, content_type)
        hashtag_category = self._detect_category(topic)
        hashtag = random.choice(HASHTAGS.get(hashtag_category, HASHTAGS['general']))
        
        # Fill template
        post_content = template.format(
            content=topic,
            highlights=highlights,
            link='[Your link here]',
            hashtag=hashtag
        )
        
        return {
            'content': post_content,
            'content_type': content_type,
            'hashtag': hashtag,
            'category': hashtag_category,
            'created': datetime.now().isoformat()
        }

    def _generate_highlights(self, topic: str, content_type: str) -> str:
        """Generate bullet point highlights for the post."""
        # Simple template-based generation
        # In production, this would use Qwen Code for better content
        highlights_map = {
            'product_update': [
                "✅ New feature available now",
                "✅ Improved user experience",
                "✅ Better performance and reliability"
            ],
            'milestone': [
                "🎯 Hard work paying off",
                "🎯 Amazing team effort",
                "🎯 Customer support making it possible"
            ],
            'insight': [
                "📊 Market trends shifting",
                "📊 New opportunities emerging",
                "📊 Innovation driving change"
            ],
            'promotion': [
                "💰 Limited time offer",
                "💰 Exclusive discount",
                "💰 Early bird special"
            ],
            'testimonial': [
                "⭐ Outstanding results",
                "⭐ Customer satisfaction",
                "⭐ Proven track record"
            ]
        }
        
        return '\n'.join(highlights_map.get(content_type, highlights_map['product_update']))

    def _detect_category(self, topic: str) -> str:
        """Detect industry category from topic."""
        topic_lower = topic.lower()
        
        if any(w in topic_lower for w in ['ai', 'ml', 'software', 'tech', 'digital']):
            return 'tech'
        elif any(w in topic_lower for w in ['marketing', 'ads', 'seo', 'content']):
            return 'marketing'
        elif any(w in topic_lower for w in ['business', 'sales', 'revenue', 'growth']):
            return 'business'
        
        return 'general'

    def create_approval_request(self, post_data: Dict) -> Path:
        """
        Create an approval request file for the post.
        
        Args:
            post_data: Dictionary with post content and metadata
            
        Returns:
            Path to created approval file
        """
        timestamp = datetime.now().isoformat()
        file_id = f"LINKEDIN_POST_{int(datetime.now().timestamp())}"
        
        content = f"""---
type: approval_request
action: linkedin_post
content_type: {post_data['content_type']}
created: {timestamp}
status: pending
hashtag: #{post_data['hashtag']}
---

# LinkedIn Post Approval Required

**Content Type:** {post_data['content_type'].replace('_', ' ').title()}  
**Created:** {timestamp}  
**Hashtag:** #{post_data['hashtag']}

## Post Content

{post_data['content']}

## To Approve

1. Review the post content above
2. Check for accuracy and tone
3. Move this file to `/Approved` folder to publish
4. The LinkedIn Poster will automatically post

## To Reject

1. Move this file to `/Rejected` folder
2. Add a comment explaining the rejection

## To Edit

1. Copy this file and modify content
2. Delete this file
3. Create new approval request with edited content

---
*This file was created by LinkedIn Poster for human-in-the-loop approval*
*⚠️ All posts require approval before publishing*
"""
        
        filepath = self.pending_approval / f'{file_id}.md'
        filepath.write_text(content, encoding='utf-8')
        
        self.logger.info(f'Approval request created: {filepath.name}')
        return filepath

    def post_to_linkedin(self, content: str) -> bool:
        """
        Post content to LinkedIn.
        
        Args:
            content: The post content to publish
            
        Returns:
            True if successful
        """
        try:
            # Ensure browser is set up
            if not self.page:
                self._setup_browser()
            
            # Check if logged in
            if not self._is_logged_in():
                self.logger.error('Not logged in to LinkedIn')
                return False
            
            # Navigate to LinkedIn homepage
            self.page.goto('https://www.linkedin.com/feed/', timeout=30000)
            self.page.wait_for_timeout(3000)
            
            # Find and click the post creation box
            try:
                # Look for the "Start a post" button
                start_post = self.page.query_selector(
                    'button:has-text("Start a post"), [aria-label="Start a post"]'
                )
                if start_post:
                    start_post.click()
                    self.page.wait_for_timeout(2000)
                else:
                    # Alternative: look for post creation textarea
                    textarea = self.page.query_selector(
                        'div[contenteditable="true"][role="textbox"]'
                    )
                    if textarea:
                        textarea.click()
                        self.page.wait_for_timeout(2000)
            except Exception as e:
                self.logger.warning(f'Could not find post creation button: {e}')
            
            # Find the post input field and type content
            try:
                # Try multiple selectors for the post input
                selectors = [
                    'div[contenteditable="true"][role="textbox"]',
                    'textarea[aria-label*="post"]',
                    'div.share-box-feed-entry__content'
                ]
                
                post_input = None
                for selector in selectors:
                    post_input = self.page.query_selector(selector)
                    if post_input:
                        break
                
                if post_input:
                    # Type content in chunks to avoid detection
                    for char in content[:500]:  # Limit to 500 chars for safety
                        post_input.type(char, delay=random.randint(10, 50))
                        if random.random() < 0.01:  # Random pause
                            time.sleep(random.uniform(0.5, 1.0))
                    
                    self.page.wait_for_timeout(1000)
                    
                    # Find and click the Post button
                    post_button = self.page.query_selector(
                        'button:has-text("Post"), button[aria-label="Post"]'
                    )
                    
                    if post_button:
                        post_button.click()
                        self.page.wait_for_timeout(3000)
                        
                        self.logger.info('Post published successfully!')
                        return True
                    else:
                        self.logger.warning('Post button not found - content may be drafted')
                        return False
                else:
                    self.logger.error('Could not find post input field')
                    return False
                    
            except Exception as e:
                self.logger.error(f'Error posting content: {e}')
                return False
            
        except Exception as e:
            self.logger.error(f'Error posting to LinkedIn: {e}')
            return False
        finally:
            if self.context:
                try:
                    self.context.close()
                except:
                    pass
                self.context = None
                self.page = None

    def process_approved_posts(self) -> List[Path]:
        """
        Process approved posts and publish them.
        
        Returns:
            List of processed file paths
        """
        processed = []
        
        if not self.approved.exists():
            return processed
        
        for file_path in self.approved.iterdir():
            if file_path.is_file() and file_path.suffix == '.md':
                self.logger.info(f'Processing approved post: {file_path.name}')
                
                # Read the approval file
                content = file_path.read_text(encoding='utf-8')
                
                # Extract post content (between ## Post Content and ## To Approve)
                try:
                    start_marker = '## Post Content\n\n'
                    end_marker = '\n\n## To Approve'
                    
                    start_idx = content.find(start_marker) + len(start_marker)
                    end_idx = content.find(end_marker)
                    
                    if start_idx > 0 and end_idx > start_idx:
                        post_content = content[start_idx:end_idx].strip()
                        
                        # Post to LinkedIn
                        success = self.post_to_linkedin(post_content)
                        
                        if success:
                            # Move to Done
                            dest = self.done / file_path.name
                            file_path.rename(dest)
                            processed.append(dest)
                            self.logger.info(f'Post published and moved to Done: {dest.name}')
                        else:
                            self.logger.error(f'Failed to publish post: {file_path.name}')
                    else:
                        self.logger.error(f'Could not extract post content from: {file_path.name}')
                        
                except Exception as e:
                    self.logger.error(f'Error processing {file_path.name}: {e}')
        
        return processed

    def log_activity(self, action: str, details: str, status: str = 'info'):
        """Log an activity."""
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
            'action_type': action,
            'details': details,
            'status': status,
            'component': 'linkedin_poster'
        })
        
        logs = logs[-500:]  # Keep last 500 entries
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='LinkedIn Poster - AI Employee Silver Tier')
    parser.add_argument('action', choices=['create', 'post-approved', 'schedule', 'setup-session'],
                       help='Action to perform')
    parser.add_argument('--topic', help='Topic/theme for the post')
    parser.add_argument('--type', dest='content_type', 
                       choices=['product_update', 'milestone', 'insight', 'promotion', 'testimonial'],
                       help='Type of content')
    parser.add_argument('--vault', help='Path to Obsidian vault')
    parser.add_argument('--frequency', choices=['daily', 'weekly', 'biweekly'],
                       help='Posting frequency')
    parser.add_argument('--time', help='Posting time (HH:MM)')
    
    args = parser.parse_args()
    
    if not args.vault and args.action != 'setup-session':
        parser.error("--vault is required for this action")
    
    poster = LinkedInPoster(args.vault) if args.vault else None
    
    if args.action == 'setup-session':
        if poster:
            poster.setup_session()
        else:
            print("Error: --vault required")
            sys.exit(1)
    
    elif args.action == 'create':
        if not args.topic:
            parser.error("--topic is required for create action")
        
        post_data = poster.create_post_content(args.topic, args.content_type)
        
        print("=" * 60)
        print("Generated LinkedIn Post")
        print("=" * 60)
        print(post_data['content'])
        print()
        
        # Create approval request
        filepath = poster.create_approval_request(post_data)
        print(f"Approval request created: {filepath}")
        print()
        print("To publish this post:")
        print("1. Review the content above")
        print(f"2. Open: {filepath}")
        print("3. Move to /Approved folder to publish")
        
        poster.log_activity('post_created', f'Topic: {args.topic}', 'success')
    
    elif args.action == 'post-approved':
        print("Processing approved posts...")
        processed = poster.process_approved_posts()
        
        if processed:
            print(f"Successfully published {len(processed)} post(s)")
            for p in processed:
                print(f"  - {p.name}")
        else:
            print("No approved posts to process or publishing failed")
        
        poster.log_activity('posts_processed', f'Count: {len(processed)}', 'success')
    
    elif args.action == 'schedule':
        if not args.frequency or not args.time:
            parser.error("--frequency and --time are required for schedule action")
        
        print(f"Scheduled {args.frequency} posting at {args.time}")
        print("Note: Use system scheduler (cron/Task Scheduler) for actual scheduling")
        print()
        print("Example cron entry:")
        print(f"0 {args.time.split(':')[0]} * * * cd /path && python linkedin_poster.py create --topic 'Daily Update' --vault /vault")


if __name__ == '__main__':
    main()
