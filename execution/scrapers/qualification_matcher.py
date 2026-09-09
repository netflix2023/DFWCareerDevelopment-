"""
Candidate qualification matching engine grounded strictly in Neftali's resume.
Designed for maximum simplicity, transparency, and accuracy (Karpathy simplicity).
"""

import re
from typing import Tuple, List, Set


# Core technical superpowers (Weight 1.5x / 15 points each)
CORE_PILLARS: Set[str] = {
    "python", "rag", "retrieval-augmented generation", "fastapi", "sql", "c++",
    "docker", "llm", "large language models", "vector database", "vector search",
    "agentic ai", "machine learning", "deep learning", "neural networks",
    "generative ai", "genai", "typescript", "microservices", "aws", "modal"
}

# Secondary tools & foundations (Weight 0.5x / 5 points each)
SECONDARY_TOOLS: Set[str] = {
    "git", "github", "linux", "react", "frontend", "backend", "full-stack",
    "rest api", "restful api", "database", "postgresql", "data analytics",
    "analytics", "business intelligence", "smart cities", "gis", "data modeling"
}

# Combine and pre-sort by length descending so longer phrases match first
ALL_SKILLS_ORDERED = sorted(list(CORE_PILLARS | SECONDARY_TOOLS), key=len, reverse=True)


def classify_role_category(title: str) -> str:
    """
    Categorizes the position based on title keywords.
    Prioritizes compound AI/ML roles before generic analytics roots.
    """
    t = title.lower()
    
    # 1. AI/ML & GenAI (Highest Priority)
    if any(k in t for k in ["generative ai", "genai", "artificial intelligence", "machine learning", "deep learning", "neural network", "ai ", "ai-", "ml "]):
        return "AI/ML & GenAI"
    if t.endswith("ai") or t.endswith("ml") or "ai/ml" in t:
        return "AI/ML & GenAI"
        
    # 2. Data & Analytics
    if any(k in t for k in ["data analyst", "data analytics", "business analyst", "bi intern", "data science"]):
        return "Data Analyst & Analytics"
        
    # 3. Data Engineering
    if any(k in t for k in ["data engineer", "data platform", "database"]):
        return "Data Engineering"
        
    # 4. GIS & Smart Cities
    if any(k in t for k in ["gis", "smart city", "geospatial", "urban"]):
        return "GIS & Smart Cities"
        
    # 5. Default to Software Engineering
    return "Software Engineering (Fullstack/Backend)"


def evaluate_qualification_match(title: str, description: str = "") -> Tuple[float, List[str], bool]:
    """
    Evaluates whether the candidate qualifies for the role using simple weighted scoring.
    - Core Skills: +0.15 points
    - Secondary Tools: +0.05 points
    - Substring duplicates (e.g. 'analytics' inside 'data analytics') are automatically suppressed.
    """
    text = f"{title} {description}".lower()
    title_lower = title.lower()
    
    # Check title alignment
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
    if not (is_technical and is_intern_or_early):
        return 0.0, [], False

    matched_skills: List[str] = []
    
    # Match skills from longest to shortest, avoiding duplicate sub-tokens
    for skill in ALL_SKILLS_ORDERED:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            # If this skill is already a sub-part of a longer matched phrase, skip it!
            # e.g., if 'data analytics' is already matched, do not add 'analytics'
            if any(skill in longer_skill for longer_skill in matched_skills if skill != longer_skill):
                continue
            matched_skills.append(skill)
            
    # Calculate simple score: Base 0.50 for verified technical intern + weighted skill points
    score = 0.50
    for skill in matched_skills:
        if skill in CORE_PILLARS:
            score += 0.15
        else:
            score += 0.05

            
    score = min(1.0, round(score, 2))
    qualifies = (score >= 0.50)
    
    return score, sorted(matched_skills), qualifies
