#!/bin/bash

# Helper script to query MySQL databases
# Usage: ./query.sh "SELECT * FROM table WHERE condition"

# Load environment variables
set -a
source "$(dirname "$0")/../.env"
set +a

# Check if query is provided
if [ -z "$1" ]; then
    echo "Usage: $0 \"SQL_QUERY\""
    echo "Examples:"
    echo "  $0 \"SHOW TABLES\""
    echo "  $0 \"SELECT * FROM table_name WHERE id = 123\""
    echo "  $0 \"SELECT * FROM table_name WHERE id = 123\\G\""
    echo ""
    echo "Current database: $MYSQL_CONNECTION_ID"
    echo "Use ./switch-db.sh to change databases"
    exit 1
fi

QUERY="$1"

# Determine which database connection to use based on MYSQL_CONNECTION_ID
case "$MYSQL_CONNECTION_ID" in
    evpbank-remote)
        HOST="$EVPBANK_REMOTE_HOST"
        PORT="$EVPBANK_REMOTE_PORT"
        DATABASE="$EVPBANK_REMOTE_DATABASE"
        USER="$EVPBANK_REMOTE_USER"
        PASSWORD="$EVPBANK_REMOTE_PASSWORD"
        ;;
    evpbank-local)
        HOST="$EVPBANK_LOCAL_HOST"
        PORT="$EVPBANK_LOCAL_PORT"
        DATABASE="$EVPBANK_LOCAL_DATABASE"
        USER="$EVPBANK_LOCAL_USER"
        PASSWORD="$EVPBANK_LOCAL_PASSWORD"
        ;;
    mokejimai-remote)
        HOST="$MOKEJIMAI_REMOTE_HOST"
        PORT="$MOKEJIMAI_REMOTE_PORT"
        DATABASE="$MOKEJIMAI_REMOTE_DATABASE"
        USER="$MOKEJIMAI_REMOTE_USER"
        PASSWORD="$MOKEJIMAI_REMOTE_PASSWORD"
        ;;
    mokejimai-local)
        HOST="$MOKEJIMAI_LOCAL_HOST"
        PORT="$MOKEJIMAI_LOCAL_PORT"
        DATABASE="$MOKEJIMAI_LOCAL_DATABASE"
        USER="$MOKEJIMAI_LOCAL_USER"
        PASSWORD="$MOKEJIMAI_LOCAL_PASSWORD"
        ;;
    default|*)
        HOST="$MYSQL_HOST"
        PORT="$MYSQL_PORT"
        DATABASE="$MYSQL_DATABASE"
        USER="$MYSQL_USER"
        PASSWORD="$MYSQL_PASSWORD"
        ;;
esac

echo "Connecting to: $MYSQL_CONNECTION_ID ($USER@$HOST:$PORT/$DATABASE)"
echo "Running query: $QUERY"
echo ""

# Execute query using Docker mariadb container which has network access
docker exec mariadb mysql -h "$HOST" -P "$PORT" -u "$USER" -p"$PASSWORD" "$DATABASE" -e "$QUERY"
