# Generate QA Test Plan (Paysera Template)

I need you to create a test plan for a JIRA Epic following the Paysera test plan template format.

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

### Step 3: Create Test Plan Markdown
Generate a test plan document in **Markdown format** following the Paysera template structure below.

---

## Test Plan Structure (Paysera Template)

The test plan must follow this exact structure:

### Header Section
```markdown
# Test Plan: [Feature/Epic Name]

**Epic:** [CORE-XXXX](jira_link)
**Date:** [Date]
**Version:** [Version number]
```

### 1. Stakeholders
List all key stakeholders with names and email addresses:
- Product Owner
- Business Analyst
- Legal/Compliance (if applicable)
- Development Lead
- QA Lead

### 2. Testing Objectives
High-level testing goals in bullet format with brief descriptions (5-7 objectives):
- **[Objective Name]** - Brief description of what will be validated
- Example: **Financial Accuracy** - Interest calculations are correct for daily balance tracking, tiered rates, compound interest

### 3. Types of Testing
List testing types that will be performed (4-6 types):
- **Functional** - Brief description
- **Integration** - Brief description
- **Regression** - Brief description
- **Compliance** - Brief description (if applicable)

### 4. Testing Start Criteria
Checklist of prerequisites before testing can begin:
- Development completion requirements
- Environment readiness
- Test data availability
- Documentation approval
- Code coverage requirements

### 5. Testing Completion Criteria
Measurable exit criteria with specific percentages and requirements:
- 100% of critical test cases executed
- 100% of high-priority test cases executed
- ≥95% of medium-priority test cases executed
- ≥80% of low-priority test cases executed
- ≥95% overall test pass rate achieved
- Defect resolution requirements
- Sign-off requirements

### 6. Resource Description

**Personnel:**
- List roles needed with brief responsibilities

**Software:**
- List tools needed with purpose (Jira, TestRail, DBeaver, Postman, browsers, etc.)

### 7. Test Scenarios

**Critical Test Areas** organized by priority:

**1. [Area Name] (Priority: CRITICAL)**
- Bullet list of specific test scenarios
- Focus on what will be tested

**2. [Area Name] (Priority: CRITICAL)**
- Bullet list of specific test scenarios

**3. [Area Name] (Priority: HIGH)**
- Bullet list of specific test scenarios

**4. [Area Name] (Priority: HIGH)**
- Bullet list of specific test scenarios

**5. [Area Name] (Priority: MEDIUM)**
- Bullet list of specific test scenarios

**6. [Area Name] (Priority: MEDIUM)**
- Bullet list of specific test scenarios

**Test Data Requirements:**
- Specific data needs (account types, currencies, edge cases)

### 8. Risk & Mitigation

**Critical Risks:**

Table format:
| Risk | Impact | Mitigation Strategy |
|------|--------|---------------------|
| [Risk name] | CRITICAL/HIGH/MEDIUM | [Strategy] |

**Contingency Plans:**
- Bullet list of contingency plans for major risks

### 9. Defect Tracking & Risk Classes

**Defect Severity Classification:**
- **Critical:** [Examples]
- **High:** [Examples]
- **Medium:** [Examples]
- **Low:** [Examples]

**Risk Classes:**
- **P0 (Blocker):** [When to use] - must be fixed before release
- **P1 (Critical):** [When to use] - must be fixed before release
- **P2 (High):** [When to use] - should be fixed or documented
- **P3 (Medium/Low):** [When to use] - can be deferred

### 10. Testing on Different Platforms

**Mandatory platform testing required for:**
- List specific platforms needed (Internet Banking, Mobile Banking, API, etc.)

**Platforms:**
- Desktop browsers: [List with versions]
- Mobile: [List OS versions]
- API: [Environment details]

### 11. Quality Criteria

Testing quality benchmarks with specific measurable targets:
- **Functional coverage:** ≥X% of planned test scenarios executed
- **Critical/High priority:** 100% test execution
- **[Domain-specific metrics]:** Specific pass rate or criteria
- **Performance:** Specific benchmarks
- **Defect metrics:** Zero critical/high severity defects open at release
- **UAT approval:** Required sign-offs

### 12. Related Documentation

Bullet list with links:
- Business Requirements: [Link]
- Technical Specifications: [Link]
- Regulatory Context: [Link] (if applicable)
- Related Tickets: [Links to all related tickets]

### Footer
```markdown
---

**Document Control:**
- Version: [Version]
- Last Updated: [Date]
- Prepared by: QA Team
```

---

## Document Characteristics

The test plan should be:
- **Concise and focused**: Keep it short (200-250 lines max)
- **Specific to the Epic**: Include real context from the tickets, not generic placeholders
- **Priority-driven**: Organize test scenarios by priority (CRITICAL → HIGH → MEDIUM)
- **Measurable**: Use specific percentages, numbers, and benchmarks
- **Professional**: Use proper markdown formatting and tables

**Length guideline**: Aim for approximately 200-250 lines, similar to a 5-7 page printed document.

---

## Output Format

### Step 4: Save Markdown Version
Save the test plan as:
```
ticket_analysis/{EPIC-ID}_Test_Plan.md
```

### Step 5: Convert to HTML
Convert the markdown test plan to a beautiful, responsive HTML document.

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
- **Professional Tables**: For schedules, risks, resources

**HTML Color Scheme:**
- Primary: #3498db (blue)
- Success: #27ae60 (green)
- Warning: #f39c12 (orange)
- Danger: #e74c3c (red)
- Dark: #2c3e50 (dark blue)
- Purple: #9b59b6 (purple for special sections)

**Key HTML Components:**
- Sidebar TOC with nested items matching the 12 sections
- Header with gradient background and metadata
- Section headers with emojis (📋 Stakeholders, 🎯 Testing Objectives, 🔍 Test Scenarios, ⚠️ Risk & Mitigation, etc.)
- Info cards for important callouts
- Focus area boxes for critical testing areas
- Metrics cards for quality criteria
- Tables for risks, resources, platforms
- Checklist styling for entry/exit criteria
- Status badges (CRITICAL, HIGH, MEDIUM priority levels)
- Footer with document control info

Use the HTML format from: `.claude/qa-analysis.md` template as a reference for styling.

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
- Technical Specifications: https://intranet.paysera.net/display/PDOC/Accruals.+Solution+Proposal
- Research: https://intranet.paysera.net/pages/viewpage.action?pageId=339771619

In the end, convert the final test plan into an HTML file!
```

---

## Quality Checklist

Before finalizing, verify:
- [ ] All 12 main sections are included in order
- [ ] Stakeholders section has real names and emails from Jira
- [ ] Testing Objectives are high-level and focused (5-7 bullets)
- [ ] Test Scenarios are organized by priority (CRITICAL, HIGH, MEDIUM)
- [ ] Exit criteria include specific measurable percentages
- [ ] Risk table uses standard format with Impact and Mitigation columns
- [ ] Quality Criteria has specific numeric benchmarks
- [ ] Document follows Paysera template format exactly
- [ ] Total length is approximately 200-250 lines
- [ ] Both .md and .html files are generated
- [ ] HTML formatting is professional and responsive

---

## Notes

- **Follow Paysera template exactly** - Do not add extra sections from IEEE 829 or other standards
- **Keep it concise** - The template is intentionally shorter than comprehensive test plan standards
- **Do NOT create test cases** - This is a test plan, not test case documentation
- **Focus on priorities** - Emphasize CRITICAL and HIGH priority areas
- **Be specific with metrics** - Use actual numbers (e.g., "≥95% coverage", "<5 min execution time")
- **Reference real stakeholders** - Use names from Jira comments/tickets
- **Use standard Paysera sections** - Stakeholders, Testing Objectives, Types of Testing, etc.
- **HTML is required** - Always generate both markdown and HTML versions

---

**Template Reference:**
See https://intranet.paysera.net/pages/viewpage.action?pageId=335939249 for the official Paysera test plan template.

---

**Generated by:** qa-analysis-claude
**Template Version:** 2.0 (Paysera Format)
**Last Updated:** February 6, 2026
