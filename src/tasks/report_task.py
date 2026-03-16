# src/tasks/report_task.py

from crewai import Task
from src.agents.reporter_agent import reporter_agent
from src.tasks.analyze_task import analyze_task
from src.tasks.mapping_task import mapping_task
from src.tasks.etl_task import etl_task
from src.tasks.validation_task import validation_task

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
