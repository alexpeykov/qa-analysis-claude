#!/usr/bin/env python3
"""
Test script to verify API connections to Jira, GitLab, and Confluence.
Run this to ensure your credentials are working correctly.
"""

from src.config import Config
from src.jira_client import JiraClient
from src.gitlab_client import GitLabClient
from src.confluence_client import ConfluenceClient
import sys


def test_jira():
    """Test Jira connection."""
    print("Testing Jira connection...")
    try:
        client = JiraClient()
        # Just test the connection by trying to access the API
        import requests
        response = requests.get(
            f"{client.base_url}/rest/api/2/myself",
            auth=client.auth,
            headers=client.headers
        )
        response.raise_for_status()
        user_data = response.json()
        print(f"✅ Jira: Connected as {user_data.get('displayName', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Jira: Connection failed - {e}")
        return False


def test_gitlab():
    """Test GitLab connection."""
    print("Testing GitLab connection...")
    try:
        client = GitLabClient()
        import requests
        response = requests.get(
            f"{client.base_url}/api/v4/user",
            headers=client.headers
        )
        response.raise_for_status()
        user_data = response.json()
        print(f"✅ GitLab: Connected as {user_data.get('name', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ GitLab: Connection failed - {e}")
        return False


def test_confluence():
    """Test Confluence connection."""
    print("Testing Confluence connection...")
    try:
        client = ConfluenceClient()
        import requests
        response = requests.get(
            f"{client.base_url}/rest/api/user/current",
            auth=client.auth,
            headers=client.headers
        )
        response.raise_for_status()
        user_data = response.json()
        print(f"✅ Confluence: Connected as {user_data.get('displayName', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Confluence: Connection failed - {e}")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("QA Analysis Tool - Connection Test")
    print("=" * 60)
    print()

    # Validate configuration
    print("Checking configuration...")
    is_valid, missing = Config.validate()
    if not is_valid:
        print("❌ Configuration incomplete. Missing fields:")
        for field in missing:
            print(f"   - {field}")
        print("\nPlease check your .env file.")
        sys.exit(1)
    print("✅ Configuration: All required fields present")
    print()

    # Test connections
    results = {
        'jira': test_jira(),
        'gitlab': test_gitlab(),
        'confluence': test_confluence()
    }

    print()
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    all_passed = all(results.values())

    if all_passed:
        print("✅ All connections successful!")
        print("\nYou're ready to run QA analysis:")
        print("python3 qa_analyze.py --jira <YOUR-TICKET-URL>")
    else:
        print("⚠️  Some connections failed:")
        for service, passed in results.items():
            status = "✅ Passed" if passed else "❌ Failed"
            print(f"   {service.capitalize()}: {status}")
        print("\nPlease check your .env file and API tokens.")
        sys.exit(1)


if __name__ == '__main__':
    main()
