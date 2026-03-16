# src/tasks/mapping_task.py

from crewai import Task
from src.agents.mapper_agent import mapper_agent
from src.tasks.analyze_task import analyze_task

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
