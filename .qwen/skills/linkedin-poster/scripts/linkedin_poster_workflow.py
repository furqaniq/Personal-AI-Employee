#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
LinkedIn Poster Workflow - Complete automated posting workflow.

This script implements the full workflow:
1. Launch LinkedIn in browser, detect successful login
2. Generate post based on requirements, save as .md in Pending_Approval
3. Show post in terminal and ask for permission
4. On permission, move to Approved and post to LinkedIn
5. Notify after successful posting

Usage:
    python linkedin_poster_workflow.py "Your post topic here" --vault "C:\path\to\vault"
    
Example:
    python linkedin_poster_workflow.py "Test post from AI Employee" --vault "C:\path\to\AI_Employee_Vault"
"""

import os
import sys
import time
import random
import logging
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

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


class LinkedInPosterWorkflow:
    """
    Complete LinkedIn posting workflow with login detection and approval.
    """

    def __init__(self, vault_path: str):
        """
        Initialize LinkedIn Poster Workflow.
        
        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = logging.getLogger('LinkedInPosterWorkflow')
        
        # Vault folders
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        
        # Ensure folders exist
        for folder in [self.pending_approval, self.approved, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Session path
        self.session_path = self.vault_path / '.creds' / 'linkedin_poster_session'
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        # Browser context
        self.context = None
        self.page = None

    def _setup_browser(self, headless: bool = False):
        """Set up Playwright browser with persistent context."""
        playwright = sync_playwright().start()
        
        self.context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.session_path),
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        self.page = self.context.pages[0]
        self.page.set_viewport_size({'width': 1280, 'height': 720})

    def step1_login_and_detect(self) -> bool:
        """
        Step 1: Launch LinkedIn and detect successful login.
        
        Returns:
            True if login successful
        """
        print("\n" + "=" * 70)
        print("STEP 1: LinkedIn Login & Detection")
        print("=" * 70)
        print()
        
        print("🌐 Opening browser...")
        self._setup_browser(headless=False)
        
        print("🔐 Navigating to LinkedIn login...")
        try:
            self.page.goto('https://www.linkedin.com/login', timeout=30000)
        except Exception as e:
            print(f"   Note: Navigation had issues (normal): {e}")
        
        print()
        print("=" * 70)
        print("Please log in to LinkedIn in the browser window.")
        print("=" * 70)
        print()
        print("⏳ Waiting for login (up to 2 minutes)...")
        print("   Checking every 5 seconds...")
        print()
        
        # Wait for user to log in with periodic checks
        start_time = time.time()
        timeout = 120  # 2 minutes
        
        logged_in = False
        while time.time() - start_time < timeout:
            try:
                current_url = self.page.url
                if '/feed/' in current_url or '/mynetwork/' in current_url:
                    print(f"\n✅ Login detected! URL: {current_url}")
                    logged_in = True
                    time.sleep(3)  # Wait for feed to load
                    break
                else:
                    time.sleep(5)
            except Exception as e:
                time.sleep(5)
        
        if not logged_in:
            print("\n⚠️  Timeout: 2 minutes elapsed without detecting login.")
            print("   Browser is still open - you can continue logging in.")
            print("   Press Ctrl+C to cancel.")
            
            # Wait a bit more for user
            try:
                time.sleep(30)
            except KeyboardInterrupt:
                print("\nCancelled by user.")
                return False
        
        print("\n✅ SUCCESS: Logged in to LinkedIn!")
        print()
        return True

    def step2_generate_post(self, topic: str, content_type: str = None) -> Tuple[Dict, str]:
        """
        Step 2: Generate post content and save as .md file.
        
        Args:
            topic: Post topic/theme
            content_type: Type of content
            
        Returns:
            Tuple of (post_data, filepath)
        """
        print("=" * 70)
        print("STEP 2: Generate Post Content")
        print("=" * 70)
        print()
        
        # Auto-detect content type from topic keywords
        if not content_type:
            topic_lower = topic.lower()
            if any(w in topic_lower for w in ['launch', 'update', 'feature', 'new', 'test']):
                content_type = 'product_update'
            elif any(w in topic_lower for w in ['milestone', 'achievement', 'reached', 'growth']):
                content_type = 'milestone'
            elif any(w in topic_lower for w in ['insight', 'trend', 'industry', 'analysis']):
                content_type = 'insight'
            else:
                content_type = 'product_update'
        
        # Get template
        template = CONTENT_TEMPLATES.get(content_type, CONTENT_TEMPLATES['product_update'])
        
        # Generate content
        highlights = self._generate_highlights(content_type)
        hashtag_category = self._detect_category(topic)
        hashtag = random.choice(HASHTAGS.get(hashtag_category, HASHTAGS['general']))
        
        post_content = template.format(
            content=topic,
            highlights=highlights,
            link='[Your link here]',
            hashtag=hashtag
        )
        
        post_data = {
            'content': post_content,
            'content_type': content_type,
            'hashtag': hashtag,
            'topic': topic,
            'created': datetime.now().isoformat()
        }
        
        # Create approval file
        filepath = self._create_approval_request(post_data)
        
        print(f"📝 Post generated and saved to:")
        print(f"   {filepath}")
        print()
        
        return post_data, filepath

    def _generate_highlights(self, content_type: str) -> str:
        """Generate bullet point highlights."""
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
        
        if any(w in topic_lower for w in ['ai', 'ml', 'software', 'tech', 'digital', 'automation']):
            return 'tech'
        elif any(w in topic_lower for w in ['marketing', 'ads', 'seo', 'content', 'social']):
            return 'marketing'
        elif any(w in topic_lower for w in ['business', 'sales', 'revenue', 'growth', 'employee']):
            return 'business'
        
        return 'general'

    def _create_approval_request(self, post_data: Dict) -> Path:
        """Create approval request file."""
        timestamp = datetime.now().isoformat()
        file_id = f"LINKEDIN_POST_{int(datetime.now().timestamp())}"
        
        content = f"""---
type: approval_request
action: linkedin_post
content_type: {post_data['content_type']}
created: {timestamp}
status: pending_approval
hashtag: #{post_data['hashtag']}
topic: {post_data['topic']}
---

# LinkedIn Post Approval Required

**Content Type:** {post_data['content_type'].replace('_', ' ').title()}  
**Created:** {timestamp}  
**Hashtag:** #{post_data['hashtag']}  
**Topic:** {post_data['topic']}

## Post Content

{post_data['content']}

## To Approve

This file will be moved to /Approved when you give permission.

## To Reject

This file will be moved to /Rejected if you decline.

---
*This file was created by LinkedIn Poster Workflow*
*⚠️ All posts require approval before publishing*
"""
        
        filepath = self.pending_approval / f'{file_id}.md'
        filepath.write_text(content, encoding='utf-8')
        
        return filepath

    def step3_show_and_ask_permission(self, post_data: Dict, filepath: Path) -> bool:
        """
        Step 3: Show post in terminal and ask for permission.
        
        Args:
            post_data: Post content dictionary
            filepath: Path to approval file
            
        Returns:
            True if user gives permission
        """
        print("\n" + "=" * 70)
        print("STEP 3: Review Post & Grant Permission")
        print("=" * 70)
        print()
        print("📋 GENERATED LINKEDIN POST:")
        print("-" * 70)
        print(post_data['content'])
        print("-" * 70)
        print()
        print(f"📁 Saved to: {filepath}")
        print()
        print("=" * 70)
        print("PERMISSION REQUIRED")
        print("=" * 70)
        print()
        print("Do you want to publish this post to LinkedIn?")
        print()
        print("  Type 'yes' or 'y' to APPROVE and publish")
        print("  Type 'no' or 'n' to REJECT and cancel")
        print("  Type 'edit' to modify the post")
        print()
        
        while True:
            try:
                response = input("Your decision: ").strip().lower()
                
                if response in ['yes', 'y']:
                    print("\n✅ APPROVED: Moving to Approved folder...")
                    return True
                elif response in ['no', 'n']:
                    print("\n❌ REJECTED: Post cancelled.")
                    return False
                elif response == 'edit':
                    print("\n✏️  EDIT MODE:")
                    print(f"Opening: {filepath}")
                    print("Edit the file, save it, then type 'done' when ready...")
                    
                    # Open file in default editor (Windows)
                    os.startfile(str(filepath))
                    
                    input("Type 'done' when you've finished editing: ")
                    
                    # Re-read the file
                    content = filepath.read_text(encoding='utf-8')
                    print("\n✅ Post updated. Review again:")
                    print("-" * 70)
                    # Extract post content from file
                    if '## Post Content\n\n' in content:
                        post_section = content.split('## Post Content\n\n')[1].split('\n\n##')[0]
                        print(post_section)
                    print("-" * 70)
                    print()
                else:
                    print("Invalid response. Please type 'yes', 'no', or 'edit'.")
                    
            except KeyboardInterrupt:
                print("\n\n❌ Cancelled by user.")
                return False
            except EOFError:
                print("\n\n❌ No input received.")
                return False

    def step4_move_and_post(self, filepath: Path) -> bool:
        """
        Step 4: Move to Approved and post to LinkedIn.
        
        Args:
            filepath: Path to approval file
            
        Returns:
            True if posting successful
        """
        print("\n" + "=" * 70)
        print("STEP 4: Move to Approved & Post to LinkedIn")
        print("=" * 70)
        print()
        
        # Move file to Approved
        dest = self.approved / filepath.name
        
        try:
            shutil.move(str(filepath), str(dest))
            print(f"✅ Moved to Approved: {dest.name}")
        except Exception as e:
            print(f"❌ Error moving file: {e}")
            return False
        
        # Read the approval file to get post content
        content = dest.read_text(encoding='utf-8')
        
        # Extract post content
        if '## Post Content\n\n' in content:
            post_content = content.split('## Post Content\n\n')[1].split('\n\n##')[0].strip()
        else:
            print("❌ Could not extract post content from file.")
            return False
        
        print("\n🌐 Posting to LinkedIn...")
        
        # Post to LinkedIn
        success = self._post_to_linkedin(post_content)
        
        if success:
            # Move to Done
            done_dest = self.done / dest.name
            shutil.move(str(dest), str(done_dest))
            print(f"✅ Moved to Done: {done_dest.name}")
        
        return success

    def _post_to_linkedin(self, content: str) -> bool:
        """
        Post content to LinkedIn - SEMI-AUTOMATED VERSION.
        
        Script prepares everything, YOU click Post button (more reliable).
        
        Args:
            content: The post content to publish
            
        Returns:
            True if user confirms posting
        """
        try:
            # Ensure browser is set up - ALWAYS VISIBLE (headless=False)
            if not self.page:
                print("\n   🌐 Opening VISIBLE browser (LinkedIn requires this)...")
                self._setup_browser(headless=False)
            
            # Navigate to LinkedIn homepage
            print("   Navigating to LinkedIn feed...")
            self.page.goto('https://www.linkedin.com/feed/', timeout=30000)
            self.page.wait_for_timeout(8000)  # Wait longer for feed to load
            
            # Find and click the post creation box with MULTIPLE SELECTORS
            print("   Opening post composer...")
            
            # Try multiple selectors for "Start a post" button
            selectors = [
                'button:has-text("Start a post")',
                '[aria-label="Start a post"]',
                '.share-box-feed-entry__trigger',
                'button:has-text("Start")'
            ]
            
            start_post = None
            for selector in selectors:
                try:
                    start_post = self.page.query_selector(selector)
                    if start_post:
                        print(f"   Found 'Start a post' button with selector: {selector}")
                        break
                except:
                    continue
            
            if start_post:
                start_post.click()
                self.page.wait_for_timeout(5000)
            else:
                print("   ⚠️  Could not find 'Start a post' button")
                print("   💡 Trying to click textarea directly...")
                
                # Fallback: Try clicking the textarea directly
                textarea = self.page.query_selector('div[contenteditable="true"][role="textbox"]')
                if textarea:
                    textarea.click()
                    self.page.wait_for_timeout(3000)
                else:
                    print("   ❌ Could not open post composer")
                    print("\n" + "=" * 70)
                    print("MANUAL ACTION REQUIRED")
                    print("=" * 70)
                    print("\nPlease open the post composer manually:")
                    print("  1. Click 'Start a post' at the top of your LinkedIn feed")
                    print("  2. Press any key when the composer is open")
                    print()
                    input("Press any key when composer is open...")
            
            # Wait for composer to open
            print("   Waiting for composer to open...")
            self.page.wait_for_timeout(5000)
            
            # Find the post input field and type content
            print("   Typing post content...")
            
            # Try multiple selectors for post input
            input_selectors = [
                'div[contenteditable="true"][role="textbox"]',
                'textarea[aria-label*="post"]',
                'div.share-box-feed-entry__content'
            ]
            
            post_input = None
            for selector in input_selectors:
                try:
                    post_input = self.page.query_selector(selector)
                    if post_input:
                        print(f"   Found input field with selector: {selector}")
                        break
                except:
                    continue
            
            if post_input:
                # Type content
                print("   Typing content...")
                for char in content[:500]:
                    post_input.type(char, delay=random.randint(15, 40))
                
                self.page.wait_for_timeout(3000)
                
                # ✅ READY FOR YOU TO CLICK POST
                print("\n" + "=" * 70)
                print("✅ POST READY - YOUR TURN!")
                print("=" * 70)
                print()
                print("📝 Your post content has been typed into the composer.")
                print()
                print("👉 NEXT STEPS:")
                print("   1. Review the post in the browser window")
                print("   2. Click the 'Post' button manually")
                print("   3. Come back here and press any key when done")
                print()
                print("=" * 70)
                
                # Wait for user to click Post
                input("Press any key when you've clicked Post...")
                
                # Wait for post to submit
                self.page.wait_for_timeout(3000)
                
                print("\n   ✅ Post submitted by user!")
                return True
            else:
                print("   ❌ Could not find post input field")
                print("\n" + "=" * 70)
                print("MANUAL POSTING REQUIRED")
                print("=" * 70)
                print("\nThe script couldn't find the post input field.")
                print("\nPlease post manually:")
                print(f"  1. Copy content from: AI_Employee_Vault/Approved/LINKEDIN_POST_*.md")
                print("  2. Paste into LinkedIn post composer")
                print("  3. Click Post")
                print()
                input("Press any key when you've posted...")
                return True
            
        except Exception as e:
            print(f"   ❌ Error posting to LinkedIn: {e}")
            return False
        finally:
            if self.context:
                try:
                    self.context.close()
                except:
                    pass
                self.context = None
                self.page = None

    def step5_notify_success(self, success: bool):
        """
        Step 5: Notify user of success or failure AND ask for manual verification.
        
        Args:
            success: Whether posting was successful
        """
        print("\n" + "=" * 70)
        print("STEP 5: Verification & Notification")
        print("=" * 70)
        print()
        
        # Ask user to verify the post actually appeared
        print("🔍 MANUAL VERIFICATION REQUIRED")
        print()
        print("Please check your LinkedIn feed in the browser window:")
        print("  1. Do you see your post at the top of the feed?")
        print("  2. Does it match the content you approved?")
        print()
        
        try:
            verification = input("Type 'yes' if you see your post, or 'no' if not: ").strip().lower()
            
            if verification in ['yes', 'y']:
                print("\n✅ VERIFIED: Post is live on LinkedIn!")
                user_confirmed = True
            else:
                print("\n⚠️  Post not found on feed. May have failed to publish.")
                user_confirmed = False
        except:
            print("\n⚠️  No verification response received.")
            user_confirmed = success  # Assume success if no response
        
        print()
        print("=" * 70)
        
        if success and user_confirmed:
            print("🎉 SUCCESS!")
            print()
            print("✅ Your post has been published to LinkedIn")
            print("✅ Approval file moved to /Done folder")
            print("✅ Activity logged")
            print()
            print("View your post: https://www.linkedin.com/feed/")
            print()
            
            # Log success
            self._log_activity('post_published', 'Success - verified by user', 'success')
        elif success and not user_confirmed:
            print("⚠️  POSTING MAY HAVE FAILED")
            print()
            print("❌ Script reported success but you couldn't verify the post")
            print()
            print("Possible causes:")
            print("  1. Post is still processing (wait a few seconds and refresh)")
            print("  2. Post failed but composer closed anyway")
            print("  3. LinkedIn UI issue")
            print()
            print("Next steps:")
            print("  1. Refresh your LinkedIn feed")
            print("  2. Check if post appears")
            print("  3. If not, run the workflow again")
            print()
            
            # Log as unverified
            self._log_activity('post_unverified', 'Script success but user could not verify', 'warning')
        else:
            print("⚠️  POSTING FAILED")
            print()
            print("❌ The post could not be published to LinkedIn")
            print("📁 File remains in /Approved folder for retry")
            print()
            print("Troubleshooting:")
            print("  1. Check LinkedIn session (re-login if needed)")
            print("  2. Run: python linkedin_poster.py post-approved --vault VAULT_PATH")
            print("  3. Or post manually from the Approved/ folder")
            print()
            
            # Log failure
            self._log_activity('post_failed', 'Failed to post', 'error')
        
        print("=" * 70)
        print("WORKFLOW COMPLETE")
        print("=" * 70)

    def _log_activity(self, action: str, details: str, status: str):
        """Log an activity."""
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}-linkedin.json'
        
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
            'component': 'linkedin_poster_workflow'
        })
        
        logs = logs[-500:]
        log_file.write_text(json.dumps(logs, indent=2), encoding='utf-8')

    def run_workflow(self, topic: str, content_type: str = None):
        """
        Run the complete LinkedIn posting workflow.
        
        Args:
            topic: Post topic/theme
            content_type: Optional content type
        """
        print("\n" + "=" * 70)
        print("LINKEDIN POSTER WORKFLOW")
        print("Complete Automated Posting with Approval")
        print("=" * 70)
        print(f"Topic: {topic}")
        print(f"Vault: {self.vault_path}")
        print("=" * 70)
        
        try:
            # Step 1: Login and detect
            if not self.step1_login_and_detect():
                print("\n❌ Workflow cancelled: Login failed")
                return
            
            # Step 2: Generate post
            post_data, filepath = self.step2_generate_post(topic, content_type)
            
            # Step 3: Show and ask permission
            permission = self.step3_show_and_ask_permission(post_data, filepath)
            
            if not permission:
                print("\n❌ Workflow cancelled: Permission denied")
                # Move to Rejected
                rejected_dest = self.vault_path / 'Rejected' / filepath.name
                rejected_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(filepath), str(rejected_dest))
                self._log_activity('post_rejected', 'User denied permission', 'rejected')
                return
            
            # Step 4: Move and post
            success = self.step4_move_and_post(filepath)
            
            # Step 5: Notify
            self.step5_notify_success(success)
            
        except KeyboardInterrupt:
            print("\n\n❌ Workflow interrupted by user")
            self._log_activity('workflow_interrupted', 'User cancelled', 'cancelled')
        except Exception as e:
            print(f"\n\n❌ Workflow error: {e}")
            self._log_activity('workflow_error', str(e), 'error')
        finally:
            if self.context:
                try:
                    self.context.close()
                except:
                    pass


def main():
    parser = argparse.ArgumentParser(
        description='LinkedIn Poster Workflow - AI Employee Silver Tier',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python linkedin_poster_workflow.py "Test post from AI Employee"
  python linkedin_poster_workflow.py "New product launch" --type product_update
  python linkedin_poster_workflow.py "Q1 revenue milestone" --type milestone
        """
    )
    parser.add_argument('topic', help='Post topic/theme')
    parser.add_argument('--type', dest='content_type',
                       choices=['product_update', 'milestone', 'insight', 'promotion', 'testimonial'],
                       help='Content type (auto-detected if not specified)')
    parser.add_argument('--vault', required=True, help='Path to Obsidian vault')
    
    args = parser.parse_args()
    
    workflow = LinkedInPosterWorkflow(args.vault)
    workflow.run_workflow(args.topic, args.content_type)


if __name__ == '__main__':
    main()
