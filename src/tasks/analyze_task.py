# src/tasks/analyze_task.py

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
