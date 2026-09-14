# Self-Annealing Error Log & Pipeline Issue Ledger

> **Purpose**: Record all pipeline bugs, parser anomalies, deduplication flaws, and root-cause solutions to prevent regressions. Inspect this log before modifying scrapers, parsers, or normalizers.

---

## Issue 1: Garbage Company Name Parsing (`\u21b3` / `↳`)
* **Date**: 2026-09-08
* **Component**: `execution/scrapers/pipeline.py` & `execution/scrapers/url_utils.py`
* **Symptom**: Job entries displayed `\u21b3` or `↳` as the company name (e.g., Boeing, NXP, Nationwide).
* **Root Cause**: Upstream aggregator feeds use visual indent characters (`↳`) for multi-location sub-rows. Scraper extracted the link text or table row directly without resolving the parent company entity.
* **Solution**:
  1. Detect if `company` is empty, whitespace, or starts with non-alphanumeric punctuation (`\u21b3`, `↳`, `-`).
  2. Fall back to parsing the organization subdomain from `urlparse(apply_url).netloc.split(".")[0]` (e.g., `boeing.wd1...` $\to$ `Boeing`, `nxp.wd3...` $\to$ `NXP`, `nationwide.wd1...` $\to$ `Nationwide`).
  3. Clean title-case normalization.

---

## Issue 2: Non-Deterministic Workday URL Duplication
* **Date**: 2026-09-08
* **Component**: `execution/scrapers/url_utils.py` (`generate_job_id`)
* **Symptom**: The same underlying Boeing requisition was duplicated as two distinct jobs (`JR2026520976-1` on `EXTERNAL_CAREERS` and `JR2026520976` on `INTERN`).
* **Root Cause**: `generate_job_id()` hashed the full canonical URL string. Enterprise Workday instances often host identical requisitions across multiple internal board slugs with minor suffix variants (`-1`, `-2`).
* **Solution**:
  1. For Workday URLs, extract the core requisition code using regex `r"_([A-Z]{0,2}\d+)(?:-\d+)?(?:\?|$)"`.
  2. Hash `f"{normalized_company}::{requisition_id}"` so duplicate board URLs for the same job collapse into one canonical record.

---

## Issue 3: Linear Heuristic Scoring & Redundant Keyword Overlap
* **Date**: 2026-09-08
* **Component**: `execution/scrapers/qualification_matcher.py`
* **Symptom**: Generic Business Analyst or IT roles received high match scores simply by repeating generic buzzwords ("database", "analytics"), equaling the score of core technical pillars ("python", "rag", "llm").
* **Root Cause**: Equal-weighted flat scoring formula `0.4 + (len(matches) * 0.08)` without category weighting or token deduplication. Short tokens ("analytics") were counted twice when "data analytics" also matched.
* **Solution**:
  1. Categorize candidate skills into Core Technical Pillars (weight 1.5), Frameworks/Systems (weight 1.0), and Secondary/General (weight 0.5).
  2. Sort keywords by length descending and suppress substring duplicates before scoring.
  3. Enforce compound phrase matching precedence in role categorization.

---

## Issue 4: Unsanitized Multi-Location String Bloat
* **Date**: 2026-09-08
* **Component**: `execution/scrapers/pipeline.py`
* **Symptom**: Raw scraped string contained messy multi-city concatenations like `"30 locationsRidley Park, PASeattle, WALong Beach, CAMesa..."`.
* **Root Cause**: Feed tables aggregated all nationwide office locations into a single unspaced string for national roles.
* **Solution**:
  1. Detect multi-location blobs (e.g. `locations` in text or string length $> 80$).
  2. If `is_dfw` is True, extract the specific matching DFW municipality (e.g. `"Dallas, TX"` or `"Plano, TX"`).
  3. Standardize string to `"Dallas, TX (Multi-Location / Hybrid)"` or clean city/state pairs.

---

## Issue 5: Seed URLs Redirecting to General Career Portals Instead of Direct Job Postings
* **Date**: 2026-09-08
* **Component**: `execution/scrapers/pipeline.py` (`CURATED_DFW_POSITIONS`) & `link_validator.py`
* **Symptom**: Candidate clicked apply links and landed on general corporate homepages/search bars (e.g. att.jobs, ti.com) rather than direct application pages.
* **Root Cause**: Early development seed list contained placeholder / synthetic URL slugs without live requisition IDs.
* **Solution**:
  1. Completely purge synthetic seed entries.
  2. Require every candidate job link to possess a direct ATS requisition path (e.g. `boards.greenhouse.io/<co>/jobs/<id>`, `jobs.ashbyhq.com/<co>/<uuid>`, `jobs.lever.co/<co>/<uuid>`, `*.myworkdayjobs.com/..._<req_id>`).
  3. In `link_validator.py`, detect when a URL redirects away from an ATS job path to a generic `/careers` or home search page.

