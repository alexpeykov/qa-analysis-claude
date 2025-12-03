#!/usr/bin/env python3
"""
Script to create folders (sections) in TestRail.

Usage:
    python3 create_testrail_folder.py --project 1 --folder "My Test Folder"
    python3 create_testrail_folder.py --project 1 --folder "Parent/Child/Grandchild"
    python3 create_testrail_folder.py --project 1 --suite 2 --folder "Suite Folder"
"""

import argparse
import sys
from src.config import Config
from src.testrail_client import TestRailClient


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Create folders (sections) in TestRail',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a single folder
  python3 create_testrail_folder.py --project 1 --folder "QA Tests"

  # Create nested folders (hierarchy)
  python3 create_testrail_folder.py --project 1 --folder "QA Tests/CORE-5725/Functional"

  # Create folder in specific suite
  python3 create_testrail_folder.py --project 1 --suite 2 --folder "Regression Tests"

  # With description
  python3 create_testrail_folder.py --project 1 --folder "CORE-5725" --description "Test cases for ticket CORE-5725"
        """
    )

    parser.add_argument(
        '--project',
        '-p',
        type=int,
        help='TestRail project ID'
    )

    parser.add_argument(
        '--folder',
        '-f',
        help='Folder name or path (e.g., "Parent/Child" for nested folders)'
    )

    parser.add_argument(
        '--suite',
        '-s',
        type=int,
        help='Optional suite ID (for multi-suite projects)'
    )

    parser.add_argument(
        '--description',
        '-d',
        help='Optional folder description (only applies to last folder in path)'
    )

    parser.add_argument(
        '--list-projects',
        action='store_true',
        help='List all available projects and exit'
    )

    parser.add_argument(
        '--list-suites',
        type=int,
        metavar='PROJECT_ID',
        help='List all suites for a project and exit'
    )

    parser.add_argument(
        '--list-sections',
        type=int,
        metavar='PROJECT_ID',
        help='List all existing sections for a project and exit'
    )

    return parser.parse_args()


def list_projects(client: TestRailClient):
    """List all projects."""
    print("\n" + "=" * 80)
    print("Available Projects:")
    print("=" * 80)

    projects = client.get_projects()

    for project in projects:
        print(f"\nID: {project['id']}")
        print(f"Name: {project['name']}")
        print(f"Announcement: {project.get('announcement', 'None')}")
        print(f"Suite Mode: {project['suite_mode']}")  # 1 = single suite, 2 = single suite + baselines, 3 = multiple suites


def list_suites(client: TestRailClient, project_id: int):
    """List all suites for a project."""
    print("\n" + "=" * 80)
    print(f"Suites for Project {project_id}:")
    print("=" * 80)

    suites = client.get_suites(project_id)

    if not suites:
        print("No suites found. This might be a single-suite project.")
        return

    for suite in suites:
        print(f"\nID: {suite['id']}")
        print(f"Name: {suite['name']}")
        print(f"Description: {suite.get('description', 'None')}")


def list_sections(client: TestRailClient, project_id: int, suite_id: int = None):
    """List all sections for a project."""
    print("\n" + "=" * 80)
    print(f"Sections for Project {project_id}:")
    if suite_id:
        print(f"Suite: {suite_id}")
    print("=" * 80)

    sections = client.get_sections(project_id, suite_id)

    if not sections:
        print("No sections found.")
        return

    # Group by depth
    def print_section(section, indent=0):
        prefix = "  " * indent + "├─ "
        print(f"{prefix}[{section['id']}] {section['name']}")
        if section.get('description'):
            print(f"{' ' * (indent * 2 + 3)}Description: {section['description']}")

    # Build hierarchy
    sections_by_parent = {}
    for section in sections:
        parent_id = section.get('parent_id')
        if parent_id not in sections_by_parent:
            sections_by_parent[parent_id] = []
        sections_by_parent[parent_id].append(section)

    # Print root sections and their children recursively
    def print_hierarchy(parent_id, indent=0):
        if parent_id in sections_by_parent:
            for section in sections_by_parent[parent_id]:
                print_section(section, indent)
                print_hierarchy(section['id'], indent + 1)

    print_hierarchy(None, 0)


def main():
    """Main execution function."""
    args = parse_arguments()

    # Validate configuration
    if not Config.TESTRAIL_URL or not Config.TESTRAIL_EMAIL or not Config.TESTRAIL_API_KEY:
        print("ERROR: TestRail credentials not configured.", file=sys.stderr)
        print("Please ensure TESTRAIL_URL, TESTRAIL_EMAIL, and TESTRAIL_API_KEY are set in .env file.", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    client = TestRailClient()

    # Handle list commands
    if args.list_projects:
        list_projects(client)
        return

    if args.list_suites is not None:
        list_suites(client, args.list_suites)
        return

    if args.list_sections is not None:
        list_sections(client, args.list_sections, args.suite)
        return

    # Validate required arguments for folder creation
    if not args.project or not args.folder:
        print("ERROR: --project and --folder are required for creating folders.", file=sys.stderr)
        print("Use --help for usage information.", file=sys.stderr)
        sys.exit(1)

    # Create folder(s)
    print("\n" + "=" * 80)
    print("Creating TestRail Folder(s)")
    print("=" * 80)
    print(f"Project ID: {args.project}")
    if args.suite:
        print(f"Suite ID: {args.suite}")
    print(f"Folder Path: {args.folder}")
    if args.description:
        print(f"Description: {args.description}")
    print("=" * 80)
    print()

    try:
        # Split folder path into hierarchy
        folder_path = [name.strip() for name in args.folder.split('/') if name.strip()]

        if not folder_path:
            print("ERROR: Invalid folder path.", file=sys.stderr)
            sys.exit(1)

        # Create nested sections
        descriptions = {}
        if args.description and len(folder_path) > 0:
            # Apply description to the last folder in path
            descriptions[folder_path[-1]] = args.description

        result = client.create_nested_sections(
            project_id=args.project,
            path=folder_path,
            suite_id=args.suite,
            descriptions=descriptions
        )

        print()
        print("=" * 80)
        print("✓ Folder Creation Complete!")
        print("=" * 80)
        print(f"Final Section ID: {result['id']}")
        print(f"Final Section Name: {result['name']}")
        print(f"Parent ID: {result.get('parent_id', 'None (root level)')}")
        print(f"Suite ID: {result.get('suite_id', 'None')}")
        print()
        print(f"TestRail URL: {Config.TESTRAIL_URL}/index.php?/suites/view/{result.get('suite_id', 0)}")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
