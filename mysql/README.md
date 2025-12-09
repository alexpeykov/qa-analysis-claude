# MySQL Database Query Tools

This directory contains tools for querying MySQL databases configured in the project.

## Quick Start - Using the Query Script (Recommended)

The easiest way to query databases is using the helper script:

```bash
./mysql/query-remote.sh "SELECT * FROM table_name WHERE condition"
```

The script automatically uses the database connection specified by `MYSQL_CONNECTION_ID` in the `.env` file.

### Examples

```bash
# Query EVPBank remote database (current default)
./mysql/query-remote.sh "SELECT * FROM client WHERE covenantee_id = 186662"

# Query with vertical formatting for better readability
./mysql/query-remote.sh "SELECT * FROM client WHERE covenantee_id = 186662\G"

# Count records
./mysql/query-remote.sh "SELECT COUNT(*) FROM client"

# Show table structure
./mysql/query-remote.sh "DESCRIBE client"

# List all tables
./mysql/query-remote.sh "SHOW TABLES"
```

## MySQL MCP Wrapper (Alternative Method)

This is a wrapper for the MySQL MCP server that supports multiple database connections.

### Configuration

The MySQL MCP wrapper can be configured in two ways:

### 1. Environment Variables (Recommended)

The wrapper automatically reads database configurations from the `.env` file in the project root. No additional configuration needed!

Available database connections:
- **Default MySQL**: `MYSQL_*` environment variables
- **EVPBank Local**: `EVPBANK_LOCAL_*` environment variables
- **EVPBank Remote**: `EVPBANK_REMOTE_*` environment variables
- **Mokejimai Local**: `MOKEJIMAI_LOCAL_*` environment variables
- **Mokejimai Remote**: `MOKEJIMAI_REMOTE_*` environment variables

Required environment variables for each connection:
- `*_HOST` - Database host
- `*_PORT` - Database port (usually 3306)
- `*_DATABASE` - Database name
- `*_USER` - Database username
- `*_PASSWORD` - Database password

Example in `.env`:
```env
# EVPBank Local
EVPBANK_LOCAL_HOST=localhost
EVPBANK_LOCAL_PORT=3306
EVPBANK_LOCAL_DATABASE=evpbank
EVPBANK_LOCAL_USER=root
EVPBANK_LOCAL_PASSWORD=password

# EVPBank Remote
EVPBANK_REMOTE_HOST=remote.server.com
EVPBANK_REMOTE_PORT=3306
EVPBANK_REMOTE_DATABASE=evpbank
EVPBANK_REMOTE_USER=remote_user
EVPBANK_REMOTE_PASSWORD=remote_password
```

### 2. config.json (Optional)

If you prefer, you can also create a `config.json` file in this directory. The wrapper will use `config.json` if it exists, otherwise it will fall back to environment variables.

To generate `config.json` from your current environment variables:
```bash
node generate-config.js
```

## Usage

The wrapper will:
1. Look for `config.json` first
2. If not found, load configurations from `.env` file
3. Use the first available connection
4. Log which connection is active

Currently, the wrapper uses the first configured connection. All connections with complete credentials will be available.

## Building

```bash
npm run build
```

## How It Works

1. The wrapper loads database configurations from `.env` or `config.json`
2. It selects the first available connection
3. It passes the connection details to the upstream MySQL MCP server via environment variables
4. The upstream server provides READ-ONLY access to the database

## SSH Tunnels for Remote Connections

Both remote database connections (EVPBank Remote and Mokejimai Remote) require SSH tunnels to be established before connecting.

**SSH Tunnel Configuration:**
- SSH Host: Your assigned SSH gateway server
- SSH Port: `22`
- SSH Username: Check with your team
- SSH Password: Check with your team

**Setting up SSH tunnels:**

For EVPBank Remote:
```bash
ssh -L 7450:evpbank.dev.lan:7450 username@your-ssh-gateway
```

For Mokejimai Remote:
```bash
ssh -L 7550:evp-lt.dev.lan:7550 username@your-ssh-gateway
```

Keep these SSH sessions running in separate terminal windows while using the remote database connections.

## Configured Databases

1. **Default MySQL** - General purpose MySQL connection
2. **EVPBank Local** - Local Docker database (`evpbank.dev.docker:3306`)
3. **EVPBank Remote** - Remote database via SSH tunnel (`evpbank.dev.lan:7450`)
4. **Mokejimai Local** - Local Docker database (`mokejimai.dev.docker:3306`)
5. **Mokejimai Remote** - Remote database via SSH tunnel (`evp-lt.dev.lan:7550`)

## Switching Database Connections

### Quick Switch (Recommended)

Use the switcher script for fast database switching:

```bash
# Switch using shortcuts
./mysql/switch-db.sh er   # evpbank-remote
./mysql/switch-db.sh el   # evpbank-local
./mysql/switch-db.sh mr   # mokejimai-remote
./mysql/switch-db.sh ml   # mokejimai-local

# Or use numbers
./mysql/switch-db.sh 1    # evpbank-local
./mysql/switch-db.sh 2    # evpbank-remote
./mysql/switch-db.sh 3    # mokejimai-local
./mysql/switch-db.sh 4    # mokejimai-remote

# Or use full connection IDs
./mysql/switch-db.sh evpbank-remote

# Interactive menu (no arguments)
./mysql/switch-db.sh
```

### Manual Method

Edit the `MYSQL_CONNECTION_ID` variable in the `.env` file:

```bash
# Use EVPBank remote database (default)
MYSQL_CONNECTION_ID=evpbank-remote

# Use EVPBank local database
MYSQL_CONNECTION_ID=evpbank-local

# Use Mokejimai remote database
MYSQL_CONNECTION_ID=mokejimai-remote

# Use Mokejimai local database
MYSQL_CONNECTION_ID=mokejimai-local
```

## How the Query Script Works

The [query-remote.sh](query-remote.sh) script:

1. Loads environment variables from the `.env` file
2. Selects the database connection based on `MYSQL_CONNECTION_ID`
3. Executes the query using the `mariadb` Docker container which has network access to remote databases

This approach works reliably because:
- The Docker containers run on the Ubuntu remote host
- The remote host has direct network access to `evpbank.dev.lan` and `evp-lt.dev.lan`
- No SSH tunnel is needed when running from Docker containers on the remote host

## Previous Query Results

### EVPBank - Client with covenantee_id 186662 (2025-12-09)

**Database**: evpbank-remote (gateway)
**Table**: client
**Query**: `SELECT * FROM client WHERE covenantee_id = 186662`

**Result**: Found client ID **42**

| Field | Value |
|-------|-------|
| id | 42 |
| code | 36807140260 |
| client_type | natural |
| covenantee_id | 186662 |
| country_code | lt |
| level | fully_identified |
| onboarding_date | 2019-09-25 16:03:07 |

### Mokejimai - ARO record with id 3108 (2025-12-09)

**Database**: mokejimai-remote (evp_lt)
**Table**: aros
**Query**: `SELECT * FROM aros WHERE id = 3108`

**Result**: Found ARO record

| Field | Value |
|-------|-------|
| id | 3108 |
| parent_id | 3066 |
| model | UserLogin |
| foreign_key | 115345 |
| alias | NULL |
| lft | 1370 |
| rght | 1371 |

## Troubleshooting

### MCP MySQL Tools Not Working

The MCP MySQL tools (`mcp__mysql__*`) may fail with "Connection lost" errors when accessing remote databases. This is because:

1. The MCP server runs on the local macOS host
2. Remote databases require SSH tunnels
3. Connection timeouts or network issues can occur
4. The upstream MySQL MCP server submodule may not be initialized

**Solution**: Use the [query-remote.sh](query-remote.sh) script instead, which runs queries from within the Docker environment where network access is reliable.

## Testing All Connections

Run the comprehensive test script to verify all database connections:

```bash
./mysql/test-all-connections.sh
```

This will test all four databases by checking if they can connect and show tables. Each test verifies:
- Connection is established successfully
- Database tables are visible
- No connection errors occur

## Tips

1. **Use `\G` for vertical output**: Add `\G` at the end of your query for better readability with many columns
2. **Export results to file**: Redirect output with `> results.txt`
3. **Check table structure first**: Use `DESCRIBE table_name` or `SHOW TABLES`
4. **Always test queries with LIMIT**: Start with `LIMIT 5` on large tables
5. **Quick switch and query**: Chain commands with `&&`
   ```bash
   ./mysql/switch-db.sh er && ./mysql/query-remote.sh "SELECT * FROM client LIMIT 5"
   ```

## Notes

- Only connections with ALL required fields (host, port, database, username, password) will be loaded
- The wrapper provides READ-ONLY access to databases for safety
- Remote connections require active SSH tunnels (see SSH Tunnels section above)
- If credentials are not filled in, those connections will be skipped
