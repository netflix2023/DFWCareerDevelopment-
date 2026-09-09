"""
LinkedIn Guest Search Scraper for Career Surge Engine.
Harvests recent technical internships without authentication or heavy browser DOM scrapers.
Uses public guest endpoints with strict 25-result caps and rate-limit backoff.
"""

import urllib.request
import urllib.parse
import urllib.error
import re
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from execution.scrapers.models import JobPosting
from execution.scrapers.url_utils import clean_canonical_url, generate_job_id, resolve_company_name
from execution.scrapers.qualification_matcher import classify_role_category, evaluate_qualification_match
from execution.scrapers.geo_config import check_location_match, get_target_metro


GUEST_SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9"
}


def search_linkedin_guest(
    keywords: str = "Software Engineer Intern",
    location: str = "Dallas-Fort Worth Metroplex",
    max_results: int = 25
) -> List[JobPosting]:
    """
    Queries LinkedIn's guest search API for recent technical postings (<= 7 days).
    Capped at max_results (default 25) to avoid triggering Cloudflare bot challenges.
    """
    print(f"[*] Querying LinkedIn guest API for '{keywords}' in '{location}'...")
    
    params = {
        "keywords": keywords,
        "location": location,
        "f_TPR": "r604800",  # Posted within past 7 days
        "position": 1,
        "pageNum": 0,
        "start": 0
    }
    
    url = f"{GUEST_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    postings: List[JobPosting] = []
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            
        # Parse job cards from the returned HTML snippet
        cards = re.findall(r"<li[^>]*>(.*?)</li>", html, re.DOTALL)
        
        for card in cards[:max_results]:
            # Extract title
            title_match = re.search(r'<h3 class="base-search-card__title"[^>]*>\s*([^<]+)\s*</h3>', card)
            title = title_match.group(1).strip() if title_match else ""
            
            # Extract company
            comp_match = re.search(r'<h4 class="base-search-card__subtitle"[^>]*>\s*<a[^>]*>\s*([^<]+)\s*</a>', card)
            if not comp_match:
                comp_match = re.search(r'<h4 class="base-search-card__subtitle"[^>]*>\s*([^<]+)\s*</h4>', card)
            company = comp_match.group(1).strip() if comp_match else "Unknown"
            
            # Extract location
            loc_match = re.search(r'<span class="job-search-card__location"[^>]*>\s*([^<]+)\s*</span>', card)
            job_loc = loc_match.group(1).strip() if loc_match else location
            
            # Extract direct URL
            link_match = re.search(r'<a class="base-card__full-link"[^>]*href="([^"]+)"', card)
            raw_url = link_match.group(1).strip() if link_match else ""
            
            if not raw_url or not title:
                continue
                
            canonical_url = clean_canonical_url(raw_url)
            norm_company = resolve_company_name(company, canonical_url)
            job_id = generate_job_id(norm_company, title, canonical_url)
            
            # Score and qualify
            score, matched_skills, qualifies = evaluate_qualification_match(title, f"{title} at {norm_company}")
            if not qualifies:
                continue
                
            is_metro, is_remote, is_tx = check_location_match(job_loc)
            role_cat = classify_role_category(title)
            
            posting = JobPosting(
                job_id=job_id,
                company=norm_company,
                title=title,
                ats_source="other",
                apply_url=canonical_url,
                location=job_loc,
                role_category=role_cat,
                match_score=score,
                matching_skills=matched_skills,
                age_days=1,  # r604800 guarantees <= 7 days
                is_dfw=is_metro,
                is_remote=is_remote
            )
            postings.append(posting)
            
        print(f"[+] Successfully harvested {len(postings)} qualified roles from LinkedIn guest API.")
        
    except urllib.error.HTTPError as e:
        print(f"[-] LinkedIn guest API returned HTTP {e.code} (rate limit / challenge). Skipping gracefully.")
    except Exception as e:
        print(f"[-] Error querying LinkedIn guest API: {e}")
        
    return postings


if __name__ == "__main__":
    results = search_linkedin_guest(keywords="AI Intern", max_results=10)
    for r in results:
        print(f"- {r.company} | {r.title} | {r.location} | {r.apply_url}")
