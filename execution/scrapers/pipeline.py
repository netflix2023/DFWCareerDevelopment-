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

from execution.scrapers.models import JobPosting
from execution.scrapers.url_utils import (
    clean_canonical_url,
    detect_ats_source,
    generate_job_id,
    resolve_company_name,
    extract_requisition_id,
    sanitize_location
)
from execution.scrapers.qualification_matcher import classify_role_category, evaluate_qualification_match
from execution.scrapers.link_validator import validate_job_links_concurrently
from execution.scrapers.geo_config import check_location_match, get_target_metro
from execution.storage.database import upsert_jobs


# Primary feed endpoints for live ATS listings (verified genuine requisition sources)
FEED_URLS = [
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/README.md",
    "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/README.md"
]


def harvest_feed(feed_url: str) -> List[Dict[str, Any]]:
    """
    Harvests genuine job opportunities directly from community verified ATS tables.
    Tracks parent company name across sub-rows (↳) to ensure accurate entity mapping.
    """
    print(f"[*] Harvesting stream: {feed_url}")
    items = []
    try:
        req = urllib.request.Request(feed_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            
        trs = re.findall(r"<tr>(.*?)</tr>", content, re.DOTALL)
        last_company = ""
        for tr in trs[1:]:
            tds = re.findall(r"<td>(.*?)</td>", tr, re.DOTALL)
            if len(tds) >= 5:
                # Check company cell - inherit parent company if this is an indented sub-row
                comp_text = re.sub(r"<[^>]+>", "", tds[0]).strip()
                if "↳" in comp_text or not comp_text or comp_text == "↳":
                    company = last_company
                else:
                    comp_match = re.search(r">([^<]+)</a>", tds[0]) or re.search(r"<strong>([^<]+)</strong>", tds[0])
                    company = comp_match.group(1).strip() if comp_match else comp_text
                    last_company = company
                    
                title = re.sub(r"<[^>]+>", "", tds[1]).strip()
                loc = re.sub(r"<[^>]+>", "", tds[2]).strip()
                
                # Extract first link from application cell (points directly to ATS)
                apply_match = re.search(r'href="([^"]+)"', tds[3])
                apply_url = apply_match.group(1).strip() if apply_match else ""
                
                # Skip if no application link found
                if not apply_url:
                    continue
                    
                age_str = re.sub(r"<[^>]+>", "", tds[4]).strip()
                age_days = None
                age_num = re.search(r"(\d+)", age_str)
                if age_num:
                    age_days = int(age_num.group(1))
                    
                items.append({
                    "company": company,
                    "title": title,
                    "location": loc,
                    "raw_url": apply_url,
                    "age_days": age_days,
                    "description": f"{title} at {company} in {loc}"
                })
        print(f"[+] Successfully parsed {len(items)} genuine entries from feed.")
    except Exception as e:
        print(f"[-] Error fetching feed {feed_url}: {e}")
    return items


def run_intelligence_pipeline(max_age_days: int = 7) -> List[JobPosting]:
    """Executes the full collection, normalization, qualification matching, and deduplication pipeline."""
    print("[1/4] Collecting job opportunities from direct feeds and ATS tables...")
    raw_entries = []
    
    # Ingest from high-volume verified ATS feed streams
    for feed in FEED_URLS:
        raw_entries.extend(harvest_feed(feed))
        
    print(f"Total raw candidates collected: {len(raw_entries)}")
    
    print("[2/4] Filtering, normalizing canonical URLs, and matching candidate qualifications...")
    seen_jobs: Dict[str, JobPosting] = {}
    
    for entry in raw_entries:
        raw_url = entry.get("raw_url", "")
        if not raw_url:
            continue
            
        canonical_url = clean_canonical_url(raw_url)
        ats_source = detect_ats_source(canonical_url)
        raw_company = entry.get("company", "Unknown")
        company = resolve_company_name(raw_company, canonical_url)
        title = entry.get("title", "")
        raw_location = entry.get("location", "")
        age = entry.get("age_days")
        description = entry.get("description", "")
        
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
            
        # Geographic filtering with dynamic target metro
        is_metro, is_remote, is_state = check_location_match(raw_location)
        is_dfw = is_metro  # backwards compatibility with models
        
        # We target the active metro as priority 1, Remote US as priority 2, and State as priority 3
        if not (is_metro or is_remote or is_state):
            continue
            
        # Filter for age <= max_age_days (or recent)
        if age is not None and age > max_age_days:
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
    
    # Sort: DFW first, then by match_score descending, then by age ascending
    active_jobs.sort(key=lambda j: (j.is_dfw, j.match_score, -(j.age_days or 0)), reverse=True)
    
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
        
    output_json = os.path.join("output", "scraped_jobs", "dfw_qualifying_jobs.json")
    output_csv = os.path.join("output", "clean_csvs", "dfw_qualifying_jobs.csv")
    
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

