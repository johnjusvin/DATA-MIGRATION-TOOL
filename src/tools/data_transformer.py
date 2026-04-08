# src/tools/data_transformer.py

import json
import hashlib
import re
from datetime import datetime
import base64
from crewai.tools import tool
from src.utils.dlq import DeadLetterQueue


def apply_transformation(value, rule: str, context_data: dict = None):
    """Applies a single transformation rule to a value."""
    if value is None:
        if rule.startswith("default:"):
            return rule.split(":", 1)[1]
        return None

    if rule == "cast_to_int":
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    elif rule == "cast_to_decimal":
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    elif rule == "title_case":
        return str(value).strip().title()
        
    elif rule == "lower_case":
        return str(value).strip().lower()

    elif rule == "mask_pii":
        return "*" * len(str(value))

    elif rule == "hash_sha256":
        return hashlib.sha256(str(value).encode('utf-8')).hexdigest()
        
    elif rule == "encrypt_b64":
        return base64.b64encode(str(value).encode('utf-8')).decode('utf-8')

    elif rule.startswith("lookup:"):
        # e.g., "lookup:customer_data" looks into injected context
        lookup_table = rule.split(":", 1)[1]
        if context_data and lookup_table in context_data:
            return context_data[lookup_table].get(str(value), value)
        return value

    elif rule.startswith("regex_extract:"):
        pattern = rule.split(":", 1)[1]
        match = re.search(pattern, str(value))
        return match.group(1) if match else value

    elif rule == "parse_date_YYYYMMDD":
        try:
            if isinstance(value, str):
                value = value.strip().replace("-", "").replace("/", "")
                return datetime.strptime(value[:8], "%Y%m%d").strftime("%Y-%m-%d")
            return str(value)
        except (ValueError, TypeError):
            return None

    elif rule.startswith("map_values:"):
        mapping_str = rule.split(":", 1)[1]
        mapping = {}
        for pair in mapping_str.split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                # Convert string booleans
                if v.lower() == "true":
                    v = True
                elif v.lower() == "false":
                    v = False
                mapping[k.strip()] = v
        return mapping.get(str(value).strip(), value)
        
    elif rule.startswith("default:"):
        return value

    else:
        return value


@tool("Transform Data Batch")
def transform_batch(batch_json: str, column_mappings_json: str, transformations_json: str, context_json: str = "{}", table_name: str = "unknown") -> str:
    """Transforms a batch of data by renaming columns and applying transformation rules, including complex lookups/joins.

    Args:
        batch_json: JSON string of the data batch (list of records)
        column_mappings_json: JSON string mapping old column names to new names
        transformations_json: JSON string mapping old column names to transformation rules
        context_json: JSON string containing reference data for lookups (acts like JOIN dictionary)
        table_name: Optional table name for logging purposes

    Returns:
        Transformed data batch as a JSON string
    """
    records = json.loads(batch_json)
    column_mappings = json.loads(column_mappings_json)
    transformations = json.loads(transformations_json)
    context_data = json.loads(context_json)
    
    dlq = DeadLetterQueue()

    transformed = []
    errors = []

    for i, record in enumerate(records):
        new_record = {}
        try:
            for old_col, new_col in column_mappings.items():
                value = record.get(old_col)

                # Apply transformation if one exists for this column
                if old_col in transformations:
                    value = apply_transformation(value, transformations[old_col], context_data)

                new_record[new_col] = value

            transformed.append(new_record)
        except Exception as e:
            error_msg = f"Row {i} ({old_col}): {str(e)}"
            errors.append(error_msg)
            dlq.log_failure("transformation", table_name, dict(record), error_msg)

    result = {
        "data": transformed,
        "total_transformed": len(transformed),
        "total_errors": len(errors),
        "errors": errors
    }
    return json.dumps(result, default=str)


