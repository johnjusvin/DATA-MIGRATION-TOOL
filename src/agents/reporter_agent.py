# src/agents/reporter_agent.py

from crewai import Agent
from src.utils.ollama_llm import get_ollama_llm

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
    llm=get_ollama_llm(),
    verbose=True,
    allow_delegation=False,
    max_iter=3
)
