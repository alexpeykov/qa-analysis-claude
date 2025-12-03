#!/usr/bin/env python3
"""
Script to create test cases in TestRail from text input with automatic expected result generation.

This script parses test case descriptions in the format:
    Title
    1.Step one
    2.Step two
    3.Step three
    Final expected result

It generates appropriate expected results for each step and creates the test case in TestRail.
"""

import argparse
import sys
import re
from typing import List, Dict, Tuple
from src.testrail_client import TestRailClient


def parse_test_case_text(text: str) -> Tuple[str, List[str], str]:
    """
    Parse test case text into title, steps, and final expected result.

    Args:
        text: Multi-line text with title, numbered steps, and expected result

    Returns:
        Tuple of (title, steps_list, final_expected_result)

    Example:
        Input:
            Load DB fixtures from test plan
            1.Switch to local DB
            2.Load the fixtures from the test plan
            3.Examine the output
            The fixtures are supposed to be imported without any errors.

        Output:
            ("Load DB fixtures from test plan",
             ["Switch to local DB", "Load the fixtures from the test plan", "Examine the output"],
             "The fixtures are supposed to be imported without any errors.")
    """
    lines = text.strip().split('\n')

    if not lines:
        raise ValueError("Empty test case text")

    # First line is the title
    title = lines[0].strip()

    # Find numbered steps (lines starting with number followed by dot)
    steps = []
    step_pattern = re.compile(r'^\s*(\d+)\.\s*(.+)$')
    final_result_start = len(lines)

    for i, line in enumerate(lines[1:], start=1):
        match = step_pattern.match(line)
        if match:
            step_text = match.group(2).strip()
            steps.append(step_text)
        elif line.strip() and steps:  # Non-empty line after steps started
            final_result_start = i
            break

    # Everything after the steps is the final expected result
    final_expected = '\n'.join(lines[final_result_start:]).strip()

    if not steps:
        raise ValueError(f"No numbered steps found in test case text. Make sure steps start with '1.', '2.', etc.")

    if not final_expected:
        raise ValueError("No final expected result found")

    return title, steps, final_expected


def generate_expected_results(steps: List[str], final_expected: str) -> List[str]:
    """
    Generate appropriate expected results for each step based on the step action.

    Args:
        steps: List of test step descriptions
        final_expected: The final expected result for the overall test

    Returns:
        List of expected results matching the number of steps
    """
    expected_results = []

    for i, step in enumerate(steps):
        step_lower = step.lower()
        is_last_step = (i == len(steps) - 1)

        # Generate expected result based on common action verbs
        if 'switch' in step_lower or 'navigate' in step_lower or 'go to' in step_lower or 'open' in step_lower:
            expected = f"Successfully switched/navigated to the specified location"
        elif 'enter' in step_lower or 'input' in step_lower or 'type' in step_lower:
            expected = f"Data is entered successfully"
        elif 'click' in step_lower or 'press' in step_lower or 'select' in step_lower:
            expected = f"Action is executed successfully"
        elif 'load' in step_lower or 'import' in step_lower or 'execute' in step_lower or 'run' in step_lower:
            expected = f"Operation completes without errors"
        elif 'verify' in step_lower or 'check' in step_lower or 'examine' in step_lower or 'validate' in step_lower:
            # For examination/verification steps, use the final expected result
            if is_last_step and final_expected:
                expected = final_expected
            else:
                expected = f"Verification is successful and data is correct"
        elif 'delete' in step_lower or 'remove' in step_lower:
            expected = f"Item is deleted/removed successfully"
        elif 'create' in step_lower or 'add' in step_lower:
            expected = f"Item is created/added successfully"
        elif 'update' in step_lower or 'edit' in step_lower or 'modify' in step_lower:
            expected = f"Item is updated/modified successfully"
        elif 'save' in step_lower:
            expected = f"Changes are saved successfully"
        elif 'search' in step_lower or 'find' in step_lower:
            expected = f"Search results are displayed correctly"
        elif 'login' in step_lower or 'log in' in step_lower:
            expected = f"User is logged in successfully"
        elif 'logout' in step_lower or 'log out' in step_lower:
            expected = f"User is logged out successfully"
        else:
            # Generic expected result
            if is_last_step and final_expected:
                expected = final_expected
            else:
                expected = f"Step completes successfully"

        expected_results.append(expected)

    return expected_results


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


def create_test_case_from_text(
    client: TestRailClient,
    section_id: int,
    test_case_text: str,
    type_id: int,
    priority_id: int,
    refs: str = None
) -> Dict:
    """
    Create a test case from text input.

    Args:
        client: TestRail client
        section_id: TestRail section ID
        test_case_text: Multi-line text with title, steps, and expected result
        type_id: Test case type ID
        priority_id: Priority ID
        refs: Optional references (e.g., Jira ticket)

    Returns:
        Created test case dictionary
    """
    # Parse the text
    title, steps, final_expected = parse_test_case_text(test_case_text)

    # Generate expected results for each step
    expected_results = generate_expected_results(steps, final_expected)

    # Build custom steps
    custom_steps = []
    for step, expected in zip(steps, expected_results):
        custom_steps.append({
            'content': step,
            'expected': expected
        })

    # Create the test case
    test_case = client.add_case(
        section_id=section_id,
        title=title,
        type_id=type_id,
        priority_id=priority_id,
        refs=refs,
        custom_steps_separated=custom_steps
    )

    return test_case


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Create test cases in TestRail from text input',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python3 create_test_case_from_text.py \\
    --project 2 \\
    --suite 14 \\
    --section-id 90046 \\
    --type "Functional" \\
    --priority "High" \\
    --refs "CORE-5567" \\
    --input "Load DB fixtures from test plan
1.Switch to local DB
2.Load the fixtures from the test plan
3.Examine the output
The fixtures are supposed to be imported without any errors. The info is supposed to be present in the DB tables."
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

    # Section identification
    section_group = parser.add_mutually_exclusive_group(required=True)
    section_group.add_argument(
        '--section-id',
        type=int,
        help='TestRail section ID'
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
        help='Test case type (default: Functional)'
    )

    parser.add_argument(
        '--priority',
        default='Medium',
        help='Test case priority (default: Medium)'
    )

    parser.add_argument(
        '--refs',
        help='References (e.g., Jira ticket IDs like "CORE-5567")'
    )

    # Input
    parser.add_argument(
        '--input',
        required=True,
        help='Test case text (title, numbered steps, and expected result)'
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()

    try:
        # Initialize TestRail client
        client = TestRailClient()

        # Get type and priority IDs
        type_id = get_type_id(client, args.type)
        priority_id = get_priority_id(client, args.priority)

        # Get section ID
        if args.section_id:
            section_id = args.section_id
        else:
            if not args.suite:
                print("Error: --suite is required when using --section-name")
                return 1
            section_id = get_section_id(client, args.project, args.suite, args.section_name)

        # Parse the test case text to get title for display
        title, steps, _ = parse_test_case_text(args.input)

        print("=" * 80)
        print("Creating TestRail Test Case from Text")
        print("=" * 80)
        print(f"Title: {title}")
        print(f"Steps: {len(steps)}")
        print(f"Type: {args.type} (ID: {type_id})")
        print(f"Priority: {args.priority} (ID: {priority_id})")
        if args.refs:
            print(f"References: {args.refs}")
        print("=" * 80)
        print()

        # Create the test case
        print(f"Creating test case: '{title}'...")
        print(f"Generating expected results for {len(steps)} steps...")

        test_case = create_test_case_from_text(
            client=client,
            section_id=section_id,
            test_case_text=args.input,
            type_id=type_id,
            priority_id=priority_id,
            refs=args.refs
        )

        print()
        print("=" * 80)
        print("✓ Test Case Created Successfully!")
        print("=" * 80)
        print(f"Test Case ID: {test_case['id']}")
        print(f"Title: {test_case['title']}")
        print(f"Steps: {len(steps)}")
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
