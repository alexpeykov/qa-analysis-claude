#!/usr/bin/env python3
"""
Wrapper script for QA Analysis that automatically saves output to ticket_analysis folder.

This script automatically:
1. Creates a filename based on the ticket ID and timestamp
2. Saves the output to the ticket_analysis/ folder
3. Shows the path to the generated file

Usage:
    python3 analyze_ticket.py --jira <JIRA_URL> [--mr <MR_URL>] [--confluence <CONF_URL>]
"""

import argparse
import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path


def extract_ticket_id(jira_url):
    """Extract ticket ID from Jira URL."""
    # Handle URLs like https://jira.paysera.net/browse/PROJ-123
    parts = jira_url.split('/')
    if 'browse' in parts:
        idx = parts.index('browse')
        if idx + 1 < len(parts):
            return parts[idx + 1].split('?')[0]
    return None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='QA Analysis Tool - Automatically saves to ticket_analysis folder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python3 analyze_ticket.py --jira https://jira.paysera.net/browse/PROJ-123

  # With merge request
  python3 analyze_ticket.py \\
    --jira https://jira.paysera.net/browse/PROJ-123 \\
    --mr https://gitlab.paysera.net/project/-/merge_requests/456

  # Full analysis
  python3 analyze_ticket.py \\
    --jira https://jira.paysera.net/browse/PROJ-123 \\
    --linked https://jira.paysera.net/browse/PROJ-124 \\
    --mr https://gitlab.paysera.net/project/-/merge_requests/456 \\
    --confluence https://intranet.paysera.net/pages/viewpage.action?pageId=789
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
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    args = parse_arguments()

    # Extract ticket ID for filename
    ticket_id = extract_ticket_id(args.jira)
    if not ticket_id:
        print(f"Warning: Could not extract ticket ID from {args.jira}", file=sys.stderr)
        ticket_id = "unknown"

    # Create output directory
    output_dir = Path(__file__).parent / "ticket_analysis"
    output_dir.mkdir(exist_ok=True)

    # Generate filename with timestamp - always .html for text format
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extension = "html" if args.format == "text" else "json"
    filename = f"{ticket_id}_{timestamp}.{extension}"
    output_path = output_dir / filename

    print("=" * 80)
    print(f"QA Analysis for ticket: {ticket_id}")
    print("=" * 80)
    print(f"Output will be saved to: {output_path}")
    print("=" * 80)
    print()

    # Build command for qa_analyze.py
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "qa_analyze.py"),
        "--jira", args.jira,
        "--format", args.format,
        "--output", str(output_path)
    ]

    if args.linked:
        cmd.extend(["--linked"] + args.linked)

    if args.mr:
        cmd.extend(["--mr"] + args.mr)

    if args.confluence:
        cmd.extend(["--confluence"] + args.confluence)

    # Execute the analysis
    try:
        result = subprocess.run(cmd, check=True)

        print()
        print("=" * 80)
        print("✅ Analysis Complete!")
        print("=" * 80)
        print(f"📄 File saved to: {output_path}")
        print(f"📊 File size: {output_path.stat().st_size} bytes")
        print()
        print("Next steps:")
        print(f"1. Open the file: open {output_path}")
        print("2. Copy the content")
        print("3. Paste into Claude for analysis")
        print("=" * 80)

        return 0

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: Analysis failed with exit code {e.returncode}", file=sys.stderr)
        return e.returncode
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
