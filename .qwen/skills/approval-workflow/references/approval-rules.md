# Approval Rules Reference

## Overview

This document defines the approval rules for the AI Employee system. All sensitive actions must follow these rules to ensure proper human oversight.

---

## Approval Matrix

### Email Actions

| Scenario | Approval Required | Reason |
|----------|-------------------|--------|
| Reply to known contact | No | Trusted relationship |
| Reply to new contact | Yes | First impression matters |
| Bulk email (>5 recipients) | Yes | Risk of spam |
| Email with attachment | Yes | Security review needed |
| Email about payment | Yes | Financial implications |
| Email about legal matters | Yes | Legal review needed |

---

### LinkedIn Actions

| Scenario | Approval Required | Reason |
|----------|-------------------|--------|
| Post content | Yes | Brand representation |
| Connection request (known company) | No | Trusted network |
| Connection request (unknown) | Yes | Verify legitimacy |
| Comment on post | No | Low risk |
| Direct message | Yes | Personal communication |

---

### Financial Actions

| Amount | Scenario | Approval Required |
|--------|----------|-------------------|
| < $50 | Recurring payment | No |
| < $50 | New payee | Yes |
| $50-$500 | Any payment | Yes |
| > $500 | Any payment | Yes + Documentation |

---

### File Operations

| Operation | Approval Required | Reason |
|-----------|-------------------|--------|
| Create file | No | Low risk |
| Read file | No | Low risk |
| Move file (within vault) | No | Reversible |
| Move file (outside vault) | Yes | Data leaving system |
| Delete file | Yes | Irreversible action |
| Share file externally | Yes | Data privacy |

---

## Risk Assessment Framework

### Risk Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **Low** | Reversible, no financial impact | Reading files, internal moves |
| **Medium** | Reversible, external communication | Emails, social posts |
| **High** | Irreversible or financial impact | Payments, deletions |

### Risk Factors

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| Reversibility | Fully reversible | Partially reversible | Irreversible |
| Financial Impact | $0 | $1-$500 | >$500 |
| External Visibility | Internal | External audience | Public |
| Data Sensitivity | Public data | Internal data | Confidential |

---

## Approval Workflow States

```
┌─────────────────┐
│   Created       │
│   (Pending)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│ Approved│ │ Rejected │
└────┬────┘ └──────────┘
     │
     ▼
┌─────────┐
│ Executed│
│ (Done)  │
└─────────┘
```

---

## Expiry Rules

| Priority | Default Expiry | Escalation |
|----------|---------------|------------|
| High | 4 hours | After 2 hours |
| Medium | 24 hours | After 12 hours |
| Low | 7 days | After 3 days |

### Escalation Process

1. **Initial reminder** at 50% of expiry time
2. **Second reminder** at 75% of expiry time
3. **Escalate** to alternative contact if no response
4. **Auto-reject** after expiry (configurable)

---

## Delegation Rules

### Auto-Approval Conditions

| Condition | Actions |
|-----------|---------|
| Known contact + routine reply | Email send |
| Recurring payment < $50 | Payment processing |
| Connection from known company | LinkedIn accept |
| File move within vault | File operations |

### Never Auto-Approve

- Payments to new payees
- File deletions
- Bulk communications
- Legal document changes
- Credential updates

---

## Audit Requirements

### Required Log Fields

```json
{
  "timestamp": "ISO 8601 timestamp",
  "action_type": "Type of action",
  "actor": "Who initiated",
  "approver": "Who approved (if applicable)",
  "decision_time": "Time to decision",
  "execution_time": "Time to execute",
  "status": "success|failure|rejected"
}
```

### Retention Period

| Log Type | Retention |
|----------|-----------|
| Approval requests | 90 days |
| Approved actions | 1 year |
| Rejected actions | 1 year |
| Audit reports | 3 years |

---

## Exception Handling

### Emergency Approval

For urgent situations:

1. Contact designated approver directly
2. Verbal approval acceptable
3. Document after the fact
4. Create approval file retroactively

### Approval Unavailable

If approver is unavailable:

1. Wait until expiry
2. Escalate to backup approver
3. Document the delay
4. Adjust SLA if needed

---

## Company-Specific Rules

### Known Contacts List

Add your known/trusted contact domains:

```
client.com
partner.com
yourcompany.com
```

### Known Companies

For LinkedIn connection auto-approval:

```
Google
Microsoft
Amazon
[Your target companies]
```

### Payment Thresholds

Adjust based on your business:

| Level | Threshold |
|-------|-----------|
| Auto-approve | < $50 |
| Standard approval | $50 - $500 |
| Enhanced approval | > $500 |

---

## Compliance Notes

1. **GDPR**: All external communications logged
2. **SOX**: Financial approvals retained 7 years
3. **HIPAA**: Health data requires explicit approval
4. **PCI-DSS**: Payment data never stored in plain text

---

*Reference: Approval Rules for Silver Tier*
*Last updated: 2026-03-24*
