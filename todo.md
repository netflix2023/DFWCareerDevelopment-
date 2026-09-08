# September Surge Fast-Track: Agile Task Board (`todo.md`)

> **Hierarchy**: `subtask` -> `task` -> `section` -> `folder` -> `feature-branch`  
> **Rule**: Work on **ONE and only ONE** active task at a time (`[/]`).

---

## Sprint 0: Architecture & Environment Bootstrap

- [x] **Task 0.1: Master Reference & Instructions Definition**
  - [x] Author comprehensive, production-ready `AGENTS.md` in `Career/`
  - [x] Mirror instructions to `GEMINI.md` and `CLAUDE.md`
  - [x] Initialize Agile `todo.md` and living `progress_log.md`
- [ ] **Task 0.2: Project Directory Scaffold & Directives Setup**
  - [ ] Scaffold folders: `directives/mvps/`, `directives/user_stories/`, `execution/scrapers/`, `execution/parsers/`, `execution/tailor/`, `execution/tests/`, `output/scraped_jobs/`, `output/clean_csvs/`, `output/tailored_resumes/`, `.tmp/scratch/`
  - [ ] Create `.env.example` with ATS API rate limits and User-Agent headers
  - [ ] Initialize `directives/company_tokens.json` with target Greenhouse/Lever/Ashby companies (Stripe, Databricks, Palantir, Ramp, Figma, Cloudflare, etc.)
  - [ ] Create baseline candidate profile schema in `directives/user_stories/candidate_profile.json`
  - [ ] Author `directives/resume_guide_2.0_spec.md` with What-How-Result rules and 75% target matching criteria

---

## Sprint 1: ATS Public Ingestion Pipeline (TDD)

- [ ] **Task 1.1: Base Scraper & Rate-Limiting Engine (`execution/scrapers/base_scraper.py`)**
  - [ ] Step 1 (Red): Write failing unit test for jittered backoff, retry handling, and header rotation
  - [ ] Step 2 (Green): Implement lightweight `BaseScraper` class with Canary D rate-limit guard
  - [ ] Step 3 (Verify): Pass 100% of base scraper tests
- [ ] **Task 1.2: Greenhouse Public Board Client (`execution/scrapers/greenhouse_client.py`)**
  - [ ] Step 1 (Red): Write failing test with mocked Greenhouse JSON payload for internship/entry-level filter
  - [ ] Step 2 (Green): Implement `GreenhouseClient` to query `/v1/boards/{company}/jobs?content=true`
  - [ ] Step 3 (Verify): Test against real and mocked payloads; assert accurate role, department, and description extraction
- [ ] **Task 1.3: Lever Public Postings Client (`execution/scrapers/lever_client.py`)**
  - [ ] Step 1 (Red): Write failing test for Lever JSON payload parsing
  - [ ] Step 2 (Green): Implement `LeverClient` querying `/v0/postings/{company}?mode=json`
  - [ ] Step 3 (Verify): Assert correct extraction and < 48-hour age filter
- [ ] **Task 1.4: Ashby JSON Job Board Client (`execution/scrapers/ashby_client.py`)**
  - [ ] Step 1 (Red): Write failing test for Ashby POST API response
  - [ ] Step 2 (Green): Implement `AshbyClient`
  - [ ] Step 3 (Verify): Pass Ashby test suite
- [ ] **Task 1.5: LinkedIn Guest Recent Postings Scraper (`execution/scrapers/linkedin_guest.py`)**
  - [ ] Step 1 (Red): Write failing test for guest search HTML card parser with `f_TPR=r86400`
  - [ ] Step 2 (Green): Implement lightweight guest endpoint parser with BeautifulSoup
  - [ ] Step 3 (Verify): Verify fallback behavior and 0 headless browser dependencies

---

## Sprint 2: Job Description Parsing & 75% Keyword Matrix (TDD)

- [ ] **Task 2.1: JD Qualification & Tech Stack Extractor (`execution/parsers/jd_parser.py`)**
  - [ ] Step 1 (Red): Write failing tests against golden standard SWE intern and Data analyst JDs
  - [ ] Step 2 (Green): Implement regex/NLP token extractor for languages, frameworks, databases, and graduation year criteria
  - [ ] Step 3 (Verify): Verify accurate role level classification (< 2 years experience vs senior)
- [ ] **Task 2.2: Semantic Keyword Matcher & Gap Analyzer (`execution/parsers/keyword_matcher.py`)**
  - [ ] Step 1 (Red): Write tests calculating keyword overlap against candidate profile
  - [ ] Step 2 (Green): Implement 75% keyword density scoring algorithm (Jaccard + n-gram overlap)
  - [ ] Step 3 (Verify): Verify Canary E (Truth Guard) flags missing skills without hallucinating

---

## Sprint 3: Resume Tailoring Engine (Resume Guide 2.0)

- [ ] **Task 3.1: Past-Tense What-How-Result Bullet Formatter (`execution/tailor/bullet_formatter.py`)**
  - [ ] Step 1 (Red): Write tests enforcing past-tense action verbs, technology integration, and metric validation
  - [ ] Step 2 (Green): Implement bullet transformer aligning candidate project experiences to target JD keywords
  - [ ] Step 3 (Verify): Verify single-column plaintext/markdown conformity
- [ ] **Task 3.2: End-to-End Resume Markdown Generator (`execution/tailor/resume_generator.py`)**
  - [ ] Step 1 (Red): Write test asserting generated 1-page resume contains correct contact, education, skills, projects, and experience
  - [ ] Step 2 (Green): Implement Jinja2 Markdown and plaintext template engine
  - [ ] Step 3 (Verify): Export sample tailored resume to `output/tailored_resumes/`

---

## Sprint 4: Sub-Agent Quality Review & Delivery

- [ ] **Task 4.1: Automated Sub-Agent Review & Truth Guard Audit Script**
- [ ] **Task 4.2: Project Completion & `LEARNING.md` Documentation**
