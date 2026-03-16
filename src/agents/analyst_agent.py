# src/agents/analyst_agent.py

from crewai import Agent
from src.tools.schema_reader import read_legacy_schema, get_table_row_counts
from src.utils.ollama_llm import get_ollama_llm

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
    llm=get_ollama_llm(),
    verbose=True,
    allow_delegation=False,
    max_iter=5
)
