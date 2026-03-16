# src/tools/validator_tools.py

import json
from sqlalchemy import text
from crewai.tools import tool
from src.tools.db_connector import get_legacy_engine, get_modern_engine
from src.utils.config_loader import load_config


def _get_legacy_quote() -> str:
    """Returns the appropriate identifier quote character for legacy DB."""
    try:
        config = load_config()
        db_type = config.get("source", {}).get("type", "mysql")
        if db_type in ("postgresql", "mssql"):
            return '"'
        return '`'
    except Exception:
        return '`'


def _get_modern_quote() -> str:
    """Returns the appropriate identifier quote character for modern DB."""
    try:
        config = load_config()
        db_type = config.get("target", {}).get("type", "postgresql")
        if db_type == "mysql":
            return '`'
        return '"'
    except Exception:
        return '"'


@tool("Compare Row Counts")
def compare_row_counts(legacy_table: str, modern_table: str) -> str:
    """Compares row counts between legacy and modern database tables.

    Args:
        legacy_table: Table name in the legacy database
        modern_table: Table name in the modern database

    Returns:
        Comparison result with PASS/FAIL status
    """
    try:
        legacy_engine = get_legacy_engine()
        modern_engine = get_modern_engine()
        lq = _get_legacy_quote()
        mq = _get_modern_quote()

        with legacy_engine.connect() as conn:
            legacy_count = conn.execute(
                text(f"SELECT COUNT(*) FROM {lq}{legacy_table}{lq}")
            ).scalar()

        with modern_engine.connect() as conn:
            modern_count = conn.execute(
                text(f"SELECT COUNT(*) FROM {mq}{modern_table}{mq}")
            ).scalar()

        status = "✅ PASS" if legacy_count == modern_count else "⚠️ WARN"
        return (
            f"{status}: {legacy_table} → {modern_table}\n"
            f"  Legacy rows: {legacy_count}\n"
            f"  Modern rows: {modern_count}\n"
            f"  Difference:  {modern_count - legacy_count}"
        )
    except Exception as e:
        return f"❌ FAIL: Could not compare {legacy_table} → {modern_table}: {str(e)}"


@tool("Check Null Values")
def check_null_values(table_name: str, required_columns_json: str) -> str:
    """Checks for null values in required columns of a modern database table.

    Args:
        table_name: Table name in the modern database
        required_columns_json: JSON list of column names that should not be null

    Returns:
        Null check results with PASS/FAIL per column
    """
    try:
        required_columns = json.loads(required_columns_json)
        engine = get_modern_engine()
        mq = _get_modern_quote()
        results = []

        with engine.connect() as conn:
            for col in required_columns:
                count = conn.execute(
                    text(f"SELECT COUNT(*) FROM {mq}{table_name}{mq} WHERE {mq}{col}{mq} IS NULL")
                ).scalar()

                status = "✅ PASS" if count == 0 else "❌ FAIL"
                results.append(f"  {status}: {col} — {count} nulls found")

        return f"Null check for '{table_name}':\n" + "\n".join(results)
    except Exception as e:
        return f"❌ FAIL: Null check failed for '{table_name}': {str(e)}"


@tool("Check Foreign Key Integrity")
def check_foreign_key_integrity(
    child_table: str,
    child_column: str,
    parent_table: str,
    parent_column: str
) -> str:
    """Checks that all foreign key references in the modern database are valid.

    Args:
        child_table: Table containing the foreign key
        child_column: Column with the foreign key
        parent_table: Referenced table
        parent_column: Referenced column

    Returns:
        FK integrity check result with PASS/FAIL
    """
    try:
        engine = get_modern_engine()
        mq = _get_modern_quote()
        query = text(
            f"SELECT COUNT(*) FROM {mq}{child_table}{mq} c "
            f"LEFT JOIN {mq}{parent_table}{mq} p ON c.{mq}{child_column}{mq} = p.{mq}{parent_column}{mq} "
            f"WHERE p.{mq}{parent_column}{mq} IS NULL AND c.{mq}{child_column}{mq} IS NOT NULL"
        )

        with engine.connect() as conn:
            orphan_count = conn.execute(query).scalar()

        status = "✅ PASS" if orphan_count == 0 else "❌ FAIL"
        return (
            f"{status}: FK {child_table}.{child_column} → "
            f"{parent_table}.{parent_column}\n"
            f"  Orphaned records: {orphan_count}"
        )
    except Exception as e:
        return (
            f"❌ FAIL: FK check {child_table}.{child_column} → "
            f"{parent_table}.{parent_column}: {str(e)}"
        )


@tool("Compare Sample Records")
def compare_sample_records(
    legacy_table: str,
    modern_table: str,
    column_mappings_json: str,
    sample_size: int = 10
) -> str:
    """Compares sample records between legacy and modern databases.

    Args:
        legacy_table: Source table in legacy database
        modern_table: Target table in modern database
        column_mappings_json: JSON mapping of old column names to new names
        sample_size: Number of records to sample (default 10)

    Returns:
        Comparison results showing matches and mismatches
    """
    try:
        column_mappings = json.loads(column_mappings_json)
        legacy_engine = get_legacy_engine()
        modern_engine = get_modern_engine()
        lq = _get_legacy_quote()
        mq = _get_modern_quote()

        # Use parameterized sample_size to prevent injection
        sample_size = int(sample_size)

        with legacy_engine.connect() as conn:
            legacy_result = conn.execute(
                text(f"SELECT * FROM {lq}{legacy_table}{lq} LIMIT :sz"),
                {"sz": sample_size}
            )
            legacy_rows = legacy_result.fetchall()
            legacy_cols = list(legacy_result.keys())

        with modern_engine.connect() as conn:
            modern_result = conn.execute(
                text(f"SELECT * FROM {mq}{modern_table}{mq} LIMIT :sz"),
                {"sz": sample_size}
            )
            modern_rows = modern_result.fetchall()
            modern_cols = list(modern_result.keys())

        results = []
        results.append(
            f"Sample comparison: {legacy_table} → {modern_table}"
        )
        results.append(f"  Legacy records sampled: {len(legacy_rows)}")
        results.append(f"  Modern records sampled: {len(modern_rows)}")
        results.append(f"  Legacy columns: {legacy_cols}")
        results.append(f"  Modern columns: {modern_cols}")

        if len(legacy_rows) == len(modern_rows):
            results.append("  ✅ Sample sizes match")
        else:
            results.append(
                f"  ⚠️ Sample sizes differ: {len(legacy_rows)} vs {len(modern_rows)}"
            )

        return "\n".join(results)
    except Exception as e:
        return (
            f"❌ FAIL: Sample comparison failed for "
            f"{legacy_table} → {modern_table}: {str(e)}"
        )
