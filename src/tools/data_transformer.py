# src/tools/data_transformer.py

import json
from datetime import datetime
from crewai.tools import tool


def apply_transformation(value, rule: str):
    """Applies a single transformation rule to a value."""
    if value is None:
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
            k, v = pair.split("=")
            # Convert string booleans
            if v.lower() == "true":
                v = True
            elif v.lower() == "false":
                v = False
            mapping[k.strip()] = v
        return mapping.get(str(value).strip(), value)

    else:
        return value


@tool("Transform Data Batch")
def transform_batch(batch_json: str, column_mappings_json: str, transformations_json: str) -> str:
    """Transforms a batch of data by renaming columns and applying transformation rules.

    Args:
        batch_json: JSON string of the data batch (list of records)
        column_mappings_json: JSON string mapping old column names to new names
        transformations_json: JSON string mapping old column names to transformation rules

    Returns:
        Transformed data batch as a JSON string
    """
    records = json.loads(batch_json)
    column_mappings = json.loads(column_mappings_json)
    transformations = json.loads(transformations_json)

    transformed = []
    errors = []

    for i, record in enumerate(records):
        new_record = {}
        try:
            for old_col, new_col in column_mappings.items():
                value = record.get(old_col)

                # Apply transformation if one exists for this column
                if old_col in transformations:
                    value = apply_transformation(value, transformations[old_col])

                new_record[new_col] = value

            transformed.append(new_record)
        except Exception as e:
            errors.append(f"Row {i}: {str(e)}")

    result = {
        "data": transformed,
        "total_transformed": len(transformed),
        "total_errors": len(errors),
        "errors": errors
    }
    return json.dumps(result, default=str)
