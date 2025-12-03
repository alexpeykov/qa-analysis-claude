#!/usr/bin/env python3
"""
Script to create test cases in TestRail.

This script creates test cases in a specified TestRail section/folder with
configurable properties like type, priority, and steps.
"""

import argparse
import sys
from typing import List, Dict, Any
from src.testrail_client import TestRailClient


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Create test cases in TestRail',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create test cases from command line
  python3 create_test_cases.py \\
    --project 2 \\
    --suite 14 \\
    --section-name "5567 - Add persisted events" \\
    --type "Functional" \\
    --priority "High" \\
    --title "Load DB fixtures from test plan" \\
    --steps "Switch to local DB" "Load the fixtures from the test plan" "Examine the output" \\
    --expected "Fixtures imported without errors" "Info present in DB tables" "Output verified"

  # Create test case with references
  python3 create_test_cases.py \\
    --project 2 \\
    --suite 14 \\
    --section-id 90046 \\
    --type "Functional" \\
    --priority "High" \\
    --title "Process transfer 9990001" \\
    --refs "CORE-5567" \\
    --steps "Enter evpbank container" "Execute command" "Examine output" \\
    --expected "Command executes without errors" "Statement is created" "Output verified"
        """
    )

    # Required arguments
    parser.add_argument(
        '--project',
        type=int,
        required=True,
        help='TestRail project ID'
    )

    parser.add_argument(
        '--suite',
        type=int,
        help='TestRail suite ID (required for multi-suite projects)'
    )

    # Section identification (one of these is required)
    section_group = parser.add_mutually_exclusive_group(required=True)
    section_group.add_argument(
        '--section-id',
        type=int,
        help='TestRail section ID (if you know it)'
    )
    section_group.add_argument(
        '--section-name',
        type=str,
        help='TestRail section name (will search for it)'
    )

    # Test case properties
    parser.add_argument(
        '--type',
        default='Functional',
        help='Test case type (default: Functional). Options: Functional, Acceptance, Regression, etc.'
    )

    parser.add_argument(
        '--priority',
        default='Medium',
        help='Test case priority (default: Medium). Options: Low, Medium, High, Critical'
    )

    parser.add_argument(
        '--title',
        required=True,
        help='Test case title'
    )

    parser.add_argument(
        '--refs',
        help='References (e.g., Jira ticket IDs like "CORE-5567")'
    )

    parser.add_argument(
        '--estimate',
        help='Time estimate (e.g., "30s", "1m", "2h")'
    )

    parser.add_argument(
        '--preconditions',
        help='Preconditions for the test case'
    )

    parser.add_argument(
        '--steps',
        nargs='+',
        help='Test steps (space-separated)'
    )

    parser.add_argument(
        '--expected',
        nargs='+',
        help='Expected results for each step (space-separated, must match number of steps)'
    )

    return parser.parse_args()


def get_type_id(client: TestRailClient, type_name: str) -> int:
    """Get type ID from type name."""
    types = client.get_case_types()
    type_map = {t['name'].lower(): t['id'] for t in types}

    type_name_lower = type_name.lower()
    if type_name_lower in type_map:
        return type_map[type_name_lower]

    # Default to Functional (usually ID 1)
    print(f"Warning: Type '{type_name}' not found, using 'Functional' (ID: 1)")
    return 1


def get_priority_id(client: TestRailClient, priority_name: str) -> int:
    """Get priority ID from priority name."""
    priorities = client.get_priorities()
    priority_map = {p['name'].lower(): p['id'] for p in priorities}

    priority_name_lower = priority_name.lower()
    if priority_name_lower in priority_map:
        return priority_map[priority_name_lower]

    # Default to Medium (usually ID 2)
    print(f"Warning: Priority '{priority_name}' not found, using 'Medium' (ID: 2)")
    return 2


def get_section_id(client: TestRailClient, project_id: int, suite_id: int, section_name: str) -> int:
    """Get section ID from section name."""
    section = client.find_section_by_name(project_id, section_name, suite_id)
    if not section:
        raise ValueError(f"Section '{section_name}' not found in project {project_id}, suite {suite_id}")
    return section['id']


def create_test_case(
    client: TestRailClient,
    section_id: int,
    title: str,
    type_id: int,
    priority_id: int,
    refs: str = None,
    estimate: str = None,
    preconditions: str = None,
    steps: List[str] = None,
    expected: List[str] = None
) -> Dict[str, Any]:
    """Create a single test case."""

    # Build steps if provided
    custom_steps = None
    if steps:
        if not expected or len(expected) != len(steps):
            raise ValueError(f"Number of expected results ({len(expected) if expected else 0}) must match number of steps ({len(steps)})")

        custom_steps = []
        for i, step in enumerate(steps):
            custom_steps.append({
                'content': step,
                'expected': expected[i] if expected else ''
            })

    # Create the test case
    test_case = client.add_case(
        section_id=section_id,
        title=title,
        type_id=type_id,
        priority_id=priority_id,
        refs=refs,
        estimate=estimate,
        custom_preconds=preconditions,
        custom_steps_separated=custom_steps
    )

    return test_case


def main():
    """Main execution function."""
    args = parse_arguments()

    print("=" * 80)
    print("Creating TestRail Test Case")
    print("=" * 80)
    print(f"Project ID: {args.project}")
    if args.suite:
        print(f"Suite ID: {args.suite}")
    print(f"Title: {args.title}")
    print(f"Type: {args.type}")
    print(f"Priority: {args.priority}")
    if args.refs:
        print(f"References: {args.refs}")
    print("=" * 80)
    print()

    try:
        # Initialize TestRail client
        client = TestRailClient()

        # Get type and priority IDs
        type_id = get_type_id(client, args.type)
        priority_id = get_priority_id(client, args.priority)

        # Get section ID
        if args.section_id:
            section_id = args.section_id
            print(f"Using section ID: {section_id}")
        else:
            if not args.suite:
                print("Error: --suite is required when using --section-name")
                return 1

            print(f"Looking up section '{args.section_name}'...")
            section_id = get_section_id(client, args.project, args.suite, args.section_name)
            print(f"✓ Found section ID: {section_id}")

        print()

        # Create the test case
        print(f"Creating test case: '{args.title}'...")
        test_case = create_test_case(
            client=client,
            section_id=section_id,
            title=args.title,
            type_id=type_id,
            priority_id=priority_id,
            refs=args.refs,
            estimate=args.estimate,
            preconditions=args.preconditions,
            steps=args.steps,
            expected=args.expected
        )

        print()
        print("=" * 80)
        print("✓ Test Case Created Successfully!")
        print("=" * 80)
        print(f"Test Case ID: {test_case['id']}")
        print(f"Title: {test_case['title']}")
        print(f"Type: {args.type} (ID: {type_id})")
        print(f"Priority: {args.priority} (ID: {priority_id})")
        if args.refs:
            print(f"References: {args.refs}")
        print()
        print(f"TestRail URL: {client.base_url}/index.php?/cases/view/{test_case['id']}")
        print("=" * 80)

        return 0

    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ Error: {e}")
        print("=" * 80)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
