# tests/test_transformer.py
import pytest
import json
from src.tools.data_transformer import apply_transformation, transform_batch

def test_apply_transformation_basic():
    # Test casting
    assert apply_transformation("123.4", "cast_to_int") == 123
    assert apply_transformation("invalid", "cast_to_int") is None
    
    # Test title_case
    assert apply_transformation(" john doe ", "title_case") == "John Doe"
    
    # Test Date Parsing
    assert apply_transformation("2026-04-08", "parse_date_YYYYMMDD") == "2026-04-08"
    assert apply_transformation("20260408", "parse_date_YYYYMMDD") == "2026-04-08"

def test_apply_transformation_complex():
    # Test Mapping
    assert apply_transformation("A", "map_values:A=True,B=False") is True
    assert apply_transformation("B", "map_values:A=True,B=False") is False
    assert apply_transformation("C", "map_values:A=True,B=False") == "C" 
    
    # Test Regex Extraction
    assert apply_transformation("Invoice: INV-9990", "regex_extract:INV-(\\d+)") == "9990"
    
    # Test PII Masking
    assert apply_transformation("sensitive_data", "mask_pii") == "*************"

def test_transform_batch_function():
    batch_data = [{"legacy_id": "1", "name": "alice "}]
    col_mappings = {"legacy_id": "id", "name": "user_name"}
    transformations = {"legacy_id": "cast_to_int", "name": "title_case"}
    
    result_str = transform_batch(
        json.dumps(batch_data),
        json.dumps(col_mappings),
        json.dumps(transformations)
    )
    result = json.loads(result_str)
    
    assert result["total_transformed"] == 1
    assert result["total_errors"] == 0
    assert result["data"][0] == {"id": 1, "user_name": "Alice"}
