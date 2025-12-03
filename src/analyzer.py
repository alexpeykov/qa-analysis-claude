"""
QA Analysis orchestrator that fetches and analyzes data from Jira, GitLab, and Confluence.
"""
from typing import Dict, List, Any
from src.jira_client import JiraClient
from src.gitlab_client import GitLabClient
from src.confluence_client import ConfluenceClient


class QAAnalyzer:
    """Main analyzer class for QA ticket analysis."""

    def __init__(self):
        self.jira_client = JiraClient()
        self.gitlab_client = GitLabClient()
        self.confluence_client = ConfluenceClient()

    def fetch_all_data(
        self,
        jira_ticket_url: str,
        linked_ticket_urls: List[str] = None,
        merge_request_urls: List[str] = None,
        confluence_urls: List[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch all data from Jira, GitLab, and Confluence.

        Args:
            jira_ticket_url: URL to main Jira ticket
            linked_ticket_urls: List of URLs to linked Jira tickets
            merge_request_urls: List of URLs to GitLab merge requests
            confluence_urls: List of URLs to Confluence pages

        Returns:
            Dictionary containing all fetched data organized by source
        """
        data = {
            'main_ticket': None,
            'linked_tickets': [],
            'merge_requests': [],
            'documentation': []
        }

        # Fetch main Jira ticket
        print(f"Fetching main Jira ticket: {jira_ticket_url}")
        data['main_ticket'] = self.jira_client.get_ticket_analysis_data(jira_ticket_url)

        # Fetch linked tickets
        if linked_ticket_urls:
            for url in linked_ticket_urls:
                print(f"Fetching linked ticket: {url}")
                try:
                    ticket_data = self.jira_client.get_ticket_analysis_data(url)
                    data['linked_tickets'].append(ticket_data)
                except Exception as e:
                    print(f"Error fetching linked ticket {url}: {e}")
                    data['linked_tickets'].append({'error': str(e), 'url': url})

        # Fetch merge requests
        if merge_request_urls:
            for url in merge_request_urls:
                print(f"Fetching merge request: {url}")
                try:
                    mr_data = self.gitlab_client.get_merge_request_analysis_data(url)
                    data['merge_requests'].append(mr_data)
                except Exception as e:
                    print(f"Error fetching merge request {url}: {e}")
                    data['merge_requests'].append({'error': str(e), 'url': url})

        # Fetch Confluence documentation
        if confluence_urls:
            for url in confluence_urls:
                print(f"Fetching Confluence page: {url}")
                try:
                    page_data = self.confluence_client.get_page_analysis_data(url)
                    data['documentation'].append(page_data)
                except Exception as e:
                    print(f"Error fetching Confluence page {url}: {e}")
                    data['documentation'].append({'error': str(e), 'url': url})

        return data

    def format_data_for_analysis(self, data: Dict[str, Any]) -> str:
        """
        Format fetched data into a comprehensive text summary for Claude analysis.

        Args:
            data: Dictionary containing all fetched data

        Returns:
            Formatted string containing all relevant information
        """
        output = []

        # Main Ticket Section
        output.append("=" * 80)
        output.append("MAIN JIRA TICKET")
        output.append("=" * 80)

        if data['main_ticket']:
            ticket = data['main_ticket']
            output.append(f"\nTicket Key: {ticket['ticket_key']}")
            output.append(f"Summary: {ticket['summary']}")
            output.append(f"Type: {ticket['issue_type']}")
            output.append(f"Status: {ticket['status']}")
            output.append(f"Priority: {ticket['priority']}")
            output.append(f"Assignee: {ticket['assignee']}")
            output.append(f"Reporter: {ticket['reporter']}")
            output.append(f"\nDescription:\n{ticket['description']}")

            if ticket['comments']:
                output.append(f"\n--- Comments ({len(ticket['comments'])}) ---")
                for i, comment in enumerate(ticket['comments'], 1):
                    author = comment.get('author', {}).get('displayName', 'Unknown')
                    created = comment.get('created', '')
                    body = comment.get('body', '')
                    output.append(f"\nComment #{i} by {author} on {created}:")
                    output.append(body)

            if ticket['linked_tickets']:
                output.append(f"\n--- Linked Tickets ({len(ticket['linked_tickets'])}) ---")
                for link in ticket['linked_tickets']:
                    output.append(f"- {link['key']}: {link['summary']} ({link['type']}, Status: {link['status']})")

        # Linked Tickets Section
        if data['linked_tickets']:
            output.append("\n" + "=" * 80)
            output.append("LINKED JIRA TICKETS")
            output.append("=" * 80)

            for ticket in data['linked_tickets']:
                if 'error' in ticket:
                    output.append(f"\nError fetching {ticket.get('url', 'unknown')}: {ticket['error']}")
                    continue

                output.append(f"\n--- {ticket['ticket_key']} ---")
                output.append(f"Summary: {ticket['summary']}")
                output.append(f"Status: {ticket['status']}")
                output.append(f"Priority: {ticket['priority']}")
                output.append(f"\nDescription:\n{ticket['description']}")

                if ticket['comments']:
                    output.append(f"\nComments ({len(ticket['comments'])}):")
                    for i, comment in enumerate(ticket['comments'], 1):
                        author = comment.get('author', {}).get('displayName', 'Unknown')
                        body = comment.get('body', '')
                        output.append(f"\nComment #{i} by {author}:")
                        output.append(body)

        # Merge Requests Section
        if data['merge_requests']:
            output.append("\n" + "=" * 80)
            output.append("GITLAB MERGE REQUESTS")
            output.append("=" * 80)

            for mr in data['merge_requests']:
                if 'error' in mr:
                    output.append(f"\nError fetching {mr.get('url', 'unknown')}: {mr['error']}")
                    continue

                output.append(f"\n--- Merge Request: {mr['title']} ---")
                output.append(f"State: {mr['state']}")
                output.append(f"Author: {mr['author']}")
                output.append(f"Branch: {mr['source_branch']} → {mr['target_branch']}")
                output.append(f"Files Changed: {mr['files_changed']}")
                output.append(f"\nDescription:\n{mr['description']}")

                output.append(f"\n--- Commits ({len(mr['commits'])}) ---")
                for commit in mr['commits']:
                    output.append(f"- {commit.get('short_id', '')}: {commit.get('title', '')}")

                output.append(f"\n--- Code Changes ---")
                for change in mr['changes'][:10]:  # Limit to first 10 files
                    output.append(f"\nFile: {change.get('new_path', change.get('old_path', 'unknown'))}")
                    output.append(f"Status: {change.get('new_file', False) and 'New' or change.get('deleted_file', False) and 'Deleted' or 'Modified'}")

                    diff = change.get('diff', '')
                    if len(diff) > 1000:
                        output.append(f"Diff (truncated): {diff[:1000]}... [truncated]")
                    else:
                        output.append(f"Diff: {diff}")

                if len(mr['changes']) > 10:
                    output.append(f"\n... and {len(mr['changes']) - 10} more files")

                if mr['discussions']:
                    output.append(f"\n--- Discussions/Comments ({len(mr['discussions'])}) ---")
                    for discussion in mr['discussions']:
                        for note in discussion.get('notes', []):
                            author = note.get('author', {}).get('name', 'Unknown')
                            body = note.get('body', '')
                            output.append(f"\n{author}: {body}")

        # Documentation Section
        if data['documentation']:
            output.append("\n" + "=" * 80)
            output.append("CONFLUENCE DOCUMENTATION")
            output.append("=" * 80)

            for page in data['documentation']:
                if 'error' in page:
                    output.append(f"\nError fetching {page.get('url', 'unknown')}: {page['error']}")
                    continue

                output.append(f"\n--- {page['title']} ---")
                output.append(f"Space: {page['space']}")
                output.append(f"Version: {page['version']}")
                output.append(f"Last Updated: {page['last_updated']}")
                output.append(f"\nContent:\n{page['content']}")

                if page['comments']:
                    output.append(f"\n--- Comments ({len(page['comments'])}) ---")
                    for comment in page['comments']:
                        body = comment.get('body', {}).get('view', {}).get('value', '')
                        output.append(f"\n{body}")

        return "\n".join(output)
