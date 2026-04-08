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

@tool("Detect Schema Drift")
def detect_schema_drift(baseline_schema_json: str) -> str:
    """Compares a previously recorded legacy schema against the live legacy database to detect mid-migration dropped/added columns.
    
    Args:
        baseline_schema_json: JSON string of the older schema
        
    Returns:
        JSON string containing the drift alert or indicating 'no_drift'
    """
    if not baseline_schema_json or baseline_schema_json.strip() == "{}":
        return json.dumps({"status": "error", "message": "No baseline schema provided"})
        
    baseline = json.loads(baseline_schema_json)
    live_schema_str = read_legacy_schema.func() # Or directly run logic
    live = json.loads(live_schema_str)
    
    drift_report = {
        "status": "stable",
        "tables_added": [],
        "tables_dropped": [],
        "columns_added": {},
        "columns_dropped": {}
    }
    
    # Check tables
    baseline_tables = set(baseline.keys())
    live_tables = set(live.keys())
    
    drift_report["tables_added"] = list(live_tables - baseline_tables)
    drift_report["tables_dropped"] = list(baseline_tables - live_tables)
    
    # Check columns for common tables
    for table in baseline_tables.intersection(live_tables):
        base_cols = {col["name"]: col["type"] for col in baseline[table]["columns"]}
        live_cols = {col["name"]: col["type"] for col in live[table]["columns"]}
        
        added_cols = list(set(live_cols.keys()) - set(base_cols.keys()))
        dropped_cols = list(set(base_cols.keys()) - set(live_cols.keys()))
        
        if added_cols:
            drift_report["columns_added"][table] = added_cols
        if dropped_cols:
            drift_report["columns_dropped"][table] = dropped_cols
            
    # Determine if alert is needed
    if any([drift_report["tables_added"], drift_report["tables_dropped"], 
            drift_report["columns_added"], drift_report["columns_dropped"]]):
        drift_report["status"] = "DRIFT_DETECTED"
        
    return json.dumps(drift_report, indent=2)
