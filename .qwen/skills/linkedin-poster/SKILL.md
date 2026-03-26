---
name: linkedin-poster
description: |
  Silver Tier LinkedIn Poster skill for Qwen Code.
  Automatically posts business content to LinkedIn to generate sales leads.
  
  Prerequisites:
  - LinkedIn account with active profile
  - Playwright installed (npm install -g @playwright/mcp)
  - Browser session folder for persistent login
  - Content calendar or topics to post about
  
  Use this skill when:
  - You want to auto-post business updates to LinkedIn
  - You need to generate sales leads through social media
  - You want to maintain consistent LinkedIn presence
  
  ⚠️ WARNING: Respect LinkedIn's Terms of Service. Use responsibly.
  ⚠️ Human-in-the-Loop: All posts require approval before publishing.
---

# LinkedIn Poster Skill

This skill enables Qwen Code to create and post business content to LinkedIn automatically.

## Architecture

```
Qwen Code → Content Generator → Approval Request → Human Approves → LinkedIn Post
                                      ↓
                              Pending_Approval/
```

## Setup Instructions

### Step 1: Install Playwright

```bash
npm install -g @playwright/mcp
playwright install chromium
```

### Step 2: Install Python Dependencies

```bash
pip install playwright
playwright install chromium
```

### Step 3: First-Time Login

```bash
python scripts/linkedin_poster.py --setup-session
```

## Usage

### Complete Workflow (Recommended) ⭐

This is the automated workflow with login detection and terminal approval:

```bash
cd .qwen/skills/linkedin-poster/scripts

# Run complete workflow (login → generate → approve → post → notify)
python linkedin_poster_workflow.py "Your post topic here" \
  --vault "C:\path\to\AI_Employee_Vault"

# Example
python linkedin_poster_workflow.py "Test post from AI Employee Silver Tier" \
  --vault "C:\Users\...\AI_Employee_Vault"
```

**What it does:**
1. 🌐 Opens browser and navigates to LinkedIn
2. 🔐 Detects when you're logged in (auto-detection)
3. 📝 Generates post based on your topic
4. 💬 Shows post in terminal and asks for permission
5. ✅ On approval: posts to LinkedIn and notifies you
6. 📁 Moves files through workflow: Pending → Approved → Done

### Manual Mode (Legacy)

### Create Post (Draft for Approval)

```bash
python scripts/linkedin_poster.py create \
  --topic "New product launch" \
  --vault "/path/to/vault"
```

### Post Approved Content

```bash
python scripts/linkedin_poster.py post-approved \
  --vault "/path/to/vault"
```

### Schedule Regular Posts

```bash
python scripts/linkedin_poster.py schedule \
  --frequency daily \
  --time "09:00" \
  --vault "/path/to/vault"
```

## Content Types

| Type | Description | Example |
|------|-------------|---------|
| Product Update | New features, launches | "Excited to announce our new AI feature..." |
| Business Milestone | Achievements, metrics | "Reached 1000 customers this month!" |
| Industry Insight | Thought leadership | "3 trends shaping the future of AI..." |
| Customer Success | Testimonials, case studies | "How Company X increased revenue by 50%..." |
| Behind the Scenes | Team, culture | "Meet our amazing development team..." |

## Human-in-the-Loop Pattern

All posts require approval before publishing:

1. **Qwen creates** post content and approval file
2. **Human reviews** content in `Pending_Approval/`
3. **Move to** `Approved/` to publish
4. **LinkedIn Poster** publishes the post
5. **File moved to** `Done/`

## Approval File Example

```markdown
---
type: approval_request
action: linkedin_post
content_type: product_update
created: 2026-03-24T23:00:00Z
status: pending
---

# LinkedIn Post Approval Required

## Content

🚀 Excited to announce our new AI Employee feature!

This Silver Tier update includes:
✅ Gmail integration
✅ LinkedIn monitoring  
✅ Email MCP for sending

#AI #Automation #Productivity

## To Approve

Move this file to `/Approved` folder.

## To Reject

Move to `/Rejected` with reason.
```

## Company Handbook Rules

| Rule | Behavior |
|------|----------|
| Post frequency | Max 2 posts/day |
| Approval required | All posts before publishing |
| Content review | Check for accuracy, tone |
| Hashtags | Max 5 per post |
| Mentions | Require explicit approval |

## Qwen Code Integration

### Generate Post from Business Goals

```bash
qwen --prompt "Create a LinkedIn post about our Q1 revenue growth from Business_Goals.md" \
  --cwd /path/to/vault
```

### Generate Post from Recent Activity

```bash
qwen --prompt "Create a LinkedIn post summarizing this week's completed tasks from /Done folder" \
  --cwd /path/to/vault
```

## Content Templates

### Product Launch

```
🚀 Exciting News!

We're thrilled to announce [Product/Feature Name]!

Key benefits:
✅ [Benefit 1]
✅ [Benefit 2]
✅ [Benefit 3]

Ready to get started? [Link]

#ProductLaunch #Innovation #[YourIndustry]
```

### Business Milestone

```
📈 Milestone Alert!

We just reached [achievement]!

This wouldn't be possible without:
- Our amazing team
- Our loyal customers
- [Other factors]

Thank you for being part of our journey!

#Milestone #Growth #Grateful
```

### Industry Insight

```
💡 Industry Insight

[Observation about industry trend]

Here's what we're seeing:
1. [Trend 1]
2. [Trend 2]
3. [Trend 3]

What's your take on this?

#IndustryInsights #ThoughtLeadership #[YourIndustry]
```

## Posting Best Practices

| Do | Don't |
|----|-------|
| Post consistently (1-2x/day) | Spam with multiple posts/day |
| Use relevant hashtags (3-5) | Overuse hashtags (10+) |
| Engage with comments | Post and disappear |
| Share valuable content | Only promotional content |
| Use images when possible | Text-only posts always |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Login required | Run with `--setup-session` flag |
| Post fails | Check session is valid |
| Content rejected | Review LinkedIn community guidelines |
| Rate limited | Reduce posting frequency |

## Security Notes

- **Never share** your LinkedIn session
- Add session path to `.gitignore`
- Always require human approval before posting
- Review content for accuracy

## File Structure

```
.qwen/skills/linkedin-poster/
├── SKILL.md (this file)
├── scripts/
│   ├── linkedin_poster.py
│   └── base_watcher.py
└── references/
    ├── content-templates.md
    └── posting-best-practices.md
```

---

*Silver Tier Skill v0.1 - For use with AI Employee Hackathon*
