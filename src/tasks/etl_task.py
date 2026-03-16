# src/tasks/etl_task.py

from crewai import Task
from src.agents.etl_agent import etl_agent
from src.tasks.analyze_task import analyze_task
from src.tasks.mapping_task import mapping_task

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
