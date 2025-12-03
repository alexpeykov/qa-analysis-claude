# QA Analysis Claude - Project Summary

## Overview

This project provides an automated QA analysis tool that integrates with Jira, GitLab, and Confluence to generate comprehensive test cases and analysis reports using Claude AI.

## Key Features

✅ **Automated Data Fetching**
- Fetches Jira tickets, comments, and linked tickets
- Retrieves GitLab merge request code changes and discussions
- Pulls Confluence documentation and comments

✅ **Comprehensive Analysis**
- Executive summary of changes
- 10-15 creative test ideas
- 8-12 detailed test cases with acceptance criteria

✅ **Secure Credential Management**
- Environment-based configuration
- No credentials in code or git
- Team-friendly setup with .env.example

✅ **Flexible Output**
- Console output or file export
- Text format for Claude analysis
- JSON format for programmatic use

## Project Structure

```
qa-analysis-claude/
├── README.md              # Full documentation
├── SECURITY.md            # Security guidelines
├── USAGE_GUIDE.md         # Quick reference
├── SIMPLE_PROMPT.md       # Manual prompt template
├── PROJECT_SUMMARY.md     # This file
├── requirements.txt       # Python dependencies
├── qa_analyze.py          # Main executable script
├── .env.example           # Credential template
├── .gitignore            # Git exclusions
├── .claude/
│   └── qa-analysis.md    # Claude analysis prompt template
└── src/
    ├── config.py         # Configuration loader
    ├── jira_client.py    # Jira API integration
    ├── gitlab_client.py  # GitLab API integration
    ├── confluence_client.py  # Confluence API integration
    └── analyzer.py       # Data orchestration and formatting
```

## Quick Start

1. **Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   pip install -r requirements.txt
   ```

2. **Run Analysis**
   ```bash
   python qa_analyze.py \
     --jira https://jira.paysera.net/browse/PROJ-123 \
     --mr https://gitlab.paysera.net/project/-/merge_requests/456
   ```

3. **Use Output**
   - Copy generated prompt
   - Provide to Claude
   - Get comprehensive QA analysis

## Technology Stack

- **Python 3.x** - Core language
- **requests** - HTTP API calls
- **python-dotenv** - Environment variable management
- **Jira REST API v2** - Ticket data
- **GitLab REST API v4** - Merge request data
- **Confluence REST API** - Documentation data

## Security Features

- ✅ Credentials stored in `.env` (gitignored)
- ✅ Template file for team sharing
- ✅ No hardcoded credentials
- ✅ Token-based authentication
- ✅ Comprehensive security documentation

## Use Cases

1. **Pre-Release QA** - Analyze tickets before testing begins
2. **Test Case Generation** - Automatically generate test scenarios
3. **Code Review Support** - Understand changes with context
4. **Documentation Review** - Ensure docs match implementation
5. **Regression Planning** - Identify affected areas
6. **Team Onboarding** - Help new QA understand tickets quickly

## Output Examples

### Test Ideas Generated
- Functional testing scenarios
- Edge case identification
- Integration test suggestions
- Security vulnerability checks
- Performance considerations
- User experience validations

### Test Cases Include
- Unique test case IDs
- Priority ratings
- Preconditions
- Step-by-step instructions
- Expected results
- Acceptance criteria

## Integration Options

### Manual Use
- Run script on demand
- Copy output to Claude
- Review and refine results

### CI/CD Integration
```yaml
qa-analysis:
  script:
    - python qa_analyze.py --jira $TICKET_URL --mr $MR_URL
  artifacts:
    paths:
      - analysis.txt
```

### API Integration
```python
from src.analyzer import QAAnalyzer

analyzer = QAAnalyzer()
data = analyzer.fetch_all_data(jira_ticket_url="...")
formatted = analyzer.format_data_for_analysis(data)
```

## Team Workflow

1. Developer creates Jira ticket and MR
2. QA runs analysis script with ticket/MR URLs
3. Script fetches all relevant data
4. Generated prompt provided to Claude
5. Claude generates test cases and analysis
6. QA reviews and executes tests
7. Results documented in Jira

## Maintenance

### Adding New Features
- API clients are modular and extensible
- Add new methods to client classes
- Update analyzer to include new data
- Modify Claude prompt template as needed

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Token Rotation
- Update `.env` file with new tokens
- No code changes required
- Team members manage independently

## Future Enhancements

Potential additions:
- [ ] Direct API integration with Claude
- [ ] Automated test case export to test management tools
- [ ] Risk scoring and prioritization
- [ ] Historical analysis comparison
- [ ] Slack/Teams integration for notifications
- [ ] Test execution tracking
- [ ] Multi-language support

## Documentation Files

- **README.md** - Complete setup and usage guide
- **SECURITY.md** - Credential management and security practices
- **USAGE_GUIDE.md** - Quick reference for common commands
- **SIMPLE_PROMPT.md** - Manual prompt template (no script)
- **PROJECT_SUMMARY.md** - This overview document

## Support

For issues or questions:
1. Check documentation files
2. Review error messages
3. Verify `.env` configuration
4. Contact team lead for access issues
5. Check API token expiration

## Contributing

1. Never commit `.env` files
2. Update `.env.example` for new variables
3. Document all changes in README
4. Follow existing code style
5. Test with real data before committing

## License

Internal Paysera tool - for team use only.

---

**Created**: December 2025
**Purpose**: QA Analysis automation with Claude AI
**Team**: Quality Assurance Specialists
