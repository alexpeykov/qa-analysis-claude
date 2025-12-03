"""
Configuration module for loading credentials from environment variables.
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API credentials and URLs."""

    # Jira Configuration
    JIRA_URL: str = os.getenv('JIRA_URL', '')
    JIRA_EMAIL: str = os.getenv('JIRA_EMAIL', '')
    JIRA_API_TOKEN: str = os.getenv('JIRA_API_TOKEN', '')

    # GitLab Configuration
    GITLAB_URL: str = os.getenv('GITLAB_URL', '')
    GITLAB_EMAIL: str = os.getenv('GITLAB_EMAIL', '')
    GITLAB_PERSONAL_ACCESS_TOKEN: str = os.getenv('GITLAB_PERSONAL_ACCESS_TOKEN', '')
    GITLAB_FEED_TOKEN: str = os.getenv('GITLAB_FEED_TOKEN', '')

    # Confluence Configuration
    CONFLUENCE_URL: str = os.getenv('CONFLUENCE_URL', '')
    CONFLUENCE_EMAIL: str = os.getenv('CONFLUENCE_EMAIL', '')
    CONFLUENCE_API_TOKEN: str = os.getenv('CONFLUENCE_API_TOKEN', '')

    # TestRail Configuration
    TESTRAIL_URL: str = os.getenv('TESTRAIL_URL', '')
    TESTRAIL_EMAIL: str = os.getenv('TESTRAIL_EMAIL', '')
    TESTRAIL_API_KEY: str = os.getenv('TESTRAIL_API_KEY', '')

    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate that all required configuration values are present.

        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        missing = []

        if not cls.JIRA_URL:
            missing.append('JIRA_URL')
        if not cls.JIRA_EMAIL:
            missing.append('JIRA_EMAIL')
        if not cls.JIRA_API_TOKEN:
            missing.append('JIRA_API_TOKEN')

        if not cls.GITLAB_URL:
            missing.append('GITLAB_URL')
        if not cls.GITLAB_EMAIL:
            missing.append('GITLAB_EMAIL')
        if not cls.GITLAB_PERSONAL_ACCESS_TOKEN:
            missing.append('GITLAB_PERSONAL_ACCESS_TOKEN')

        if not cls.CONFLUENCE_URL:
            missing.append('CONFLUENCE_URL')
        if not cls.CONFLUENCE_EMAIL:
            missing.append('CONFLUENCE_EMAIL')
        if not cls.CONFLUENCE_API_TOKEN:
            missing.append('CONFLUENCE_API_TOKEN')

        return (len(missing) == 0, missing)
