# src/tools/data_profiler.py
import json
import pandas as pd
from crewai.tools import tool

@tool("Profile Data Batch")
def profile_data_batch(batch_json: str) -> str:
    """Calculates data quality scores and profiling metrics (nulls, uniqueness) for a batch of data.
    
    Args:
        batch_json: JSON string of the data batch (list of records)
        
    Returns:
        JSON string containing data profiling metrics (null counts, uniqueness, min/max).
    """
    records = json.loads(batch_json)
    if not records:
        return json.dumps({"status": "empty", "message": "No data to profile"})
        
    df = pd.DataFrame(records)
    metrics = {
        "total_rows": len(df),
        "columns": {}
    }
    
    for col in df.columns:
        col_data = df[col]
        metrics["columns"][col] = {
            "null_count": int(col_data.isnull().sum()),
            "null_percentage": round(float(col_data.isnull().sum() / len(df) * 100), 2),
            "unique_count": int(col_data.nunique()),
        }
        
        if pd.api.types.is_numeric_dtype(col_data):
            metrics["columns"][col].update({
                "min": float(col_data.min()) if not pd.isna(col_data.min()) else None,
                "max": float(col_data.max()) if not pd.isna(col_data.max()) else None,
                "mean": float(col_data.mean()) if not pd.isna(col_data.mean()) else None,
            })
            
    # Simple Data Quality Score (100 - average null percentage)
    avg_nulls = sum(c["null_percentage"] for c in metrics["columns"].values()) / len(metrics["columns"])
    metrics["data_quality_score"] = round(100 - avg_nulls, 2)
    
    return json.dumps(metrics, default=str)
