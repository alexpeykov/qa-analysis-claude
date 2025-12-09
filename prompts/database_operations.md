# Database Operations Prompts

This file contains useful prompts for working with databases in the QA Analysis project and searching between different database systems.

## MySQL Database Operations

### Basic Connection and Queries

#### Connect to Database
```
Connect to the MySQL database using the credentials from .env file
```

#### Show Databases
```
Show me all databases in MySQL
```

#### Show Tables
```
Show me all tables in the [database_name] database
```

#### Describe Table Structure
```
Show me the structure of the [table_name] table
```

#### Query Data
```
Query all data from table [table_name] in the database
```

```
Query [table_name] table and show only records where [column_name] equals [value]
```

### Advanced Queries

#### Search Across Tables
```
Search for the value [search_value] across all columns in table [table_name]
```

```
Search for records in [table_name] where [column_name] contains [search_term]
```

#### Join Queries
```
Join tables [table1] and [table2] on [join_condition] and show [columns]
```

#### Aggregate Queries
```
Show me the count of records in [table_name] grouped by [column_name]
```

```
Calculate the sum/average/min/max of [column_name] in table [table_name]
```

### Data Modification

#### Insert Data
```
Insert a new record into [table_name] with values [column1]='[value1]', [column2]='[value2]'
```

#### Update Data
```
Update records in [table_name] where [condition] and set [column_name] to [new_value]
```

#### Delete Data
```
Delete records from [table_name] where [condition]
```

### Database Management

#### Create Table
```
Create a new table [table_name] with columns [column_definitions]
```

#### Create Index
```
Create an index on [column_name] in table [table_name] for better query performance
```

#### Backup Database
```
Create a backup of the [database_name] database to file [backup_file.sql]
```

#### Restore Database
```
Restore the [database_name] database from backup file [backup_file.sql]
```

#### Show Table Indexes
```
Show me all indexes on table [table_name]
```

#### Analyze Query Performance
```
Analyze the performance of this query: [SQL_QUERY]
```

## Cross-Database Search Operations

### Search in Multiple Databases

#### Search Across All Databases
```
Search for the value [search_value] across all databases and tables in MySQL
```

#### Find Tables with Specific Column
```
Find all tables that have a column named [column_name] across all databases
```

#### Compare Data Between Databases
```
Compare the data in table [table_name] between database [db1] and database [db2]
```

#### Search by Pattern
```
Search for records matching pattern [pattern] in column [column_name] across all tables in database [database_name]
```

### Schema Comparison

#### Compare Table Structures
```
Compare the structure of table [table_name] between database [db1] and database [db2]
```

#### Find Schema Differences
```
Show me all schema differences between database [db1] and database [db2]
```

#### List Missing Tables
```
Show me which tables exist in [db1] but not in [db2]
```

### Data Migration Between Databases

#### Copy Table Between Databases
```
Copy the table [table_name] from database [source_db] to database [target_db]
```

#### Sync Data Between Databases
```
Synchronize data in table [table_name] from [source_db] to [target_db]
```

#### Export Data for Migration
```
Export data from [table_name] in [database_name] to CSV/JSON format for migration
```

## QA Analysis Project Specific Queries

### TestRail Data Queries

#### Find Test Cases
```
Show me all test cases in the qa_analysis database related to [feature_name]
```

#### Search Test Run Results
```
Search for test run results where status is [status] and project_id is [project_id]
```

#### Analyze Test Coverage
```
Show me the test coverage statistics for project [project_id]
```

### Jira Data Queries

#### Search Cached Jira Data
```
Search for Jira tickets cached in the database where [condition]
```

#### Find Related Tickets
```
Show me all tickets linked to [ticket_key] in the database
```

### GitLab Data Queries

#### Search Merge Requests
```
Search for merge requests in the database where state is [state] and author is [author]
```

#### Find Code Changes
```
Show me all merge requests that modified file [file_path]
```

## Database Debugging and Diagnostics

### Connection Issues

#### Test Connection
```
Test the MySQL database connection using the credentials from .env
```

#### Show Connection Status
```
Show me the current MySQL connection status and active connections
```

#### Check Database Size
```
Show me the size of database [database_name] and each table
```

### Performance Analysis

#### Show Slow Queries
```
Show me the slowest queries running on the database
```

#### Analyze Table Performance
```
Analyze the performance of table [table_name] and suggest optimizations
```

#### Check Index Usage
```
Show me which indexes are being used and which are not for table [table_name]
```

### Data Integrity

#### Find Duplicate Records
```
Find duplicate records in table [table_name] based on column [column_name]
```

#### Check Foreign Key Constraints
```
Show me all foreign key constraints for table [table_name]
```

#### Validate Data Consistency
```
Check data consistency between tables [table1] and [table2] using [relationship]
```

## Database Search Techniques

### Full-Text Search

#### Search Text Content
```
Perform a full-text search for [search_term] across all text columns in database [database_name]
```

#### Search with Wildcards
```
Search for records where [column_name] matches the pattern [pattern_with_wildcards]
```

### Regular Expression Search

#### Regex Pattern Search
```
Search for records in [table_name] where [column_name] matches regex pattern [regex_pattern]
```

#### Find Email Addresses
```
Find all records with email addresses in table [table_name]
```

#### Find URLs
```
Find all records containing URLs in column [column_name]
```

### Date-based Search

#### Search by Date Range
```
Find all records in [table_name] created between [start_date] and [end_date]
```

#### Recent Records
```
Show me records from [table_name] created in the last [N] days
```

#### Records by Month/Year
```
Show me all records from [table_name] created in [month] [year]
```

## Database Maintenance

### Optimization

#### Optimize Tables
```
Optimize all tables in database [database_name] for better performance
```

#### Rebuild Indexes
```
Rebuild all indexes for table [table_name]
```

#### Update Statistics
```
Update table statistics for query optimizer in database [database_name]
```

### Cleanup

#### Remove Old Data
```
Delete records from [table_name] older than [N] days
```

#### Archive Historical Data
```
Archive records from [table_name] older than [date] to archive table
```

#### Clean Up Test Data
```
Remove all test data from database [database_name]
```

## Advanced Database Operations

### Stored Procedures and Functions

#### List Stored Procedures
```
Show me all stored procedures in database [database_name]
```

#### Execute Stored Procedure
```
Execute stored procedure [procedure_name] with parameters [parameters]
```

#### Create Function
```
Create a database function [function_name] that [functionality]
```

### Triggers

#### List Triggers
```
Show me all triggers on table [table_name]
```

#### Create Trigger
```
Create a trigger on [table_name] that executes [action] when [event] occurs
```

### Views

#### Create View
```
Create a view [view_name] that shows [query_description]
```

#### List Views
```
Show me all views in database [database_name]
```

## Integration with External Systems

### TestRail Integration

#### Import TestRail Data
```
Import test cases from TestRail project [project_id] into the local database
```

#### Sync TestRail Results
```
Synchronize test run results from TestRail to the local database
```

### Jira Integration

#### Cache Jira Tickets
```
Cache Jira ticket [ticket_key] and all related information to the database
```

#### Update Cached Data
```
Update the cached Jira data for project [project_key] in the database
```

## Database Comparison and Validation

### Data Validation

#### Compare Record Counts
```
Compare the number of records in table [table_name] between [db1] and [db2]
```

#### Validate Data Integrity
```
Validate that all foreign key references in [table_name] are valid
```

#### Check for Orphaned Records
```
Find orphaned records in [table_name] that have no parent in [parent_table]
```

### Schema Validation

#### Validate Schema
```
Validate that the database schema matches the expected structure from migrations
```

#### Check Missing Indexes
```
Identify missing indexes that could improve query performance in [database_name]
```

## Reporting and Analytics

### Generate Reports

#### Test Results Summary
```
Generate a summary report of test results from the last [N] days
```

#### Database Growth Report
```
Show me the database growth trends over the last [N] months
```

#### Activity Report
```
Generate an activity report showing database operations in the last [N] days
```

## Example Complex Queries

### Multi-Database Analysis
```
Compare test case coverage between TestRail (project [id1]) and local database, showing missing test cases
```

### Cross-Reference Search
```
Find all Jira tickets in the database that have associated test cases but no test run results
```

### Historical Analysis
```
Show me the trend of test case creation and execution over the last 6 months
```

### Data Relationship Mapping
```
Show me all relationships between Jira tickets, test cases, and test runs for [feature_name]
```
