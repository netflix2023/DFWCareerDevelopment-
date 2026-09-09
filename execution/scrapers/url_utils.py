"""URL sanitization, canonicalization, and ATS platform identification."""

import re
import hashlib
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from typing import Literal


TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gh_src", "lever-source", "ref", "source", "refid", "s", "sid",
    "employment_source", "iis", "iiss", "shared_id", "c", "mode"
}


def clean_canonical_url(url: str) -> str:
    """Strips all tracking, referral, and session parameters to ensure clean deduplication."""
    if not url:
        return ""
    
    parsed = urlparse(url)
    
    # Strip trailing slashes from path for consistency
    clean_path = parsed.path.rstrip("/")
    
    # Filter out known tracking and referral query parameters
    query_params = parse_qsl(parsed.query, keep_blank_values=False)
    filtered_params = [
        (k, v) for k, v in query_params 
        if k.lower() not in TRACKING_PARAMS and not k.lower().startswith("utm_")
    ]
    
    clean_query = urlencode(filtered_params)
    
    clean_url = urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        clean_path,
        parsed.params,
        clean_query,
        ""  # strip fragment
    ))
    return clean_url


def detect_ats_source(url: str) -> Literal["greenhouse", "lever", "ashby", "workday", "other"]:
    """Identifies the underlying ATS provider from the canonical URL."""
    url_lower = url.lower()
    if "greenhouse.io" in url_lower:
        return "greenhouse"
    elif "lever.co" in url_lower:
        return "lever"
    elif "ashbyhq.com" in url_lower:
        return "ashby"
    elif "myworkdayjobs.com" in url_lower or "workday" in url_lower:
        return "workday"
    return "other"


def generate_job_id(company: str, title: str, canonical_url: str) -> str:
    """Generates a deterministic unique hash ID for the position."""
    raw_key = f"{company.strip().lower()}::{title.strip().lower()}::{canonical_url.strip().lower()}"
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:16]
