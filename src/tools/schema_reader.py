# src/tools/schema_reader.py

from sqlalchemy import inspect, text
from crewai.tools import tool
from src.tools.db_connector import get_legacy_engine
from src.utils.config_loader import load_config
import json


def _get_quote_char() -> str:
    """Returns the appropriate identifier quote character based on the legacy DB type."""
    try:
        config = load_config()
        db_type = config.get("source", {}).get("type", "mysql")
        if db_type in ("postgresql", "mssql"):
            return '"'
        return '`'
    except Exception:
        return '`'


@tool("Read Legacy Database Schema")
def read_legacy_schema() -> str:
    """Reads the complete schema of the legacy database including all tables,
    columns, data types, primary keys, foreign keys, and nullable info."""
    engine = get_legacy_engine()
    inspector = inspect(engine)
    schema_report = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        pk = inspector.get_pk_constraint(table_name)
        fks = inspector.get_foreign_keys(table_name)

        schema_report[table_name] = {
            "columns": [
                {
                    "name": col["name"],
                    "type": str(col["type"]),
                    "nullable": col.get("nullable", True),
                    "default": str(col.get("default", "None")),
                }
                for col in columns
            ],
            "primary_keys": pk.get("constrained_columns", []),
            "foreign_keys": [
                {
                    "columns": fk["constrained_columns"],
                    "referred_table": fk["referred_table"],
                    "referred_columns": fk["referred_columns"],
                }
                for fk in fks
            ],
        }

    return json.dumps(schema_report, indent=2)


@tool("Get Table Row Counts")
def get_table_row_counts() -> str:
    """Returns the row count for every table in the legacy database."""
    engine = get_legacy_engine()
    inspector = inspect(engine)
    q = _get_quote_char()
    counts = {}

    with engine.connect() as conn:
        for table_name in inspector.get_table_names():
            result = conn.execute(text(f"SELECT COUNT(*) FROM {q}{table_name}{q}"))
            counts[table_name] = result.scalar()

    return json.dumps(counts, indent=2)
