# src/tasks/validation_task.py

from crewai import Task
from src.agents.validator_agent import validator_agent
from src.tasks.etl_task import etl_task

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
