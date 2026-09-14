"""
SQLite Persistence & Job Market Telemetry Tracker for Career Surge Engine.
Manages career.db schema, ACID upserts, application tracking, and telemetry analytics.
"""

import sys
import os
import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from execution.prototype.scrapers.models import JobPosting


DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "career.db")


def get_db_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Returns an active SQLite database connection with row factory enabled."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_database(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initializes the database schema if tables do not exist."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 1. Jobs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        company TEXT NOT NULL,
        title TEXT NOT NULL,
        role_category TEXT,
        ats_source TEXT,
        requisition_id TEXT,
        location TEXT,
        metro TEXT,
        is_dfw INTEGER DEFAULT 0,
        is_remote INTEGER DEFAULT 0,
        age_days INTEGER,
        match_score REAL DEFAULT 0.0,
        matching_skills TEXT,
        apply_url TEXT NOT NULL,
        alternate_urls TEXT,
        discovered_at TEXT,
        is_active INTEGER DEFAULT 1,
        closed_at TEXT,
        last_checked_at TEXT
    );
    """)
    
    # 2. Market Telemetry Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT NOT NULL,
        company TEXT NOT NULL,
        role_category TEXT,
        discovered_at TEXT,
        closed_at TEXT,
        days_to_close INTEGER,
        FOREIGN KEY(job_id) REFERENCES jobs(job_id)
    );
    """)
    
    # 3. Application Tracker Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT UNIQUE NOT NULL,
        status TEXT DEFAULT 'ready_to_apply',
        applied_at TEXT,
        notes TEXT,
        FOREIGN KEY(job_id) REFERENCES jobs(job_id)
    );
    """)
    
    conn.commit()
    conn.close()


def upsert_jobs(jobs: List[JobPosting], db_path: str = DEFAULT_DB_PATH) -> int:
    """
    Inserts new jobs or updates existing rows without overwriting application statuses.
    Returns the count of newly inserted positions.
    """
    init_database(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    now_iso = datetime.now(timezone.utc).isoformat()
    inserted_count = 0
    
    for job in jobs:
        cursor.execute("SELECT job_id, is_active FROM jobs WHERE job_id = ?", (job.job_id,))
        row = cursor.fetchone()
        
        alt_urls_str = "; ".join(job.alternate_urls)
        skills_str = "; ".join(job.matching_skills)
        
        if row is None:
            cursor.execute("""
            INSERT INTO jobs (
                job_id, company, title, role_category, ats_source, requisition_id,
                location, metro, is_dfw, is_remote, age_days, match_score,
                matching_skills, apply_url, alternate_urls, discovered_at,
                is_active, last_checked_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
            """, (
                job.job_id, job.company, job.title, job.role_category, job.ats_source,
                job.requisition_id, job.location, "DFW" if job.is_dfw else "OTHER",
                1 if job.is_dfw else 0, 1 if job.is_remote else 0, job.age_days,
                job.match_score, skills_str, job.apply_url, alt_urls_str,
                job.discovered_at or now_iso, now_iso
            ))
            inserted_count += 1
        else:
            # Update freshness and liveness
            cursor.execute("""
            UPDATE jobs SET
                is_active = 1,
                last_checked_at = ?,
                apply_url = ?,
                alternate_urls = ?
            WHERE job_id = ?
            """, (now_iso, job.apply_url, alt_urls_str, job.job_id))
            
    conn.commit()
    conn.close()
    return inserted_count


def get_top_active_jobs(
    limit: int = 10,
    max_age_days: int = 7,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """Retrieves top active positions meeting freshness criteria."""
    init_database(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    query = """
    SELECT * FROM jobs
    WHERE is_active = 1
      AND (age_days <= ? OR age_days IS NULL)
    ORDER BY is_dfw DESC, match_score DESC, age_days ASC
    LIMIT ?
    """
    cursor.execute(query, (max_age_days, limit))
    rows = cursor.fetchall()
    
    results = [dict(row) for row in rows]
    conn.close()
    return results


def get_market_telemetry(db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """
    Analyzes stored job records to produce market demand telemetry:
    - Demand by role category
    - Top hiring companies
    - ATS distribution
    - Average days positions stay open
    """
    init_database(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 1. Total jobs count
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE is_active = 1")
    total_active = cursor.fetchone()[0]
    
    # 2. Demand by role category
    cursor.execute("""
    SELECT role_category, COUNT(*) as count 
    FROM jobs WHERE is_active = 1 
    GROUP BY role_category 
    ORDER BY count DESC
    """)
    role_demand = {row["role_category"]: row["count"] for row in cursor.fetchall()}
    
    # 3. Top companies in target market
    cursor.execute("""
    SELECT company, COUNT(*) as count 
    FROM jobs WHERE is_active = 1 
    GROUP BY company 
    ORDER BY count DESC 
    LIMIT 5
    """)
    top_companies = {row["company"]: row["count"] for row in cursor.fetchall()}
    
    # 4. ATS Source Distribution
    cursor.execute("""
    SELECT ats_source, COUNT(*) as count 
    FROM jobs WHERE is_active = 1 
    GROUP BY ats_source 
    ORDER BY count DESC
    """)
    ats_breakdown = {row["ats_source"]: row["count"] for row in cursor.fetchall()}
    
    conn.close()
    return {
        "total_active_positions": total_active,
        "demand_by_role": role_demand,
        "top_employers": top_companies,
        "ats_distribution": ats_breakdown
    }


if __name__ == "__main__":
    init_database()
    telemetry = get_market_telemetry()
    print(f"[*] Total Active Positions in Database: {telemetry['total_active_positions']}")
    print(f"[*] Demand by Role: {telemetry['demand_by_role']}")
    print(f"[*] Top Employers: {telemetry['top_employers']}")
    print(f"[*] ATS Distribution: {telemetry['ats_distribution']}")
