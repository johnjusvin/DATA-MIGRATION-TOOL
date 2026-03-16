# src/agents/mapper_agent.py

from crewai import Agent
from src.tools.schema_reader import read_legacy_schema
from src.utils.ollama_llm import get_ollama_llm

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
    llm=get_ollama_llm(),
    verbose=True,
    allow_delegation=False,
    max_iter=5
)
