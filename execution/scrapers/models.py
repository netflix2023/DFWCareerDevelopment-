"""Data models and schemas for the ATS job intelligence pipeline."""

from dataclasses import dataclass, field, asdict
from typing import Literal, Optional, List, Dict, Any
from datetime import datetime


@dataclass
class JobPosting:
    """Canonical representation of an ingested technical job posting."""
    job_id: str
    company: str
    title: str
    ats_source: Literal["greenhouse", "lever", "ashby", "workday", "other"]
    apply_url: str
    location: str
    discovered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    role_category: str = "Software Engineering"
    match_score: float = 0.0
    matching_skills: List[str] = field(default_factory=list)
    age_days: Optional[int] = None
    is_dfw: bool = False
    is_remote: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
