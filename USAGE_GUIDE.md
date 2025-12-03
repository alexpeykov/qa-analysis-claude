# Quick Usage Guide

## One-Command QA Analysis

### Basic Usage (Just a Jira ticket)
```bash
python qa_analyze.py --jira https://jira.paysera.net/browse/PROJ-123
```

### With Merge Request
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456
```

### Full Analysis (Everything)
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --linked https://jira.paysera.net/browse/PROJ-124 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
  --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789
```

### Save to File
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
  --output my_analysis.txt
```

## What Happens Next

1. Script fetches all data from Jira, GitLab, and Confluence
2. Generates a comprehensive prompt with all information
3. You copy the output and give it to Claude
4. Claude analyzes everything and generates:
   - Executive summary
   - 10-15 test ideas
   - 8-12 detailed test cases

## Input Format

### Jira URLs
- ✅ `https://jira.paysera.net/browse/PROJ-123`
- ❌ `PROJ-123` (must be full URL)

### GitLab MR URLs
- ✅ `https://gitlab.paysera.net/project/subproject/-/merge_requests/456`
- ❌ `456` (must be full URL)

### Confluence URLs
- ✅ `https://intranet.paysera.net/pages/viewpage.action?pageId=12345`
- ⚠️ Must include `pageId=` parameter

## Multiple URLs

You can provide multiple URLs for linked tickets, MRs, and docs:

```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --linked https://jira.paysera.net/browse/PROJ-124 \
           https://jira.paysera.net/browse/PROJ-125 \
           https://jira.paysera.net/browse/PROJ-126 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
       https://gitlab.paysera.net/project/-/merge_requests/457 \
  --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789 \
               https://intranet.paysera.net/pages/viewpage.action?pageId=790
```

## Troubleshooting

### "Missing required configuration values"
→ Your `.env` file is missing or incomplete. Copy `.env.example` to `.env` and add your credentials.

### "Could not extract ticket key from URL"
→ Check your URL format. Must be full URLs, not just ticket keys.

### "Authentication failed"
→ Your API tokens may be expired. Generate new ones and update your `.env` file.

## Pro Tips

1. **Save output to file** for easy sharing: `--output analysis.txt`
2. **Use JSON format** for custom processing: `--format json`
3. **Run without internet?** Data is fetched fresh each time, so you need access to Jira/GitLab/Confluence
4. **Share with team?** Share the output file, never your `.env` file!
