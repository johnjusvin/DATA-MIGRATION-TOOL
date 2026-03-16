# 🚀 Automated Data Migration from Legacy System to Modern Database
### Powered by CrewAI Multi-Agent Framework

---

> **This README is the single source of truth for the Antigravity Agent.**
> Read every section completely before executing anything.
> Every step is mandatory. Never skip. Never assume.

---

## 🧠 What Is This System?

This system is a **fully automated, intelligent data migration pipeline** that uses **CrewAI multi-agent orchestration** to move data from any legacy database to any modern database — safely, completely, and with zero manual intervention.

The system uses a **crew of 5 specialized AI agents**, each with a precise role, working in sequence to:

1. Analyze the legacy database structure
2. Map old schema to new schema
3. Extract, transform, and load all data in batches
4. Validate every row migrated
5. Generate a full audit report

This is not a one-time script. This is a **production-grade, reusable migration engine** that works with any database combination.

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ANTIGRAVITY AGENT                            │
│                     (CrewAI Orchestrator)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  config.yaml                                                        │
│      │                                                              │
│      ▼                                                              │
│  ┌──────────────┐                                                   │
│  │   AGENT 1    │  🔍 Schema Analyst                                │
│  │              │  → Reads legacy DB, maps all tables/columns       │
│  └──────┬───────┘                                                   │
│         │                                                           │
│  ┌──────▼───────┐                                                   │
│  │   AGENT 2    │  🗺️  Schema Mapper                                │
│  │              │  → Maps old structure to new structure            │
│  └──────┬───────┘                                                   │
│         │                                                           │
│  ┌──────▼───────┐                                                   │
│  │   AGENT 3    │  ⚙️  ETL Specialist                               │
│  │              │  → Extracts, transforms, loads all data           │
│  └──────┬───────┘                                                   │
│         │                                                           │
│  ┌──────▼───────┐                                                   │
│  │   AGENT 4    │  ✅ Data Validator                                 │
│  │              │  → Verifies every row, checks integrity           │
│  └──────┬───────┘                                                   │
│         │                                                           │
│  ┌──────▼───────┐                                                   │
│  │   AGENT 5    │  📋 Migration Reporter                            │
│  │              │  → Generates full audit report                    │
│  └──────────────┘                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Folder Structure

Build this exact folder structure. Every file has a purpose. Do not rename or move files.

```
data-migration/
│
├── main.py                          ← ENTRY POINT — run this to start migration
├── config.yaml                      ← ALL database configs and migration settings
├── requirements.txt                 ← Python dependencies
├── .env                             ← API keys and secrets (never commit this)
│
├── src/
│   ├── __init__.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── analyst_agent.py         ← Agent 1: Schema Analyst
│   │   ├── mapper_agent.py          ← Agent 2: Schema Mapper
│   │   ├── etl_agent.py             ← Agent 3: ETL Specialist
│   │   ├── validator_agent.py       ← Agent 4: Data Validator
│   │   └── reporter_agent.py        ← Agent 5: Migration Reporter
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── analyze_task.py          ← Task definition for Agent 1
│   │   ├── mapping_task.py          ← Task definition for Agent 2
│   │   ├── etl_task.py              ← Task definition for Agent 3
│   │   ├── validation_task.py       ← Task definition for Agent 4
│   │   └── report_task.py           ← Task definition for Agent 5
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── db_connector.py          ← Connects to any DB (MySQL, PostgreSQL, SQLite, etc.)
│   │   ├── schema_reader.py         ← Reads legacy DB structure
│   │   ├── data_extractor.py        ← Pulls data from legacy DB in batches
│   │   ├── data_transformer.py      ← Cleans and reshapes data
│   │   ├── data_loader.py           ← Inserts data into modern DB
│   │   └── validator_tools.py       ← Row counts, checksums, integrity checks
│   │
│   ├── crew/
│   │   ├── __init__.py
│   │   └── migration_crew.py        ← Assembles all agents and tasks into the crew
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                ← Logging system
│       ├── progress_tracker.py      ← Saves/resumes migration progress
│       ├── rollback.py              ← Undoes migration if something fails
│       └── config_loader.py        ← Reads config.yaml
│
├── logs/
│   └── migration.log                ← Auto-generated — do not edit manually
│
├── reports/
│   └── report_YYYY-MM-DD.md         ← Auto-generated migration report
│
└── progress/
    └── progress.json                ← Auto-generated progress tracker
```

---

## ⚙️ Step 1 — Environment Setup

### 1.1 Install Python Dependencies

```bash
pip install crewai
pip install crewai-tools
pip install sqlalchemy
pip install pandas
pip install pymysql
pip install psycopg2-binary
pip install pymongo
pip install pyyaml
pip install python-dotenv
pip install great-expectations
pip install colorlog
```

Save all of these in `requirements.txt`:

```
crewai>=0.28.0
crewai-tools>=0.1.0
sqlalchemy>=2.0.0
pandas>=2.0.0
pymysql>=1.1.0
psycopg2-binary>=2.9.0
pymongo>=4.0.0
pyyaml>=6.0
python-dotenv>=1.0.0
great-expectations>=0.18.0
colorlog>=6.7.0
```

### 1.2 Create `.env` File

```env
# LLM API Key (CrewAI uses this to power agents)
OPENAI_API_KEY=your_openai_key_here

# Legacy Database
LEGACY_DB_TYPE=mysql
LEGACY_DB_HOST=localhost
LEGACY_DB_PORT=3306
LEGACY_DB_NAME=legacy_database
LEGACY_DB_USER=root
LEGACY_DB_PASSWORD=your_legacy_password

# Modern Database
MODERN_DB_TYPE=postgresql
MODERN_DB_HOST=localhost
MODERN_DB_PORT=5432
MODERN_DB_NAME=modern_database
MODERN_DB_USER=admin
MODERN_DB_PASSWORD=your_modern_password
```

> ⚠️ **CRITICAL**: Never hardcode passwords in source code. Always use `.env` file.

---

## ⚙️ Step 2 — Build `config.yaml`

This is the control center of the entire system. Everything the agents need is here.

```yaml
# config.yaml

migration:
  name: "Legacy to Modern Migration"
  batch_size: 500           # rows per batch
  max_retries: 3            # retry failed batches this many times
  resume_on_failure: true   # resume from last checkpoint if crash

source:
  type: mysql               # mysql | postgresql | sqlite | mongodb | mssql | oracle
  host: ${LEGACY_DB_HOST}
  port: ${LEGACY_DB_PORT}
  database: ${LEGACY_DB_NAME}
  user: ${LEGACY_DB_USER}
  password: ${LEGACY_DB_PASSWORD}

target:
  type: postgresql          # mysql | postgresql | sqlite | mongodb
  host: ${MODERN_DB_HOST}
  port: ${MODERN_DB_PORT}
  database: ${MODERN_DB_NAME}
  user: ${MODERN_DB_USER}
  password: ${MODERN_DB_PASSWORD}

tables:
  - name: customers
    source_table: CUST_MASTER
    target_table: customers
    column_mappings:
      CUST_ID: id
      CUST_NAME: full_name
      BIRTH_DT: date_of_birth
      STATUS: is_active
    transformations:
      CUST_ID: "cast_to_int"
      CUST_NAME: "title_case"
      BIRTH_DT: "parse_date_YYYYMMDD"
      STATUS: "map_values:A=True,I=False"

  - name: orders
    source_table: ORD_MASTER
    target_table: orders
    column_mappings:
      ORD_ID: id
      CUST_NO: customer_id
      ORD_DT: order_date
      TOTAL_AMT: total_amount
    transformations:
      ORD_ID: "cast_to_int"
      CUST_NO: "cast_to_int"
      ORD_DT: "parse_date_YYYYMMDD"
      TOTAL_AMT: "cast_to_decimal"

logging:
  level: INFO               # DEBUG | INFO | WARNING | ERROR
  file: logs/migration.log

reporting:
  output_dir: reports/
  format: markdown          # markdown | html | txt
```

---

## ⚙️ Step 3 — Build the Database Connector Tool

**File: `src/tools/db_connector.py`**

This tool makes the system work with ANY database. Agents use this tool to connect.

```python
# src/tools/db_connector.py

from sqlalchemy import create_engine, text
from crewai.tools import tool
import os

def get_connection_string(db_type, host, port, dbname, user, password):
    """Builds the correct connection string for any database type."""
    connectors = {
        "mysql":      f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}",
        "postgresql": f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}",
        "sqlite":     f"sqlite:///{dbname}",
        "mssql":      f"mssql+pyodbc://{user}:{password}@{host}:{port}/{dbname}",
    }
    if db_type not in connectors:
        raise ValueError(f"Unsupported database type: {db_type}")
    return connectors[db_type]


def get_legacy_engine():
    conn_str = get_connection_string(
        os.getenv("LEGACY_DB_TYPE"),
        os.getenv("LEGACY_DB_HOST"),
        os.getenv("LEGACY_DB_PORT"),
        os.getenv("LEGACY_DB_NAME"),
        os.getenv("LEGACY_DB_USER"),
        os.getenv("LEGACY_DB_PASSWORD"),
    )
    return create_engine(conn_str)


def get_modern_engine():
    conn_str = get_connection_string(
        os.getenv("MODERN_DB_TYPE"),
        os.getenv("MODERN_DB_HOST"),
        os.getenv("MODERN_DB_PORT"),
        os.getenv("MODERN_DB_NAME"),
        os.getenv("MODERN_DB_USER"),
        os.getenv("MODERN_DB_PASSWORD"),
    )
    return create_engine(conn_str)


@tool("Test Database Connections")
def test_connections() -> str:
    """Tests connectivity to both legacy and modern databases."""
    results = []
    try:
        engine = get_legacy_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        results.append("✅ Legacy DB connection: SUCCESS")
    except Exception as e:
        results.append(f"❌ Legacy DB connection: FAILED — {str(e)}")

    try:
        engine = get_modern_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        results.append("✅ Modern DB connection: SUCCESS")
    except Exception as e:
        results.append(f"❌ Modern DB connection: FAILED — {str(e)}")

    return "\n".join(results)
```

---

## ⚙️ Step 4 — Build the 5 Agents

### Agent 1: Schema Analyst
**File: `src/agents/analyst_agent.py`**

```python
from crewai import Agent
from src.tools.schema_reader import read_legacy_schema, get_table_row_counts

analyst_agent = Agent(
    role="Senior Database Analyst",
    goal=(
        "Thoroughly analyze the legacy database. "
        "Identify every table, every column, every data type, "
        "every primary key, every foreign key, and every data quality issue. "
        "Produce a complete, accurate schema analysis report."
    ),
    backstory=(
        "You are a veteran database engineer with 20 years of experience "
        "reverse-engineering legacy systems. You leave nothing undiscovered. "
        "You document everything with precision. You are the first agent to run "
        "and your output determines everything that follows."
    ),
    tools=[read_legacy_schema, get_table_row_counts],
    verbose=True,
    allow_delegation=False,
    max_iter=5
)
```

### Agent 2: Schema Mapper
**File: `src/agents/mapper_agent.py`**

```python
from crewai import Agent
from src.tools.schema_reader import read_legacy_schema

mapper_agent = Agent(
    role="Data Architecture Mapper",
    goal=(
        "Using the schema analysis report, create a precise mapping "
        "from every legacy column to the correct modern column. "
        "Identify required type conversions, value transformations, "
        "and any columns that need to be split or merged."
    ),
    backstory=(
        "You are a data architect who specializes in translating old, messy "
        "database schemas into clean, normalized modern structures. "
        "You understand every data type conversion and every edge case. "
        "Your mappings are always 100% accurate and cover every column."
    ),
    tools=[read_legacy_schema],
    verbose=True,
    allow_delegation=False,
    max_iter=5
)
```

### Agent 3: ETL Specialist
**File: `src/agents/etl_agent.py`**

```python
from crewai import Agent
from src.tools.data_extractor import extract_table_batch
from src.tools.data_transformer import transform_batch
from src.tools.data_loader import load_batch_to_modern_db

etl_agent = Agent(
    role="ETL Pipeline Specialist",
    goal=(
        "Execute the full Extract-Transform-Load pipeline for every table. "
        "Extract data in batches of 500 rows. Apply all transformations from "
        "the schema mapping. Load clean data into the modern database. "
        "Never lose a single row. Handle errors gracefully and log everything."
    ),
    backstory=(
        "You are an ETL engineer who has migrated petabytes of data across "
        "hundreds of projects. You always work in batches to protect memory. "
        "You never skip rows. You handle errors row by row so one bad record "
        "never stops the entire migration. You are thorough and methodical."
    ),
    tools=[extract_table_batch, transform_batch, load_batch_to_modern_db],
    verbose=True,
    allow_delegation=False,
    max_iter=20
)
```

### Agent 4: Data Validator
**File: `src/agents/validator_agent.py`**

```python
from crewai import Agent
from src.tools.validator_tools import (
    compare_row_counts,
    check_null_values,
    check_foreign_key_integrity,
    compare_sample_records
)

validator_agent = Agent(
    role="Data Quality Validator",
    goal=(
        "After migration, validate that every single row was migrated correctly. "
        "Compare row counts between legacy and modern databases. "
        "Check for null values in required fields. "
        "Verify foreign key relationships are intact. "
        "Compare sample records between old and new to confirm data accuracy. "
        "Report any discrepancy immediately."
    ),
    backstory=(
        "You are a data quality engineer with zero tolerance for errors. "
        "You trust nothing until you verify it yourself. "
        "You have caught data corruption issues that everyone else missed. "
        "Your validation reports are the final word on whether a migration succeeded."
    ),
    tools=[compare_row_counts, check_null_values, check_foreign_key_integrity, compare_sample_records],
    verbose=True,
    allow_delegation=False,
    max_iter=10
)
```

### Agent 5: Migration Reporter
**File: `src/agents/reporter_agent.py`**

```python
from crewai import Agent

reporter_agent = Agent(
    role="Technical Documentation Specialist",
    goal=(
        "Compile all outputs from every agent into a single, clear, "
        "professional migration report in Markdown format. "
        "The report must include: total tables migrated, row counts per table, "
        "transformation summary, validation results, errors found, "
        "and overall migration status (SUCCESS / PARTIAL / FAILED)."
    ),
    backstory=(
        "You are a technical writer who specializes in database operations. "
        "You take raw technical outputs and turn them into clean, readable reports "
        "that both engineers and managers can understand. "
        "Your reports are used as the official audit trail for every migration."
    ),
    tools=[],
    verbose=True,
    allow_delegation=False,
    max_iter=3
)
```

---

## ⚙️ Step 5 — Build the 5 Tasks

### Task 1: Analyze
**File: `src/tasks/analyze_task.py`**

```python
from crewai import Task
from src.agents.analyst_agent import analyst_agent

analyze_task = Task(
    description=(
        "Connect to the legacy database defined in config.yaml. "
        "List every table. For each table: get column names, data types, "
        "primary keys, foreign keys, nullable columns, and total row count. "
        "Flag any data quality issues found (mixed types, nulls in key fields, "
        "duplicate rows, inconsistent formats). "
        "Output a structured schema analysis report."
    ),
    expected_output=(
        "A complete schema analysis report listing every table, "
        "its columns with data types, row counts, keys, and any data issues found."
    ),
    agent=analyst_agent
)
```

### Task 2: Map
**File: `src/tasks/mapping_task.py`**

```python
from crewai import Task
from src.agents.mapper_agent import mapper_agent

mapping_task = Task(
    description=(
        "Using the schema analysis report from the analyst agent, "
        "create a precise column-by-column mapping from legacy to modern schema. "
        "For each column specify: old name, new name, old type, new type, "
        "and any transformation rule required (e.g. cast_to_int, parse_date, "
        "map_values, title_case, etc). "
        "Also identify migration order based on foreign key dependencies — "
        "parent tables must be migrated before child tables."
    ),
    expected_output=(
        "A complete mapping document showing old column to new column for every table, "
        "with transformation rules and migration order."
    ),
    agent=mapper_agent,
    context=[analyze_task]
)
```

### Task 3: ETL
**File: `src/tasks/etl_task.py`**

```python
from crewai import Task
from src.agents.etl_agent import etl_agent

etl_task = Task(
    description=(
        "Using the schema mapping, execute the full ETL pipeline: "
        "1. EXTRACT: Pull data from each legacy table in batches of 500 rows. "
        "2. TRANSFORM: Apply every transformation rule from the mapping. "
        "   Handle nulls, fix data types, clean strings, map values. "
        "3. LOAD: Insert transformed batches into the modern database. "
        "   Use upsert logic to allow safe re-runs. "
        "4. Track progress after every batch. Save to progress/progress.json. "
        "5. If a batch fails, retry up to 3 times before logging and skipping. "
        "Migrate tables in the order specified by the mapping (parent tables first)."
    ),
    expected_output=(
        "A detailed ETL execution log showing rows extracted, transformed, "
        "and loaded per table. Any rows that failed must be listed separately."
    ),
    agent=etl_agent,
    context=[analyze_task, mapping_task]
)
```

### Task 4: Validate
**File: `src/tasks/validation_task.py`**

```python
from crewai import Task
from src.agents.validator_agent import validator_agent

validation_task = Task(
    description=(
        "Validate the migration by performing these checks for every table: "
        "1. ROW COUNT CHECK: Compare total rows in legacy vs modern. "
        "2. NULL CHECK: Verify no required fields are null in modern DB. "
        "3. FOREIGN KEY CHECK: Confirm all relationships are intact. "
        "4. SAMPLE CHECK: Pick 10 random records per table, compare old vs new. "
        "5. TYPE CHECK: Verify all columns have the correct data types. "
        "Mark each table as PASS, WARN, or FAIL with a reason."
    ),
    expected_output=(
        "A validation report showing PASS/WARN/FAIL status for every table "
        "with specific details on any issues found."
    ),
    agent=validator_agent,
    context=[etl_task]
)
```

### Task 5: Report
**File: `src/tasks/report_task.py`**

```python
from crewai import Task
from src.agents.reporter_agent import reporter_agent

report_task = Task(
    description=(
        "Compile all outputs from the analyst, mapper, ETL, and validator agents "
        "into a single professional migration report. "
        "Save it to reports/ with today's date in the filename. "
        "The report must include these sections: "
        "1. Executive Summary "
        "2. Migration Configuration (source, target, date, duration) "
        "3. Tables Migrated (name, row count, status) "
        "4. Transformations Applied "
        "5. Validation Results "
        "6. Errors and Skipped Rows "
        "7. Overall Status: SUCCESS / PARTIAL SUCCESS / FAILED "
        "8. Recommended Next Steps"
    ),
    expected_output=(
        "A complete, professional Markdown migration report saved to the reports/ directory."
    ),
    agent=reporter_agent,
    context=[analyze_task, mapping_task, etl_task, validation_task]
)
```

---

## ⚙️ Step 6 — Assemble the Crew

**File: `src/crew/migration_crew.py`**

```python
from crewai import Crew, Process
from src.agents.analyst_agent import analyst_agent
from src.agents.mapper_agent import mapper_agent
from src.agents.etl_agent import etl_agent
from src.agents.validator_agent import validator_agent
from src.agents.reporter_agent import reporter_agent
from src.tasks.analyze_task import analyze_task
from src.tasks.mapping_task import mapping_task
from src.tasks.etl_task import etl_task
from src.tasks.validation_task import validation_task
from src.tasks.report_task import report_task


def build_migration_crew() -> Crew:
    return Crew(
        agents=[
            analyst_agent,
            mapper_agent,
            etl_agent,
            validator_agent,
            reporter_agent
        ],
        tasks=[
            analyze_task,
            mapping_task,
            etl_task,
            validation_task,
            report_task
        ],
        process=Process.sequential,   # Runs agents in exact order, one at a time
        verbose=True,
        memory=True,                  # Agents remember context from previous tasks
        max_rpm=10                    # API rate limit protection
    )
```

---

## ⚙️ Step 7 — Build `main.py` (Entry Point)

**File: `main.py`**

```python
import os
import time
from dotenv import load_dotenv
from src.crew.migration_crew import build_migration_crew
from src.utils.logger import setup_logger
from src.tools.db_connector import test_connections

load_dotenv()
logger = setup_logger()

def main():
    logger.info("=" * 60)
    logger.info("  AUTOMATED DATA MIGRATION — STARTING")
    logger.info("=" * 60)

    # Step 1: Test connections before doing anything
    logger.info("Testing database connections...")
    connection_results = test_connections()
    print(connection_results)

    if "FAILED" in connection_results:
        logger.error("Cannot proceed — fix database connections first.")
        return

    # Step 2: Build and run the crew
    logger.info("Assembling migration crew...")
    start_time = time.time()

    crew = build_migration_crew()
    result = crew.kickoff()

    # Step 3: Done
    elapsed = round(time.time() - start_time, 2)
    logger.info(f"Migration completed in {elapsed} seconds")
    logger.info("Check reports/ directory for the full migration report.")

    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
```

---

## ⚙️ Step 8 — Build the Logger

**File: `src/utils/logger.py`**

```python
import logging
import colorlog
import os
from datetime import datetime

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] %(levelname)-8s%(reset)s %(message)s",
        log_colors={
            "DEBUG":    "cyan",
            "INFO":     "green",
            "WARNING":  "yellow",
            "ERROR":    "red",
            "CRITICAL": "bold_red",
        }
    )
    file_formatter = logging.Formatter("[%(asctime)s] %(levelname)-8s %(message)s")

    logger = logging.getLogger("migration")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
```

---

## ⚙️ Step 9 — Build the Progress Tracker

**File: `src/utils/progress_tracker.py`**

```python
import json
import os

PROGRESS_FILE = "progress/progress.json"

def load_progress() -> dict:
    os.makedirs("progress", exist_ok=True)
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def save_progress(table_name: str, status: str, rows_done: int, last_batch: int):
    progress = load_progress()
    progress[table_name] = {
        "status": status,
        "rows_done": rows_done,
        "last_batch": last_batch
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def is_completed(table_name: str) -> bool:
    progress = load_progress()
    return progress.get(table_name, {}).get("status") == "completed"

def get_last_batch(table_name: str) -> int:
    progress = load_progress()
    return progress.get(table_name, {}).get("last_batch", 0)
```

---

## ⚙️ Step 10 — Build the Rollback System

**File: `src/utils/rollback.py`**

```python
from sqlalchemy import text
from src.tools.db_connector import get_modern_engine
from src.utils.logger import setup_logger

logger = setup_logger()

def rollback_table(table_name: str):
    """Deletes all rows inserted into a modern DB table during migration."""
    engine = get_modern_engine()
    with engine.connect() as conn:
        result = conn.execute(text(f"DELETE FROM {table_name}"))
        conn.commit()
        logger.warning(f"ROLLBACK: Deleted {result.rowcount} rows from {table_name}")

def rollback_all(tables: list):
    """Rolls back all migrated tables in reverse order (children before parents)."""
    for table in reversed(tables):
        rollback_table(table)
    logger.warning("ROLLBACK COMPLETE — All migrated data removed from modern DB")
```

---

## 🚀 How to Run the System

### Full Migration (Normal Run)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Fill in your .env file with DB credentials

# 3. Update config.yaml with your tables and column mappings

# 4. Run the migration
python main.py
```

### Resume After a Crash

The system automatically resumes from the last saved batch. Just re-run:

```bash
python main.py
```

Progress tracker reads `progress/progress.json` and skips completed tables automatically.

### Rollback Everything

```bash
python -c "from src.utils.rollback import rollback_all; rollback_all(['customers', 'orders', 'products'])"
```

### View the Migration Report

```bash
cat reports/report_YYYY-MM-DD.md
```

---

## ✅ Post-Migration Validation Checklist

The system runs these automatically, but verify manually if any table shows FAIL:

- [ ] Row count in modern DB matches legacy DB (or expected difference if deduplication ran)
- [ ] No NULL values in primary key columns
- [ ] All foreign key relationships are valid
- [ ] Date columns contain real dates, not strings
- [ ] Boolean columns contain True/False, not raw legacy codes
- [ ] No duplicate rows in any table
- [ ] Migration report generated in `reports/` directory
- [ ] No ERROR lines in `logs/migration.log`

---

## ❌ Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `Connection refused` | Wrong host/port in .env | Verify DB is running, check credentials |
| `Table not found` | Wrong table name in config.yaml | Check exact table names in legacy DB |
| `Data type mismatch` | Wrong transformation rule | Update transformation in config.yaml |
| `Duplicate key violation` | Re-running without rollback | Add upsert logic or run rollback first |
| `Memory error` | Batch size too large | Reduce `batch_size` in config.yaml to 100 |
| `API rate limit` | Too many LLM calls | Reduce `max_rpm` in migration_crew.py |
| `Null constraint violation` | Missing required field | Add null handling in transformer tool |

---

## 📋 Final Migration Report Format

The Reporter Agent generates this automatically at the end of every run:

```markdown
# Migration Report — 2024-01-15

## Executive Summary
Migration from MySQL (legacy_db) to PostgreSQL (modern_db) completed
successfully. 3 tables migrated. 1.25 million rows total. 0 data loss.

## Configuration
- Source:    MySQL @ localhost:3306/legacy_db
- Target:    PostgreSQL @ localhost:5432/modern_db
- Duration:  14 minutes 32 seconds
- Batch Size: 500

## Tables Migrated
| Table      | Legacy Rows | Modern Rows | Status   |
|------------|-------------|-------------|----------|
| customers  | 52,000      | 51,997      | ✅ PASS  |
| orders     | 1,200,000   | 1,200,000   | ✅ PASS  |
| products   | 8,500       | 8,500       | ✅ PASS  |

## Validation Results
All tables PASSED validation.
3 duplicate customers removed (expected behavior).

## Overall Status: ✅ SUCCESS
```

---

## 🔑 The 10 Rules the Antigravity Agent Must Never Break

1. **Always read `config.yaml` first** — everything starts there
2. **Always test DB connections before migrating** — never assume they work
3. **Always migrate parent tables before child tables** — or foreign keys will break
4. **Always use batches** — never load all rows into memory at once
5. **Always save progress after every batch** — so crashes do not lose work
6. **Always validate after every table** — catch issues early, not at the end
7. **Never hardcode credentials** — always use `.env`
8. **Never skip the rollback system** — it will be needed eventually
9. **Never delete legacy data** — it is your backup until validation passes
10. **Always generate the final report** — it is the proof the migration succeeded

---

> Built for the **Antigravity Agent** using **CrewAI + Python**
> This README is the complete specification. Follow it exactly.
> Every section is mandatory. No steps are optional.