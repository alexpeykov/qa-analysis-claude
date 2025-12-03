# Quick Start Guide - 5 Minutes to Your First Analysis

## Step 1: Setup (One Time Only)

```bash
# Clone the repository
git clone <your-repo-url>
cd qa-analysis-claude

# Copy environment template
cp .env.example .env

# Edit .env and add YOUR credentials
nano .env
# (or use VS Code, vim, etc.)

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run Your First Analysis

```bash
python qa_analyze.py --jira https://jira.paysera.net/browse/YOUR-TICKET-123
```

## Step 3: Copy Output to Claude

The script will print a comprehensive prompt. Copy it and paste into:
- Claude Code (this tool!)
- claude.ai
- Claude API

## Step 4: Get Your Results

Claude will generate:
- ✅ Executive summary
- ✅ 10-15 test ideas
- ✅ 8-12 detailed test cases

## Common Usage Patterns

### Pattern 1: Bug Fix Analysis
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/BUG-123 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456
```

### Pattern 2: Feature Analysis
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/FEAT-123 \
  --linked https://jira.paysera.net/browse/FEAT-124 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
  --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789
```

### Pattern 3: Save to File for Later
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
  --output my_analysis.txt
```

## Getting Your Credentials

### Jira API Token
1. Visit: https://jira.paysera.net/
2. Profile → Account Settings → Security → Create API Token
3. Copy token to `.env` → `JIRA_API_TOKEN`

### GitLab Personal Access Token
1. Visit: https://gitlab.paysera.net/
2. Profile → Preferences → Access Tokens
3. Create token with: `api`, `read_user`, `read_repository`
4. Copy to `.env` → `GITLAB_PERSONAL_ACCESS_TOKEN`

### Confluence API Token
1. Visit: https://intranet.paysera.net/
2. Profile → Account Settings → Security → Create API Token
3. Copy token to `.env` → `CONFLUENCE_API_TOKEN`

## Troubleshooting

### Error: "Missing required configuration values"
➜ Your `.env` file is missing. Run: `cp .env.example .env` and add your credentials.

### Error: "Could not extract ticket key"
➜ Use full URLs, not just ticket keys. Must start with `https://`

### Error: "Authentication failed"
➜ Check your API tokens are correct and not expired.

## Pro Tips

💡 **Save time**: Use `--output` to save results for sharing
💡 **Multiple tickets**: Add multiple `--linked` URLs space-separated
💡 **Raw data**: Use `--format json` for custom processing
💡 **Help anytime**: Run `python qa_analyze.py --help`

## Need More Info?

- **Full docs**: See [README.md](README.md)
- **Security**: See [SECURITY.md](SECURITY.md)
- **Usage examples**: See [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Manual prompts**: See [SIMPLE_PROMPT.md](SIMPLE_PROMPT.md)

---

**Ready?** Run your first analysis now! 🚀
