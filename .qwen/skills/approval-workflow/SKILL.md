---
name: approval-workflow
description: |
  Silver Tier Approval Workflow skill for Qwen Code.
  Manages human-in-the-loop (HITL) approval for sensitive actions.
  
  Prerequisites:
  - Obsidian vault with proper folder structure
  - Qwen Code installed and configured
  - Company_Handbook.md with approval rules
  
  Use this skill when:
  - Sensitive actions require human approval
  - You need audit trail for decisions
  - Multiple approval levels are needed
  - Compliance requires human oversight
  
  This skill implements the standard HITL pattern.
---

# Approval Workflow Skill

This skill manages human-in-the-loop approval for sensitive actions.

## Architecture

```
Action Needed → Create Approval Request → Pending_Approval/
                                              ↓
                                        Human Reviews
                                              ↓
                    ┌─────────────────────────┴─────────────────────────┐
                    ↓                                                   ↓
              Move to Approved                                    Move to Rejected
                    ↓                                                   ↓
            Execute Action                                      Log & Notify
                    ↓
              Move to Done
```

## Vault Folder Structure

```
AI_Employee_Vault/
├── Pending_Approval/     # Awaiting human decision
├── Approved/             # Approved, ready to execute
├── Rejected/             # Rejected with reason
├── Done/                 # Completed actions
└── Logs/                 # Audit trail
```

## Approval Request Format

Every approval request follows this standard format:

```markdown
---
type: approval_request
action: send_email
created: 2026-03-24T23:45:00Z
status: pending
priority: high
expires: 2026-03-25T23:45:00Z
reason: New contact requires approval
---

# Approval Required: Send Email

**Action:** Send Email  
**Created:** 2026-03-24T23:45:00Z  
**Priority:** High  
**Expires:** 2026-03-25T23:45:00Z  

## Action Details

**To:** newcontact@example.com  
**Subject:** Project Proposal  
**Body:** [Email content]

## Why Approval is Needed

Recipient is not in known contacts list.
First-time communication requires human review.

## Risk Assessment

| Factor | Level |
|--------|-------|
| Reversibility | Reversible |
| Financial Impact | None |
| External Communication | Yes |

## To Approve

1. Review the action details above
2. Move this file to `/Approved` folder
3. The system will automatically execute the action

## To Reject

1. Move this file to `/Rejected` folder
2. Add a comment explaining the rejection

## To Request Changes

1. Add comments to this file
2. Move back to `/Needs_Action` for revision

---
*This file was created by Approval Workflow for human-in-the-loop approval*
```

## Usage

### Create Approval Request

```bash
python scripts/approval_workflow.py create \
  --action "send_email" \
  --details '{"to": "user@example.com", "subject": "Hello"}' \
  --reason "New contact" \
  --vault "/path/to/vault"
```

### Check Pending Approvals

```bash
python scripts/approval_workflow.py pending --vault "/path/to/vault"
```

### Process Approved Actions

```bash
python scripts/approval_workflow.py process --vault "/path/to/vault"
```

### Get Approval Statistics

```bash
python scripts/approval_workflow.py stats --vault "/path/to/vault"
```

## Action Types

| Action | Auto-Approve | Require Approval |
|--------|--------------|------------------|
| Email to known contact | ✅ | - |
| Email to new contact | - | ✅ |
| Payment < $50 | ✅ (recurring) | - |
| Payment > $50 | - | ✅ |
| File delete | - | ✅ |
| LinkedIn post | - | ✅ |
| Connection accept | ✅ (known co.) | ✅ (unknown) |

## Company Handbook Integration

Approval decisions follow rules in `Company_Handbook.md`:

```yaml
Approval Rules:
  Email:
    known_contacts: auto_approve
    new_contacts: require_approval
    bulk_send: require_approval
    
  Payments:
    under_50: auto_if_recurring
    over_50: require_approval
    new_payee: require_approval
    
  Files:
    create_read: auto_approve
    delete: require_approval
    move: auto_approve
```

## Qwen Code Integration

### Create Approval Request

```bash
qwen --prompt "Create approval request for sending email to new client" \
  --cwd /path/to/vault
```

### Check for Approved Actions

```bash
qwen --prompt "Check /Approved folder and process pending actions" \
  --cwd /path/to/vault
```

### Audit Trail

```bash
qwen --prompt "Generate approval audit report from /Logs" \
  --cwd /path/to/vault
```

## Approval Workflow Patterns

### Pattern 1: Simple Approval

```
1. AI creates approval file
2. Human moves to Approved
3. AI executes action
4. File moved to Done
```

### Pattern 2: Approval with Revision

```
1. AI creates approval file
2. Human requests changes
3. AI revises and resubmits
4. Human approves
5. AI executes action
```

### Pattern 3: Escalation

```
1. AI creates approval file
2. No response within 24 hours
3. Escalate to higher priority
4. Notify human via multiple channels
```

## Notification System

### Email Notifications

```markdown
Subject: Approval Required: [Action Type]

An action requires your approval:

- Action: [Type]
- Created: [Timestamp]
- Priority: [Level]
- Expires: [Timestamp]

Review in: /Pending_Approval/[filename].md
```

### Escalation Rules

| Time Since Created | Action |
|-------------------|--------|
| > 1 hour (high priority) | Send reminder |
| > 24 hours | Escalate priority |
| > 48 hours | Multiple notifications |

## Audit Trail

All approval actions are logged:

```json
{
  "timestamp": "2026-03-24T23:45:00Z",
  "action_type": "approval_request",
  "action": "send_email",
  "status": "approved",
  "approved_by": "human",
  "decision_time": "2026-03-25T08:30:00Z",
  "execution_time": "2026-03-25T08:30:15Z"
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Approval not appearing | Check Pending_Approval folder |
| Action not executing | Check Approved folder permissions |
| Audit log missing | Check Logs folder exists |
| Expired approvals | Run cleanup script |

## Best Practices

1. **Clear reasons** - Always explain why approval is needed
2. **Actionable details** - Include all information for decision
3. **Reasonable expiry** - Set appropriate deadlines
4. **Priority levels** - Use high/medium/low appropriately
5. **Audit everything** - Log all decisions and executions

## File Structure

```
.qwen/skills/approval-workflow/
├── SKILL.md (this file)
├── scripts/
│   ├── approval_workflow.py
│   └── base_watcher.py
└── references/
    ├── approval-rules.md
    └── audit-guide.md
```

---

*Silver Tier Skill v0.1 - For use with AI Employee Hackathon*
