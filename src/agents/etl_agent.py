# src/agents/etl_agent.py

from crewai import Agent
from src.tools.data_extractor import extract_table_batch
from src.tools.data_transformer import transform_batch
from src.tools.data_loader import load_batch_to_modern_db
from src.utils.ollama_llm import get_ollama_llm

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
    llm=get_ollama_llm(),
    verbose=True,
    allow_delegation=False,
    max_iter=20
)
