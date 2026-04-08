# src/utils/audit.py
import json
import os
from datetime import datetime
from sqlalchemy import text
from src.tools.db_connector import get_modern_engine

class AuditLogger:
    """Manages immutable audit logging for the migration directly into the target database."""
    
    def __init__(self, table_name="migration_audit_log"):
        self.table_name = table_name
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        engine = get_modern_engine()
        # Ensure target database supports this syntax, otherwise adjust for dialects
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            action VARCHAR(50),
            table_name VARCHAR(100),
            records_affected INT,
            details TEXT,
            status VARCHAR(20)
        )
        """
        try:
            with engine.connect() as conn:
                # SQLAlchemy text wrapper
                conn.execute(text(query))
                conn.commit()
        except Exception as e:
            # Fallback for systems lacking SERIAL or IF NOT EXISTS (e.g. simple SQLite)
            pass

    def log(self, action: str, table_name: str, records_affected: int, status: str, details: dict = None):
        """Insert a tamper-evident log row into the target audit table."""
        engine = get_modern_engine()
        details_str = json.dumps(details) if details else "{}"
        
        # Simple parameterization
        query = text(f"""
            INSERT INTO {self.table_name} (action, table_name, records_affected, details, status)
            VALUES (:action, :table_name, :records, :details, :status)
        """)
        
        try:
            with engine.connect() as conn:
                conn.execute(query, {
                    "action": action, 
                    "table_name": table_name, 
                    "records": records_affected, 
                    "details": details_str, 
                    "status": status
                })
                conn.commit()
        except Exception as e:
            print(f"Failed to write audit log: {e}")

