"""
Automated Tech Internship Intelligence Pipeline.
Ingests direct ATS job postings (Greenhouse, Lever, Ashby, Workday),
filters for DFW / Remote roles, cleans URLs, and matches against candidate qualifications.
"""

import urllib.request
import re
import json
import csv
import os
import sys
from typing import List, Dict, Any
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from execution.prototype.scrapers.models import JobPosting
from execution.prototype.scrapers.url_utils import (
    clean_canonical_url,
    detect_ats_source,
    generate_job_id,
    resolve_company_name,
    extract_requisition_id,
    sanitize_location
)
from execution.prototype.scrapers.base_harvester import MarkdownFeedHarvester
from execution.prototype.scrapers.qualification_matcher import classify_role_category, evaluate_qualification_match
from execution.prototype.scrapers.link_validator import validate_job_links_concurrently
from execution.prototype.scrapers.geo_config import check_location_match, get_target_metro
from execution.prototype.storage.database import upsert_jobs


# Primary feed endpoints for live ATS listings (verified genuine requisition sources)
FEED_URLS = [
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2027-Internships/dev/README.md",
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md",
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/README.md",
    "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/README.md"
]


def harvest_feed(feed_url: str) -> List[Dict[str, Any]]:
    """Harvests genuine job opportunities using MarkdownFeedHarvester adapter with retry protection."""
    harvester = MarkdownFeedHarvester([feed_url])
    return harvester.harvest()


def run_intelligence_pipeline(max_age_days: int = 7) -> List[JobPosting]:
    """Executes the full collection, normalization, qualification matching, and deduplication pipeline."""
    print("[1/4] Collecting job opportunities from direct feeds and ATS tables...")
    raw_entries: List[Dict[str, Any]] = []
    
    # Ingest from high-volume verified ATS feed streams
    for feed in FEED_URLS:
        raw_entries.extend(harvest_feed(feed))
        
    print(f"Total raw candidates collected: {len(raw_entries)}")
    
    print("[2/4] Early filtering by geographic scope and posting recency...")
    seen_jobs: Dict[str, JobPosting] = {}
    
    for entry in raw_entries:
        raw_url = entry.get("raw_url", "")
        if not raw_url:
            continue
            
        # Optimization: Early Age Filter before heavy URL parsing and regex hashing
        age = entry.get("age_days")
        if age is not None and age > max_age_days:
            continue
            
        # Optimization: Early Geographic Filter (DFW / Target Metro / Remote)
        raw_location = entry.get("location", "")
        is_metro, is_remote, is_state = check_location_match(raw_location)
        if not (is_metro or is_remote or is_state):
            continue
            
        is_dfw = is_metro  # backwards compatibility with models
        
        # Clean canonical URL and detect ATS source
        canonical_url = clean_canonical_url(raw_url)
        ats_source = detect_ats_source(canonical_url)
        
        # Company name resolution
        raw_company = entry.get("company", "Unknown")
        company = resolve_company_name(raw_company, canonical_url)
        title = entry.get("title", "")
        description = entry.get("description", "")
        
        # Deterministic job ID based on company + requisition_id (or title)
        job_id = generate_job_id(company, title, canonical_url)
        
        # Deduplicate identical requisitions across internal career boards
        if job_id in seen_jobs:
            existing_job = seen_jobs[job_id]
            if canonical_url != existing_job.apply_url and canonical_url not in existing_job.alternate_urls:
                # Prefer external careers or primary boards as main URL
                if "external_careers" in canonical_url.lower() and "external_careers" not in existing_job.apply_url.lower():
                    existing_job.alternate_urls.append(existing_job.apply_url)
                    existing_job.apply_url = canonical_url
                else:
                    existing_job.alternate_urls.append(canonical_url)
            continue
            
        # Sanitize multi-location string bloat (e.g. 30 locationsRidley Park...)
        location = sanitize_location(raw_location, is_dfw=is_dfw)
            
        # Match candidate qualifications
        match_score, matched_skills, qualifies = evaluate_qualification_match(title, description)
        if not qualifies:
            continue
            
        role_category = classify_role_category(title)
        req_id = extract_requisition_id(canonical_url)
        
        posting = JobPosting(
            job_id=job_id,
            company=company,
            title=title,
            ats_source=ats_source,
            apply_url=canonical_url,
            location=location,
            role_category=role_category,
            match_score=match_score,
            matching_skills=matched_skills,
            age_days=age,
            is_dfw=is_dfw,
            is_remote=is_remote,
            requisition_id=req_id
        )
        
        seen_jobs[job_id] = posting
        
    verified_jobs = list(seen_jobs.values())
    print(f"[3/4] Filtered and scored {len(verified_jobs)} matching candidate opportunities.")
    
    print("[4/4] Validating live HTTP link health concurrently (5 worker threads)...")
    active_jobs, dead_jobs = validate_job_links_concurrently(verified_jobs, max_workers=5, timeout=5)
    
    # Sort: DFW first, then by match_score descending, then by age ascending (missing age penalized to 99)
    active_jobs.sort(
        key=lambda j: (
            j.is_dfw,
            j.match_score,
            -(j.age_days if j.age_days is not None else 99)
        ),
        reverse=True
    )
    
    print(f"[+] Verified {len(active_jobs)} LIVE, working positions ready for immediate application!")
    return active_jobs


def save_deliverables(jobs: List[JobPosting], json_path: str, csv_path: str):
    """Saves structured data outputs to JSON and CSV formats."""
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Save JSON
    data = [j.to_dict() for j in jobs]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[+] Saved structured JSON: {json_path}")
    
    # Save CSV
    if jobs:
        headers = [
            "job_id", "company", "title", "role_category", "ats_source",
            "requisition_id", "location", "is_dfw", "is_remote", "age_days",
            "match_score", "matching_skills", "apply_url", "alternate_urls", "discovered_at"
        ]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for j in jobs:
                writer.writerow([
                    j.job_id,
                    j.company,
                    j.title,
                    j.role_category,
                    j.ats_source,
                    j.requisition_id or "",
                    j.location,
                    j.is_dfw,
                    j.is_remote,
                    j.age_days if j.age_days is not None else "",
                    j.match_score,
                    "; ".join(j.matching_skills),
                    j.apply_url,
                    "; ".join(j.alternate_urls),
                    j.discovered_at
                ])
        print(f"[+] Saved clean CSV spreadsheet: {csv_path}")
        
    # Persist to local SQLite relational store (career.db)
    inserted = upsert_jobs(jobs)
    print(f"[+] Persisted {len(jobs)} records into SQLite career.db ({inserted} new positions).")




if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    output_json = os.path.join("execution", "output", "scraped_jobs", "dfw_qualifying_jobs.json")
    output_csv = os.path.join("execution", "output", "clean_csvs", "dfw_qualifying_jobs.csv")
    
    matched_jobs = run_intelligence_pipeline(max_age_days=7)
    save_deliverables(matched_jobs, output_json, output_csv)
    
    print("\n" + "="*80)
    print(f"TOP QUALIFYING POSITIONS IN DFW / REMOTE (TOTAL: {len(matched_jobs)})")
    print("="*80)
    for idx, job in enumerate(matched_jobs, 1):
        loc_badge = "[DFW METRO]" if job.is_dfw else "[REMOTE/TX]"
        print(f"{idx}. {loc_badge} {job.company} - {job.title}")
        print(f"   Category: {job.role_category} | ATS: {job.ats_source} | Score: {int(job.match_score*100)}% Match")
        print(f"   Location: {job.location} | Age: {job.age_days if job.age_days is not None else 'Active'} days ago")
        print(f"   Skills Matched: {', '.join(job.matching_skills)}")
        print(f"   Apply Link: {job.apply_url}\n")

