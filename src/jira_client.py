"""
Jira API client for fetching ticket information.
"""
import requests
from typing import Dict, List, Any, Optional
from requests.auth import HTTPBasicAuth
from src.config import Config


class JiraClient:
    """Client for interacting with Jira API."""

    def __init__(self):
        self.base_url = Config.JIRA_URL.rstrip('/')
        self.auth = HTTPBasicAuth(Config.JIRA_EMAIL, Config.JIRA_API_TOKEN)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_ticket(self, ticket_key: str) -> Dict[str, Any]:
        """
        Fetch a Jira ticket by its key.

        Args:
            ticket_key: Jira ticket key (e.g., PROJ-123)

        Returns:
            Dictionary containing ticket information
        """
        url = f"{self.base_url}/rest/api/2/issue/{ticket_key}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_ticket_comments(self, ticket_key: str) -> List[Dict[str, Any]]:
        """
        Fetch all comments for a Jira ticket.

        Args:
            ticket_key: Jira ticket key

        Returns:
            List of comment dictionaries
        """
        url = f"{self.base_url}/rest/api/2/issue/{ticket_key}/comment"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data.get('comments', [])

    def get_linked_tickets(self, ticket_key: str) -> List[Dict[str, Any]]:
        """
        Fetch all linked tickets for a Jira ticket.

        Args:
            ticket_key: Jira ticket key

        Returns:
            List of linked ticket information
        """
        ticket = self.get_ticket(ticket_key)
        issue_links = ticket.get('fields', {}).get('issuelinks', [])

        linked_tickets = []
        for link in issue_links:
            if 'outwardIssue' in link:
                linked_tickets.append({
                    'key': link['outwardIssue']['key'],
                    'type': link['type']['outward'],
                    'summary': link['outwardIssue']['fields']['summary'],
                    'status': link['outwardIssue']['fields']['status']['name']
                })
            elif 'inwardIssue' in link:
                linked_tickets.append({
                    'key': link['inwardIssue']['key'],
                    'type': link['type']['inward'],
                    'summary': link['inwardIssue']['fields']['summary'],
                    'status': link['inwardIssue']['fields']['status']['name']
                })

        return linked_tickets

    def extract_ticket_key_from_url(self, url: str) -> Optional[str]:
        """
        Extract ticket key from Jira URL.

        Args:
            url: Jira ticket URL

        Returns:
            Ticket key or None if not found
        """
        # Handle URLs like https://jira.paysera.net/browse/PROJ-123
        parts = url.split('/')
        if 'browse' in parts:
            idx = parts.index('browse')
            if idx + 1 < len(parts):
                return parts[idx + 1].split('?')[0]
        return None

    def get_ticket_analysis_data(self, ticket_url: str) -> Dict[str, Any]:
        """
        Get comprehensive ticket data for analysis.

        Args:
            ticket_url: URL to Jira ticket

        Returns:
            Dictionary with ticket, comments, and linked tickets data
        """
        ticket_key = self.extract_ticket_key_from_url(ticket_url)
        if not ticket_key:
            raise ValueError(f"Could not extract ticket key from URL: {ticket_url}")

        ticket = self.get_ticket(ticket_key)
        comments = self.get_ticket_comments(ticket_key)
        linked_tickets = self.get_linked_tickets(ticket_key)

        return {
            'ticket_key': ticket_key,
            'summary': ticket['fields'].get('summary', ''),
            'description': ticket['fields'].get('description', ''),
            'status': ticket['fields'].get('status', {}).get('name', ''),
            'priority': ticket['fields'].get('priority', {}).get('name', ''),
            'assignee': ticket['fields'].get('assignee', {}).get('displayName', 'Unassigned'),
            'reporter': ticket['fields'].get('reporter', {}).get('displayName', 'Unknown'),
            'created': ticket['fields'].get('created', ''),
            'updated': ticket['fields'].get('updated', ''),
            'issue_type': ticket['fields'].get('issuetype', {}).get('name', ''),
            'comments': comments,
            'linked_tickets': linked_tickets,
            'full_data': ticket
        }
