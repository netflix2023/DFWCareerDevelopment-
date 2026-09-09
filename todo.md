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

- [x] **Module 6: Daily Email Digest & Native Gmail Delivery**
  - [x] 6.1 Build `execution/notifier/email_dispatcher.py` with responsive HTML template and Resend API
  - [x] 6.2 Add free native Gmail SMTP support (`smtp.gmail.com:587`) for zero-cost direct email delivery
  - [x] 6.3 Render clean summary table of Top 10 positions with direct 1-click apply buttons
  - [x] 6.4 Transition from custom script to official **CodeRabbit GitHub App** for automated PR review


- [ ] **Phase 2: Pillar 2 — Tailoring Personas Beyond Keyword Stuffing (Module 7)**
  - [ ] 7.1 **Role Persona Clustering (Vector Mapping)**:
    - [ ] 7.1a Branch `feature/vector-fastembed`: Local CPU sentence-transformers vector embeddings
    - [ ] 7.1b Branch `feature/vector-qdrant`: Persistent Dockerized Qdrant/pgvector integration
  - [ ] 7.2 **Semantic Claim Linter**: Deterministic linter flagging weak claims and highlighting metrics (throughput, latency, volume)
  - [ ] 7.3 **Differential Resume Generation**:
    - [ ] 7.3a Branch `feature/resume-typst`: Blazing-fast Typst compiler producing ATS-verified vector PDFs
    - [ ] 7.3b Branch `feature/resume-html-pdf`: Tailwind/HTML templates rendered via Headless Chromium


- [ ] **Phase 2: Cloud Automation & GitHub Sync (Module 8)**
  - [ ] 8.1 Connect remote repository `netflix2023/career-surge-engine` and sync `main`
  - [ ] 8.2 Install official CodeRabbit GitHub App on repository for automated code and design PR reviews
  - [ ] 8.3 Initialize GitHub Actions workflow `.github/workflows/daily_pipeline.yml` (7:00 AM CDT cron)


- [ ] **Phase 3: Pillar 1 & Pillar 3 — Market Timing Arbitrage & Smart Apply**
  - [ ] 9.1 **Direct ATS API Harvesters**: Implement `AshbyApiHarvester` (GraphQL) and `GreenhouseApiHarvester` (JSON REST)
  - [ ] 9.2 **Temporal Trend Analytics & First-Mover Index**: Track company posting cadence and shelf-life / ghost job alerts
  - [ ] 9.3 **Manifest V3 Chrome Extension** (`feature/smart-apply-extension`): Natural typing pacing, form pre-fill, human final-click
  - [ ] 9.4 **STAR-Method Question Synthesis**: Local RAG grounded in candidate project documentation for bespoke application questions
