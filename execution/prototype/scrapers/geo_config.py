"""
Geographic configuration module for Career Surge Engine.
Allows dynamic target metro selection (DFW, Austin, NYC, Remote, etc.)
configurable via .env (TARGET_METRO).
"""

import os
from typing import Dict, List, Tuple


METRO_REGIONS: Dict[str, List[str]] = {
    "DFW": [
        "dallas", "plano", "irving", "richardson", "frisco",
        "fort worth", "ft worth", "dfw", "grapevine", "westlake",
        "denton", "arlington", "carrollton", "garland", "mckinney"
    ],
    "AUSTIN": [
        "austin", "round rock", "cedar park", "georgetown", "san marcos"
    ],
    "HOUSTON": [
        "houston", "woodlands", "sugar land", "katy", "spring"
    ],
    "NYC": [
        "new york", "nyc", "manhattan", "brooklyn", "queens", "jersey city", "hoboken"
    ],
    "SF_BAY": [
        "san francisco", "sf", "san jose", "sunnyvale", "palo alto", "mountain view",
        "oakland", "berkeley", "fremont", "redwood city", "santa clara"
    ],
    "SEATTLE": [
        "seattle", "bellevue", "redmond", "kirkland"
    ]
}

REMOTE_KEYWORDS = [
    "remote", "usa", "us", "anywhere", "telecommute", "work from home", "virtual"
]


def get_target_metro() -> str:
    """Returns the active target metro from environment variable TARGET_METRO."""
    return os.getenv("TARGET_METRO", "DFW").upper().strip()


def check_location_match(location: str) -> Tuple[bool, bool, bool]:
    """
    Evaluates whether a job location matches the configured target metro and/or remote.
    Returns: (is_target_metro, is_remote, is_state_match)
    """
    if not location:
        return False, False, False
        
    loc_lower = location.lower()
    active_metro = get_target_metro()
    
    # 1. State Match (Texas by default if target is DFW/Austin/Houston)
    is_state = False
    if active_metro in ("DFW", "AUSTIN", "HOUSTON"):
        is_state = bool("tx" in loc_lower or "texas" in loc_lower)

    # 2. Target Metro Match
    target_cities = METRO_REGIONS.get(active_metro, METRO_REGIONS["DFW"])
    is_metro = False
    for city in target_cities:
        if city in loc_lower:
            # Disambiguate multi-state cities (e.g. Arlington, IL/VA vs Arlington, TX)
            if city in ("arlington", "spring", "westlake"):
                if is_state:
                    is_metro = True
                    break
            else:
                is_metro = True
                break
    
    # 3. Remote Match
    is_remote = any(r in loc_lower for r in REMOTE_KEYWORDS)
        
    # If target is set to ALL or REMOTE, adjust accordingly
    if active_metro == "ALL":
        return True, is_remote, is_state
    if active_metro == "REMOTE":
        return is_remote, is_remote, is_state
        
    return is_metro, is_remote, is_state

