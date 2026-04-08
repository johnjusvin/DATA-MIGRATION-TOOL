# src/tools/data_loader.py

import json
import pandas as pd
from sqlalchemy import text, Table, MetaData, select, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.mysql import insert as mysql_insert
from crewai.tools import tool
from src.tools.db_connector import get_modern_engine
from src.utils.progress_tracker import save_progress
from src.utils.logger import setup_logger
from src.utils.audit import AuditLogger
import logging

logger = setup_logger()


@tool("Load Batch to Modern Database")
def load_batch_to_modern_db(
    target_table: str,
    batch_json: str,
    table_name: str,
    batch_number: int
) -> str:
    """Loads a transformed batch of data into the modern database with upsert capability.

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

        # Get database type for proper upsert implementation
        from src.utils.config_loader import load_config
        import os
        config = load_config()
        db_type = config.get("target", {}).get("type", "postgresql").lower()

        # Use upsert (INSERT ... ON CONFLICT DO UPDATE) for PostgreSQL
        # or (INSERT ... ON DUPLICATE KEY UPDATE) for MySQL
        with engine.begin() as conn:
            # Get table metadata
            metadata = MetaData()
            table = Table(target_table, metadata, autoload_with=engine)
            
            # Prepare data for bulk insert
            data_to_insert = df.to_dict(orient='records')
            
            if db_type == "postgresql":
                # PostgreSQL upsert
                stmt = pg_insert(table).values(data_to_insert)
                pk_columns = [col.name for col in table.primary_key.columns]
                if pk_columns:
                    update_dict = {col.name: stmt.excluded[col.name] 
                                 for col in table.columns 
                                 if col.name not in pk_columns}
                    stmt = stmt.on_conflict_do_update(
                        index_elements=pk_columns,
                        set_=update_dict
                    )
                else:
                    stmt = insert(table).values(data_to_insert)
                
                try:
                    result = conn.execute(stmt)
                except Exception as pg_err:
                    from src.utils.dlq import DeadLetterQueue
                    dlq = DeadLetterQueue()
                    logger.warning(f"Batch upsert failed for PostgreSQL: {pg_err}. Failing over to row-by-row insert.")
                    inserted_count = 0
                    for record in data_to_insert:
                        try:
                            with conn.begin_nested():
                                single_stmt = pg_insert(table).values(record)
                                if pk_columns:
                                    single_update = {col.name: single_stmt.excluded[col.name] 
                                                   for col in table.columns if col.name not in pk_columns}
                                    single_stmt = single_stmt.on_conflict_do_update(
                                        index_elements=pk_columns, set_=single_update
                                    )
                                else:
                                    single_stmt = insert(table).values(record)
                                conn.execute(single_stmt)
                                inserted_count += 1
                        except Exception as row_error:
                            dlq.log_failure("load_postgres", target_table, record, str(row_error))
                    
                    audit = AuditLogger()
                    audit.log("BATCH_LOAD_FALLBACK", target_table, inserted_count, "PARTIAL_SUCCESS", {"batch_number": batch_number, "failed_count": len(data_to_insert) - inserted_count, "error": str(pg_err)})
                    return f"⚠️ Loaded {inserted_count}/{len(data_to_insert)} rows into '{target_table}' (batch {batch_number}) via fallback."
                
            elif db_type == "mysql":
                # MySQL upsert
                stmt = mysql_insert(table).values(data_to_insert)
                pk_columns = [col.name for col in table.primary_key.columns]
                if pk_columns:
                    update_dict = {col.name: stmt.inserted[col.name] 
                                 for col in table.columns 
                                 if col.name not in pk_columns}
                    stmt = stmt.on_duplicate_key_update(update_dict)
                else:
                    stmt = insert(table).values(data_to_insert)
                
                try:
                    result = conn.execute(stmt)
                except Exception as mysql_err:
                    from src.utils.dlq import DeadLetterQueue
                    dlq = DeadLetterQueue()
                    logger.warning(f"Batch upsert failed for MySQL: {mysql_err}. Failing over to row-by-row insert.")
                    inserted_count = 0
                    for record in data_to_insert:
                        try:
                            with conn.begin_nested():
                                single_stmt = mysql_insert(table).values(record)
                                if pk_columns:
                                    single_update = {col.name: single_stmt.inserted[col.name] 
                                                   for col in table.columns if col.name not in pk_columns}
                                    single_stmt = single_stmt.on_duplicate_key_update(single_update)
                                else:
                                    single_stmt = insert(table).values(record)
                                conn.execute(single_stmt)
                                inserted_count += 1
                        except Exception as row_error:
                            dlq.log_failure("load_mysql", target_table, record, str(row_error))
                            
                    audit = AuditLogger()
                    audit.log("BATCH_LOAD_FALLBACK", target_table, inserted_count, "PARTIAL_SUCCESS", {"batch_number": batch_number, "failed_count": len(data_to_insert) - inserted_count, "error": str(mysql_err)})
                    return f"⚠️ Loaded {inserted_count}/{len(data_to_insert)} rows into '{target_table}' (batch {batch_number}) via fallback."

                
            else:
                # For other databases, use regular insert with error handling
                try:
                    df.to_sql(
                        target_table,
                        engine,
                        if_exists="append",
                        index=False,
                        method="multi"
                    )
                    result = None  # to_sql doesn't return result easily
                except Exception as insert_error:
                    from src.utils.dlq import DeadLetterQueue
                    dlq = DeadLetterQueue()
                    logger.warning(f"Insert error (might be duplicate or invalid data): {insert_error}")
                    # Try one by one insert to log specifically which row failed
                    inserted_count = 0
                    for record in data_to_insert:
                        try:
                            # Create a savepoint if the DB driver supports it
                            try:
                                with conn.begin_nested():
                                    stmt = insert(table).values(record)
                                    conn.execute(stmt)
                                    inserted_count += 1
                            except Exception:
                                # Fallback if nested transactions aren't supported
                                stmt = insert(table).values(record)
                                conn.execute(stmt)
                                inserted_count += 1
                        except Exception as row_error:
                            dlq.log_failure("load", target_table, record, str(row_error))
                            continue
                            
                    audit = AuditLogger()
                    audit.log("BATCH_LOAD_FALLBACK", target_table, inserted_count, "PARTIAL_SUCCESS", {"batch_number": batch_number, "failed_count": len(data_to_insert) - inserted_count, "error": str(insert_error)})
                    return f"⚠️ Loaded {inserted_count}/{len(data_to_insert)} rows into '{target_table}' (batch {batch_number}) - check DLQ for failed rows"

            # Update progress tracker
            rows_loaded = len(data_to_insert) if result is None else getattr(result, 'rowcount', len(data_to_insert))
            save_progress(
                table_name=table_name,
                status="in_progress",
                rows_done=batch_number * len(records),
                last_batch=batch_number
            )
            
            # Log successful completion to the Audit Table
            audit = AuditLogger()
            audit.log("BATCH_LOAD", target_table, rows_loaded, "SUCCESS", {"batch_number": batch_number})

            return f"✅ Upserted {rows_loaded} rows into '{target_table}' (batch {batch_number})"

    except Exception as e:
        from src.utils.dlq import DeadLetterQueue
        dlq = DeadLetterQueue()
        logger.error(f"Error loading batch {batch_number} into '{target_table}': {str(e)}")
        
        # Log failure to the Audit Table
        audit = AuditLogger()
        audit.log("BATCH_LOAD_FATAL", target_table, 0, "FAILED", {"batch_number": batch_number, "error": str(e)})

        # Log all records in this batch to the DLQ since the whole batch failed unexpectedly
        if 'records' in locals():
            for record in records:
                 dlq.log_failure("load_batch_fatal", target_table, record, str(e))
                 
        return f"❌ FAILED loading batch {batch_number} into '{target_table}' (saved to DLQ): {str(e)}"

