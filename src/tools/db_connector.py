# src/tools/db_connector.py

from sqlalchemy import create_engine, text
from crewai.tools import tool
import os


def get_connection_string(db_type, host, port, dbname, user, password):
    """Builds the correct connection string for any database type."""
    connectors = {
        "mysql":      f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}",
        "postgresql": f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}",
        "sqlite":     f"sqlite:///{dbname}",
        "mssql":      f"mssql+pyodbc://{user}:{password}@{host}:{port}/{dbname}",
    }
    if db_type not in connectors:
        raise ValueError(f"Unsupported database type: {db_type}")
    return connectors[db_type]


def get_legacy_engine():
    conn_str = get_connection_string(
        os.getenv("LEGACY_DB_TYPE"),
        os.getenv("LEGACY_DB_HOST"),
        os.getenv("LEGACY_DB_PORT"),
        os.getenv("LEGACY_DB_NAME"),
        os.getenv("LEGACY_DB_USER"),
        os.getenv("LEGACY_DB_PASSWORD"),
    )
    return create_engine(conn_str)


def get_modern_engine():
    conn_str = get_connection_string(
        os.getenv("MODERN_DB_TYPE"),
        os.getenv("MODERN_DB_HOST"),
        os.getenv("MODERN_DB_PORT"),
        os.getenv("MODERN_DB_NAME"),
        os.getenv("MODERN_DB_USER"),
        os.getenv("MODERN_DB_PASSWORD"),
    )
    return create_engine(conn_str)


def test_db_connections() -> str:
    """Tests connectivity to both legacy and modern databases.
    This is a plain function callable from main.py."""
    results = []
    try:
        engine = get_legacy_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        results.append("✅ Legacy DB connection: SUCCESS")
    except Exception as e:
        results.append(f"❌ Legacy DB connection: FAILED — {str(e)}")

    try:
        engine = get_modern_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        results.append("✅ Modern DB connection: SUCCESS")
    except Exception as e:
        results.append(f"❌ Modern DB connection: FAILED — {str(e)}")

    return "\n".join(results)


@tool("Test Database Connections")
def test_connections() -> str:
    """Tests connectivity to both legacy and modern databases."""
    return test_db_connections()
