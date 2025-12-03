# 🚀 START HERE - QA Analysis Claude Skill

## What Is This?

This tool **automates QA analysis** by fetching data from Jira, GitLab, and Confluence, then using Claude AI to generate comprehensive test cases and analysis reports.

**Time saved per ticket: 2-3 hours!**

---

## 🎯 Quick Navigation

**Just want to get started?** → Read [QUICKSTART.md](QUICKSTART.md)

**Need full documentation?** → Read [README.md](README.md)

**Want to see an example?** → Read [EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md)

**Quick command reference?** → Read [USAGE_GUIDE.md](USAGE_GUIDE.md)

**Security concerns?** → Read [SECURITY.md](SECURITY.md)

**Manual analysis without script?** → Read [SIMPLE_PROMPT.md](SIMPLE_PROMPT.md)

**Project overview?** → Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## ⚡ Get Started in 3 Steps

### 1️⃣ Setup (5 minutes, one time only)

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Run Analysis

```bash
python qa_analyze.py --jira https://jira.paysera.net/browse/YOUR-TICKET-123
```

### 3️⃣ Get Results

Copy the output → Paste to Claude → Receive comprehensive analysis!

---

## 📊 What You Get

### Input (What You Provide)
- 🎫 Jira ticket URL
- 🔀 Merge request URL(s) - optional
- 📚 Confluence page URL(s) - optional
- 🔗 Linked ticket URLs - optional

### Output (What Claude Generates)
- 📋 **Executive Summary** - Overview of changes and impact
- 💡 **10-15 Test Ideas** - Creative scenarios covering all aspects
- ✅ **8-12 Detailed Test Cases** - Step-by-step with acceptance criteria

---

## 🎨 Example Command

```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PAY-1234 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/567 \
  --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789 \
  --output my_analysis.txt
```

---

## 📚 Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| [START_HERE.md](START_HERE.md) | This file! Overview and navigation | **Read first** |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute getting started guide | **Setup time** |
| [README.md](README.md) | Complete documentation | Reference/Troubleshooting |
| [EXAMPLE_OUTPUT.md](EXAMPLE_OUTPUT.md) | Sample input/output | See what to expect |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | Command reference | Quick lookup |
| [SECURITY.md](SECURITY.md) | Credential management | Before sharing |
| [SIMPLE_PROMPT.md](SIMPLE_PROMPT.md) | Manual template | No script option |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Architecture overview | Understanding codebase |
| [PROJECT_STRUCTURE.txt](PROJECT_STRUCTURE.txt) | File tree | Understanding layout |

---

## 🔐 Security First

**IMPORTANT:** Your `.env` file contains credentials and is **gitignored**.

✅ **DO:**
- Keep `.env` file local only
- Use `.env.example` as template
- Rotate tokens regularly

❌ **DON'T:**
- Commit `.env` to git
- Share your `.env` file
- Email your credentials

➡️ Read [SECURITY.md](SECURITY.md) for details

---

## 🛠️ Technology Stack

- **Python 3.x** - Core language
- **Jira REST API v2** - Ticket data
- **GitLab REST API v4** - Code changes
- **Confluence REST API** - Documentation
- **Claude AI** - Analysis generation

---

## 🎯 Common Use Cases

### 1. Bug Fix Analysis
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/BUG-123 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456
```

### 2. Feature Development
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/FEAT-123 \
  --linked https://jira.paysera.net/browse/FEAT-124 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
  --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789
```

### 3. Quick Analysis
```bash
python qa_analyze.py --jira https://jira.paysera.net/browse/PROJ-123
```

---

## 🎓 Workflow

```
1. Developer creates ticket & MR
         ↓
2. QA runs: python qa_analyze.py --jira URL --mr URL
         ↓
3. Script fetches all data from Jira/GitLab/Confluence
         ↓
4. Script generates comprehensive prompt
         ↓
5. QA copies prompt to Claude
         ↓
6. Claude analyzes and generates test cases
         ↓
7. QA reviews and executes tests
         ↓
8. Results documented in Jira
```

---

## ⚙️ Project Structure

```
qa-analysis-claude/
├── 📖 Documentation (10 files)
│   ├── START_HERE.md         ← You are here
│   ├── QUICKSTART.md
│   ├── README.md
│   └── ...
├── 🐍 Python Code (7 files, 864 lines)
│   ├── qa_analyze.py         ← Main script
│   └── src/                  ← API clients
├── 🔧 Configuration
│   ├── .env                  ← Your credentials
│   ├── .env.example          ← Template
│   └── requirements.txt      ← Dependencies
└── 🤖 Claude Integration
    └── .claude/qa-analysis.md ← AI prompt template
```

---

## 🚨 Troubleshooting

### "Missing required configuration values"
➜ Copy `.env.example` to `.env` and add your credentials

### "Could not extract ticket key"
➜ Use full URLs: `https://jira.paysera.net/browse/PROJ-123`

### "Authentication failed"
➜ Check your API tokens in `.env` - they may be expired

### Need more help?
➜ Read [README.md](README.md) troubleshooting section

---

## 🎉 Ready to Start?

**Option 1: Full Setup**
Read [QUICKSTART.md](QUICKSTART.md) for step-by-step instructions

**Option 2: Quick Start**
If you already have credentials:
```bash
cp .env.example .env
# Edit .env with your credentials
pip install -r requirements.txt
python qa_analyze.py --jira <YOUR-TICKET-URL>
```

---

## 📞 Support

- **Setup issues**: Check [README.md](README.md) → Troubleshooting
- **Security questions**: Check [SECURITY.md](SECURITY.md)
- **Usage questions**: Check [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Access issues**: Contact your team lead

---

## 🎯 Next Steps

1. ✅ Read this file (you're doing it!)
2. ⏭️ Go to [QUICKSTART.md](QUICKSTART.md)
3. 🚀 Run your first analysis
4. 📊 Review the results
5. 🎉 Share with your team!

---

**Questions?** Start with [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md)

**Ready?** Let's analyze some tickets! 🚀
