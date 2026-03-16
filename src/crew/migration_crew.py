# src/crew/migration_crew.py

from crewai import Crew, Process
from src.agents.analyst_agent import analyst_agent
from src.agents.mapper_agent import mapper_agent
from src.agents.etl_agent import etl_agent
from src.agents.validator_agent import validator_agent
from src.agents.reporter_agent import reporter_agent
from src.tasks.analyze_task import analyze_task
from src.tasks.mapping_task import mapping_task
from src.tasks.etl_task import etl_task
from src.tasks.validation_task import validation_task
from src.tasks.report_task import report_task


def build_migration_crew() -> Crew:
    return Crew(
        agents=[
            analyst_agent,
            mapper_agent,
            etl_agent,
            validator_agent,
            reporter_agent
        ],
        tasks=[
            analyze_task,
            mapping_task,
            etl_task,
            validation_task,
            report_task
        ],
        process=Process.sequential,   # Runs agents in exact order, one at a time
        verbose=True,
        memory=False,                 # Disabled — requires OpenAI embeddings by default
                                      # Context is passed via task.context instead
        max_rpm=10                    # API rate limit protection
    )
