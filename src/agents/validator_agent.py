# src/agents/validator_agent.py

from crewai import Agent
from src.tools.validator_tools import (
    compare_row_counts,
    check_null_values,
    check_foreign_key_integrity,
    compare_sample_records
)
from src.utils.ollama_llm import get_ollama_llm

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
    llm=get_ollama_llm(),
    verbose=True,
    allow_delegation=False,
    max_iter=10
)
