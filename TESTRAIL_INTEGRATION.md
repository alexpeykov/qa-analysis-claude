# TestRail Integration

## Overview

The QA Analysis tool now integrates with TestRail to automate the creation of:
- ✅ **Folders (Sections)** - Organize test cases
- 📋 **Test Cases** (coming soon)
- 🏃 **Test Runs** (coming soon)

## Setup

### 1. Credentials Already Configured

Your TestRail credentials have been added to `.env`:
```
TESTRAIL_URL=https://testrail.paysera.net/
TESTRAIL_EMAIL=aleksandar.peykov@paysera.net
TESTRAIL_API_KEY=OzJq.2qbxBLBEMgnUrTR-DBU.NClp6WQVsvoik5qb
```

### 2. Get Your TestRail API Key

If you need to generate a new API key:
1. Go to [https://testrail.paysera.net/](https://testrail.paysera.net/)
2. Click on your name (top right) → My Settings
3. Scroll to "API Keys" section
4. Click "Add Key" or use existing key
5. Copy the key to `.env` → `TESTRAIL_API_KEY`

## Features

### ✅ Create Folders (Sections)

Create single or nested folders in TestRail to organize your test cases.

#### List Available Projects

```bash
python3 create_testrail_folder.py --list-projects
```

#### List Suites in a Project

```bash
python3 create_testrail_folder.py --list-suites 1
```

#### List Existing Sections

```bash
python3 create_testrail_folder.py --list-sections 1
```

#### Create a Single Folder

```bash
python3 create_testrail_folder.py --project 1 --folder "QA Tests"
```

#### Create Nested Folders (Hierarchy)

```bash
python3 create_testrail_folder.py --project 1 --folder "QA Tests/CORE-5725/Functional Tests"
```

This creates:
```
QA Tests/
└── CORE-5725/
    └── Functional Tests/
```

#### Create Folder with Description

```bash
python3 create_testrail_folder.py --project 1 --folder "CORE-5725" --description "Test cases for ticket CORE-5725: Currency filter bug"
```

#### Create Folder in Specific Suite

For multi-suite projects:

```bash
python3 create_testrail_folder.py --project 1 --suite 2 --folder "Regression Tests"
```

## Command Reference

```bash
python3 create_testrail_folder.py [OPTIONS]

Required:
  --project, -p PROJECT_ID    TestRail project ID
  --folder, -f FOLDER_PATH    Folder name or path (e.g., "Parent/Child")

Optional:
  --suite, -s SUITE_ID        Suite ID (for multi-suite projects)
  --description, -d TEXT      Folder description
  --list-projects             List all projects and exit
  --list-suites PROJECT_ID    List all suites for a project
  --list-sections PROJECT_ID  List all sections for a project
```

## Usage Examples

### Example 1: Basic Setup

```bash
# 1. List projects to find your project ID
python3 create_testrail_folder.py --list-projects

# Output:
# ID: 1
# Name: EVP Bank
# Suite Mode: 1 (single suite)

# 2. Create root folder for your tests
python3 create_testrail_folder.py --project 1 --folder "Automated QA Tests"
```

### Example 2: Organize by Ticket

```bash
# Create folder structure for CORE-5725
python3 create_testrail_folder.py \
  --project 1 \
  --folder "Automated QA Tests/CORE-5725" \
  --description "Test cases for CORE-5725: Account statements currency filter bug"

# Result:
# ✓ Section 'Automated QA Tests' already exists (ID: 123)
# Creating section 'CORE-5725'...
# ✓ Created section 'CORE-5725' (ID: 124)
```

### Example 3: Create Test Categories

```bash
# Create nested structure with test categories
python3 create_testrail_folder.py \
  --project 1 \
  --folder "Automated QA Tests/CORE-5725/Functional Tests"

python3 create_testrail_folder.py \
  --project 1 \
  --folder "Automated QA Tests/CORE-5725/Edge Cases"

python3 create_testrail_folder.py \
  --project 1 \
  --folder "Automated QA Tests/CORE-5725/Regression Tests"

# Result hierarchy:
# Automated QA Tests/
# └── CORE-5725/
#     ├── Functional Tests/
#     ├── Edge Cases/
#     └── Regression Tests/
```

### Example 4: Check Existing Structure

```bash
# View current folder hierarchy
python3 create_testrail_folder.py --list-sections 1

# Output:
# ├─ [123] Automated QA Tests
#   ├─ [124] CORE-5725
#     Description: Test cases for CORE-5725
#     ├─ [125] Functional Tests
#     ├─ [126] Edge Cases
#     └─ [127] Regression Tests
```

## Python API Usage

You can also use the TestRail client directly in Python:

```python
from src.testrail_client import TestRailClient

# Initialize client
client = TestRailClient()

# Create a single folder
section = client.add_section(
    project_id=1,
    name="My Test Folder",
    description="Description here"
)
print(f"Created section ID: {section['id']}")

# Create nested folders
result = client.create_nested_sections(
    project_id=1,
    path=["Parent", "Child", "Grandchild"],
    descriptions={
        "Parent": "Top level folder",
        "Grandchild": "Deepest folder"
    }
)
print(f"Final section ID: {result['id']}")

# Get or create (idempotent)
section = client.get_or_create_section(
    project_id=1,
    name="My Folder"
)
# Will return existing folder if it exists, or create new one
```

## Integration with QA Analysis

In the future, you'll be able to automatically create TestRail test cases from your QA analysis reports:

```bash
# Future functionality:
python3 qa_analyze.py --jira CORE-5725 --create-testrail-cases --project 1
```

This will:
1. Fetch ticket data
2. Generate QA analysis with test cases
3. Automatically create folders in TestRail
4. Create test cases from the analysis
5. Return TestRail URLs for review

## Troubleshooting

### Error: "401 Unauthorized" or "Authentication failed"
This is the most common error and means your API key is invalid or not recognized.

**Steps to fix:**
1. Go to https://testrail.paysera.net/
2. Click on your name (top right) → **My Settings**
3. Scroll to the **API Keys** section
4. Check if "API Access is enabled" checkbox is checked - if not, enable it
5. Click **Add Key** to generate a new API key
6. Copy the ENTIRE key (it should be a long string like `ZDFBnPlycOwOAoJ5n4ln-...`)
7. Update `.env` file with the new key:
   ```
   TESTRAIL_API_KEY=your_complete_key_here
   ```
8. Make sure your email in `.env` exactly matches your TestRail login email

**Note:** API keys can expire or be revoked. Always generate a fresh key if authentication fails.

### Error: "403 Forbidden"
- Your account doesn't have permission for this project
- Contact your TestRail admin to grant access

### Error: "No projects found"
- Your account has no access to any projects
- Contact your TestRail admin

### Error: "Invalid project ID"
- Use `--list-projects` to see available project IDs
- Verify you're using the correct project ID number

## TestRail Project Structure

TestRail has the following hierarchy:

```
Project
└── Suite (optional, for multi-suite mode)
    └── Section (Folder)
        └── Section (Nested Folder)
            └── Test Case
```

- **Project**: Top-level container (e.g., "EVP Bank")
- **Suite**: Optional grouping (only in multi-suite mode)
- **Section**: Folders to organize test cases
- **Test Case**: Individual test with steps and expected results

## Tips

💡 **Use consistent naming**: Follow a pattern like `TICKET-ID/Category` for easy navigation

💡 **Check before creating**: Use `--list-sections` to avoid duplicates

💡 **Organize by feature**: Group related test cases together

💡 **Use descriptions**: Add context to folders with `--description`

💡 **Nested is better**: Create hierarchy for better organization

## Security Notes

- ✅ API keys are stored securely in `.env` (gitignored)
- ✅ Each team member uses their own credentials
- ⚠️ Never commit API keys to git
- ⚠️ Rotate keys periodically for security

## Coming Soon

- 📋 **Create Test Cases**: Automatically generate test cases from QA analysis
- 🏃 **Create Test Runs**: Set up test runs for execution
- 📊 **Update Test Results**: Mark tests as passed/failed
- 🔄 **Sync with Jira**: Link TestRail cases to Jira tickets

---

**TestRail folder management is now fully functional!** 🎉
