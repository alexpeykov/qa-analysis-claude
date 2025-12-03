# Simple Prompt for Claude (No Script Required)

If you want to manually provide information to Claude without using the script, use this prompt template:

---

# QA Analysis Request

You are a Quality Assurance Analysis expert. Please analyze the following ticket information and generate:

1. **Executive Summary** - Overview of the ticket, changes, and impact
2. **Test Ideas** - 10-15 creative test scenarios covering functional, edge cases, integration, security, performance, etc.
3. **Detailed Test Cases** - 8-12 comprehensive test cases with:
   - Test case ID and title
   - Priority level
   - Preconditions
   - Step-by-step test instructions
   - Test data
   - Expected results
   - Acceptance criteria

## Input Information

### Jira Ticket
**URL**: [paste Jira ticket URL]

**Summary**: [paste ticket summary]

**Description**: [paste ticket description]

**Comments**:
[paste any important comments]

**Linked Tickets**:
[paste information about linked tickets if any]

---

### Merge Request (if applicable)
**URL**: [paste MR URL]

**Title**: [paste MR title]

**Description**: [paste MR description]

**Code Changes**: [paste or describe key code changes]

**Discussions**: [paste important MR comments/discussions]

---

### Documentation (if applicable)
**URL**: [paste Confluence/doc URL]

**Content**: [paste relevant documentation]

---

Please provide comprehensive QA analysis based on the above information.

---

## Instructions for Use

1. Copy this template
2. Fill in all the relevant information from your Jira ticket, GitLab MR, and documentation
3. Paste the completed prompt to Claude
4. Receive your comprehensive QA analysis

## Tip

For better results, use the automated script (`qa_analyze.py`) which fetches all information automatically and formats it properly for Claude analysis.
