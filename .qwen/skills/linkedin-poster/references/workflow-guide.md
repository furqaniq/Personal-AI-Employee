# LinkedIn Poster Workflow Guide

## Overview

The LinkedIn Poster Workflow automates the complete posting process with human-in-the-loop approval:

```
┌─────────────────────────────────────────────────────────────────┐
│                    LINKEDIN POSTER WORKFLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Launch LinkedIn → Detect Login                         │
│           ↓                                                      │
│  Step 2: Generate Post → Save to Pending_Approval               │
│           ↓                                                      │
│  Step 3: Show in Terminal → Ask Permission                      │
│           ↓                                                      │
│  Step 4: Move to Approved → Post to LinkedIn                    │
│           ↓                                                      │
│  Step 5: Notify Success → Move to Done                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\linkedin-poster\scripts

python linkedin_poster_workflow.py "Test post from AI Employee Silver Tier" ^
  --vault "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

---

## Step-by-Step Walkthrough

### Step 1: Launch LinkedIn & Detect Login

**What happens:**
- Browser opens automatically
- Navigates to LinkedIn login page
- Waits for you to log in (up to 2 minutes)
- Auto-detects when you reach `/feed/` page
- Confirms successful login

**Terminal output:**
```
======================================================================
STEP 1: LinkedIn Login & Detection
======================================================================

🌐 Opening browser...
🔐 Navigating to LinkedIn login...

======================================================================
Please log in to LinkedIn in the browser window.
======================================================================

⏳ Waiting for login (up to 2 minutes)...
   Checking every 5 seconds...

✅ Login detected! URL: https://www.linkedin.com/feed/

✅ SUCCESS: Logged in to LinkedIn!
```

---

### Step 2: Generate Post Content

**What happens:**
- Analyzes your topic to determine content type
- Generates post with appropriate template
- Adds relevant hashtags
- Saves as `.md` file in `Pending_Approval/`

**Terminal output:**
```
======================================================================
STEP 2: Generate Post Content
======================================================================

📝 Post generated and saved to:
   C:\Users\...\AI_Employee_Vault\Pending_Approval\LINKEDIN_POST_1774525000.md
```

**Generated file:**
```markdown
---
type: approval_request
action: linkedin_post
content_type: product_update
created: 2026-03-26T16:30:00
status: pending_approval
hashtag: #AI
topic: Test post from AI Employee Silver Tier
---

# LinkedIn Post Approval Required

**Content Type:** Product Update
**Hashtag:** #AI

## Post Content

🚀 Exciting Update!

Test post from AI Employee Silver Tier

Key highlights:
✅ New feature available now
✅ Improved user experience
✅ Better performance and reliability

#ProductUpdate #Innovation #AI
```

---

### Step 3: Show Post & Ask Permission

**What happens:**
- Displays generated post in terminal
- Shows where file is saved
- Asks for approval with interactive prompt
- Options: `yes`, `no`, `edit`

**Terminal output:**
```
======================================================================
STEP 3: Review Post & Grant Permission
======================================================================

📋 GENERATED LINKEDIN POST:
----------------------------------------------------------------------
🚀 Exciting Update!

Test post from AI Employee Silver Tier

Key highlights:
✅ New feature available now
✅ Improved user experience
✅ Better performance and reliability

#ProductUpdate #Innovation #AI
----------------------------------------------------------------------

📁 Saved to: C:\Users\...\Pending_Approval\LINKEDIN_POST_1774525000.md

======================================================================
PERMISSION REQUIRED
======================================================================

Do you want to publish this post to LinkedIn?

  Type 'yes' or 'y' to APPROVE and publish
  Type 'no' or 'n' to REJECT and cancel
  Type 'edit' to modify the post

Your decision: _
```

**Responses:**

| Input | Action |
|-------|--------|
| `yes` or `y` | Approve and continue to posting |
| `no` or `n` | Reject and cancel (moves to Rejected/) |
| `edit` | Opens file in default editor for editing |

**Edit mode:**
```
✏️  EDIT MODE:
Opening: C:\Users\...\Pending_Approval\LINKEDIN_POST_1774525000.md
Edit the file, save it, then type 'done' when ready...

Type 'done' when you've finished editing: _
```

---

### Step 4: Move to Approved & Post

**What happens:**
- Moves approval file to `Approved/` folder
- Uses saved LinkedIn session
- Opens post composer
- Types post content
- Clicks Post button
- On success, moves file to `Done/`

**Terminal output:**
```
======================================================================
STEP 4: Move to Approved & Post to LinkedIn
======================================================================

✅ Moved to Approved: LINKEDIN_POST_1774525000.md

🌐 Posting to LinkedIn...
   Navigating to LinkedIn feed...
   Opening post composer...
   Typing post content...
   Clicking Post button...
   ✅ Post published!
✅ Moved to Done: LINKEDIN_POST_1774525000.md
```

---

### Step 5: Notification

**What happens:**
- Shows success or failure message
- Provides link to view post
- Logs activity to `Logs/` folder

**Terminal output (Success):**
```
======================================================================
STEP 5: Notification
======================================================================

🎉 SUCCESS!

✅ Your post has been published to LinkedIn
✅ Approval file moved to /Done folder
✅ Activity logged

View your post: https://www.linkedin.com/feed/

======================================================================
WORKFLOW COMPLETE
======================================================================
```

**Terminal output (Failure):**
```
======================================================================
STEP 5: Notification
======================================================================

⚠️  POSTING FAILED

❌ The post could not be published to LinkedIn
📁 File remains in /Approved folder for retry

Troubleshooting:
  1. Check LinkedIn session (re-login if needed)
  2. Run: python linkedin_poster.py post-approved --vault VAULT_PATH
```

---

## Command Reference

### Basic Usage

```bash
# Auto-detect content type from topic
python linkedin_poster_workflow.py "Your post topic" --vault "PATH"

# Specify content type
python linkedin_poster_workflow.py "Q1 revenue milestone" --type milestone --vault "PATH"
```

### Content Types

| Type | When to Use | Example Topic |
|------|-------------|---------------|
| `product_update` | New features, launches | "New AI feature released" |
| `milestone` | Achievements, goals | "Reached 1000 customers" |
| `insight` | Industry analysis, trends | "AI trends in 2026" |
| `promotion` | Offers, discounts | "50% off this week" |
| `testimonial` | Customer success | "Client X increased revenue 50%" |

### Auto-Detection Rules

The workflow auto-detects content type from keywords:

| Keywords | Detected Type |
|----------|---------------|
| launch, update, feature, new, test | product_update |
| milestone, achievement, reached, growth | milestone |
| insight, trend, industry, analysis | insight |
| offer, deal, discount, promo | promotion |
| testimonial, success, result, client | testimonial |

---

## File Locations

| File/Location | Purpose |
|---------------|---------|
| `Pending_Approval/LINKEDIN_POST_*.md` | Awaiting approval |
| `Approved/LINKEDIN_POST_*.md` | Approved, ready to post |
| `Done/LINKEDIN_POST_*.md` | Posted successfully |
| `Rejected/LINKEDIN_POST_*.md` | Rejected posts |
| `Logs/YYYY-MM-DD-linkedin.json` | Activity logs |
| `.creds/linkedin_poster_session/` | Browser session |

---

## Troubleshooting

### "Login not detected"

**Symptoms:**
- You logged in but script doesn't detect it
- Timeout after 2 minutes

**Solution:**
1. Make sure you navigate to feed: `https://www.linkedin.com/feed/`
2. Wait for full page load
3. Check browser console for errors

---

### "Post button not found"

**Symptoms:**
- Post composer opens but Post button not clicked

**Solution:**
1. Check LinkedIn UI hasn't changed
2. Try manual posting: `python linkedin_poster.py post-approved --vault PATH`
3. Re-run workflow

---

### "Session expired"

**Symptoms:**
- Browser opens but not logged in

**Solution:**
```bash
# Re-setup session
cd .qwen/skills/linkedin-poster/scripts
python linkedin_poster.py --setup-session
```

---

## Activity Log Format

Logs are saved to `Logs/YYYY-MM-DD-linkedin.json`:

```json
{
  "timestamp": "2026-03-26T16:30:00",
  "action_type": "post_published",
  "details": "Success",
  "status": "success",
  "component": "linkedin_poster_workflow"
}
```

---

## Best Practices

1. **Review before approving** - Always read the generated post
2. **Use edit mode** - Refine content before posting
3. **Check hashtags** - Ensure they're relevant to your industry
4. **Monitor logs** - Review `Logs/` folder regularly
5. **Keep session fresh** - Re-login monthly

---

## Example Sessions

### Example 1: Product Launch

```bash
python linkedin_poster_workflow.py "Excited to announce our new AI Employee Silver Tier with Gmail and LinkedIn integration" --vault "VAULT_PATH"
```

**Generated Post:**
```
🚀 Exciting Update!

Excited to announce our new AI Employee Silver Tier with Gmail and LinkedIn integration

Key highlights:
✅ New feature available now
✅ Improved user experience
✅ Better performance and reliability

#ProductUpdate #Innovation #AI
```

---

### Example 2: Business Milestone

```bash
python linkedin_poster_workflow.py "Reached 1000 GitHub stars on our AI Employee project" --type milestone --vault "VAULT_PATH"
```

**Generated Post:**
```
📈 Milestone Alert!

Reached 1000 GitHub stars on our AI Employee project

This achievement is thanks to:
🎯 Hard work paying off
🎯 Amazing team effort
🎯 Customer support making it possible

#Milestone #Growth #Success
```

---

### Example 3: Industry Insight

```bash
python linkedin_poster_workflow.py "AI automation trends in 2026: What every business should know" --type insight --vault "VAULT_PATH"
```

**Generated Post:**
```
💡 Industry Insight

AI automation trends in 2026: What every business should know

Key observations:
📊 Market trends shifting
📊 New opportunities emerging
📊 Innovation driving change

#IndustryInsights #ThoughtLeadership #AI
```

---

*LinkedIn Poster Workflow Guide v1.0*
*Silver Tier - AI Employee Hackathon*
