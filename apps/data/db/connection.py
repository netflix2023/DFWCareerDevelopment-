"""
Neon PostgreSQL direct connection client for Python ETL pipelines.
Uses DATABASE_URL_UNPOOLED for persistent TCP transactions, schema DDL, and bulk upserts.
"""

import os
import sys
from typing import Optional

try:
    import psycopg
except ImportError:
    psycopg = None


def get_direct_connection():
    """
    Returns an active direct unpooled psycopg connection.
    Targeted for Python bulk scraper ingestion and Alembic migrations.
    """
    if psycopg is None:
        raise ImportError(
            "psycopg is required for Python database operations. "
            "Install via: pip install 'psycopg[binary]'"
        )

    db_url = os.environ.get("DATABASE_URL_UNPOOLED") or os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError(
            "Missing DATABASE_URL_UNPOOLED or DATABASE_URL in environment. "
            "Please configure your Neon PostgreSQL connection string."
        )

    return psycopg.connect(db_url)
