# QA Analysis Claude Skill

A Claude skill for Quality Assurance specialists to interact with Jira, GitLab, and Confluence.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd qa-analysis-claude
```

### 2. Configure Your Credentials

**IMPORTANT: Never commit your `.env` file to the repository!**

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your personal credentials:
   ```bash
   nano .env
   # or use your preferred editor
   ```

3. Replace the placeholder values with your actual credentials:
   - **Jira**: Your Paysera email and Jira API token
   - **GitLab**: Your Paysera email, personal access token, and feed token
   - **Confluence**: Your Paysera email and Confluence API token

### 3. Getting Your API Tokens

#### Jira API Token
1. Go to [https://jira.paysera.net/](https://jira.paysera.net/)
2. Click on your profile → Account Settings → Security
3. Create a new API token

#### GitLab Personal Access Token
1. Go to [https://gitlab.paysera.net/](https://gitlab.paysera.net/)
2. Click on your profile → Preferences → Access Tokens
3. Create a new token with appropriate scopes (api, read_user, read_repository)

#### GitLab Feed Token
1. Go to [https://gitlab.paysera.net/](https://gitlab.paysera.net/)
2. Click on your profile → Preferences → Access Tokens
3. Your feed token is displayed under "Feed token"

#### Confluence API Token
1. Go to [https://intranet.paysera.net/](https://intranet.paysera.net/)
2. Click on your profile → Account Settings → Security
3. Create a new API token

## Security Notes

- ✅ The `.env` file is listed in `.gitignore` and will NOT be committed
- ✅ Use `.env.example` as a template (no real credentials)
- ✅ Each team member must create their own `.env` file
- ⚠️ Never share your API tokens in chat, email, or commits
- ⚠️ If a token is accidentally exposed, revoke it immediately and create a new one

## Installation

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - For making API calls to Jira, GitLab, and Confluence
- `python-dotenv` - For loading environment variables from .env file

## Project Structure

```
qa-analysis-claude/
├── .env                      # Your personal credentials (NOT in git)
├── .env.example              # Template for credentials (committed to git)
├── .gitignore               # Ensures .env is not committed
├── README.md                # This file
├── SECURITY.md              # Security guidelines
├── requirements.txt         # Python dependencies
├── qa_analyze.py            # Main execution script
├── .claude/
│   └── qa-analysis.md       # Claude prompt template
└── src/
    ├── __init__.py
    ├── config.py            # Configuration and credential loading
    ├── jira_client.py       # Jira API client
    ├── gitlab_client.py     # GitLab API client
    ├── confluence_client.py # Confluence API client
    └── analyzer.py          # Main analysis orchestrator
```

## Usage

### Quick Start

Run the QA analysis tool with a Jira ticket:

```bash
python qa_analyze.py --jira https://jira.paysera.net/browse/PROJ-123
```

### Full Analysis with All Sources

```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --linked https://jira.paysera.net/browse/PROJ-124 \
           https://jira.paysera.net/browse/PROJ-125 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
       https://gitlab.paysera.net/project/-/merge_requests/457 \
  --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789
```

### Command Line Options

- `--jira URL` (required): URL to the main Jira ticket
- `--linked URL [URL ...]`: URLs to linked Jira tickets (optional, multiple allowed)
- `--mr URL [URL ...]`: URLs to GitLab merge requests (optional, multiple allowed)
- `--confluence URL [URL ...]`: URLs to Confluence pages (optional, multiple allowed)
- `--output FILE` or `-o FILE`: Save output to file instead of printing to console
- `--format {text,json}`: Output format (default: text)
  - `text`: Generates a Claude-ready prompt with all data
  - `json`: Raw JSON data for programmatic processing

### Examples

#### Example 1: Basic ticket analysis
```bash
python qa_analyze.py --jira https://jira.paysera.net/browse/PROJ-123
```

#### Example 2: Ticket with merge request
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456
```

#### Example 3: Full analysis saved to file
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --linked https://jira.paysera.net/browse/PROJ-124 \
  --mr https://gitlab.paysera.net/project/-/merge_requests/456 \
  --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789 \
  --output analysis_prompt.txt
```

#### Example 4: Get raw JSON data
```bash
python qa_analyze.py \
  --jira https://jira.paysera.net/browse/PROJ-123 \
  --format json \
  --output data.json
```

### Workflow

1. **Run the analysis script** with your ticket URLs
2. **Review the generated prompt** (printed to console or saved to file)
3. **Copy the prompt to Claude** (Claude Code, claude.ai, or API)
4. **Receive comprehensive QA analysis** including:
   - Executive summary of the ticket and changes
   - 10-15 creative test ideas
   - 8-12 detailed test cases with steps and acceptance criteria

### What You Get

The tool generates a comprehensive prompt for Claude that includes:

#### From Jira:
- Ticket summary, description, status, priority
- All comments and discussions
- Linked tickets and their relationships
- Ticket metadata (assignee, reporter, dates)

#### From GitLab:
- Merge request description and status
- All code changes and diffs
- Commit history
- Code review discussions and comments
- Files modified/added/deleted

#### From Confluence:
- Documentation content
- Page metadata and version history
- Comments and discussions

#### Claude's Analysis Output:
1. **Executive Summary**: Overview of the ticket, changes, and impact
2. **Test Ideas**: 10-15 creative test scenarios covering functional, edge cases, integration, security, performance, etc.
3. **Detailed Test Cases**: 8-12 comprehensive test cases with:
   - Test case ID and title
   - Priority level
   - Preconditions
   - Step-by-step test instructions
   - Test data
   - Expected results
   - Acceptance criteria

## Advanced Usage

### Using as a Python Module

You can also import and use the components in your own Python scripts:

```python
from src.analyzer import QAAnalyzer

analyzer = QAAnalyzer()

# Fetch data
data = analyzer.fetch_all_data(
    jira_ticket_url="https://jira.paysera.net/browse/PROJ-123",
    merge_request_urls=["https://gitlab.paysera.net/project/-/merge_requests/456"]
)

# Format for analysis
formatted_text = analyzer.format_data_for_analysis(data)
print(formatted_text)
```

### Integration with CI/CD

You can integrate this tool into your CI/CD pipeline:

```yaml
# Example GitLab CI configuration
qa-analysis:
  script:
    - pip install -r requirements.txt
    - python qa_analyze.py --jira $JIRA_TICKET_URL --mr $CI_MERGE_REQUEST_URL --output analysis.txt
  artifacts:
    paths:
      - analysis.txt
```

## Troubleshooting

### Common Issues

**Error: Missing required configuration values**
- Ensure your `.env` file exists and contains all required values
- Check that you copied `.env.example` to `.env` and filled in your credentials

**Error: Could not extract ticket key/MR info from URL**
- Verify the URL format is correct
- Ensure you're using full URLs, not just ticket keys
- For Confluence, make sure the URL contains `pageId=` parameter

**Error: Authentication failed**
- Verify your API tokens are correct and not expired
- Check that you're using the right email address
- Try generating new API tokens

**Error: Permission denied**
- Ensure your account has access to the Jira ticket, GitLab project, or Confluence page
- Contact your admin if you need additional permissions

### Getting Help

- Check [SECURITY.md](SECURITY.md) for credential management issues
- Review the error messages for specific guidance
- Contact your team lead for access or permission issues

## Contributing

When contributing to this project:
1. Never commit your `.env` file
2. Update `.env.example` if you add new environment variables (without real values)
3. Update this README with any setup changes

## TestRail Integration

This project includes tools for managing TestRail test cases and folders.

### Creating TestRail Folders

Create folders/sections in TestRail for organizing test cases:

```bash
python3 create_testrail_folder.py \
  --project 2 \
  --suite 14 \
  --folder "CORE-5567 - Feature Name" \
  --description "https://jira.paysera.net/browse/CORE-5567"
```

**Options:**
- `--project`: TestRail project ID (required)
- `--suite`: TestRail suite ID (required for multi-suite projects)
- `--folder`: Folder name (required)
- `--description`: Optional folder description

### Creating Test Cases

#### Method 1: From Natural Text Input (Recommended)

Create test cases from text with automatic expected result generation:

```bash
python3 create_test_case_from_text.py \
  --project 2 \
  --suite 14 \
  --section-id 90046 \
  --type "Functional" \
  --priority "High" \
  --refs "CORE-5567" \
  --input "Load DB fixtures from test plan
1.Switch to local DB
2.Load the fixtures from the test plan
3.Examine the output
The fixtures are supposed to be imported without any errors. The info is supposed to be present in the DB tables."
```

The script will automatically generate appropriate expected results for each step based on the action described.

#### Method 2: Explicit Steps and Expected Results

Create test cases by explicitly specifying steps and their expected results:

```bash
python3 create_test_cases.py \
  --project 2 \
  --suite 14 \
  --section-id 90046 \
  --type "Functional" \
  --priority "High" \
  --title "Load DB fixtures from test plan" \
  --refs "CORE-5567" \
  --steps "Switch to local DB" "Load the fixtures" "Examine output" \
  --expected "Fixtures imported successfully" "Data present in DB" "Output verified"
```

**Options:**
- `--project`: TestRail project ID (required)
- `--suite`: TestRail suite ID
- `--section-id`: TestRail section ID (required, use this OR --section-name)
- `--section-name`: TestRail section name (will search for it)
- `--type`: Test case type (default: Functional)
- `--priority`: Test priority (default: Medium)
- `--title`: Test case title (required)
- `--refs`: References like Jira ticket IDs
- `--steps`: Test steps (space-separated)
- `--expected`: Expected results for each step (must match number of steps)
- `--estimate`: Time estimate (e.g., "30s", "1m", "2h")
- `--preconditions`: Preconditions for the test

**Example: Create multiple test cases with text input**

```bash
# Test Case 1
python3 create_test_case_from_text.py --project 2 --suite 14 --section-id 90046 \
  --type "Functional" --priority "High" --refs "CORE-5567" \
  --input "Process transfer 9990001 with command from test plan
1.Enter evpbank container via terminal
2.Execute the command app/console paysera:debug:intermediate-statement 99990001
3.Examine the output
The command is supposed to be executed without any errors. Statement is supposed to be created"

# Test Case 2
python3 create_test_case_from_text.py --project 2 --suite 14 --section-id 90046 \
  --type "Functional" --priority "High" --refs "CORE-5567" \
  --input "Process transfer 9990002 with command from test plan
1.Enter evpbank container via terminal
2.Execute the command app/console paysera:debug:intermediate-statement 99990002
3.Examine the output
The command is supposed to be executed without any errors. Statement is supposed to be created"
```

### Creating Test Runs

Create test runs that include test cases from specified folders:

```bash
python3 create_test_run.py \
  --project 2 \
  --suite 14 \
  --name "CORE-5567 - Test Run" \
  --refs "CORE-5567" \
  --description "Testing CORE-5567 functionality" \
  --folders "5567 - Add persisted events for TransferStatusForReservationStatementListener"
```

**Options:**
- `--project`: TestRail project ID (required)
- `--suite`: TestRail suite ID (required)
- `--name`: Test run name (required)
- `--refs`: References like Jira ticket IDs
- `--description`: Test run description
- `--folders`: Folder/section names to include test cases from (space-separated, required)

**Example: Create test run from multiple folders**

```bash
python3 create_test_run.py \
  --project 2 \
  --suite 14 \
  --name "Sprint 42 - Regression Test Run" \
  --refs "SPRINT-42" \
  --description "Full regression testing for Sprint 42" \
  --folders "5567 - Feature A" "5568 - Feature B" "5569 - Feature C"
```

### TestRail Workflow

1. **Create a folder** for your Jira ticket
2. **Note the section ID** from the output
3. **Create test cases** in that section
4. **Create a test run** including test cases from the folder(s)
5. **Verify in TestRail** using the provided URLs

See [prompts/create_testrail_folder.md](prompts/create_testrail_folder.md), [prompts/create_test_cases.md](prompts/create_test_cases.md), and [prompts/create_test_run.md](prompts/create_test_run.md) for detailed templates.

## Support

For issues with credentials or access, contact your team lead or IT support.
