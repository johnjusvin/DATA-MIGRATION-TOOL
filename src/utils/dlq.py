import os
import json
import csv
from datetime import datetime
from threading import Lock

class DeadLetterQueue:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DeadLetterQueue, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, dlq_dir="dlq"):
        if self._initialized: return
        self.dlq_dir = dlq_dir
        os.makedirs(self.dlq_dir, exist_ok=True)
        self._initialized = True
        
    def log_failure(self, step: str, table_name: str, record: dict, error_message: str):
        """Log a failed record to the Dead Letter Queue."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        date_str = datetime.now().strftime('%Y%m%d')
        
        # Structure by step and table
        table_dir = os.path.join(self.dlq_dir, step, table_name)
        os.makedirs(table_dir, exist_ok=True)
        
        filename = os.path.join(table_dir, f"{date_str}_dlq.jsonl")
        
        dlq_entry = {
            "timestamp": timestamp,
            "error": error_message,
            "record": record
        }
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(dlq_entry) + '\n')
