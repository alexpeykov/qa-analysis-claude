#!/bin/bash

# Quick database switcher for MySQL connections
# Usage: ./switch-db.sh [connection-id]

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

# Function to map shortcuts to connection IDs
map_connection() {
    case "$1" in
        1|el) echo "evpbank-local" ;;
        2|er) echo "evpbank-remote" ;;
        3|ml) echo "mokejimai-local" ;;
        4|mr) echo "mokejimai-remote" ;;
        evpbank-local|evpbank-remote|mokejimai-local|mokejimai-remote) echo "$1" ;;
        *) echo "" ;;
    esac
}

# Function to show current connection
show_current() {
    if [ -f "$ENV_FILE" ]; then
        CURRENT=$(grep "^MYSQL_CONNECTION_ID=" "$ENV_FILE" | cut -d'=' -f2)
        echo "Current connection: $CURRENT"
    else
        echo "Error: .env file not found at $ENV_FILE"
        exit 1
    fi
}

# Function to show menu
show_menu() {
    echo ""
    echo "Available database connections:"
    echo "  1 | el) evpbank-local     - EVPBank Local Docker (app@evpbank.dev.docker:3306/gateway)"
    echo "  2 | er) evpbank-remote    - EVPBank Remote (stanislav.zlatkov@evpbank.dev.lan:7450/gateway)"
    echo "  3 | ml) mokejimai-local   - Mokejimai Local Docker (app@mokejimai.dev.docker:3306/evp_lt)"
    echo "  4 | mr) mokejimai-remote  - Mokejimai Remote (stanislav.zlatkov@evp-lt.dev.lan:7550/evp_lt)"
    echo ""
}

# Function to update .env file
update_connection() {
    local NEW_CONNECTION=$1

    if [ -f "$ENV_FILE" ]; then
        # Use sed to update the MYSQL_CONNECTION_ID line
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/^MYSQL_CONNECTION_ID=.*/MYSQL_CONNECTION_ID=$NEW_CONNECTION/" "$ENV_FILE"
        else
            # Linux
            sed -i "s/^MYSQL_CONNECTION_ID=.*/MYSQL_CONNECTION_ID=$NEW_CONNECTION/" "$ENV_FILE"
        fi
        echo "✓ Switched to: $NEW_CONNECTION"
    else
        echo "Error: .env file not found at $ENV_FILE"
        exit 1
    fi
}

# Main logic
if [ -z "$1" ]; then
    # No argument provided, show menu
    show_current
    show_menu
    read -p "Enter your choice (1-4 or el/er/ml/mr): " CHOICE

    if [ -z "$CHOICE" ]; then
        echo "No choice made. Exiting."
        exit 0
    fi

    # Map choice to connection
    CONNECTION=$(map_connection "$CHOICE")

    if [ -z "$CONNECTION" ]; then
        echo "Invalid choice: $CHOICE"
        exit 1
    fi

    update_connection "$CONNECTION"
else
    # Argument provided
    CONNECTION=$(map_connection "$1")

    if [ -z "$CONNECTION" ]; then
        echo "Invalid connection ID: $1"
        echo ""
        show_menu
        exit 1
    fi

    update_connection "$CONNECTION"
fi

# Show the new connection
echo ""
show_current
