---
name: bronze-file-processor
description: |
  Bronze Tier AI Employee skill for processing files in Obsidian vault.
  Reads action files from /Needs_Action, processes them according to
  Company_Handbook.md rules, and moves completed items to /Done.

  Use this skill when:
  - New files appear in /Needs_Action folder
  - You need to process pending tasks
  - You want to generate plans for complex tasks
  - You need to request human approval for sensitive actions
---

# Bronze File Processor Skill

This skill enables Qwen Code to act as an AI Employee for basic file processing tasks.

## Quick Start

```bash
# Process all pending files
qwen --prompt "Process all files in /Needs_Action" --cwd /path/to/vault

# Or use the interactive mode
qwen --cwd /path/to/vault
```

## Workflow

### 1. Read Pending Items

First, check what needs attention:

```
List all files in /Needs_Action folder and read their content.
```

### 2. Process Each Item

For each file:

1. **Read** the file content and frontmatter
2. **Classify** the type and priority
3. **Determine** required actions based on Company_Handbook.md
4. **Execute** simple actions or **request approval** for sensitive ones

### 3. Create Plans (if needed)

For complex tasks, create a plan:

```markdown
---
type: plan
created: 2026-03-24T10:00:00Z
status: in_progress
---

# Plan: [Task Name]

## Objective
[Clear statement of what needs to be accomplished]

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Approval Required
[Yes/No - if yes, create approval request file]
```

### 4. Request Approval (if needed)

For sensitive actions (payments, new contacts, etc.):

```markdown
---
type: approval_request
action: [action_type]
created: 2026-03-24T10:00:00Z
expires: 2026-03-25T10:00:00Z
status: pending
---

# Approval Required

## Action Details
[Full description of what will be done]

## Why Approval is Needed
[Explanation based on Company_Handbook.md rules]

## To Approve
Move this file to /Approved folder.

## To Reject
Move this file to /Rejected folder with reason.
```

### 5. Move to Done

When complete:

```
Move processed file from /Needs_Action to /Done folder.
```

## Rules Reference

### Auto-Approve (No Human Needed)

- File processing and organization
- Reading and summarizing content
- Creating plans
- Responding to known contacts (routine)

### Require Approval

- Sending emails to new contacts
- Any payment or financial transaction
- Deleting files
- Actions with irreversible consequences

## Example Session

```
User: Process all files in /Needs_Action

Assistant: I'll process the pending files. Let me start by reading them.

*Reads files in /Needs_Action*

I found 2 files:
1. FILE_document_1234567890.md - A PDF dropped for processing
2. FILE_notes_1234567891.md - Text file with meeting notes

Processing FILE_document_1234567890.md:
- Type: file_drop
- Action needed: Review and categorize
- This is a routine task, no approval needed

*Processes the file*

Processing FILE_notes_1234567891.md:
- Type: file_drop
- Action needed: Extract action items
- Creating plan for follow-up tasks

*Creates plan and moves files to /Done*

All files processed successfully!
```

## Error Handling

### If File is Unclear

```markdown
---
type: clarification_needed
original_file: FILE_xxx.md
---

# Clarification Required

The file content is unclear. Please provide guidance on:
- [Specific question 1]
- [Specific question 2]

Move to /Inbox when clarified.
```

### If Action Fails

```markdown
---
type: error_log
timestamp: 2026-03-24T10:00:00Z
---

# Action Failed

**File:** FILE_xxx.md
**Attempted Action:** [description]
**Error:** [error message]
**Next Step:** [suggested resolution]
```

## Dashboard Update

After processing, update Dashboard.md:

1. Increment "Completed Today" count
2. Add entry to "Recent Activity" table
3. Update "Pending Tasks" count
4. Set `last_updated` timestamp

## Tips for Success

1. **Always read Company_Handbook.md first** - It contains the rules
2. **Be conservative with approvals** - When in doubt, ask
3. **Log everything** - Future you will thank you
4. **Move files promptly** - Don't leave processed files in Needs_Action
5. **Update Dashboard** - Keep the status current

---

*Bronze Tier Skill v0.1 - For use with AI Employee Hackathon*
