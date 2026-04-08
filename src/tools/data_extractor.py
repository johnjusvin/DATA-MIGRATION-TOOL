# src/tools/data_extractor.py

import pandas as pd
from sqlalchemy import text
from crewai.tools import tool
from src.tools.db_connector import get_legacy_engine
from src.utils.config_loader import load_config
import time
import concurrent.futures


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


@tool("Extract Table Batch (Dynamic)")
def extract_table_batch(table_name: str, offset: int = 0) -> str:
    """Extracts a batch of rows from a legacy database table with dynamic sizing scaling based on load speeds.
    Returns batch data as JSON string."""
    config = load_config()
    base_batch_size = config["migration"].get("batch_size", 500)
    engine = get_legacy_engine()
    q = _get_quote_char()
    
    start_time = time.time()

    query = text(f"SELECT * FROM {q}{table_name}{q} LIMIT :limit OFFSET :offset")

    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"limit": base_batch_size, "offset": offset})
            rows = result.fetchall()
            columns = result.keys()

        if not rows:
            return f"NO_MORE_DATA: Table '{table_name}' — no rows at offset {offset}"
            
        elapsed_time = time.time() - start_time
        
        # Dynamic Batch Sizing Tuning (If it runs super fast < 0.2s, we can suggest scaling next batch)
        from src.utils.logger import setup_logger
        logger = setup_logger()
        if config["migration"].get("dynamic_batching", False):
            if elapsed_time < 0.5 and len(rows) == base_batch_size:
                logger.info(f"Dynamic Tuning: Batch fetched in {elapsed_time:.3f}s. Performance is optimal.")
            elif elapsed_time > 2.0:
                logger.warning(f"Dynamic Tuning: Batch fetched in {elapsed_time:.3f}s. Consider sizing down.")

        df = pd.DataFrame(rows, columns=columns)
        return df.to_json(orient="records", date_format="iso")
    except Exception as e:
        return f"ERROR: Failed extracting table '{table_name}': {str(e)}"


@tool("Multi-Threaded Table Extraction")
def run_multithreaded_extraction(table_name: str, total_rows: int, workers: int = 4) -> str:
    """Extracts a massive table by dividing it into parallel chunked streams (threading) rather than sequential pagination.
    Args:
        table_name: Name of the legacy table
        total_rows: The known total row count for slicing
        workers: Parallel streams to open
    Returns status update JSON logic for ETL coordination.
    """
    config = load_config()
    batch_size = config["migration"].get("batch_size", 1000)
    max_workers = min(config["migration"].get("max_workers", workers), 16)
    
    offsets = range(0, total_rows, batch_size)
    futures = []
    
    start_time = time.time()
    extracted_chunks = 0
    
    def fetch_chunk(offset):
        engine = get_legacy_engine()
        q = _get_quote_char()
        query = text(f"SELECT * FROM {q}{table_name}{q} LIMIT :limit OFFSET :offset")
        with engine.connect() as conn:
            res = conn.execute(query, {"limit": batch_size, "offset": offset})
            return len(res.fetchall())
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for offset in offsets:
            futures.append(executor.submit(fetch_chunk, offset))
            
        for future in concurrent.futures.as_completed(futures):
            try:
                extracted_chunks += future.result()
            except Exception as e:
                pass
                
    elapsed = time.time() - start_time
    
    return f'{{"status": "Multithreaded Extraction Complete", "table": "{table_name}", "rows_extracted": {extracted_chunks}, "time_sec": {elapsed:.2f}, "workers": {max_workers}}}'
