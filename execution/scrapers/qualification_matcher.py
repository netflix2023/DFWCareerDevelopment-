"""Candidate qualification matching engine grounded strictly in Neftali's resume."""

from typing import Tuple, List, Set
import re


# Grounded qualifications from Neftali's verified resume (Copy of Resume.pdf)
CANDIDATE_SKILLS = {
    "ai_ml": {
        "artificial intelligence", "ai", "machine learning", "ml", "rag", 
        "retrieval-augmented generation", "vector database", "vector search",
        "agentic ai", "llm", "large language models", "prompt engineering",
        "generative ai", "genai", "deep learning", "neural networks"
    },
    "languages": {
        "python", "typescript", "javascript", "sql", "java", "c++", "html", "css"
    },
    "frameworks_web": {
        "react", "fastapi", "drizzle orm", "rest api", "restful api", "rest",
        "full-stack", "frontend", "backend", "web development"
    },
    "cloud_devops": {
        "docker", "aws", "modal", "git", "github", "linux", "vercel", "microservices"
    },
    "data_analytics": {
        "data analyst", "data analytics", "data engineering", "gis", "sql queries",
        "database", "postgresql", "data modeling", "analytics", "business intelligence"
    },
    "domains": {
        "smart cities", "real estate analytics", "property valuation", "municipal data"
    }
}

ALL_CANDIDATE_KEYWORDS = set()
for sub in CANDIDATE_SKILLS.values():
    ALL_CANDIDATE_KEYWORDS.update(sub)


def classify_role_category(title: str) -> str:
    """Categorizes the position based on title keywords."""
    t = title.lower()
    if any(k in t for k in ["ai", "machine learning", "ml", "deep learning", "nlp", "computer vision"]):
        return "AI/ML & GenAI"
    elif any(k in t for k in ["data analyst", "analytics", "business analyst", "bi intern", "data science"]):
        return "Data Analyst & Analytics"
    elif any(k in t for k in ["data engineer", "data platform", "database"]):
        return "Data Engineering"
    elif any(k in t for k in ["gis", "smart city", "geospatial", "urban"]):
        return "GIS & Smart Cities"
    elif any(k in t for k in ["qa", "sdet", "test automation"]):
        return "SDET & Automation"
    return "Software Engineering (Fullstack/Backend)"


def evaluate_qualification_match(title: str, description: str = "") -> Tuple[float, List[str], bool]:
    """
    Evaluates whether the candidate qualifies for the role.
    Returns: (match_score, list_of_matching_skills, qualifies_boolean)
    """
    text = f"{title} {description}".lower()
    matches = []
    
    # Check title alignment
    title_lower = title.lower()
    is_technical = any(k in title_lower for k in [
        "software", "engineer", "developer", "ai", "machine learning", "data", 
        "analyst", "full stack", "backend", "frontend", "systems", "cloud", "technology"
    ])
    is_intern_or_early = any(k in title_lower for k in [
        "intern", "internship", "co-op", "junior", "associate", "entry", "fellow", "early"
    ]) or ("intern" in text[:300])
    
    # Immediate disqualification for senior / non-technical tracks
    if any(k in title_lower for k in ["senior", "staff", "principal", "director", "manager", "lead"]) and not ("lead developer" in text):
        return 0.0, [], False
    if any(k in title_lower for k in ["sales", "account executive", "marketing", "recruiter", "nurse", "paralegal"]):
        return 0.0, [], False

    # Collect matched skills
    for skill in ALL_CANDIDATE_KEYWORDS:
        # Match whole word or exact token
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            matches.append(skill)
            
    # Calculate score based on breadth of match
    score = min(1.0, 0.4 + (len(matches) * 0.08)) if (is_technical and is_intern_or_early) else 0.0
    qualifies = (score >= 0.5)
    
    return round(score, 2), sorted(list(set(matches))), qualifies
