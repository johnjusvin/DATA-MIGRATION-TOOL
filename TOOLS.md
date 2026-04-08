# 🛠️ Tools Reference — Data Migration System

> Complete documentation for every tool used in the CrewAI migration pipeline.
> Each tool is a Python function decorated with `@tool()` that agents can invoke during execution.

---

## 📑 Table of Contents

| # | Tool Name | File | Used By Agent |
|---|-----------|------|---------------|
| 1 | [Test Database Connections](#1--test-database-connections) | `db_connector.py` | Main Entry Point |
| 2 | [Read Legacy Database Schema](#2--read-legacy-database-schema) | `schema_reader.py` | Agent 1 — Schema Analyst |
| 3 | [Get Table Row Counts](#3--get-table-row-counts) | `schema_reader.py` | Agent 1 — Schema Analyst |
| 4 | [Extract Table Batch](#4--extract-table-batch) | `data_extractor.py` | Agent 3 — ETL Specialist |
| 5 | [Transform Data Batch](#5--transform-data-batch) | `data_transformer.py` | Agent 3 — ETL Specialist |
| 6 | [Load Batch to Modern Database](#6--load-batch-to-modern-database) | `data_loader.py` | Agent 3 — ETL Specialist |
| 7 | [Compare Row Counts](#7--compare-row-counts) | `validator_tools.py` | Agent 4 — Data Validator |
| 8 | [Check Null Values](#8--check-null-values) | `validator_tools.py` | Agent 4 — Data Validator |
| 9 | [Check Foreign Key Integrity](#9--check-foreign-key-integrity) | `validator_tools.py` | Agent 4 — Data Validator |
| 10 | [Compare Sample Records](#10--compare-sample-records) | `validator_tools.py` | Agent 4 — Data Validator |

---

## Tool-to-Agent Mapping

```
Agent 1 (Schema Analyst)     → read_legacy_schema, get_table_row_counts
Agent 2 (Schema Mapper)      → read_legacy_schema
Agent 3 (ETL Specialist)     → extract_table_batch, transform_batch, load_batch_to_modern_db
Agent 4 (Data Validator)     → compare_row_counts, check_null_values, check_foreign_key_integrity, compare_sample_records
Agent 5 (Migration Reporter) → (no tools — compiles text reports from other agents' outputs)
```

---

## 1 — Test Database Connections

| Property | Value |
|----------|-------|
| **Tool Name** | `Test Database Connections` |
| **File** | `src/tools/db_connector.py` |
| **Function** | `test_connections()` |
| **Used By** | `main.py` (pre-flight check before migration starts) |
| **Parameters** | None |
| **Returns** | `str` — connection status for both databases |

### Purpose
Tests connectivity to **both** the legacy (source) and modern (target) databases before the migration begins. This is the first check that runs — if either connection fails, the entire migration is aborted.

### How It Works
1. Reads database credentials from environment variables (`.env`)
2. Creates a SQLAlchemy engine for the legacy database
3. Executes `SELECT 1` to verify the connection is alive
4. Repeats for the modern database
5. Returns a status string with ✅ or ❌ for each

### Output Example
```
✅ Legacy DB connection: SUCCESS
✅ Modern DB connection: SUCCESS
```

### Error Example
```
❌ Legacy DB connection: FAILED — (pymysql.err.OperationalError) Can't connect to MySQL server
❌ Modern DB connection: FAILED — (psycopg2.OperationalError) password authentication failed
```

### Helper Functions (Not Tools — Internal Use)

| Function | Description |
|----------|-------------|
| `get_connection_string(db_type, host, port, dbname, user, password)` | Builds a SQLAlchemy connection URL for the given database type |
| `get_legacy_engine()` | Returns a SQLAlchemy engine for the legacy database using `.env` variables |
| `get_modern_engine()` | Returns a SQLAlchemy engine for the modern database using `.env` variables |

### Supported Database Types

| Type | Connection Format | Driver |
|------|------------------|--------|
| `mysql` | `mysql+pymysql://user:pass@host:port/db` | PyMySQL |
| `postgresql` | `postgresql+psycopg2://user:pass@host:port/db` | psycopg2 |
| `sqlite` | `sqlite:///dbname` | Built-in |
| `mssql` | `mssql+pyodbc://user:pass@host:port/db` | pyodbc |

---

## 2 — Read Legacy Database Schema

| Property | Value |
|----------|-------|
| **Tool Name** | `Read Legacy Database Schema` |
| **File** | `src/tools/schema_reader.py` |
| **Function** | `read_legacy_schema()` |
| **Used By** | Agent 1 (Schema Analyst), Agent 2 (Schema Mapper) |
| **Parameters** | None |
| **Returns** | `str` — JSON string of the complete schema |

### Purpose
Reads the **entire structure** of the legacy database — every table, every column, every data type, every key. This is the foundational analysis that all subsequent agents depend on.

### How It Works
1. Connects to the legacy database via SQLAlchemy
2. Uses `sqlalchemy.inspect()` to introspect the database
3. For each table discovered:
   - Lists all columns with their **name**, **type**, **nullable** flag, and **default value**
   - Extracts **primary key** constraints
   - Extracts **foreign key** relationships (which columns reference which tables)
4. Returns everything as a formatted JSON string

### Output Example
```json
{
  "CUST_MASTER": {
    "columns": [
      {
        "name": "CUST_ID",
        "type": "INTEGER",
        "nullable": false,
        "default": "None"
      },
      {
        "name": "CUST_NAME",
        "type": "VARCHAR(100)",
        "nullable": true,
        "default": "None"
      }
    ],
    "primary_keys": ["CUST_ID"],
    "foreign_keys": []
  },
  "ORD_MASTER": {
    "columns": [
      {
        "name": "ORD_ID",
        "type": "INTEGER",
        "nullable": false,
        "default": "None"
      },
      {
        "name": "CUST_NO",
        "type": "INTEGER",
        "nullable": true,
        "default": "None"
      }
    ],
    "primary_keys": ["ORD_ID"],
    "foreign_keys": [
      {
        "columns": ["CUST_NO"],
        "referred_table": "CUST_MASTER",
        "referred_columns": ["CUST_ID"]
      }
    ]
  }
}
```

---

## 3 — Get Table Row Counts

| Property | Value |
|----------|-------|
| **Tool Name** | `Get Table Row Counts` |
| **File** | `src/tools/schema_reader.py` |
| **Function** | `get_table_row_counts()` |
| **Used By** | Agent 1 (Schema Analyst) |
| **Parameters** | None |
| **Returns** | `str` — JSON string with row counts per table |

### Purpose
Counts the total number of rows in **every table** of the legacy database. Used to understand data volume, plan batch sizes, and later validate that all rows were migrated.

### How It Works
1. Connects to the legacy database
2. Introspects all table names
3. Runs `SELECT COUNT(*) FROM <table>` for each table
4. Uses dynamic quoting (backticks for MySQL, double-quotes for PostgreSQL)
5. Returns counts as a JSON object

### Output Example
```json
{
  "CUST_MASTER": 52000,
  "ORD_MASTER": 1200000,
  "PROD_CATALOG": 8500
}
```

---

## 4 — Extract Table Batch

| Property | Value |
|----------|-------|
| **Tool Name** | `Extract Table Batch` |
| **File** | `src/tools/data_extractor.py` |
| **Function** | `extract_table_batch(table_name, offset)` |
| **Used By** | Agent 3 (ETL Specialist) |
| **Returns** | `str` — JSON string of extracted records or `NO_MORE_DATA` signal |

### Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `table_name` | `str` | ✅ Yes | — | Name of the legacy table to extract from |
| `offset` | `int` | ❌ No | `0` | Row offset for pagination (batch start point) |

### Purpose
Pulls data from the legacy database **in batches** to protect memory. The batch size is read from `config.yaml` (default: 500 rows). The agent calls this tool repeatedly with increasing offsets until it receives the `NO_MORE_DATA` signal.

### How It Works
1. Reads `batch_size` from `config.yaml` → `migration.batch_size`
2. Constructs a `SELECT * FROM <table> LIMIT :limit OFFSET :offset` query
3. Uses parameterized queries to prevent SQL injection
4. Converts results to a Pandas DataFrame → JSON string
5. If no rows are returned, sends the `NO_MORE_DATA` signal

### Output Example (Data Found)
```json
[
  {"CUST_ID": 1, "CUST_NAME": "john doe", "BIRTH_DT": "19850315", "STATUS": "A"},
  {"CUST_ID": 2, "CUST_NAME": "jane smith", "BIRTH_DT": "19900722", "STATUS": "I"}
]
```

### Output Example (No More Data)
```
NO_MORE_DATA: Table 'CUST_MASTER' — no rows at offset 52000
```

---

## 5 — Transform Data Batch

| Property | Value |
|----------|-------|
| **Tool Name** | `Transform Data Batch` |
| **File** | `src/tools/data_transformer.py` |
| **Function** | `transform_batch(batch_json, column_mappings_json, transformations_json)` |
| **Used By** | Agent 3 (ETL Specialist) |
| **Returns** | `str` — JSON string with transformed data + error report |

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `batch_json` | `str` | ✅ Yes | JSON string — list of records from the extractor |
| `column_mappings_json` | `str` | ✅ Yes | JSON string — maps old column names → new column names |
| `transformations_json` | `str` | ✅ Yes | JSON string — maps old column names → transformation rules |

### Purpose
The core data transformation engine. Takes raw legacy data and:
1. **Renames columns** (e.g., `CUST_NAME` → `full_name`)
2. **Transforms values** (e.g., `"19850315"` → `"1985-03-15"`)
3. **Reports errors** per row without stopping the batch

### Supported Transformation Rules

| Rule | Description | Input Example | Output Example |
|------|-------------|---------------|----------------|
| `cast_to_int` | Converts value to integer | `"42"`, `42.7` | `42` |
| `cast_to_decimal` | Converts value to float | `"3.14"` | `3.14` |
| `title_case` | Strips whitespace and converts to Title Case | `"john doe"` | `"John Doe"` |
| `parse_date_YYYYMMDD` | Parses date string `YYYYMMDD` to `YYYY-MM-DD` | `"19850315"` | `"1985-03-15"` |
| `map_values:K1=V1,K2=V2` | Maps specific values to new values | `"A"` with rule `map_values:A=True,I=False` | `True` |

### Null Handling
- All transformations return `None` if the input value is `None`
- Failed transformations (e.g., `cast_to_int` on `"abc"`) return `None` instead of crashing

### Output Example
```json
{
  "data": [
    {"id": 1, "full_name": "John Doe", "date_of_birth": "1985-03-15", "is_active": true},
    {"id": 2, "full_name": "Jane Smith", "date_of_birth": "1990-07-22", "is_active": false}
  ],
  "total_transformed": 2,
  "total_errors": 0,
  "errors": []
}
```

### Error Output Example
```json
{
  "data": [
    {"id": 1, "full_name": "John Doe", "date_of_birth": "1985-03-15", "is_active": true}
  ],
  "total_transformed": 1,
  "total_errors": 1,
  "errors": ["Row 1: 'NoneType' object has no attribute 'split'"]
}
```

---

## 6 — Load Batch to Modern Database

| Property | Value |
|----------|-------|
| **Tool Name** | `Load Batch to Modern Database` |
| **File** | `src/tools/data_loader.py` |
| **Function** | `load_batch_to_modern_db(target_table, batch_json, table_name, batch_number)` |
| **Used By** | Agent 3 (ETL Specialist) |
| **Returns** | `str` — success/failure status message |

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `target_table` | `str` | ✅ Yes | Name of the target table in the modern database |
| `batch_json` | `str` | ✅ Yes | JSON string containing transformed records (output from `transform_batch`) |
| `table_name` | `str` | ✅ Yes | Logical table name for progress tracking |
| `batch_number` | `int` | ✅ Yes | Current batch number for progress tracking |

### Purpose
Inserts transformed data into the modern database. Works with the output of `transform_batch` — automatically extracts records from the `data` field if present.

### How It Works
1. Parses the JSON input — handles both raw lists and the `{data: [...]}` format from the transformer
2. Converts records to a Pandas DataFrame
3. Uses `pandas.to_sql()` with `if_exists='append'` to insert rows
4. Updates `progress/progress.json` after each successful batch
5. Returns a status message

### Progress Tracking
After each successful batch, saves to `progress/progress.json`:
```json
{
  "customers": {
    "status": "in_progress",
    "rows_done": 1500,
    "last_batch": 3
  }
}
```

### Output Example (Success)
```
✅ Loaded 500 rows into 'customers' (batch 3)
```

### Output Example (Failure)
```
❌ FAILED loading batch 3 into 'customers': (psycopg2.errors.UniqueViolation) duplicate key value
```

---

## 7 — Compare Row Counts

| Property | Value |
|----------|-------|
| **Tool Name** | `Compare Row Counts` |
| **File** | `src/tools/validator_tools.py` |
| **Function** | `compare_row_counts(legacy_table, modern_table)` |
| **Used By** | Agent 4 (Data Validator) |
| **Returns** | `str` — PASS/WARN/FAIL comparison result |

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `legacy_table` | `str` | ✅ Yes | Table name in the legacy database |
| `modern_table` | `str` | ✅ Yes | Corresponding table name in the modern database |

### Purpose
The first validation check after migration — compares total row counts between the legacy and modern database tables to ensure no data was lost.

### How It Works
1. Runs `SELECT COUNT(*)` on the legacy table
2. Runs `SELECT COUNT(*)` on the modern table
3. Compares the two counts
4. Returns ✅ PASS if equal, ⚠️ WARN if different

### Output Example
```
✅ PASS: CUST_MASTER → customers
  Legacy rows: 52000
  Modern rows: 52000
  Difference:  0
```

---

## 8 — Check Null Values

| Property | Value |
|----------|-------|
| **Tool Name** | `Check Null Values` |
| **File** | `src/tools/validator_tools.py` |
| **Function** | `check_null_values(table_name, required_columns_json)` |
| **Used By** | Agent 4 (Data Validator) |
| **Returns** | `str` — per-column null check results |

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `table_name` | `str` | ✅ Yes | Table name in the modern database |
| `required_columns_json` | `str` | ✅ Yes | JSON array of column names that must NOT be null |

### Purpose
Verifies that required fields in the modern database contain no null values. Catches issues where transformations failed silently or data was lost.

### How It Works
1. Parses the list of required column names from JSON
2. For each column, runs `SELECT COUNT(*) WHERE <col> IS NULL`
3. Reports ✅ PASS if 0 nulls, ❌ FAIL if any nulls found

### Input Example
```json
["id", "full_name", "date_of_birth"]
```

### Output Example
```
Null check for 'customers':
  ✅ PASS: id — 0 nulls found
  ✅ PASS: full_name — 0 nulls found
  ❌ FAIL: date_of_birth — 3 nulls found
```

---

## 9 — Check Foreign Key Integrity

| Property | Value |
|----------|-------|
| **Tool Name** | `Check Foreign Key Integrity` |
| **File** | `src/tools/validator_tools.py` |
| **Function** | `check_foreign_key_integrity(child_table, child_column, parent_table, parent_column)` |
| **Used By** | Agent 4 (Data Validator) |
| **Returns** | `str` — FK integrity check result |

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `child_table` | `str` | ✅ Yes | Table containing the foreign key |
| `child_column` | `str` | ✅ Yes | Column with the foreign key reference |
| `parent_table` | `str` | ✅ Yes | Referenced (parent) table |
| `parent_column` | `str` | ✅ Yes | Referenced column in the parent table |

### Purpose
Verifies that all foreign key relationships are intact in the modern database after migration. Detects orphaned records — rows that reference a parent row that doesn't exist.

### How It Works
1. Runs a `LEFT JOIN` query between child and parent tables
2. Counts rows where the parent reference is `NULL` but the child FK value is not `NULL` (orphans)
3. Returns ✅ PASS if 0 orphans, ❌ FAIL otherwise

### SQL Logic
```sql
SELECT COUNT(*)
FROM "orders" c
LEFT JOIN "customers" p ON c."customer_id" = p."id"
WHERE p."id" IS NULL AND c."customer_id" IS NOT NULL
```

### Output Example
```
✅ PASS: FK orders.customer_id → customers.id
  Orphaned records: 0
```

---

## 10 — Compare Sample Records

| Property | Value |
|----------|-------|
| **Tool Name** | `Compare Sample Records` |
| **File** | `src/tools/validator_tools.py` |
| **Function** | `compare_sample_records(legacy_table, modern_table, column_mappings_json, sample_size)` |
| **Used By** | Agent 4 (Data Validator) |
| **Returns** | `str` — sample comparison results |

### Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `legacy_table` | `str` | ✅ Yes | — | Source table in legacy database |
| `modern_table` | `str` | ✅ Yes | — | Target table in modern database |
| `column_mappings_json` | `str` | ✅ Yes | — | JSON mapping of old column names → new names |
| `sample_size` | `int` | ❌ No | `10` | Number of records to sample |

### Purpose
Spot-checks actual data by comparing a sample of records between legacy and modern databases. This is the "trust but verify" check — ensures real data matches after transformation.

### How It Works
1. Fetches `sample_size` records from the legacy table
2. Fetches `sample_size` records from the modern table
3. Compares sample sizes and reports column structures
4. Uses parameterized queries for the sample size (prevents SQL injection)

### Output Example
```
Sample comparison: CUST_MASTER → customers
  Legacy records sampled: 10
  Modern records sampled: 10
  Legacy columns: ['CUST_ID', 'CUST_NAME', 'BIRTH_DT', 'STATUS']
  Modern columns: ['id', 'full_name', 'date_of_birth', 'is_active']
  ✅ Sample sizes match
```

---

## 🔧 Internal Helper Functions

These are **not** CrewAI tools — they are internal utilities used by the tools above.

### `db_connector.py` Helpers

| Function | Description |
|----------|-------------|
| `get_connection_string(db_type, host, port, dbname, user, password)` | Builds a SQLAlchemy connection URL based on DB type |
| `get_legacy_engine()` | Creates a SQLAlchemy engine for the legacy DB using `.env` variables |
| `get_modern_engine()` | Creates a SQLAlchemy engine for the modern DB using `.env` variables |
| `test_db_connections()` | Plain (non-tool) version of `test_connections` — callable from `main.py` |

### `schema_reader.py` / `data_extractor.py` Helpers

| Function | Description |
|----------|-------------|
| `_get_quote_char()` | Returns `` ` `` for MySQL or `"` for PostgreSQL based on `config.yaml` |

### `validator_tools.py` Helpers

| Function | Description |
|----------|-------------|
| `_get_legacy_quote()` | Returns the correct SQL identifier quote for the legacy DB |
| `_get_modern_quote()` | Returns the correct SQL identifier quote for the modern DB |

### `data_transformer.py` Helpers

| Function | Description |
|----------|-------------|
| `apply_transformation(value, rule)` | Applies a single transformation rule to a single value |

---

## 📊 Data Flow Through Tools

```
                    EXTRACT                     TRANSFORM                    LOAD
                 ┌───────────┐              ┌──────────────┐            ┌──────────┐
  Legacy DB ───→ │ extract   │ ── JSON ──→  │ transform    │ ── JSON ──→│ load     │ ───→ Modern DB
                 │ _table    │   (raw data) │ _batch       │  (clean    │ _batch   │
                 │ _batch    │              │              │   data)    │ _to      │
                 └───────────┘              └──────────────┘            │ _modern  │
                                                                       │ _db      │
                                                                       └──────────┘
                                                                            │
                                                                            ▼
                                                                   progress/progress.json
```

---

> **Built for the Antigravity Agent** using **CrewAI + Ollama (qwen2.5-coder:7b)**
> All tools use dynamic SQL quoting for cross-database compatibility.
> All tools return strings (CrewAI requirement) and handle errors gracefully.
