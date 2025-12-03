"""
GitLab API client for fetching merge request information.
"""
import requests
from typing import Dict, List, Any, Optional
from urllib.parse import quote
from src.config import Config


class GitLabClient:
    """Client for interacting with GitLab API."""

    def __init__(self):
        self.base_url = Config.GITLAB_URL.rstrip('/')
        self.token = Config.GITLAB_PERSONAL_ACCESS_TOKEN
        self.headers = {
            'PRIVATE-TOKEN': self.token,
            'Content-Type': 'application/json'
        }

    def extract_mr_info_from_url(self, url: str) -> Optional[tuple[str, str]]:
        """
        Extract project path and MR IID from GitLab URL.

        Args:
            url: GitLab merge request URL

        Returns:
            Tuple of (project_path, mr_iid) or None
        """
        # Handle URLs like https://gitlab.paysera.net/project/subproject/-/merge_requests/123
        try:
            parts = url.split('/-/merge_requests/')
            if len(parts) == 2:
                mr_iid = parts[1].split('?')[0].split('#')[0]
                project_part = parts[0].replace(self.base_url + '/', '')
                return (project_part, mr_iid)
        except Exception:
            pass
        return None

    def get_merge_request(self, project_path: str, mr_iid: str) -> Dict[str, Any]:
        """
        Fetch merge request details.

        Args:
            project_path: GitLab project path
            mr_iid: Merge request IID

        Returns:
            Dictionary containing MR information
        """
        encoded_project = quote(project_path, safe='')
        url = f"{self.base_url}/api/v4/projects/{encoded_project}/merge_requests/{mr_iid}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_merge_request_changes(self, project_path: str, mr_iid: str) -> Dict[str, Any]:
        """
        Fetch merge request file changes.

        Args:
            project_path: GitLab project path
            mr_iid: Merge request IID

        Returns:
            Dictionary containing MR changes
        """
        encoded_project = quote(project_path, safe='')
        url = f"{self.base_url}/api/v4/projects/{encoded_project}/merge_requests/{mr_iid}/changes"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_merge_request_discussions(self, project_path: str, mr_iid: str) -> List[Dict[str, Any]]:
        """
        Fetch merge request discussions/comments.

        Args:
            project_path: GitLab project path
            mr_iid: Merge request IID

        Returns:
            List of discussion dictionaries
        """
        encoded_project = quote(project_path, safe='')
        url = f"{self.base_url}/api/v4/projects/{encoded_project}/merge_requests/{mr_iid}/discussions"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_merge_request_commits(self, project_path: str, mr_iid: str) -> List[Dict[str, Any]]:
        """
        Fetch merge request commits.

        Args:
            project_path: GitLab project path
            mr_iid: Merge request IID

        Returns:
            List of commit dictionaries
        """
        encoded_project = quote(project_path, safe='')
        url = f"{self.base_url}/api/v4/projects/{encoded_project}/merge_requests/{mr_iid}/commits"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_merge_request_analysis_data(self, mr_url: str) -> Dict[str, Any]:
        """
        Get comprehensive MR data for analysis.

        Args:
            mr_url: URL to GitLab merge request

        Returns:
            Dictionary with MR details, changes, discussions, and commits
        """
        mr_info = self.extract_mr_info_from_url(mr_url)
        if not mr_info:
            raise ValueError(f"Could not extract MR info from URL: {mr_url}")

        project_path, mr_iid = mr_info

        mr = self.get_merge_request(project_path, mr_iid)
        changes = self.get_merge_request_changes(project_path, mr_iid)
        discussions = self.get_merge_request_discussions(project_path, mr_iid)
        commits = self.get_merge_request_commits(project_path, mr_iid)

        return {
            'title': mr.get('title', ''),
            'description': mr.get('description', ''),
            'state': mr.get('state', ''),
            'author': mr.get('author', {}).get('name', ''),
            'source_branch': mr.get('source_branch', ''),
            'target_branch': mr.get('target_branch', ''),
            'created_at': mr.get('created_at', ''),
            'updated_at': mr.get('updated_at', ''),
            'merged_at': mr.get('merged_at', ''),
            'changes': changes.get('changes', []),
            'discussions': discussions,
            'commits': commits,
            'files_changed': len(changes.get('changes', [])),
            'full_data': mr
        }
