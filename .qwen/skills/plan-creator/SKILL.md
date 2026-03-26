---
name: plan-creator
description: |
  Silver Tier Plan Creator skill for Qwen Code.
  Creates structured Plan.md files for complex tasks requiring
  multi-step reasoning and execution.
  
  Prerequisites:
  - Qwen Code installed and configured
  - Obsidian vault with proper folder structure
  - Company_Handbook.md with rules
  
  Use this skill when:
  - Complex tasks require step-by-step planning
  - You need to track task progress
  - Multiple approvals are needed
  - Task involves multiple systems/actions
  
  This skill implements the "Qwen Reasoning Loop" pattern.
---

# Plan Creator Skill

This skill enables Qwen Code to create structured plans for complex tasks.

## Architecture

```
Needs_Action/ → Qwen Code → Plan Creator → Plan.md → Execute Steps → Done/
                                    ↓
                            Pending_Approval/ (if needed)
```

## Plan Structure

Every Plan.md follows this standard format:

```markdown
---
type: plan
created: 2026-03-24T23:30:00Z
status: in_progress
priority: high
objective: Send invoice to Client A
source_file: EMAIL_invoice_request.md
---

# Plan: Send Invoice to Client A

## Objective

Clear statement of what needs to be accomplished.

## Context

Background information and relevant details.

## Steps

- [ ] Step 1: Read client information from CRM
- [ ] Step 2: Calculate invoice amount
- [ ] Step 3: Generate invoice PDF
- [ ] Step 4: Create email draft
- [ ] Step 5: Request approval (HITL)
- [ ] Step 6: Send email after approval
- [ ] Step 7: Log transaction
- [ ] Step 8: Move to Done

## Approval Required

| Step | Action | Status |
|------|--------|--------|
| 5 | Email send | Pending |

## Notes

Additional information and decisions made during execution.

## Progress

| Timestamp | Step | Status | Notes |
|-----------|------|--------|-------|
| 2026-03-24T23:30:00Z | 1 | Complete | Client found |
| 2026-03-24T23:31:00Z | 2 | Complete | Amount: $1,500 |
```

## Usage

### Create Plan from Action File

```bash
python scripts/plan_creator.py create \
  --source "EMAIL_invoice_request.md" \
  --vault "/path/to/vault"
```

### Update Plan Progress

```bash
python scripts/plan_creator.py update \
  --plan "PLAN_invoice_client_a.md" \
  --step 3 \
  --status complete \
  --vault "/path/to/vault"
```

### Get Plan Status

```bash
python scripts/plan_creator.py status \
  --plan "PLAN_invoice_client_a.md" \
  --vault "/path/to/vault"
```

## Qwen Code Integration

### Trigger Plan Creation

```bash
qwen --prompt "Create a plan for processing EMAIL_invoice_request.md in /Needs_Action" \
  --cwd /path/to/vault
```

### Execute Plan Steps

```bash
qwen --prompt "Execute step 3 of PLAN_invoice_client_a.md" \
  --cwd /path/to/vault
```

### Complete Plan

```bash
qwen --prompt "Complete PLAN_invoice_client_a.md and move to /Done" \
  --cwd /path/to/vault
```

## Plan Templates

### Email Response Plan

```markdown
---
type: plan
objective: Respond to email
---

# Plan: Email Response

## Steps
- [ ] Read email content
- [ ] Identify sender and context
- [ ] Determine response type
- [ ] Draft response
- [ ] Request approval (if new contact)
- [ ] Send email
- [ ] Log activity
```

### File Processing Plan

```markdown
---
type: plan
objective: Process dropped file
---

# Plan: File Processing

## Steps
- [ ] Read file content
- [ ] Identify file type
- [ ] Extract relevant information
- [ ] Determine required actions
- [ ] Execute actions
- [ ] Create summary report
- [ ] Move to Done
```

### Multi-Step Business Plan

```markdown
---
type: plan
objective: Complete business task
---

# Plan: Business Task

## Objective
[Clear goal statement]

## Context
[Background and relevant info]

## Steps
- [ ] Research phase
- [ ] Analysis phase
- [ ] Decision phase
- [ ] Action phase
- [ ] Review phase

## Approval Points
| Step | Action | Threshold |
|------|--------|-----------|
| 3 | Decision | Cost > $500 |
| 5 | Action | External communication |
```

## Reasoning Loop Pattern

The Plan Creator implements a reasoning loop:

1. **Read** - Understand the task from source file
2. **Analyze** - Break down into steps
3. **Plan** - Create Plan.md with checkboxes
4. **Execute** - Work through steps
5. **Check** - Verify completion
6. **Loop** - Repeat until all steps complete

## Company Handbook Integration

Plans respect rules in `Company_Handbook.md`:

| Rule | Plan Behavior |
|------|---------------|
| Payment > $500 | Add approval step |
| New contact | Add approval step |
| External action | Add review step |
| Irreversible action | Require explicit approval |

## Approval Workflow Integration

Plans integrate with the approval workflow:

```
Plan.md created
    ↓
Execute steps 1-3 (auto)
    ↓
Step 4 requires approval
    ↓
Create Pending_Approval file
    ↓
Human approves (moves to Approved)
    ↓
Execute step 4
    ↓
Continue remaining steps
    ↓
Move Plan to Done
```

## Progress Tracking

### Update Progress

```bash
python scripts/plan_creator.py update \
  --plan "PLAN_xxx.md" \
  --step 3 \
  --status complete \
  --notes "Invoice generated successfully" \
  --vault "/path/to/vault"
```

### Get Progress Report

```bash
python scripts/plan_creator.py report \
  --vault "/path/to/vault"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Plan not created | Check source file exists |
| Steps not executing | Verify Qwen Code access |
| Approval not working | Check vault path |
| Progress not saving | Check file permissions |

## Best Practices

1. **Clear objectives** - State goal in one sentence
2. **Atomic steps** - Each step should be actionable
3. **Approval points** - Mark steps requiring approval
4. **Progress logging** - Update after each step
5. **Completion criteria** - Define what "done" means

## File Structure

```
.qwen/skills/plan-creator/
├── SKILL.md (this file)
├── scripts/
│   ├── plan_creator.py
│   └── base_watcher.py
└── references/
    ├── plan-templates.md
    └── reasoning-loop-guide.md
```

---

*Silver Tier Skill v0.1 - For use with AI Employee Hackathon*
