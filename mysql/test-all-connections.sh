#!/bin/bash

# Test all database connections
# This script tests all four database configurations with known test queries

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SWITCH_SCRIPT="$SCRIPT_DIR/switch-db.sh"
# Use query.sh if exists, otherwise fallback to query-remote.sh
if [ -f "$SCRIPT_DIR/query.sh" ]; then
    QUERY_SCRIPT="$SCRIPT_DIR/query.sh"
else
    QUERY_SCRIPT="$SCRIPT_DIR/query-remote.sh"
fi

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "Testing All Database Connections"
echo "========================================"
echo ""

# Test counter
PASSED=0
FAILED=0

# Test function
test_query() {
    local DB_NAME=$1
    local DB_SHORT=$2
    local QUERY=$3
    local EXPECTED=$4

    echo -e "${BLUE}Testing: $DB_NAME${NC}"
    echo "Query: $QUERY"

    # Switch database
    "$SWITCH_SCRIPT" "$DB_SHORT" > /dev/null 2>&1

    # Run query
    RESULT=$("$QUERY_SCRIPT" "$QUERY" 2>&1)
    EXIT_CODE=$?

    # Check if query succeeded and contains expected value
    if [ $EXIT_CODE -eq 0 ] && echo "$RESULT" | grep -q "$EXPECTED"; then
        echo -e "${GREEN}✓ PASSED${NC}"
        echo "Found: $EXPECTED"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}"
        echo "Expected: $EXPECTED"
        echo "Result:"
        echo "$RESULT"
        ((FAILED++))
    fi
    echo ""
}

# Test 1: EVPBank Remote - Show tables
test_query \
    "EVPBank Remote" \
    "er" \
    "SHOW TABLES" \
    "client"

# Test 2: EVPBank Local - Show tables
test_query \
    "EVPBank Local" \
    "el" \
    "SHOW TABLES" \
    "client"

# Test 3: Mokejimai Remote - Show tables
test_query \
    "Mokejimai Remote" \
    "mr" \
    "SHOW TABLES" \
    "aros"

# Test 4: Mokejimai Local - Show tables
test_query \
    "Mokejimai Local" \
    "ml" \
    "SHOW TABLES" \
    "m_currency"

# Summary
echo "========================================"
echo "Test Summary"
echo "========================================"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed! ✗${NC}"
    exit 1
fi
