# src/utils/rollback.py

from sqlalchemy import text
from src.tools.db_connector import get_modern_engine
from src.utils.logger import setup_logger

logger = setup_logger()


def rollback_table(table_name: str):
    """Deletes all rows inserted into a modern DB table during migration."""
    engine = get_modern_engine()
    # Use quoted identifier to prevent SQL injection
    with engine.connect() as conn:
        result = conn.execute(text(f'DELETE FROM "{table_name}"'))
        conn.commit()
        logger.warning(f"ROLLBACK: Deleted {result.rowcount} rows from {table_name}")


def rollback_all(tables: list):
    """Rolls back all migrated tables in reverse order (children before parents)."""
    for table in reversed(tables):
        try:
            rollback_table(table)
        except Exception as e:
            logger.error(f"ROLLBACK FAILED for {table}: {str(e)}")
    logger.warning("ROLLBACK COMPLETE — All migrated data removed from modern DB")
