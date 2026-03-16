# src/tools/data_extractor.py

import pandas as pd
from sqlalchemy import text
from crewai.tools import tool
from src.tools.db_connector import get_legacy_engine
from src.utils.config_loader import load_config


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


@tool("Extract Table Batch")
def extract_table_batch(table_name: str, offset: int = 0) -> str:
    """Extracts a batch of rows from a legacy database table.
    Uses the batch_size from config.yaml. Returns batch data as JSON string."""
    config = load_config()
    batch_size = config["migration"].get("batch_size", 500)
    engine = get_legacy_engine()
    q = _get_quote_char()

    query = text(f"SELECT * FROM {q}{table_name}{q} LIMIT :limit OFFSET :offset")

    with engine.connect() as conn:
        result = conn.execute(query, {"limit": batch_size, "offset": offset})
        rows = result.fetchall()
        columns = result.keys()

    if not rows:
        return f"NO_MORE_DATA: Table '{table_name}' — no rows at offset {offset}"

    df = pd.DataFrame(rows, columns=columns)
    return df.to_json(orient="records", date_format="iso")
