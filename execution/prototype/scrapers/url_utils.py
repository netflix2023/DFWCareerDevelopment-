"""URL sanitization, canonicalization, ATS platform identification, and entity normalization."""

import re
import hashlib
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from typing import Literal, Optional


TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gh_src", "lever-source", "ref", "source", "refid", "s", "sid",
    "employment_source", "iis", "iiss", "shared_id", "c", "mode"
}

KNOWN_SUBDOMAIN_COMPANIES = {
    "boeing": "Boeing",
    "nxp": "NXP Semiconductors",
    "nationwide": "Nationwide",
    "copart": "Copart",
    "ti": "Texas Instruments",
    "att": "AT&T",
    "jpmorganchase": "JPMorgan Chase",
    "cloudflare": "Cloudflare",
    "cadencesolutions": "Cadence Solutions",
    "prolificacademicltd": "Prolific",
    "galaxydigital": "Galaxy Digital",
    "fanniemae": "Fannie Mae",
    "semgrep": "Semgrep",
    "oneapp": "ONE Finance",
    "viamrobotics": "Viam Robotics"
}

DFW_CITIES = [
    "Dallas", "Plano", "Irving", "Richardson", "Frisco",
    "Fort Worth", "Grapevine", "Westlake", "Denton"
]


def clean_canonical_url(url: str) -> str:
    """Strips all tracking, referral, and session parameters to ensure clean deduplication."""
    if not url:
        return ""
    
    parsed = urlparse(url)
    clean_path = parsed.path.rstrip("/")
    query_params = parse_qsl(parsed.query, keep_blank_values=False)
    
    filtered_params = [
        (k, v) for k, v in query_params 
        if k.lower() not in TRACKING_PARAMS and not k.lower().startswith("utm_")
    ]
    clean_query = urlencode(filtered_params)
    
    return urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        clean_path,
        parsed.params,
        clean_query,
        ""  # strip fragment
    ))


def normalize_company_brand(name: str) -> str:
    """Strips leading bullet punctuation, 'The', and legal suffixes for consistent entity hashing."""
    cleaned = re.sub(r"^[\s↳\u21b3\-\*\•]+", "", name or "").strip()
    cleaned = re.sub(r"^the\s+", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"\s+\b(company|co|corp|corporation|inc|incorporated|llc|ltd|limited)\b\.?$", "", cleaned, flags=re.IGNORECASE).strip()
    return cleaned


def resolve_company_name(company: str, url: str) -> str:
    """
    Cleans company names and resolves fallback brand from subdomain when
    upstream aggregators inject indent bullets (↳ / \u21b3).
    """
    brand = normalize_company_brand(company)
    
    # If valid alphanumeric characters remain, return the cleaned name
    if re.search(r"[A-Za-z0-9]", brand):
        return brand

    # Fallback: parse subdomain from domain URL
    if not url:
        return "Unknown"
        
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    subdomain = netloc.split(".")[0]
    
    if subdomain in KNOWN_SUBDOMAIN_COMPANIES:
        return KNOWN_SUBDOMAIN_COMPANIES[subdomain]
        
    # Standard title-case fallback
    return subdomain.replace("-", " ").replace("_", " ").title()


def extract_requisition_id(url: str) -> Optional[str]:
    """
    Extracts underlying job requisition ID from enterprise ATS URLs.
    Handles Workday root requisition codes (e.g. _JR2026520976-1 -> JR2026520976).
    """
    if not url:
        return None
        
    # Workday pattern: matches _JR12345 or _R12345 or _12345, stripping suffix -1, -2
    wd_match = re.search(r"_([A-Z]{0,4}\d+)(?:-\d+)?(?:/|\?|$)", url, re.IGNORECASE)
    if wd_match:
        return wd_match.group(1).upper()
        
    # Greenhouse pattern: /jobs/12345
    gh_match = re.search(r"/jobs/(\d+)", url)
    if gh_match:
        return gh_match.group(1)
        
    # Lever / Ashby UUID pattern
    uuid_match = re.search(r"/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", url, re.IGNORECASE)
    if uuid_match:
        return uuid_match.group(1).lower()
        
    return None


def generate_job_id(company: str, title: str, canonical_url: str) -> str:
    """
    Generates a deterministic unique hash ID for the position.
    Uses requisition ID if available to collapse identical requisitions across internal boards.
    If no requisition ID is present, hashes on company and cleaned title (excluding the variable URL).
    """
    norm_company = normalize_company_brand(company).lower()
    req_id = extract_requisition_id(canonical_url)
    
    if req_id:
        raw_key = f"{norm_company}::{req_id}"
    else:
        clean_title = re.sub(r"\s+", " ", title.strip().lower())
        raw_key = f"{norm_company}::{clean_title}"
        
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:16]


def sanitize_location(location: str, is_dfw: bool = False) -> str:
    """
    Cleans multi-location string bloat (e.g. 30 locationsRidley Park...)
    Standardizes to clean metro tags.
    """
    if not location:
        return "Unknown"
        
    cleaned = re.sub(r"\s+", " ", location).strip()
    
    # Check for multi-location bloat (keyword or long concatenated string)
    is_multi = "locations" in cleaned.lower() or len(cleaned) > 50
    
    if is_dfw and is_multi:
        # Check which specific DFW city matched
        for city in DFW_CITIES:
            if city.lower() in cleaned.lower():
                return f"{city}, TX (Multi-Location)"
        return "Dallas, TX (Multi-Location)"
        
    return cleaned


def detect_ats_source(url: str) -> Literal["greenhouse", "lever", "ashby", "workday", "icims", "other"]:
    """Identifies the underlying ATS provider from URL path and domain."""
    url_lower = url.lower()
    if "greenhouse.io" in url_lower:
        return "greenhouse"
    elif "lever.co" in url_lower:
        return "lever"
    elif "ashbyhq.com" in url_lower:
        return "ashby"
    elif "myworkdayjobs.com" in url_lower or "workday" in url_lower:
        return "workday"
    elif "icims.com" in url_lower or "icims=1" in url_lower or "careers.ti.com" in url_lower:
        return "icims"
    return "other"
