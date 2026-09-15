"""
Direct ATS Job Loader for Neon Serverless PostgreSQL.
Loads canonical scraped jobs into the Neon database using unpooled psycopg.
"""

import os
import json
from typing import List, Dict, Any
from datetime import datetime

try:
    import psycopg
    from psycopg.types.json import Jsonb
except ImportError:
    psycopg = None
    Jsonb = None


def upsert_jobs_to_neon(jobs: List[Dict[str, Any]]) -> int:
    """
    Upserts a list of normalized job dictionaries into Neon PostgreSQL.
    Returns the count of successfully upserted jobs.
    """
    if psycopg is None:
        raise ImportError(
            "psycopg is required for Neon PostgreSQL operations. "
            "Install with: pip install 'psycopg[binary]'"
        )

    db_url = os.environ.get("DATABASE_URL_UNPOOLED") or os.environ.get("DATABASE_URL")
    if not db_url:
        print("[Warning] No DATABASE_URL_UNPOOLED configured; skipping Neon direct sync.")
        return 0

    upsert_sql = """
    INSERT INTO jobs (
        id, company, title, location, is_dfw, is_remote, apply_url,
        alternate_urls, role_category, match_score, matched_keywords,
        missing_keywords, age_days, source, requisition_id, updated_at
    ) VALUES (
        %(id)s, %(company)s, %(title)s, %(location)s, %(is_dfw)s, %(is_remote)s, %(apply_url)s,
        %(alternate_urls)s, %(role_category)s, %(match_score)s, %(matched_keywords)s,
        %(missing_keywords)s, %(age_days)s, %(source)s, %(requisition_id)s, CURRENT_TIMESTAMP
    )
    ON CONFLICT (id) DO UPDATE SET
        apply_url = EXCLUDED.apply_url,
        alternate_urls = EXCLUDED.alternate_urls,
        match_score = EXCLUDED.match_score,
        matched_keywords = EXCLUDED.matched_keywords,
        missing_keywords = EXCLUDED.missing_keywords,
        age_days = EXCLUDED.age_days,
        updated_at = CURRENT_TIMESTAMP;
    """

    upserted_count = 0
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            for job in jobs:
                params = {
                    "id": job.get("id"),
                    "company": job.get("company"),
                    "title": job.get("title"),
                    "location": job.get("location"),
                    "is_dfw": bool(job.get("is_dfw")),
                    "is_remote": bool(job.get("is_remote")),
                    "apply_url": job.get("apply_url"),
                    "alternate_urls": Jsonb(job.get("alternate_urls", [])),
                    "role_category": job.get("role_category", "General"),
                    "match_score": float(job.get("match_score", 0.0)),
                    "matched_keywords": Jsonb(job.get("matched_keywords", [])),
                    "missing_keywords": Jsonb(job.get("missing_keywords", [])),
                    "age_days": job.get("age_days"),
                    "source": job.get("source", "Direct ATS"),
                    "requisition_id": job.get("requisition_id")
                }
                cur.execute(upsert_sql, params)
                upserted_count += 1
            conn.commit()

    return upserted_count
