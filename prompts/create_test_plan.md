# Generate Comprehensive QA Test Plan

I need you to create a comprehensive test plan for a JIRA Epic using the qa-analysis-claude project.

## Input Information

**JIRA Epic:** [Epic URL or Key - e.g., https://jira.paysera.net/browse/CORE-5798]

**Related JIRA Tickets:**
- [Ticket URL 1]
- [Ticket URL 2]
- [Ticket URL 3]

**Caused by / Originated from:**
- [Originating ticket URL if applicable]

**Documentation URLs (Optional):**
- Business Requirements: [URL]
- Technical Specifications: [URL]
- Mission/Context Documentation: [URL]
- Research/Analysis Documents: [URL]

**Project Location:** /Users/employee/Projects/qa-analysis-claude

---

## Instructions

### Step 1: Fetch Data
Run the project's Python script to fetch all Jira tickets and documentation:

```bash
cd /Users/employee/Projects/qa-analysis-claude
python3 analyze_ticket.py \
  --jira {EPIC_URL} \
  --linked {LINKED_TICKET_URL_1} {LINKED_TICKET_URL_2} {LINKED_TICKET_URL_3} \
  --confluence {CONFLUENCE_URL_1} {CONFLUENCE_URL_2}
```

### Step 2: Analyze Fetched Data
Read the generated HTML file from `ticket_analysis/` folder to understand:
- Epic scope and objectives
- Related tickets and their relationships
- Business requirements and context
- Technical implementation details
- Regulatory or compliance requirements
- Key stakeholders involved

### Step 3: Create Test Plan
Generate a comprehensive test plan document in **Markdown format first**, then convert to **HTML**.

---

## Test Plan Structure

The test plan must include all of the following sections:

### 1. Introduction
- **1.1 Purpose** - Why this test plan exists
- **1.2 Scope Summary** - High-level overview of what will be tested
- **1.3 Related Tickets** - Links to Epic, user stories, bugs, support tickets
- **1.4 Documentation References** - Links to requirements, specs, confluence pages

### 2. Test Strategy
- **2.1 Testing Approach** - Risk-based, exploratory, regression, compliance
- **2.2 Test Levels** - Unit, Integration, System, UAT (with specific details for each)

### 3. Test Scope
- **3.1 In Scope** - Detailed functional and non-functional areas to be tested
  - 3.1.1 Functional Areas (break down into sub-features)
  - 3.1.2 Non-Functional Areas (performance, security, compliance)
- **3.2 Out of Scope** - Explicitly list what will NOT be tested and why

### 4. Testing Focus Areas (Critical)
Identify 5-7 critical areas requiring special attention. For each:
- Priority level (CRITICAL/HIGH/MEDIUM)
- Why it's critical (business/technical/regulatory impact)
- Specific test focus points
- Risk if not properly tested

### 5. Test Environments
- **5.1 Environment Setup** - Dev, Staging, Production
- **5.2 Test Data Requirements** - Types of data needed
- **5.3 Environment Configuration** - Special configurations

### 6. Entry and Exit Criteria
- **6.1 Entry Criteria** - Checklist of prerequisites before testing starts
- **6.2 Exit Criteria** - Checklist for test completion and sign-off

### 7. Test Deliverables
- **7.1 Before Testing** - Test plan, test cases, scripts, environment docs
- **7.2 During Testing** - Daily reports, defect reports, metrics
- **7.3 After Testing** - Final reports, metrics, UAT sign-off, lessons learned

### 8. Resource Requirements
- **8.1 Human Resources** - Roles, counts, responsibilities
- **8.2 Tools and Infrastructure** - Testing tools, access requirements

### 9. Risks and Mitigation
- Table format with: Risk | Impact | Probability | Mitigation Strategy
- Include contingency plans for high-impact risks

### 10. Test Schedule
- **10.1 Timeline Overview** - Table with phases, durations, dates, owners
- **10.2 Key Milestones** - Important dates and checkpoints

### 11. Communication Plan
- **11.1 Status Reporting** - Daily, weekly, ad-hoc reporting
- **11.2 Stakeholders** - Names, roles, contact info
- **11.3 Escalation Path** - Chain of escalation for issues

### 12. Acceptance Criteria
Define when the feature is considered ready for production:
- Regulatory compliance checkpoints
- Functional completeness criteria
- Quality metrics (defect rates, pass rates, coverage)
- Performance benchmarks
- Required sign-offs

### 13. Assumptions and Dependencies
- **13.1 Assumptions** - What we're assuming to be true
- **13.2 Dependencies** - External blockers or prerequisites

### 14. Approvals
Signature table for:
- QA Lead
- Product Owner
- Development Lead
- Legal/Compliance (if applicable)

### Appendices
- **Appendix A**: Key regulatory/legal requirements (if applicable)
- **Appendix B**: Test coverage summary (number of scenarios per area)

---

## Document Characteristics

The test plan should be:
- **Comprehensive but concise**: Include all sections, but keep descriptions focused
- **Slightly longer than a template**: Add real context and details, not just placeholders
- **Actionable**: Provide specific, testable criteria and concrete dates
- **Risk-focused**: Emphasize critical areas based on business/regulatory/technical impact
- **Professional**: Use proper formatting, tables, and clear language

**Length guideline**: Aim for 10-15 pages when printed, with substantive content in each section.

---

## Output Format

### Step 4: Save Markdown Version
Save the test plan as:
```
ticket_analysis/{EPIC-ID}_Test_Plan.md
```

### Step 5: Convert to HTML
Convert the markdown test plan to a beautiful, responsive HTML document using this template structure:

**HTML Requirements:**
- **Responsive Design**: Works on desktop, tablet, mobile
- **Table of Contents**: Sticky sidebar with anchor links to all sections
- **Modern Styling**: Clean, professional design with good typography
- **Color Coding**:
  - Critical/High priority items: Red/Orange
  - Success criteria: Green
  - Warnings/Risks: Yellow
  - Info boxes: Blue
- **Interactive Elements**: Smooth scrolling, hover effects
- **Print-Friendly**: Can be printed as professional document
- **Professional Tables**: For schedules, risks, resources, approvals

**HTML Color Scheme:**
- Primary: #3498db (blue)
- Success: #27ae60 (green)
- Warning: #f39c12 (orange)
- Danger: #e74c3c (red)
- Dark: #2c3e50 (dark blue)
- Purple: #9b59b6 (purple for special sections)

**Key HTML Components:**
- Sidebar TOC with nested items
- Header with gradient background and metadata
- Section headers with emojis (📋, 🎯, 🔍, ⚠️, etc.)
- Info cards for important callouts
- Focus area boxes for critical testing areas
- Metrics cards for test coverage summary
- Tables for schedules, risks, resources
- Checklist styling for entry/exit criteria
- Status badges (In Scope, Out of Scope, Priority levels)
- Signature table for approvals
- Footer with document control info

Save the HTML version as:
```
ticket_analysis/{EPIC-ID}_Test_Plan.html
```

---

## Example Usage

```markdown
I need you to create a test plan for:

**JIRA Epic:** https://jira.paysera.net/browse/CORE-5798

**Related JIRA Tickets:**
- https://jira.paysera.net/browse/CORE-5806
- https://jira.paysera.net/browse/CORE-5813

**Caused by:**
- https://jira.paysera.net/browse/LW-2028
- https://jira.paysera.net/browse/SUPPORT-103066

**Documentation URLs:**
- Business Requirements: https://intranet.paysera.net/pages/viewpage.action?pageId=341607676
- Technical Specifications: https://intranet.paysera.net/display/NOVA/SUPPORT+103066+...
- Research: https://intranet.paysera.net/pages/viewpage.action?pageId=339771619

In the end, convert the final test plan into an HTML file!
```

---

## Quality Checklist

Before finalizing, verify:
- [ ] All 14 main sections are included
- [ ] Each section has substantive content (not just placeholders)
- [ ] Critical testing focus areas are identified with clear justification
- [ ] Risks are realistic and mitigation strategies are practical
- [ ] Timeline is realistic with proper phase overlap
- [ ] Stakeholders are identified with contact info
- [ ] Acceptance criteria are specific and measurable
- [ ] HTML formatting is professional and responsive
- [ ] Both .md and .html files are generated
- [ ] Document metadata is complete (version, date, approvals)

---

## Notes

- **Do NOT create test cases** - This is a test plan, not test case documentation
- **Focus on strategy and approach** - Not detailed step-by-step test execution
- **Include regulatory/compliance sections** - If the feature has legal requirements
- **Be specific with metrics** - Use actual numbers (e.g., ">80% coverage", "<5 min execution time")
- **Reference real stakeholders** - Use names from Jira comments/tickets
- **Realistic timelines** - Base durations on similar past projects

---

## Template Style Reference

For HTML styling, use a similar approach to the QA Analysis Report template found in:
`.claude/qa-analysis.md`

Key differences from QA Analysis Report:
- Test Plan focuses on **planning and strategy** (future-looking)
- QA Analysis focuses on **completed work analysis** (retrospective)
- Test Plan has **schedule, resources, and approvals**
- QA Analysis has **test cases generated and root cause analysis**

Both should maintain:
- Professional design with sidebar TOC
- Responsive layout
- Color-coded sections
- Clear typography
- Print-friendly styling

---

**Generated by:** qa-analysis-claude
**Template Version:** 1.0
**Last Updated:** February 5, 2026
