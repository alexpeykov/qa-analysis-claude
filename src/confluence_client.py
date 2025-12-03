"""
Confluence API client for fetching documentation.
"""
import requests
from typing import Dict, List, Any, Optional
from requests.auth import HTTPBasicAuth
from src.config import Config


class ConfluenceClient:
    """Client for interacting with Confluence API."""

    def __init__(self):
        self.base_url = Config.CONFLUENCE_URL.rstrip('/')
        self.auth = HTTPBasicAuth(Config.CONFLUENCE_EMAIL, Config.CONFLUENCE_API_TOKEN)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def extract_page_id_from_url(self, url: str) -> Optional[str]:
        """
        Extract page ID from Confluence URL.

        Args:
            url: Confluence page URL

        Returns:
            Page ID or None if not found
        """
        # Handle URLs like https://intranet.paysera.net/pages/viewpage.action?pageId=123456
        # or https://intranet.paysera.net/display/SPACE/Page+Title
        try:
            if 'pageId=' in url:
                page_id = url.split('pageId=')[1].split('&')[0]
                return page_id
            elif '/display/' in url:
                # For display URLs, we need to search by title or use a different approach
                # This is a simplified version - may need enhancement
                return None
        except Exception:
            pass
        return None

    def get_page(self, page_id: str) -> Dict[str, Any]:
        """
        Fetch Confluence page by ID.

        Args:
            page_id: Confluence page ID

        Returns:
            Dictionary containing page information
        """
        url = f"{self.base_url}/rest/api/content/{page_id}"
        params = {
            'expand': 'body.storage,version,space,history'
        }
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_page_comments(self, page_id: str) -> List[Dict[str, Any]]:
        """
        Fetch comments for a Confluence page.

        Args:
            page_id: Confluence page ID

        Returns:
            List of comment dictionaries
        """
        url = f"{self.base_url}/rest/api/content/{page_id}/child/comment"
        params = {
            'expand': 'body.view,version,history'
        }
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])

    def get_page_by_title(self, space_key: str, title: str) -> Optional[Dict[str, Any]]:
        """
        Search for a page by space and title.

        Args:
            space_key: Confluence space key
            title: Page title

        Returns:
            Page data or None if not found
        """
        url = f"{self.base_url}/rest/api/content"
        params = {
            'spaceKey': space_key,
            'title': title,
            'expand': 'body.storage,version,space,history'
        }
        response = requests.get(url, auth=self.auth, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])
        return results[0] if results else None

    def get_page_analysis_data(self, page_url: str) -> Dict[str, Any]:
        """
        Get comprehensive page data for analysis.

        Args:
            page_url: URL to Confluence page

        Returns:
            Dictionary with page content and metadata
        """
        page_id = self.extract_page_id_from_url(page_url)
        if not page_id:
            raise ValueError(f"Could not extract page ID from URL: {page_url}. Please use URLs with pageId parameter.")

        page = self.get_page(page_id)
        comments = self.get_page_comments(page_id)

        return {
            'page_id': page_id,
            'title': page.get('title', ''),
            'content': page.get('body', {}).get('storage', {}).get('value', ''),
            'space': page.get('space', {}).get('name', ''),
            'space_key': page.get('space', {}).get('key', ''),
            'created_by': page.get('history', {}).get('createdBy', {}).get('displayName', ''),
            'created_date': page.get('history', {}).get('createdDate', ''),
            'last_updated': page.get('version', {}).get('when', ''),
            'version': page.get('version', {}).get('number', ''),
            'comments': comments,
            'full_data': page
        }
