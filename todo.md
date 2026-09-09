# Career Surge Engine: Modular Agile Roadmap (`todo.md`)

> **Hierarchy**: `subtask` -> `task` -> `module` -> `feature-branch`  
> **PM/SWE Contract**: Neftali = Product Manager (The What) | Agent = Software Engineer (The How)  
> **Strict Gate**: Draft plan -> PM Approves -> Build & Verify Module-by-Module -> Git Checkpoint.

---

## Active Sprint: Data Quality, Scoring Hardening & Link Validation

- [x] **Module 1: URL Normalization, Subdomain Fallback & Workday Requisition Deduplication**
  - [x] 1.1 In `url_utils.py`, add company name resolution from domain subdomain when name is `↳` or empty
  - [x] 1.2 In `url_utils.py`, extract Workday requisition ID regex (`r"_([A-Z]{0,2}\d+)(?:-\d+)?"`)
  - [x] 1.3 In `models.py` & `pipeline.py`, hash `f"{company}::{requisition_id}"` for Workday roles and store secondary links in `alternate_urls`
  - [x] 1.4 Sanitize multi-location strings to clean localized metro labels (e.g. `"Dallas, TX (Multi-Location)"`)
  - [x] 1.5 Verify with unit tests against real Boeing, NXP, and Nationwide postings


- [x] **Module 2: Transparent Weighted Skill Scoring & Deduplication**
  - [x] 2.1 In `qualification_matcher.py`, implement 2-tier weighted scoring (Core 1.5x, Secondary 0.5x)
  - [x] 2.2 Deduplicate substring matches (e.g. matching "data analytics" suppresses "analytics")
  - [x] 2.3 Set role classification precedence to favor AI/ML & GenAI over generic analytics
  - [x] 2.4 Verify scores against Neftali's candidate profile (`PERSONA_AI_ENGINEER_INTERN_DFW.md`)


- [x] **Module 3: Fast Concurrent Live Link Validator**
  - [x] 3.1 Build `execution/scrapers/link_validator.py` with 5 worker threads (`ThreadPoolExecutor`)
  - [x] 3.2 Implement HTTP HEAD check with GET fallback (5s timeout, 1 retry with exponential backoff)
  - [x] 3.3 Filter out HTTP 404s, 410s, and closed requisition redirects
  - [x] 3.4 Verify live validation speeds on existing harvested jobs (validated in 7.97s; dropped 15 dead links; kept 12 active)


- [x] **Module 4: SQLite Database & Job Market Telemetry Tracker**
  - [x] 4.1 Create `career.db` schema: `jobs` (UNIQUE `job_id`), `job_telemetry` (demand stats, post times, close times), `applications`
  - [x] 4.2 Record job telemetry analytics: role category distribution, posting times, days active
  - [x] 4.3 Build daily broken link maintenance checker (`link_maintenance.py`) to prune closed postings automatically
  - [x] 4.4 Exclude postings older than 7 days from daily dispatches while preserving historical DB rows

- [x] **Module 5: Job Discovery Ingestion (LinkedIn Guest & Feed Normalization)**
  - [x] 5.1 Build `execution/scrapers/linkedin_guest.py` capped at 25 results with rate-limit guard
  - [x] 5.2 Decouple geographic targeting via `execution/scrapers/geo_config.py` (`TARGET_METRO`)
  - [x] 5.3 Purge synthetic/placeholder seed lists; enforce 100% genuine direct ATS requisition links

- [x] **Module 6: Daily Email Digest & Code Review Protocol**
  - [x] 6.1 Build `execution/notifier/email_dispatcher.py` with responsive HTML template and Resend API
  - [x] 6.2 Render clean summary table of Top 10 positions with direct 1-click apply buttons
  - [x] 6.3 Build CodeRabbit-style static code quality and security reviewer (`execution/review/code_review.py`)


- [ ] **Module 7: Multi-Persona Resume Tailoring Engine (Experiment 2)**
  - [ ] 7.1 Map job roles to foundational personas (`AI/ML`, `Software Engineering`, `Data Platform`)
  - [ ] 7.2 Implement verified bullet point selector and reorderer targeting matching skills
  - [ ] 7.3 Export top 3 tailored resumes in clean Markdown (`.md`) format

- [ ] **Module 8: Cloud Automation & GitHub Sync**
  - [ ] 8.1 Initialize GitHub Actions workflow `.github/workflows/daily_pipeline.yml` (7:00 AM CDT cron)
  - [ ] 8.2 Push cleanly to private repository `career-surge-engine` with PM approval
