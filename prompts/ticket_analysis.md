I need you to generate a comprehensive QA test analysis report for a Jira ticket.

Jira ticket: https://jira.paysera.net/browse/CORE-5567
Merge request (optional): https://gitlab.paysera.net/paysera/app-evpbank/-/merge_requests/11921
Linked tickets (optional):https://jira.paysera.net/browse/CORE-5561  https://jira.paysera.net/browse/CORE-5707
Confluence documentation (optional): none

Project Location: /Users/employee/Projects/qa-analysis-claude

Steps:
1. Navigate to the project directory
2. Run: python3 analyze_ticket.py --jira {JIRA_URL} --mr {MR_URL} --linked {LINKED_TICKET_URL_1} {LINKED_TICKET_URL_2} --confluence {CONFLUENCE_URL}
3. Read the generated file from ticket_analysis/ folder
4. Analyze the ticket data (description, comments, technical details, code changes, documentation)
5. Create a beautiful, well-structured HTML report
6. Save it as: ticket_analysis/{TICKET-ID}_QA_Analysis_Report.html

The HTML report must include:
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Table of Contents**: Sticky sidebar with anchor links to all sections
- **Modern Styling**: Clean, professional design with good typography
- **Color Coding**: Different colors for priority levels and section types
- **Interactive Elements**: Smooth scrolling navigation

Report sections:
- 📋 Ticket Information (ID, summary, status, priority, assignee, dates)
- 🎯 Issue Summary (2-3 paragraphs)
- 🔍 Root Cause Analysis (current behavior, impact, business context)
- 💡 Solution Implemented (technical changes, algorithm flow, key logic)
- 🧪 Test Coverage Analysis (20+ test ideas across 6 categories: Functional, Integration, Edge Cases, Regression, Security, Performance)
- ⚠️ Testing Focus Areas (5-7 critical areas requiring special attention)
- 📊 Key Metrics (files analyzed, comments reviewed, test cases created)
- 🔗 Related Documentation (MR links, related tickets, Confluence links)
- 📝 Testing Recommendations (Priority 1/2/3 with color coding)
- 🎯 Next Steps (specific action items)

Use the HTML format from: .claude/qa-analysis.md template



