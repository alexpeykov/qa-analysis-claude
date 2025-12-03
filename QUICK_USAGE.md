# Quick Usage Guide

## Easiest Way: Auto-Save to ticket_analysis Folder

Use the `analyze_ticket.py` wrapper script - it automatically saves to `ticket_analysis/` folder:

```bash
cd /Users/employee/Projects/qa-analysis-claude
python3 analyze_ticket.py --jira https://jira.paysera.net/browse/PROJ-123
```

### What It Does
✅ Automatically creates filename: `PROJ-123_20241203_143052.txt`
✅ Saves to: `ticket_analysis/` folder
✅ Shows you the file path when done
✅ Files in this folder are gitignored (won't be committed)

### Examples

#### Basic Analysis
```bash
python3 analyze_ticket.py --jira https://jira.paysera.net/browse/PROJ-123
```
Output: `ticket_analysis/PROJ-123_20241203_143052.md` (Structured Markdown Report)

#### With Merge Request
```bash
python3 analyze_ticket.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456
```
Output: `ticket_analysis/PROJ-123_20241203_143052.txt`

#### Full Analysis
```bash
python3 analyze_ticket.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --linked https://jira.paysera.net/browse/PROJ-124 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
  --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789
```
Output: `ticket_analysis/PROJ-123_20241203_143052.txt`

#### Get JSON Output
```bash
python3 analyze_ticket.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --format json
```
Output: `ticket_analysis/PROJ-123_20241203_143052.json`

## After Running

The script will show you:
```
================================================================================
✅ Analysis Complete!
================================================================================
📄 File saved to: ticket_analysis/PROJ-123_20241203_143052.txt
📊 File size: 45230 bytes

Next steps:
1. Open the file: open ticket_analysis/PROJ-123_20241203_143052.txt
2. Copy the content
3. Paste into Claude for analysis
================================================================================
```

## View Your Analyses

```bash
# List all analyses
ls -lh ticket_analysis/

# Open the latest one
open ticket_analysis/$(ls -t ticket_analysis/ | head -1)

# Open a specific ticket's latest analysis
open ticket_analysis/$(ls -t ticket_analysis/PROJ-123* | head -1)
```

## Alternative: Original Script (Manual Output)

If you want to control the output location yourself:

```bash
python3 qa_analyze.py --jira <URL> --output my_custom_name.txt
```

## Command Comparison

| Want to... | Use this command |
|------------|------------------|
| **Auto-save to ticket_analysis/** | `python3 analyze_ticket.py --jira <URL>` |
| **Print to console** | `python3 qa_analyze.py --jira <URL>` |
| **Custom output location** | `python3 qa_analyze.py --jira <URL> --output path/to/file.txt` |

## Tips

💡 **Organize by ticket**: The auto-naming uses ticket IDs, making it easy to find analyses
💡 **Timestamped**: Each run creates a new file with timestamp - no overwrites
💡 **Gitignored**: Your analyses stay private and won't be committed
💡 **Easy sharing**: Just copy the file to share with teammates

## Full Command Reference

```bash
python3 analyze_ticket.py --jira <JIRA_URL> [OPTIONS]

Options:
  --jira URL              Main Jira ticket URL (required)
  --linked URL [URL ...]  Linked Jira tickets
  --mr URL [URL ...]      GitLab merge requests
  --confluence URL [...]  Confluence pages
  --format {text,json}    Output format (default: text)
```

## Need Help?

```bash
# Show help
python3 analyze_ticket.py --help

# Test connections
python3 test_connection.py

# Check main script help
python3 qa_analyze.py --help
```
