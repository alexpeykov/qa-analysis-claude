#!/usr/bin/env python3
"""
Script to create test runs in TestRail.

This script creates a test run and includes test cases from specified folders/sections.
"""

import argparse
import sys
from typing import List
from src.testrail_client import TestRailClient


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Create a test run in TestRail with test cases from specified folders',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create test run with cases from one folder
  python3 create_test_run.py \\
    --project 2 \\
    --suite 14 \\
    --name "CORE-5567 - Test Run" \\
    --refs "CORE-5567" \\
    --description "Testing CORE-5567 functionality" \\
    --folders "5567 - Add persisted events for TransferStatusForReservationStatementListener"

  # Create test run with cases from multiple folders
  python3 create_test_run.py \\
    --project 2 \\
    --suite 14 \\
    --name "Sprint 42 Test Run" \\
    --refs "CORE-5567,CORE-5568" \\
    --description "Testing all Sprint 42 features" \\
    --folders "5567 - Feature A" "5568 - Feature B" "5569 - Feature C"
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
        required=True,
        help='TestRail suite ID'
    )

    parser.add_argument(
        '--name',
        required=True,
        help='Test run name'
    )

    # Optional arguments
    parser.add_argument(
        '--refs',
        help='References (e.g., Jira ticket IDs like "CORE-5567" or "CORE-5567,CORE-5568")'
    )

    parser.add_argument(
        '--description',
        help='Test run description'
    )

    parser.add_argument(
        '--folders',
        nargs='+',
        required=True,
        help='Folder/section names to include test cases from (space-separated)'
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()

    print("=" * 80)
    print("Creating TestRail Test Run")
    print("=" * 80)
    print(f"Project ID: {args.project}")
    print(f"Suite ID: {args.suite}")
    print(f"Name: {args.name}")
    if args.refs:
        print(f"References: {args.refs}")
    if args.description:
        print(f"Description: {args.description}")
    print(f"Folders: {', '.join(args.folders)}")
    print("=" * 80)
    print()

    try:
        # Initialize TestRail client
        client = TestRailClient()

        # Get test case IDs from specified folders
        print("Collecting test cases from folders...")
        print()
        case_ids = client.get_cases_from_sections(
            project_id=args.project,
            suite_id=args.suite,
            section_names=args.folders
        )

        if not case_ids:
            print()
            print("=" * 80)
            print("❌ Error: No test cases found in the specified folders")
            print("=" * 80)
            print("Please check:")
            print("1. Folder names are correct (case-sensitive)")
            print("2. Folders contain test cases")
            print("3. You have access to view the test cases")
            return 1

        print()
        print(f"✓ Total test cases collected: {len(case_ids)}")
        print()

        # Create the test run
        print(f"Creating test run: '{args.name}'...")
        test_run = client.add_run(
            project_id=args.project,
            name=args.name,
            suite_id=args.suite,
            description=args.description,
            case_ids=case_ids,
            include_all=False,
            refs=args.refs
        )

        print()
        print("=" * 80)
        print("✓ Test Run Created Successfully!")
        print("=" * 80)
        print(f"Test Run ID: {test_run['id']}")
        print(f"Name: {test_run['name']}")
        print(f"Test Cases: {len(case_ids)}")
        if args.refs:
            print(f"References: {args.refs}")
        if args.description:
            print(f"Description: {args.description}")
        print()
        print(f"TestRail URL: {client.base_url}/index.php?/runs/view/{test_run['id']}")
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
