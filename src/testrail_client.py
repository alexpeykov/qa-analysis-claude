"""
TestRail API client for creating folders, test cases, and test runs.
"""
import requests
from typing import Dict, List, Any, Optional
from requests.auth import HTTPBasicAuth
from src.config import Config


class TestRailClient:
    """Client for interacting with TestRail API."""

    def __init__(self):
        self.base_url = Config.TESTRAIL_URL.rstrip('/')
        self.email = Config.TESTRAIL_EMAIL
        self.api_key = Config.TESTRAIL_API_KEY
        self.auth = HTTPBasicAuth(self.email, self.api_key)
        self.headers = {
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an API request to TestRail.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., 'add_section/1')
            data: Request payload for POST/UPDATE requests

        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}/index.php?/api/v2/{endpoint}"

        try:
            if method == 'GET':
                response = requests.get(url, auth=self.auth, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, auth=self.auth, headers=self.headers, json=data)
            elif method == 'UPDATE':
                response = requests.post(url, auth=self.auth, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json() if response.text else {}

        except requests.exceptions.HTTPError as e:
            error_msg = f"TestRail API Error: {e}"
            if hasattr(e.response, 'text'):
                error_msg += f"\nResponse: {e.response.text}"
            raise Exception(error_msg)

    # ==================== Project Methods ====================

    def get_projects(self) -> List[Dict[str, Any]]:
        """
        Get all projects.

        Returns:
            List of project dictionaries
        """
        result = self._make_request('GET', 'get_projects')
        # Handle both list and dict with 'projects' key
        if isinstance(result, dict) and 'projects' in result:
            return result['projects']
        return result if isinstance(result, list) else []

    def get_project(self, project_id: int) -> Dict[str, Any]:
        """
        Get a specific project by ID.

        Args:
            project_id: TestRail project ID

        Returns:
            Project dictionary
        """
        return self._make_request('GET', f'get_project/{project_id}')

    # ==================== Suite Methods ====================

    def get_suites(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Get all test suites for a project.

        Args:
            project_id: TestRail project ID

        Returns:
            List of suite dictionaries
        """
        result = self._make_request('GET', f'get_suites/{project_id}')
        # Handle both list and dict with 'suites' key
        if isinstance(result, dict) and 'suites' in result:
            return result['suites']
        return result if isinstance(result, list) else []

    def get_suite(self, suite_id: int) -> Dict[str, Any]:
        """
        Get a specific test suite.

        Args:
            suite_id: TestRail suite ID

        Returns:
            Suite dictionary
        """
        return self._make_request('GET', f'get_suite/{suite_id}')

    # ==================== Section (Folder) Methods ====================

    def get_sections(self, project_id: int, suite_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all sections (folders) for a project/suite.

        Args:
            project_id: TestRail project ID
            suite_id: Optional suite ID (for multi-suite projects)

        Returns:
            List of section dictionaries
        """
        endpoint = f'get_sections/{project_id}'
        if suite_id:
            endpoint += f'&suite_id={suite_id}'
        result = self._make_request('GET', endpoint)
        # Handle both list and dict with 'sections' key
        if isinstance(result, dict) and 'sections' in result:
            return result['sections']
        return result if isinstance(result, list) else []

    def add_section(
        self,
        project_id: int,
        name: str,
        suite_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new section (folder) in TestRail.

        Args:
            project_id: TestRail project ID
            name: Section name
            suite_id: Optional suite ID (required for multi-suite projects)
            parent_id: Optional parent section ID (for nested folders)
            description: Optional section description

        Returns:
            Created section dictionary with id, name, parent_id, etc.
        """
        data = {
            'name': name
        }

        if suite_id:
            data['suite_id'] = suite_id

        if parent_id:
            data['parent_id'] = parent_id

        if description:
            data['description'] = description

        return self._make_request('POST', f'add_section/{project_id}', data)

    def update_section(
        self,
        section_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing section (folder).

        Args:
            section_id: TestRail section ID
            name: Optional new section name
            description: Optional new description

        Returns:
            Updated section dictionary
        """
        data = {}

        if name:
            data['name'] = name

        if description:
            data['description'] = description

        return self._make_request('POST', f'update_section/{section_id}', data)

    def delete_section(self, section_id: int) -> Dict[str, Any]:
        """
        Delete a section (folder).

        Args:
            section_id: TestRail section ID

        Returns:
            Empty dictionary on success
        """
        return self._make_request('POST', f'delete_section/{section_id}')

    # ==================== Helper Methods ====================

    def find_section_by_name(
        self,
        project_id: int,
        section_name: str,
        suite_id: Optional[int] = None,
        parent_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Find a section by name.

        Args:
            project_id: TestRail project ID
            section_name: Section name to search for
            suite_id: Optional suite ID
            parent_id: Optional parent section ID

        Returns:
            Section dictionary if found, None otherwise
        """
        sections = self.get_sections(project_id, suite_id)

        for section in sections:
            if section['name'] == section_name:
                # If parent_id is specified, check if it matches
                if parent_id is not None:
                    if section.get('parent_id') == parent_id:
                        return section
                else:
                    return section

        return None

    def get_or_create_section(
        self,
        project_id: int,
        name: str,
        suite_id: Optional[int] = None,
        parent_id: Optional[int] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get existing section or create if it doesn't exist.

        Args:
            project_id: TestRail project ID
            name: Section name
            suite_id: Optional suite ID
            parent_id: Optional parent section ID
            description: Optional description (only used when creating)

        Returns:
            Section dictionary (existing or newly created)
        """
        # Try to find existing section
        existing = self.find_section_by_name(project_id, name, suite_id, parent_id)

        if existing:
            print(f"✓ Section '{name}' already exists (ID: {existing['id']})")
            return existing

        # Create new section
        print(f"Creating section '{name}'...")
        section = self.add_section(project_id, name, suite_id, parent_id, description)
        print(f"✓ Created section '{name}' (ID: {section['id']})")
        return section

    def create_nested_sections(
        self,
        project_id: int,
        path: List[str],
        suite_id: Optional[int] = None,
        descriptions: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create nested sections (folder hierarchy).

        Args:
            project_id: TestRail project ID
            path: List of section names in hierarchy (e.g., ['Parent', 'Child', 'Grandchild'])
            suite_id: Optional suite ID
            descriptions: Optional dictionary mapping section names to descriptions

        Returns:
            The deepest (last) section dictionary

        Example:
            create_nested_sections(1, ['QA Tests', 'CORE-5725', 'Functional Tests'])
            Creates: QA Tests/CORE-5725/Functional Tests
        """
        parent_id = None
        section = None
        descriptions = descriptions or {}

        for section_name in path:
            description = descriptions.get(section_name)
            section = self.get_or_create_section(
                project_id=project_id,
                name=section_name,
                suite_id=suite_id,
                parent_id=parent_id,
                description=description
            )
            parent_id = section['id']

        return section
