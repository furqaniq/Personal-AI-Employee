# LinkedIn Poster Workflow - Complete Implementation

## ✅ Workflow Created

A complete automated LinkedIn posting workflow with human-in-the-loop approval has been implemented.

---

## Workflow Steps

### 1. Launch LinkedIn & Detect Login ✅
- Opens browser automatically
- Navigates to LinkedIn login
- Waits for user to log in (2 minute timeout)
- **Auto-detects** successful login by monitoring URL
- Confirms when `/feed/` or `/mynetwork/` is reached

### 2. Generate Post & Save to Pending_Approval ✅
- Analyzes topic to determine content type
- Generates post using templates
- Adds relevant hashtags
- Saves as `.md` file in `Pending_Approval/`

### 3. Show Post in Terminal & Ask Permission ✅
- Displays full post content in terminal
- Shows file location
- Interactive prompt: `yes` / `no` / `edit`
- Edit mode opens file in default editor

### 4. Move to Approved & Post to LinkedIn ✅
- Moves file to `Approved/` folder
- Uses saved LinkedIn session
- Opens post composer automatically
- Types content and clicks Post button
- On success, moves to `Done/`

### 5. Notify After Successful Posting ✅
- Shows success/failure message
- Provides link to view post
- Logs activity to `Logs/` folder
- Clear workflow completion message

---

## Usage

### Quick Start

```bash
cd C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\.qwen\skills\linkedin-poster\scripts

python linkedin_poster_workflow.py "Test post from AI Employee Silver Tier" ^
  --vault "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

### With Content Type

```bash
python linkedin_poster_workflow.py "Q1 revenue milestone" ^
  --type milestone ^
  --vault "C:\Users\Lenovo\OneDrive\Documents\GitHub\Personal-AI-Employee\AI_Employee_Vault"
```

---

## File Structure

```
.qwen/skills/linkedin-poster/
├── SKILL.md (updated with workflow)
├── scripts/
│   ├── linkedin_poster.py (legacy manual mode)
│   ├── linkedin_poster_workflow.py (NEW - automated workflow)
│   └── base_watcher.py
└── references/
    ├── content-templates.md
    └── workflow-guide.md (NEW - complete workflow guide)
```

---

## Features

### ✅ Auto-Detect Login
- Monitors URL every 5 seconds
- Detects `/feed/` or `/mynetwork/` pages
- Confirms with green checkmark
- 2-minute timeout (configurable)

### ✅ Interactive Approval
- Shows full post in terminal
- Three options: approve, reject, edit
- Edit mode opens file in default editor
- Re-review after editing

### ✅ File Movement
- `Pending_Approval/` → Awaiting approval
- `Approved/` → Approved, posting
- `Done/` → Posted successfully
- `Rejected/` → Declined posts

### ✅ Activity Logging
- All actions logged to `Logs/` folder
- JSON format for easy parsing
- Includes timestamps and status
- 500 most recent entries kept

### ✅ Error Handling
- Graceful failure recovery
- Clear error messages
- Retry instructions
- Files preserved on failure

---

## Example Session

```
======================================================================
LINKEDIN POSTER WORKFLOW
Complete Automated Posting with Approval
======================================================================
Topic: Test post from AI Employee
Vault: C:\Users\...\AI_Employee_Vault
======================================================================

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

======================================================================
STEP 2: Generate Post Content
======================================================================

📝 Post generated and saved to:
   C:\Users\...\Pending_Approval\LINKEDIN_POST_1774525000.md

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

Your decision: yes

✅ APPROVED: Moving to Approved folder...

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

---

## Content Templates

### Product Update
```
🚀 Exciting Update!

{topic}

Key highlights:
✅ New feature available now
✅ Improved user experience
✅ Better performance and reliability

#ProductUpdate #Innovation #{hashtag}
```

### Milestone
```
📈 Milestone Alert!

{topic}

This achievement is thanks to:
🎯 Hard work paying off
🎯 Amazing team effort
🎯 Customer support making it possible

#Milestone #Growth #{hashtag}
```

### Industry Insight
```
💡 Industry Insight

{topic}

Key observations:
📊 Market trends shifting
📊 New opportunities emerging
📊 Innovation driving change

#IndustryInsights #ThoughtLeadership #{hashtag}
```

---

## Auto-Detection

The workflow auto-detects content type from keywords:

| Keywords | Type |
|----------|------|
| launch, update, feature, new, test | product_update |
| milestone, achievement, reached, growth | milestone |
| insight, trend, industry, analysis | insight |
| offer, deal, discount, promo | promotion |
| testimonial, success, result, client | testimonial |

---

## Hashtag Suggestions

By industry category:

| Category | Hashtags |
|----------|----------|
| Tech | Technology, AI, Automation, Innovation, SaaS |
| Business | Business, Entrepreneurship, Growth, Strategy, Leadership |
| Marketing | Marketing, DigitalMarketing, ContentMarketing, SEO, SocialMedia |
| General | Business, Innovation, Success, Motivation, Networking |

---

## Troubleshooting

### Login Not Detected
- Navigate to: `https://www.linkedin.com/feed/`
- Wait for full page load
- Check browser console for errors

### Post Button Not Found
- LinkedIn UI may have changed
- Try manual posting: `python linkedin_poster.py post-approved --vault PATH`
- Re-run workflow

### Session Expired
```bash
python linkedin_poster.py --setup-session
```

---

## Files Created

| File | Purpose |
|------|---------|
| `linkedin_poster_workflow.py` | Main workflow script |
| `workflow-guide.md` | Complete usage guide |
| `SKILL.md` | Updated with workflow section |

---

## Next Steps

1. **Test the workflow:**
   ```bash
   python linkedin_poster_workflow.py "Test post" --vault "VAULT_PATH"
   ```

2. **Review generated post** in terminal

3. **Type 'yes'** to approve and publish

4. **View post** on LinkedIn after successful posting

5. **Check logs** in `Logs/` folder

---

*LinkedIn Poster Workflow v1.0*
*Created: 2026-03-26*
*Silver Tier - AI Employee Hackathon*
