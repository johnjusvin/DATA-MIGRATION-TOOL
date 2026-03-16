# src/utils/progress_tracker.py

import json
import os

PROGRESS_FILE = "progress/progress.json"


def load_progress() -> dict:
    os.makedirs("progress", exist_ok=True)
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)


def save_progress(table_name: str, status: str, rows_done: int, last_batch: int):
    progress = load_progress()
    progress[table_name] = {
        "status": status,
        "rows_done": rows_done,
        "last_batch": last_batch
    }
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def is_completed(table_name: str) -> bool:
    progress = load_progress()
    return progress.get(table_name, {}).get("status") == "completed"


def get_last_batch(table_name: str) -> int:
    progress = load_progress()
    return progress.get(table_name, {}).get("last_batch", 0)
