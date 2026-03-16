# src/tools/data_loader.py

import json
import pandas as pd
from crewai.tools import tool
from src.tools.db_connector import get_modern_engine
from src.utils.progress_tracker import save_progress


@tool("Load Batch to Modern Database")
def load_batch_to_modern_db(
    target_table: str,
    batch_json: str,
    table_name: str,
    batch_number: int
) -> str:
    """Loads a transformed batch of data into the modern database.

    Args:
        target_table: Name of the target table in the modern database
        batch_json: JSON string containing the transformed data records
        table_name: Logical table name (for progress tracking)
        batch_number: Current batch number (for progress tracking)

    Returns:
        Status message indicating success or failure
    """
    try:
        data = json.loads(batch_json)
        if isinstance(data, dict) and "data" in data:
            records = data["data"]
        else:
            records = data

        if not records:
            return f"SKIP: No records to load for {target_table}"

        df = pd.DataFrame(records)
        engine = get_modern_engine()

        # Use pandas to_sql with 'append' mode for inserting data
        # if_exists='append' adds rows without dropping the table
        df.to_sql(
            target_table,
            engine,
            if_exists="append",
            index=False,
            method="multi"
        )

        rows_loaded = len(records)

        # Update progress tracker
        save_progress(
            table_name=table_name,
            status="in_progress",
            rows_done=batch_number * len(records),
            last_batch=batch_number
        )

        return f"✅ Loaded {rows_loaded} rows into '{target_table}' (batch {batch_number})"

    except Exception as e:
        return f"❌ FAILED loading batch {batch_number} into '{target_table}': {str(e)}"
