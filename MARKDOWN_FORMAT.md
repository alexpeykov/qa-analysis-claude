# Markdown Report Format

## Overview

The tool now generates **structured Markdown (.md) reports** instead of plain text files. These reports follow a standardized format that makes them easy to read, share, and integrate into documentation systems.

## Output Format

### Filename Pattern
```
ticket_analysis/{TICKET-ID}_{TIMESTAMP}.md
```

Example: `ticket_analysis/CORE-5725_20241203_143052.md`

### Report Structure

Each report includes these sections:

1. **📋 Ticket Information** - Key metadata about the ticket
2. **🎯 Issue Summary** - What the ticket is about
3. **🔍 Root Cause Analysis** - Investigation findings
4. **💡 Solution Implemented** - Technical changes made
5. **🧪 Test Coverage Analysis** - Test ideas and cases
6. **⚠️ Testing Focus Areas** - Critical areas needing attention
7. **📊 Key Metrics** - Analysis statistics
8. **🔗 Related Documentation** - Links to related resources
9. **📝 Testing Recommendations** - Prioritized test recommendations
10. **🎯 Next Steps** - Action items

## Example Output

```markdown
# Test Analysis Report: CORE-5725

**Generated:** December 3, 2025
**Ticket:** [CORE-5725](https://jira.paysera.net/browse/CORE-5725)
**MR:** [#11485](https://gitlab.paysera.net/merge_requests/11485)

---

## 📋 Ticket Information

- **Ticket:** CORE-5725
- **Summary:** Fix payment processing bug
- **Status:** In Progress
- **Priority:** High
- **Assignee:** John Doe
- **Reporter:** Jane Smith
- **Created:** November 15, 2025
- **Updated:** December 3, 2025

---

## 🎯 Issue Summary

[Detailed summary of the issue...]

---

[Additional sections following the template...]
```

## Benefits of Markdown Format

### ✅ Better Readability
- Structured headers and sections
- Emojis for visual navigation
- Proper formatting for code, lists, and links
- Easy to scan and find information

### ✅ Easy Sharing
- Renders beautifully in GitHub, GitLab, and Confluence
- Can be viewed in any markdown viewer
- Professional appearance
- Preserves formatting when copied

### ✅ Integration Friendly
- Compatible with documentation systems
- Can be converted to HTML, PDF, or other formats
- Works with static site generators
- Easy to parse programmatically

### ✅ Version Control Ready
- Plays well with git
- Diff-friendly format
- Can be reviewed in PRs
- Trackable changes over time

## Usage

### Generate a Report

```bash
cd /Users/employee/Projects/qa-analysis-claude
python3 analyze_ticket.py --jira https://jira.paysera.net/browse/CORE-5725
```

Output: `ticket_analysis/CORE-5725_20241203_143052.md`

### View the Report

**In Terminal:**
```bash
# View with cat
cat ticket_analysis/CORE-5725_20241203_143052.md

# View with less (better for long files)
less ticket_analysis/CORE-5725_20241203_143052.md

# View in default markdown viewer
open ticket_analysis/CORE-5725_20241203_143052.md
```

**In VS Code:**
```bash
code ticket_analysis/CORE-5725_20241203_143052.md
```
Then press `Cmd+Shift+V` for preview mode

**In Browser:**
- Drag and drop the .md file into your browser (with markdown extension)
- Or use a markdown viewer like `grip` or `mdless`

### Share the Report

**Copy to Clipboard:**
```bash
cat ticket_analysis/CORE-5725_20241203_143052.md | pbcopy
```

**Upload to Confluence:**
1. Open the .md file
2. Copy all content
3. Paste into Confluence (it will preserve formatting)

**Add to Git:**
```bash
# Note: ticket_analysis/ is gitignored by default
# To share, copy to a different location first
cp ticket_analysis/CORE-5725_20241203_143052.md docs/qa-reports/
git add docs/qa-reports/CORE-5725_20241203_143052.md
git commit -m "Add QA analysis for CORE-5725"
```

## Customization

The report format is defined in `.claude/qa-analysis.md`. You can modify the template to:
- Add/remove sections
- Change emoji icons
- Adjust the structure
- Add custom sections specific to your needs

## Advanced: JSON Format

For programmatic processing, you can still get JSON output:

```bash
python3 analyze_ticket.py \
  --jira https://jira.paysera.net/browse/CORE-5725 \
  --format json
```

Output: `ticket_analysis/CORE-5725_20241203_143052.json`

## Tips

💡 **Search within reports:**
```bash
grep -r "performance" ticket_analysis/
```

💡 **Find latest report for a ticket:**
```bash
ls -t ticket_analysis/CORE-5725* | head -1
```

💡 **Count reports:**
```bash
ls ticket_analysis/*.md | wc -l
```

💡 **View report in browser:**
```bash
# Using grip (install: pip install grip)
grip ticket_analysis/CORE-5725_20241203_143052.md
```

## Troubleshooting

**Report looks wrong:**
- Check that you're using the latest template (`.claude/qa-analysis.md`)
- Verify Claude received the correct prompt format

**Can't open .md file:**
- Install a markdown viewer (e.g., MacDown, Typora, or VS Code)
- Or view in browser with markdown extension

**Want plain text instead:**
- Use the original `qa_analyze.py` script directly
- Or convert markdown to text: `pandoc report.md -t plain -o report.txt`
