# main.py — Entry Point for Automated Data Migration

import os
import time

# CRITICAL: Load .env and set dummy API key BEFORE importing CrewAI modules
from dotenv import load_dotenv
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-no-openai-key-needed-using-ollama"

# Now safe to import CrewAI-based modules
from src.crew.migration_crew import build_migration_crew
from src.utils.logger import setup_logger
from src.tools.db_connector import test_db_connections

logger = setup_logger()


def main():
    logger.info("=" * 60)
    logger.info("  AUTOMATED DATA MIGRATION — STARTING")
    logger.info(f"  LLM: Ollama ({os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:7b')})")
    logger.info("=" * 60)

    # Step 1: Test connections before doing anything
    logger.info("Testing database connections...")
    connection_results = test_db_connections()
    print(connection_results)

    if "FAILED" in connection_results:
        logger.error("Cannot proceed — fix database connections first.")
        return

    # Step 2: Build and run the crew
    logger.info("Assembling migration crew...")
    start_time = time.time()

    crew = build_migration_crew()
    result = crew.kickoff()

    # Step 3: Done
    elapsed = round(time.time() - start_time, 2)
    logger.info(f"Migration completed in {elapsed} seconds")
    logger.info("Check reports/ directory for the full migration report.")

    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
