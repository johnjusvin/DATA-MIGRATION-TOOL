# src/api/main.py
import json
import os
import sys
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
from contextlib import asynccontextmanager
from typing import Dict, Any

from src.utils.progress_tracker import get_progress

# Add root project path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
try:
    from main import main as run_migration_script
except ImportError:
    run_migration_script = None

security = HTTPBasic()

# Setup Basic Auth from Env (Simple Security Layer for the tool management)
API_USERNAME = os.getenv("API_USERNAME", "admin")
API_PASSWORD = os.getenv("API_PASSWORD", "migrate123!")

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != API_USERNAME or credentials.password != API_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup resources on API startup
    print("MIGRATION APIs - STAGE SECURE STARTUP")
    yield

app = FastAPI(title="Data Migration Studio API", lifespan=lifespan)

@app.get("/")
def read_root(username: str = Depends(get_current_username)):
    """Health check ping, auth required."""
    return {"status": "Migration APIs are active", "user": username}

@app.get("/status")
def get_migration_status(username: str = Depends(get_current_username)) -> Dict[str, Any]:
    """Retrieve the current state of the migration via the tracker."""
    progress = get_progress()
    total_progress = sum([p['rows_done'] for p in progress.values()])
    
    return {
        "status": "Running" if len(progress) > 0 and not all(s.get("status") == "completed" for s in progress.values()) else ("Completed" if len(progress) > 0 else "Pending"),
        "total_rows_migrated": total_progress,
        "table_stats": progress
    }


def execute_migration_task():
    """Background task to run the actual Migration Crew script"""
    if run_migration_script:
        try:
            print("--- KICKING OFF ACTUAL MIGRATION JOB ---")
            run_migration_script()
            print("--- MIGRATION JOB CONCLUDED ---")
        except Exception as e:
            print(f"!!! MIGRATION JOB FAILED: {e}")
    else:
        print("!!! RUN_MIGRATION_SCRIPT NOT FOUND !!!")


@app.post("/start")
def trigger_migration(background_tasks: BackgroundTasks, username: str = Depends(get_current_username)):
    """Triggers the crewai agents process asynchronously the background."""
    background_tasks.add_task(execute_migration_task)
    return {"status": "Migration Task Started in Background", "job_id": "prod-migration-job"}
    
@app.get("/dlq/stats")
def fetch_dlq_stats(username: str = Depends(get_current_username)):
    """Fetch counts from Dead Letter Queues."""
    # Logic to aggregate .jsonl row counts from dlq/ folder
    total_failed_count = 0
    errors_by_table = {}
    
    dlq_dir = os.environ.get("MIGRATION_DLQ_DIR", "dlq")
    if os.path.exists(dlq_dir):
        for root, dirs, files in os.walk(dlq_dir):
            for file in files:
                if file.endswith("dlq.jsonl"):
                    filepath = os.path.join(root, file)
                    table_name = os.path.basename(os.path.dirname(filepath))
                    with open(filepath, 'r') as f:
                        lines = len(f.readlines())
                        total_failed_count += lines
                        errors_by_table[table_name] = errors_by_table.get(table_name, 0) + lines
                        
    return {"total_failed": total_failed_count, "breakdown": errors_by_table}
