# MySQL Quick Reference

## Quick Query Command

```bash
./mysql/query-remote.sh "YOUR_SQL_QUERY"
```

## Switch Database Connections

### Quick Switch (Use This!)

```bash
./mysql/switch-db.sh er   # evpbank-remote
./mysql/switch-db.sh el   # evpbank-local
./mysql/switch-db.sh mr   # mokejimai-remote
./mysql/switch-db.sh ml   # mokejimai-local
```

### Manual Edit

Edit `MYSQL_CONNECTION_ID` in [.env](../.env):

```bash
# EVPBank Remote (gateway database)
MYSQL_CONNECTION_ID=evpbank-remote

# Mokejimai Remote (evp_lt database)
MYSQL_CONNECTION_ID=mokejimai-remote

# EVPBank Local (Docker)
MYSQL_CONNECTION_ID=evpbank-local

# Mokejimai Local (Docker)
MYSQL_CONNECTION_ID=mokejimai-local
```

## Database Information

| Connection ID | Host | Port | Database | Tables |
|--------------|------|------|----------|---------|
| evpbank-remote | evpbank.dev.lan | 7450 | gateway | client, covenantee, etc. |
| mokejimai-remote | evp-lt.dev.lan | 7550 | evp_lt | aros, user_logins, etc. |
| evpbank-local | evpbank.dev.docker | 3306 | gateway | Same as remote |
| mokejimai-local | mokejimai.dev.docker | 3306 | evp_lt | Same as remote |

## Common Queries

### EVPBank Database (gateway)

```bash
# Find client by covenantee_id
./mysql/query-remote.sh "SELECT * FROM client WHERE covenantee_id = 186662\G"

# List all tables
./mysql/query-remote.sh "SHOW TABLES"

# Check table structure
./mysql/query-remote.sh "DESCRIBE client"
```

### Mokejimai Database (evp_lt)

```bash
# Find ARO record by id
./mysql/query-remote.sh "SELECT * FROM aros WHERE id = 3108\G"

# Find user login
./mysql/query-remote.sh "SELECT * FROM user_logins WHERE id = 115345\G"

# List all tables
./mysql/query-remote.sh "SHOW TABLES"
```

## Connection Test Results

All databases verified with `SHOW TABLES` command:
- ✅ **EVPBank Remote** - Tables visible (client, covenantee, etc.)
- ✅ **EVPBank Local** - Tables visible (client, covenantee, etc.)
- ✅ **Mokejimai Remote** - Tables visible (aros, user_logins, etc.)
- ✅ **Mokejimai Local** - Tables visible (m_currency, aros, etc.)

## Quick Workflow Examples

```bash
# Switch and query in one line
./mysql/switch-db.sh er && ./mysql/query-remote.sh "SELECT COUNT(*) FROM client"

# Test all connections
./mysql/test-all-connections.sh

# Interactive switch with menu
./mysql/switch-db.sh
```

## Tips

1. **Use `\G` for vertical output** - Better for wide tables
2. **Always test with LIMIT first** - Avoid huge result sets
3. **Check table structure** - Use `DESCRIBE table_name` before querying
4. **Export results** - Redirect with `> output.txt`
5. **Quick shortcuts** - `er`, `el`, `mr`, `ml` are faster to type

## Full Documentation

See [README.md](README.md) for complete documentation.
