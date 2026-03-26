---
type: approval_request
action: send_email
from: test.client@example.com
to: test.client@example.com
subject: Re: Test Email for Workflow
original_file: EMAIL_Test_Workflow_Demo.md
gmail_id: test_12345678901234567890
created: 2026-03-27T01:24:56.896043
status: pending
priority: medium
---

# Email Approval Required

**From:** test.client@example.com  
**Subject:** Test Email for Workflow  
**Date:** Fri, 27 Mar 2026 01:25:00 +0000  
**Created:** 2026-03-27T01:24:56.896043

## Original Email Content

Hello,

I would like to inquire about your services. Can you send me more information about pricing and availability?

Looking forward to your response.

Best regards,
Test Client

---

## Suggested Reply

**To:** test.client@example.com  
**Subject:** Re: Test Email for Workflow

Dear Sender,

Thank you for reaching out!

We have received your email and appreciate you contacting us. A team member will review your message and respond within 24 hours.

Best regards,
AI Employee

---

## To Approve and Send

1. Review the suggested reply above
2. Edit if needed (modify the reply text)
3. Move this file to `/Approved` folder
4. The Email MCP will automatically send the reply

## To Reject

1. Move this file to `/Rejected` folder
2. Add a comment explaining the rejection

## To Edit Reply

1. Modify the "Suggested Reply" section above
2. Save the file
3. Move to `/Approved` when ready to send

---
*This file was created by Orchestrator for human-in-the-loop approval*
*File ID: EMAIL_Test_Workflow_Demo*
