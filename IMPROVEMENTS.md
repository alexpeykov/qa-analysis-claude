# QA Analysis Tool - Recommended Improvements

## Current Behavior

The tool currently has two ways to get linked ticket information:

1. **Auto-discovered linked tickets** (from main ticket's `issuelinks` field):
   - Only fetches basic info: key, type, summary, status
   - Does NOT fetch comments or full description
   - Fast but limited context

2. **Explicitly provided linked tickets** (via `--linked` parameter):
   - Fetches full ticket data including all comments
   - Provides complete context for analysis
   - Requires manual specification

## Recommended Enhancement

### Option 1: Auto-fetch Full Data for All Linked Tickets (Automatic)

**Change:** Modify `src/jira_client.py` to automatically fetch full ticket data for all linked tickets discovered from the main ticket.

**Implementation:**
```python
def get_linked_tickets(self, ticket_key: str, fetch_full_data: bool = True) -> List[Dict[str, Any]]:
    """
    Fetch all linked tickets for a Jira ticket.

    Args:
        ticket_key: Jira ticket key
        fetch_full_data: If True, fetches complete ticket data including comments

    Returns:
        List of linked ticket information
    """
    ticket = self.get_ticket(ticket_key)
    issue_links = ticket.get('fields', {}).get('issuelinks', [])

    linked_tickets = []
    for link in issue_links:
        if 'outwardIssue' in link:
            linked_key = link['outwardIssue']['key']
            link_type = link['type']['outward']
        elif 'inwardIssue' in link:
            linked_key = link['inwardIssue']['key']
            link_type = link['type']['inward']
        else:
            continue

        if fetch_full_data:
            # Fetch complete ticket data including comments
            try:
                full_data = self.get_ticket_analysis_data(
                    f"{self.base_url}/browse/{linked_key}"
                )
                full_data['link_type'] = link_type
                linked_tickets.append(full_data)
            except Exception as e:
                # Fallback to basic info if full fetch fails
                linked_tickets.append({
                    'key': linked_key,
                    'type': link_type,
                    'error': str(e)
                })
        else:
            # Original behavior - basic info only
            if 'outwardIssue' in link:
                linked_tickets.append({
                    'key': linked_key,
                    'type': link_type,
                    'summary': link['outwardIssue']['fields']['summary'],
                    'status': link['outwardIssue']['fields']['status']['name']
                })
            elif 'inwardIssue' in link:
                linked_tickets.append({
                    'key': linked_key,
                    'type': link_type,
                    'summary': link['inwardIssue']['fields']['summary'],
                    'status': link['inwardIssue']['fields']['status']['name']
                })

    return linked_tickets
```

**Update in `src/analyzer.py`:**
```python
def format_data_for_analysis(self, data: Dict[str, Any]) -> str:
    # ... existing code ...

    # Add section for auto-discovered linked tickets with full data
    if data['main_ticket'] and data['main_ticket']['linked_tickets']:
        output.append("\n" + "=" * 80)
        output.append("AUTO-DISCOVERED LINKED TICKETS (FROM MAIN TICKET)")
        output.append("=" * 80)

        for ticket in data['main_ticket']['linked_tickets']:
            if 'error' in ticket:
                output.append(f"\n--- {ticket['key']} ({ticket.get('link_type', 'unknown')}) ---")
                output.append(f"Error: {ticket['error']}")
                continue

            output.append(f"\n--- {ticket['ticket_key']} ({ticket.get('link_type', 'unknown')}) ---")
            output.append(f"Summary: {ticket['summary']}")
            output.append(f"Status: {ticket['status']}")
            output.append(f"Priority: {ticket['priority']}")
            output.append(f"\nDescription:\n{ticket['description']}")

            if ticket['comments']:
                output.append(f"\n--- Comments ({len(ticket['comments'])}) ---")
                for i, comment in enumerate(ticket['comments'], 1):
                    author = comment.get('author', {}).get('displayName', 'Unknown')
                    created = comment.get('created', '')
                    body = comment.get('body', '')
                    output.append(f"\nComment #{i} by {author} on {created}:")
                    output.append(body)
```

**Pros:**
- Automatic - no need to manually specify linked tickets
- Complete context for better analysis
- Maintains backward compatibility

**Cons:**
- More API calls (one per linked ticket)
- Slower execution time
- May hit Jira API rate limits with many linked tickets

### Option 2: Add Flag to Enable Full Fetch (Opt-in)

Add a command-line flag `--fetch-linked-full` to enable full linked ticket fetching:

```python
parser.add_argument(
    '--fetch-linked-full',
    action='store_true',
    help='Fetch full data (including comments) for auto-discovered linked tickets'
)
```

**Pros:**
- User controls performance vs. completeness trade-off
- Backward compatible
- Explicit behavior

**Cons:**
- Requires user to know about the flag
- Extra configuration step

## Current Workaround

Until this enhancement is implemented, users should manually specify important linked tickets using the `--linked` parameter:

```bash
python3 analyze_ticket.py \
  --jira https://jira.paysera.net/browse/CORE-5599 \
  --linked https://jira.paysera.net/browse/CORE-5693 \
           https://jira.paysera.net/browse/CARDS-3136 \
           https://jira.paysera.net/browse/SUPPORT-95617 \
  --mr https://gitlab.paysera.net/paysera/app-evpbank/-/merge_requests/12353
```

This ensures that:
1. The main ticket's linked tickets section shows the relationship mapping
2. The "LINKED JIRA TICKETS" section contains full details with all comments
3. Claude receives complete context for deep analysis

## Confluence Comments

The tool already fetches Confluence page comments (see `src/confluence_client.py` and `src/analyzer.py` lines 211-215). This data is included in the analysis output under the "CONFLUENCE DOCUMENTATION" section.

## Impact on Analysis Quality

With full linked ticket data (comments included), Claude can:
- Explain cause-and-effect relationships between tickets
- Quote key decisions from team discussions
- Identify patterns and precedents mentioned in comments
- Understand the evolution of the issue through comment threads
- Extract business rules and technical decisions that informed the solution

This significantly improves the quality and depth of the QA analysis report.
