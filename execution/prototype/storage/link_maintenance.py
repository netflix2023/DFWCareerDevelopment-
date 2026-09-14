"""
Daily Link Maintenance & Requisition Health Checker.
Scans active jobs in career.db, validates HTTP liveness concurrently,
and marks expired/closed listings inactive while updating market telemetry.
"""

import sys
import os
import time
from datetime import datetime, timezone
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from execution.prototype.storage.database import get_db_connection, init_database, DEFAULT_DB_PATH
from execution.prototype.scrapers.link_validator import check_url_liveness
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_daily_link_maintenance(
    db_path: str = DEFAULT_DB_PATH,
    max_workers: int = 5,
    timeout: int = 5
) -> Dict[str, Any]:
    """
    Checks all active jobs in SQLite database.
    Marks closed or 404 links as is_active = 0, records closed_at,
    and calculates time-to-close telemetry.
    """
    init_database(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT job_id, company, title, role_category, apply_url, discovered_at 
    FROM jobs WHERE is_active = 1
    """)
    rows = cursor.fetchall()
    
    total_scanned = len(rows)
    print(f"[*] Starting daily link health maintenance on {total_scanned} active positions...")
    
    pruned_count = 0
    active_count = 0
    now_dt = datetime.now(timezone.utc)
    now_iso = now_dt.isoformat()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {
            executor.submit(check_url_liveness, row["apply_url"], timeout): row
            for row in rows
        }
        
        for future in as_completed(future_to_job):
            row = future_to_job[future]
            job_id = row["job_id"]
            company = row["company"]
            title = row["title"]
            
            try:
                is_alive, reason = future.result()
                if is_alive:
                    cursor.execute("UPDATE jobs SET last_checked_at = ? WHERE job_id = ?", (now_iso, job_id))
                    active_count += 1
                else:
                    # Calculate days open before closing
                    days_to_close = 1
                    try:
                        disc_dt = datetime.fromisoformat(row["discovered_at"])
                        days_to_close = max(1, (now_dt - disc_dt).days)
                    except Exception:
                        pass
                        
                    # Mark inactive
                    cursor.execute("""
                    UPDATE jobs SET 
                        is_active = 0, 
                        closed_at = ?,
                        last_checked_at = ?
                    WHERE job_id = ?
                    """, (now_iso, now_iso, job_id))
                    
                    # Record telemetry
                    cursor.execute("""
                    INSERT INTO job_telemetry (job_id, company, role_category, discovered_at, closed_at, days_to_close)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (job_id, company, row["role_category"], row["discovered_at"], now_iso, days_to_close))
                    
                    pruned_count += 1
                    print(f"[-] Pruned closed requisition: {company} - {title} ({reason})")
                    
            except Exception as e:
                print(f"[-] Error verifying {company} - {title}: {e}")
                
    conn.commit()
    conn.close()
    
    summary = {
        "timestamp": now_iso,
        "total_scanned": total_scanned,
        "active_remaining": active_count,
        "pruned_closed": pruned_count
    }
    print(f"[+] Daily link maintenance complete: {active_count} active, {pruned_count} pruned.")
    return summary


if __name__ == "__main__":
    run_daily_link_maintenance()
