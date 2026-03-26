# Plan Templates Reference

## Standard Plan Structure

Every Plan.md should follow this structure:

```markdown
---
type: plan
created: YYYY-MM-DDTHH:MM:SSZ
status: in_progress
priority: [low|medium|high]
objective: [Clear objective statement]
source_file: [filename.md]
plan_type: [email_response|file_processing|invoice_generation|general]
---

# Plan: [Objective]

## Objective

[Clear statement of what needs to be accomplished]

## Context

[Background information and relevant details]

## Steps

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Approval Required

| Step | Action | Status |
|------|--------|--------|
| X | [Action] | Pending |

## Notes

[Additional information and decisions]

## Progress

| Timestamp | Step | Status | Notes |
|-----------|------|--------|-------|
| ... | ... | ... | ... |
```

---

## Plan Type Templates

### Email Response Plan

```markdown
---
type: plan
objective: Respond to email
plan_type: email_response
---

# Plan: Email Response

## Objective

Read and respond to the email in a professional manner.

## Context

Email received from [sender] regarding [topic].

## Steps

- [ ] Read email content thoroughly
- [ ] Identify sender and relationship
- [ ] Determine appropriate response type
- [ ] Draft response following Company Handbook
- [ ] Request approval (if new contact)
- [ ] Send email after approval
- [ ] Log activity in Logs folder
- [ ] Move email to Done

## Approval Required

| Step | Action | Status |
|------|--------|--------|
| 5 | Email send | [Pending/Complete] |
```

---

### File Processing Plan

```markdown
---
type: plan
objective: Process dropped file
plan_type: file_processing
---

# Plan: File Processing

## Objective

Analyze and process the dropped file appropriately.

## Context

File dropped: [filename]
File type: [pdf|docx|txt|md|etc.]

## Steps

- [ ] Read file content
- [ ] Identify file type and purpose
- [ ] Extract relevant information
- [ ] Determine required actions
- [ ] Execute actions (categorize, summarize, etc.)
- [ ] Create summary report
- [ ] Move original to appropriate folder
- [ ] Move plan to Done

## Approval Required

None (unless file contains sensitive data)
```

---

### Invoice Generation Plan

```markdown
---
type: plan
objective: Generate and send invoice
plan_type: invoice_generation
---

# Plan: Invoice Generation

## Objective

Create and send invoice to client for services rendered.

## Context

Client: [Client Name]
Service: [Service Description]
Amount: $[Amount]

## Steps

- [ ] Read client information from records
- [ ] Verify service completion
- [ ] Calculate invoice amount
- [ ] Generate invoice PDF
- [ ] Create email draft with invoice
- [ ] Request approval (HITL)
- [ ] Send email after approval
- [ ] Log transaction in Accounting
- [ ] Move to Done

## Approval Required

| Step | Action | Status |
|------|--------|--------|
| 6 | Email send | Pending |
```

---

### Multi-Step Business Plan

```markdown
---
type: plan
objective: Complete complex business task
plan_type: general
---

# Plan: [Task Name]

## Objective

[Clear, measurable objective]

## Context

[Background, stakeholders, constraints]

## Steps

### Phase 1: Research
- [ ] Gather requirements
- [ ] Research options
- [ ] Document findings

### Phase 2: Analysis
- [ ] Analyze options
- [ ] Compare pros/cons
- [ ] Make recommendation

### Phase 3: Decision
- [ ] Present to stakeholder
- [ ] Get approval
- [ ] Document decision

### Phase 4: Action
- [ ] Execute decision
- [ ] Monitor progress
- [ ] Report results

### Phase 5: Review
- [ ] Review outcomes
- [ ] Document lessons learned
- [ ] Archive materials

## Approval Required

| Step | Action | Threshold | Status |
|------|--------|-----------|--------|
| 3 | Decision | Cost > $500 | Pending |
| 5 | Action | External comms | Pending |
```

---

## Progress Tracking

### Status Indicators

| Symbol | Meaning |
|--------|---------|
| `- [ ]` | Not started |
| `- [>]` | In progress |
| `- [x]` | Complete |
| `- [-]` | Blocked |

### Progress Table Format

```markdown
| Timestamp | Step | Status | Notes |
|-----------|------|--------|-------|
| 2026-03-24T10:00:00Z | 1 | ✅ Complete | Client found in CRM |
| 2026-03-24T10:05:00Z | 2 | 🔄 In Progress | Calculating amount |
| 2026-03-24T10:10:00Z | 3 | ⏳ Pending | Waiting for approval |
```

---

## Completion Criteria

A plan is complete when:

1. All steps are marked complete (`- [x]`)
2. All approvals obtained
3. All actions executed
4. Progress table updated
5. Status changed to `complete` in frontmatter
6. File moved to `Done/` folder

---

## Best Practices

1. **Clear objectives** - One sentence, actionable
2. **Atomic steps** - Each step independently actionable
3. **Realistic estimates** - Consider time and resources
4. **Approval points** - Mark steps requiring approval
5. **Regular updates** - Update progress after each step
6. **Complete documentation** - Log all decisions and changes

---

*Reference: Plan Templates for Silver Tier*
