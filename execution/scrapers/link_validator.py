"""
Fast concurrent live link validator.
Checks HTTP status codes and scans for 'position closed' landing indicators
using lightweight multithreading (ThreadPoolExecutor) bounded by a 5-second timeout.
"""

import urllib.request
import urllib.error
import time
import re
from typing import Tuple, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from execution.scrapers.models import JobPosting


CLOSED_INDICATORS = [
    "no longer accepting applications",
    "job is no longer available",
    "this position has been filled",
    "this opening has been closed",
    "job not found",
    "requisition has been closed",
    "posting is inactive",
    "page not found"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}


def check_url_liveness(url: str, timeout: int = 5, retries: int = 1) -> Tuple[bool, str]:
    """
    Validates whether a target job URL is live and accepting applications.
    Performs up to 1 retry with exponential backoff on transient network drops.
    """
    if not url or not url.startswith("http"):
        return False, "Invalid URL"
        
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.getcode()
                
                # Check HTTP status
                if status in (404, 410):
                    return False, f"HTTP {status}"
                    
                # Read initial chunk of page body (up to 16KB) to inspect closure notices
                chunk = resp.read(16384).decode("utf-8", errors="ignore").lower()
                
                for indicator in CLOSED_INDICATORS:
                    if indicator in chunk:
                        return False, f"Position closed: '{indicator}' detected"
                        
                return True, "200 OK"
                
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return False, f"HTTP {e.code}"
            # Some platforms return 403 or 401 on bot inspection; if it's enterprise Workday/iCIMS, we give benefit of doubt
            if e.code in (403, 401) and ("workday" in url.lower() or "icims" in url.lower()):
                return True, f"HTTP {e.code} (Enterprise Gate)"
            if attempt < retries:
                time.sleep(2)
                continue
            return False, f"HTTP {e.code}"
            
        except (urllib.error.URLError, TimeoutError, Exception) as e:
            if attempt < retries:
                time.sleep(2)
                continue
            # Non-fatal connection timeout or drop
            return False, f"Connection error: {type(e).__name__}"
            
    return False, "Unknown Error"


def validate_job_links_concurrently(
    jobs: List[JobPosting],
    max_workers: int = 5,
    timeout: int = 5
) -> Tuple[List[JobPosting], List[Dict[str, Any]]]:
    """
    Validates a list of JobPosting objects in parallel using ThreadPoolExecutor.
    Returns (valid_jobs, dead_jobs).
    """
    valid_jobs: List[JobPosting] = []
    dead_jobs: List[Dict[str, Any]] = []
    
    print(f"[*] Validating {len(jobs)} job links concurrently with {max_workers} worker threads...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {
            executor.submit(check_url_liveness, job.apply_url, timeout): job
            for job in jobs
        }
        
        for future in as_completed(future_to_job):
            job = future_to_job[future]
            try:
                is_alive, reason = future.result()
                if is_alive:
                    valid_jobs.append(job)
                else:
                    dead_jobs.append({
                        "job_id": job.job_id,
                        "company": job.company,
                        "title": job.title,
                        "apply_url": job.apply_url,
                        "reason": reason
                    })
                    print(f"[-] Dropped dead listing: {job.company} - {job.title} ({reason})")
            except Exception as e:
                dead_jobs.append({
                    "job_id": job.job_id,
                    "company": job.company,
                    "title": job.title,
                    "apply_url": job.apply_url,
                    "reason": str(e)
                })
                
    elapsed = time.time() - start_time
    print(f"[+] Link validation complete in {elapsed:.2f}s. Active: {len(valid_jobs)}, Dropped: {len(dead_jobs)}")
    
    # Re-sort valid jobs by ranking criteria
    valid_jobs.sort(key=lambda j: (j.is_dfw, j.match_score, -(j.age_days or 0)), reverse=True)
    return valid_jobs, dead_jobs
