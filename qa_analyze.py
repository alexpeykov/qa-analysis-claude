#!/usr/bin/env python3
"""
QA Analysis Tool - Main execution script

This script fetches data from Jira, GitLab, and Confluence, then generates
a comprehensive prompt for Claude to analyze and generate test cases.

Usage:
    python qa_analyze.py --jira <url> [--linked <url1> <url2>] [--mr <url1> <url2>] [--confluence <url1> <url2>]
"""

import argparse
import sys
import json
from typing import List
from src.config import Config
from src.analyzer import QAAnalyzer


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='QA Analysis Tool - Analyze Jira tickets with GitLab MRs and Confluence docs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with just a Jira ticket
  python qa_analyze.py --jira https://jira.paysera.net/browse/PROJ-123

  # Full analysis with all sources
  python qa_analyze.py \\
    --jira https://jira.paysera.net/browse/PROJ-123 \\
    --linked https://jira.paysera.net/browse/PROJ-124 \\
    --mr https://gitlab.paysera.net/project/-/merge_requests/456 \\
    --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789

  # Multiple merge requests and docs
  python qa_analyze.py \\
    --jira https://jira.paysera.net/browse/PROJ-123 \\
    --mr https://gitlab.paysera.net/project/-/merge_requests/456 \\
         https://gitlab.paysera.net/project/-/merge_requests/457 \\
    --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789 \\
                 https://intranet.paysera.net/pages/viewpage.action?pageId=790
        """
    )

    parser.add_argument(
        '--jira',
        required=True,
        help='URL to the main Jira ticket'
    )

    parser.add_argument(
        '--linked',
        nargs='+',
        help='URLs to linked Jira tickets (space-separated)'
    )

    parser.add_argument(
        '--mr',
        nargs='+',
        help='URLs to GitLab merge requests (space-separated)'
    )

    parser.add_argument(
        '--confluence',
        nargs='+',
        help='URLs to Confluence documentation pages (space-separated)'
    )

    parser.add_argument(
        '--output',
        '-o',
        help='Output file path (default: prints to stdout)'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format: text for Claude prompt, json for raw data (default: text)'
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()

    # Validate configuration
    is_valid, missing = Config.validate()
    if not is_valid:
        print("ERROR: Missing required configuration values:", file=sys.stderr)
        for field in missing:
            print(f"  - {field}", file=sys.stderr)
        print("\nPlease ensure your .env file is properly configured.", file=sys.stderr)
        print("See README.md for setup instructions.", file=sys.stderr)
        sys.exit(1)

    print("Starting QA Analysis...\n")
    print(f"Main Ticket: {args.jira}")

    if args.linked:
        print(f"Linked Tickets: {len(args.linked)}")
    if args.mr:
        print(f"Merge Requests: {len(args.mr)}")
    if args.confluence:
        print(f"Confluence Pages: {len(args.confluence)}")

    print("\n" + "=" * 80)

    # Initialize analyzer
    analyzer = QAAnalyzer()

    # Fetch all data
    try:
        data = analyzer.fetch_all_data(
            jira_ticket_url=args.jira,
            linked_ticket_urls=args.linked,
            merge_request_urls=args.mr,
            confluence_urls=args.confluence
        )
    except Exception as e:
        print(f"\nERROR: Failed to fetch data: {e}", file=sys.stderr)
        sys.exit(1)

    print("=" * 80)
    print("\nData fetching completed!\n")

    # Format output based on requested format
    if args.format == 'json':
        output = json.dumps(data, indent=2, default=str)
    else:
        # Generate formatted text for Claude analysis
        formatted_data = analyzer.format_data_for_analysis(data)

        # Read the Claude prompt template
        try:
            with open('.claude/qa-analysis.md', 'r') as f:
                prompt_template = f.read()
        except FileNotFoundError:
            print("ERROR: Claude prompt template not found at .claude/qa-analysis.md", file=sys.stderr)
            sys.exit(1)

        # Replace placeholder with actual data
        output = prompt_template.replace('{{DATA_CONTENT}}', formatted_data)

    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Analysis prompt written to: {args.output}")
        print("\nNext steps:")
        print(f"1. Review the generated prompt in {args.output}")
        print("2. Copy the content and provide it to Claude")
        print("3. Claude will generate comprehensive QA analysis and test cases")
    else:
        print("=" * 80)
        print("CLAUDE ANALYSIS PROMPT")
        print("=" * 80)
        print("\nCopy the text below and provide it to Claude:\n")
        print(output)

    print("\n" + "=" * 80)
    print("QA Analysis preparation complete!")
    print("=" * 80)


if __name__ == '__main__':
    main()
