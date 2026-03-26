# LinkedIn Browser Requirements

## ⚠️ IMPORTANT: No Headless Mode for LinkedIn

**LinkedIn blocks headless browsers** for security and anti-automation reasons.

---

## What is Headless Mode?

**Headless browser** = Browser running without visible UI (in background)

**Visible browser** = Normal browser window you can see and interact with

---

## Why LinkedIn Blocks Headless

1. **Security** - Prevents automated scraping
2. **Anti-bot measures** - Detects automation tools
3. **Terms of Service** - Prohibits automated access
4. **User safety** - Prevents spam and fake accounts

---

## How Our Script Handles This

### ✅ Always Uses Visible Browser

```python
# In linkedin_poster_workflow.py
def _post_to_linkedin(self, content: str) -> bool:
    # ALWAYS VISIBLE (headless=False)
    # LinkedIn blocks headless browsers
    if not self.page:
        self._setup_browser(headless=False)  # ← MUST BE FALSE
```

### ❌ What Doesn't Work

```python
# This will FAIL with LinkedIn
self._setup_browser(headless=True)  # ❌ BLOCKED
```

---

## What You'll See

When posting to LinkedIn, a **visible browser window** will open:

```
======================================================================
STEP 4: Move to Approved & Post to LinkedIn
======================================================================

✅ Moved to Approved: LINKEDIN_POST_1774526205.md

🌐 Posting to LinkedIn...
   Navigating to LinkedIn feed...
   ⚠️  NOTE: Browser is visible - LinkedIn requires this for posting
   Opening post composer...
   Found post trigger with selector: .share-box-feed-entry__trigger
   Waiting for composer to open...
   Typing post content...
   Found input field with selector: div[contenteditable="true"][role="textbox"]
   Waiting for Post button to be enabled...
   Clicking Post button...
   Found Post button with selector: button:has-text("Post")
   Post button enabled: True
   ✅ Post published!
✅ Moved to Done: LINKEDIN_POST_1774526205.md
```

---

## User Experience

### What Happens

1. **Browser opens** - You see it appear
2. **Navigates to LinkedIn** - Automatically goes to feed
3. **Post composer opens** - Window appears
4. **Content is typed** - You can watch it being typed
5. **Post button clicked** - Automatically clicks
6. **Post published** - You see it appear on your feed
7. **Browser closes** - Automatically closes when done

### What You Can Do

- **Watch the process** - Verify what's being posted
- **Intervene if needed** - Close browser to cancel
- **Verify before posting** - See the exact content
- **Manual override** - Take over and post manually if automation fails

---

## Troubleshooting

### "Browser doesn't open"

**Cause:** Script trying to use headless mode

**Solution:**
- Check script has `headless=False`
- Re-run workflow: `python linkedin_poster_workflow.py "topic" --vault "PATH"`

### "LinkedIn detects automation"

**Cause:** LinkedIn's anti-bot detection

**Solution:**
- Use visible browser (already implemented)
- Wait longer between actions (implemented)
- Use saved session cookies (implemented)
- Don't run too frequently (wait 5+ minutes between posts)

### "Post button not clickable"

**Cause:** LinkedIn UI issues

**Solution:**
- Watch the browser window
- If stuck, manually click Post button
- Script will detect and continue
- Or use Ctrl+Enter keyboard shortcut

---

## Best Practices

1. **Don't close browser** - Let automation complete
2. **Watch first post** - Verify it works correctly
3. **Stay nearby** - In case manual intervention needed
4. **Check LinkedIn feed** - Confirm post appeared
5. **Limit frequency** - Max 10-20 posts per day

---

## Alternative: Semi-Automated Workflow

If full automation keeps failing:

### Option 1: Manual Posting

1. Run workflow to generate post
2. Copy content from approval file
3. Open LinkedIn manually
4. Paste and post
5. Move file to Done/

### Option 2: Review Before Posting

1. Run workflow
2. When browser opens, review content
3. Type 'yes' in terminal to confirm
4. Script continues with posting

---

## Security Notes

- **Session saved locally** - Cookies stored in `.creds/linkedin_poster_session/`
- **No credentials stored** - Only session cookies
- **Local execution only** - No cloud services
- **You control posting** - Can cancel anytime

---

## Files Updated

| File | Change |
|------|--------|
| `linkedin_poster_workflow.py` | Forced `headless=False` for LinkedIn |
| `LINKEDIN_BROWSER_REQUIREMENTS.md` | This documentation |

---

*LinkedIn Browser Requirements v1.0*
*Created: 2026-03-26*
*Silver Tier - AI Employee Hackathon*
