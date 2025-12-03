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

    def get_sections(self, project_id: int, suite_id: Optional[int] = None, limit: int = 250, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get all sections (folders) for a project/suite.

        Args:
            project_id: TestRail project ID
            suite_id: Optional suite ID (for multi-suite projects)
            limit: Maximum number of results (default: 250)
            offset: Offset for pagination (default: 0)

        Returns:
            List of section dictionaries
        """
        endpoint = f'get_sections/{project_id}'
        params = []
        if suite_id:
            params.append(f'suite_id={suite_id}')
        params.append(f'limit={limit}')
        params.append(f'offset={offset}')

        if params:
            endpoint += '&' + '&'.join(params)

        result = self._make_request('GET', endpoint)
        # Handle both list and dict with 'sections' key
        if isinstance(result, dict) and 'sections' in result:
            return result['sections']
        return result if isinstance(result, list) else []

    def get_all_sections(self, project_id: int, suite_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get ALL sections for a project/suite with automatic pagination.

        Args:
            project_id: TestRail project ID
            suite_id: Optional suite ID (for multi-suite projects)

        Returns:
            List of all section dictionaries
        """
        all_sections = []
        offset = 0
        limit = 250

        while True:
            sections = self.get_sections(project_id, suite_id, limit, offset)
            if not sections:
                break
            all_sections.extend(sections)
            if len(sections) < limit:
                break
            offset += limit

        return all_sections

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

    # ==================== Test Case Methods ====================

    def get_case_fields(self) -> List[Dict[str, Any]]:
        """
        Get all available custom fields for test cases.

        Returns:
            List of field dictionaries
        """
        result = self._make_request('GET', 'get_case_fields')
        if isinstance(result, list):
            return result
        return []

    def get_case_types(self) -> List[Dict[str, Any]]:
        """
        Get all available test case types.

        Returns:
            List of case type dictionaries
        """
        result = self._make_request('GET', 'get_case_types')
        if isinstance(result, list):
            return result
        return []

    def get_priorities(self) -> List[Dict[str, Any]]:
        """
        Get all available priorities.

        Returns:
            List of priority dictionaries
        """
        result = self._make_request('GET', 'get_priorities')
        if isinstance(result, list):
            return result
        return []

    def get_cases(self, project_id: int, suite_id: Optional[int] = None, section_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get test cases for a project/suite/section.

        Args:
            project_id: TestRail project ID
            suite_id: Optional suite ID
            section_id: Optional section ID to filter by

        Returns:
            List of test case dictionaries
        """
        endpoint = f'get_cases/{project_id}'
        params = []
        if suite_id:
            params.append(f'suite_id={suite_id}')
        if section_id:
            params.append(f'section_id={section_id}')

        if params:
            endpoint += '&' + '&'.join(params)

        result = self._make_request('GET', endpoint)
        if isinstance(result, dict) and 'cases' in result:
            return result['cases']
        return result if isinstance(result, list) else []

    def add_case(
        self,
        section_id: int,
        title: str,
        type_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        estimate: Optional[str] = None,
        refs: Optional[str] = None,
        custom_steps_separated: Optional[List[Dict[str, str]]] = None,
        custom_preconds: Optional[str] = None,
        custom_expected: Optional[str] = None,
        **custom_fields
    ) -> Dict[str, Any]:
        """
        Create a new test case.

        Args:
            section_id: TestRail section ID where the test case will be created
            title: Test case title
            type_id: Optional test case type ID (default: 1 for Functional)
            priority_id: Optional priority ID (default: 2 for Medium)
            estimate: Optional time estimate (e.g., "30s", "1m", "2h")
            refs: Optional references (e.g., Jira ticket IDs)
            custom_steps_separated: Optional list of step dictionaries with 'content' and 'expected' keys
            custom_preconds: Optional preconditions
            custom_expected: Optional expected result
            **custom_fields: Additional custom fields

        Returns:
            Created test case dictionary

        Example:
            add_case(
                section_id=123,
                title="Test login functionality",
                type_id=1,
                priority_id=3,
                custom_steps_separated=[
                    {"content": "Navigate to login page", "expected": "Login page is displayed"},
                    {"content": "Enter credentials", "expected": "Credentials are accepted"}
                ]
            )
        """
        data = {
            'title': title
        }

        if type_id:
            data['type_id'] = type_id

        if priority_id:
            data['priority_id'] = priority_id

        if estimate:
            data['estimate'] = estimate

        if refs:
            data['refs'] = refs

        if custom_steps_separated:
            data['custom_steps_separated'] = custom_steps_separated

        if custom_preconds:
            data['custom_preconds'] = custom_preconds

        if custom_expected:
            data['custom_expected'] = custom_expected

        # Add any additional custom fields
        for key, value in custom_fields.items():
            if value is not None:
                data[key] = value

        return self._make_request('POST', f'add_case/{section_id}', data)

    def update_case(
        self,
        case_id: int,
        title: Optional[str] = None,
        type_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        estimate: Optional[str] = None,
        refs: Optional[str] = None,
        custom_steps_separated: Optional[List[Dict[str, str]]] = None,
        **custom_fields
    ) -> Dict[str, Any]:
        """
        Update an existing test case.

        Args:
            case_id: TestRail test case ID
            title: Optional new title
            type_id: Optional new test case type ID
            priority_id: Optional new priority ID
            estimate: Optional new time estimate
            refs: Optional new references
            custom_steps_separated: Optional new steps
            **custom_fields: Additional custom fields to update

        Returns:
            Updated test case dictionary
        """
        data = {}

        if title:
            data['title'] = title

        if type_id:
            data['type_id'] = type_id

        if priority_id:
            data['priority_id'] = priority_id

        if estimate:
            data['estimate'] = estimate

        if refs:
            data['refs'] = refs

        if custom_steps_separated:
            data['custom_steps_separated'] = custom_steps_separated

        # Add any additional custom fields
        for key, value in custom_fields.items():
            if value is not None:
                data[key] = value

        return self._make_request('POST', f'update_case/{case_id}', data)

    def delete_case(self, case_id: int) -> Dict[str, Any]:
        """
        Delete a test case.

        Args:
            case_id: TestRail test case ID

        Returns:
            Empty dictionary on success
        """
        return self._make_request('POST', f'delete_case/{case_id}')

    # ==================== Test Run Methods ====================

    def get_runs(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Get all test runs for a project.

        Args:
            project_id: TestRail project ID

        Returns:
            List of test run dictionaries
        """
        result = self._make_request('GET', f'get_runs/{project_id}')
        if isinstance(result, dict) and 'runs' in result:
            return result['runs']
        return result if isinstance(result, list) else []

    def get_run(self, run_id: int) -> Dict[str, Any]:
        """
        Get a specific test run.

        Args:
            run_id: TestRail test run ID

        Returns:
            Test run dictionary
        """
        return self._make_request('GET', f'get_run/{run_id}')

    def add_run(
        self,
        project_id: int,
        name: str,
        suite_id: Optional[int] = None,
        description: Optional[str] = None,
        case_ids: Optional[List[int]] = None,
        include_all: bool = True,
        refs: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new test run.

        Args:
            project_id: TestRail project ID
            name: Test run name
            suite_id: Optional suite ID (required for multi-suite projects)
            description: Optional test run description
            case_ids: Optional list of test case IDs to include (if include_all is False)
            include_all: Include all test cases (default: True)
            refs: Optional references (e.g., Jira ticket IDs)

        Returns:
            Created test run dictionary

        Example:
            add_run(
                project_id=2,
                name="CORE-5567 - Test Run",
                suite_id=14,
                description="Testing CORE-5567 functionality",
                case_ids=[424042, 424043, 424044],
                include_all=False,
                refs="CORE-5567"
            )
        """
        data = {
            'name': name,
            'include_all': include_all
        }

        if suite_id:
            data['suite_id'] = suite_id

        if description:
            data['description'] = description

        if refs:
            data['refs'] = refs

        if not include_all and case_ids:
            data['case_ids'] = case_ids

        return self._make_request('POST', f'add_run/{project_id}', data)

    def update_run(
        self,
        run_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        refs: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a test run.

        Args:
            run_id: TestRail test run ID
            name: Optional new name
            description: Optional new description
            refs: Optional new references

        Returns:
            Updated test run dictionary
        """
        data = {}

        if name:
            data['name'] = name

        if description:
            data['description'] = description

        if refs:
            data['refs'] = refs

        return self._make_request('POST', f'update_run/{run_id}', data)

    def close_run(self, run_id: int) -> Dict[str, Any]:
        """
        Close a test run.

        Args:
            run_id: TestRail test run ID

        Returns:
            Closed test run dictionary
        """
        return self._make_request('POST', f'close_run/{run_id}')

    def delete_run(self, run_id: int) -> Dict[str, Any]:
        """
        Delete a test run.

        Args:
            run_id: TestRail test run ID

        Returns:
            Empty dictionary on success
        """
        return self._make_request('POST', f'delete_run/{run_id}')

    def get_cases_from_sections(
        self,
        project_id: int,
        suite_id: int,
        section_names: List[str]
    ) -> List[int]:
        """
        Get all test case IDs from specified sections by name.

        Args:
            project_id: TestRail project ID
            suite_id: TestRail suite ID
            section_names: List of section names to get cases from

        Returns:
            List of test case IDs
        """
        all_case_ids = []

        # Get ALL sections with pagination
        sections = self.get_all_sections(project_id, suite_id)

        # Find sections by name
        for section_name in section_names:
            matching_section = None
            for section in sections:
                if section['name'] == section_name:
                    matching_section = section
                    break

            if matching_section:
                # Get all cases in this section
                cases = self.get_cases(project_id, suite_id, matching_section['id'])
                case_ids = [case['id'] for case in cases]
                all_case_ids.extend(case_ids)
                print(f"✓ Found {len(case_ids)} test cases in section '{section_name}'")
            else:
                print(f"⚠ Warning: Section '{section_name}' not found")

        return all_case_ids
