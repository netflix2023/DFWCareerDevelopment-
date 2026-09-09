# September Surge Fast-Track: AI Agent Instructions & Master Architecture

> **Project Title**: September Surge Fast-Track: Automated Career Prep, Job Scraper & Resume Tailoring Engine  
> **Environment**: Antigravity IDE | Chromebook Linux + Google Drive Persistence  
> **Collaboration Model**: **Neftali = Product Manager (Design & The What)** | **Agent = Senior Software Engineer (Code & The How)**  
> **Synchronized**: `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md`

---

## 0. Mission & Non-Negotiable Principles

### Primary Mission
Discover active technical internships and entry-level SWE, Data Science, and AI roles **within hours of posting**, parse qualifications based on the **Resume Guide 2.0** standard, and auto-tailor resumes so applicants apply **within 24–48 hours before automated ATS candidate caps hit**.

### Non-Negotiable Principles
1. **Speed to Application (First-In, First-Reviewed)**: Beat ATS applicant volume caps (first 50–100 candidates get screened). Rapid discovery (< 24–48 hrs) is paramount.
2. **Maximize True Keyword Match (Zero Hallucinations)**: Extract real qualifications from JDs to target a 75% keyword match. NEVER fabricate or invent candidate skills.
3. **No-Spam & Clean Applications**: Strict human review gate before any resume export or application submission. Quality over robotic spam.
4. **Karpathy Simplicity**: "As complex as needed, as simple as possible." Plain JSON, SQLite, and direct HTTP REST endpoints over brittle headless browsers.
5. **Strict Plan Approval Gate**: The Software Engineer MUST ALWAYS draft an implementation plan and obtain explicit Product Manager (Neftali) approval before modifying production code or schemas. Once a plan is approved, the Engineer builds and verifies that module autonomously without asking permission for routine coding steps.
6. **Module-by-Module Delivery**: Deliver and test ONE isolated module at a time. Never combine multiple unfinished features.
7. **Novice-Friendly Technical Clarity**: Explain technical concepts in clear, simple language (Feynman style) so the Product Manager easily understands the codebase and system mechanics.

---

## 1. Team Dynamics & Engineering Workflow

* **Product Manager (Neftali)**:
  * Owns the vision, business requirements, product design, feature priorities, and "the what".
  * Reviews and approves implementation plans and architectural decision gates.
* **Software Engineer (Agent)**:
  * Owns the technical architecture, code quality, testing, error logging, and "the how".
  * Explains technical concepts clearly for a novice, documenting the exact chain-of-thought (why and how).
  * Executes approved plans step-by-step and module-by-module.
* **Self-Annealing System (`execution/error_log.md`)**:
  * Any runtime error, parser failure, or deduplication flaw must be recorded in `execution/error_log.md` with root-cause fixes.
  * The Engineer must inspect this log before proposing code modifications to prevent repeating errors.
* **Code Review Protocol (CodeRabbit Style)**:
  * Before committing or merging code, run an automated review checking:
    1. *Correctness & Regressions*: Does it resolve the root cause without breaking existing features?
    2. *Input Sanitization*: Are URLs, company names, and multi-location strings cleaned?
    3. *Type Safety & Exceptions*: Are types hinted and HTTP exceptions caught gracefully?
* **Chain-of-Thought & Feynman Explanations**: Always document why and how code works in plain English.

---

## 2. Storage, Worktree & Git Management Model

* **Drive Persistence**: Root is `/home/neftalibautista1415/AntigravityProjects/Career` (Windows: `g:\My Drive\AntigravityProjects\Career`).
* **Directives Stay in Root**: All blueprints, schemas, source guides, and candidate personas live centrally in `directives/`.
* **Git as Local Version Control System**: Git tracks every step locally. Every feature or fix is developed cleanly on a dedicated branch or worktree to guarantee that `main` is never broken.
* **Protected GitHub Sync**: `.gitignore` strictly protects `.env`, credentials, local SQLite caches (`career.db`), and Drive artifacts. Remote pushing to `career-surge-engine` requires explicit PM approval.

---

## 3. Resume Tailoring Engine: Two Planned Experiments

The engine will support two distinct tailoring architectures:
1. **Experiment 2 (Modular Multi-Persona System) — Priority 1 (Current Focus)**:
   * Maintains distinct pre-built personas (`PERSONA_AI_ENGINEER_INTERN_DFW.md`, `PERSONA_SWE_INTERN_DFW.md`, `PERSONA_DATA_ANALYST_DFW.md`).
   * Routes each incoming job description to the best-matching baseline persona, then selects and re-orders verified bullet points to highlight matching skills in clean Markdown (`.md`) format.
2. **Experiment 1 (Direct Title Re-Alignment) — Priority 2**:
   * Takes a single master resume and dynamically alters bullet points to mirror target job titles. Tested after Experiment 2.

---

## 4. Current Repository Blueprint

```
Career/
├── AGENTS.md                         # Master Agent reference & PM agreement (this file)
├── .env                              # Local environment keys (ignored by git)
├── .env.example                      # Configuration template
├── .gitignore                        # Strict guard for .env, secrets, *.db, and SQLite
├── todo.md                           # Agile task hierarchy checklist
├── progress_log.md                   # Living session state and handoff notes
├── directives/                       # Central blueprints & personas (Root only)
│   ├── RESUME_GUIDE_2.0.md           # Verbatim Resume Guide 2.0 master specification
│   ├── RESUME_FORMAT_TEMPLATE_AND_EXAMPLES.md # Exact visual layout & live examples
│   ├── KEYWORD_MATRIX.md             # Curated SWE & AI Intern qualification taxonomy
│   ├── sources/
│   │   └── TARGET_PLATFORMS.md       # Categorized job platforms matrix (Tier 1-4)
│   └── user_stories/
│       ├── PERSONA_SWE_INTERN_DFW.md # DFW SWE Candidate Persona
│       └── PERSONA_AI_ENGINEER_INTERN_DFW.md # DFW AI Candidate Persona
├── execution/                        # Core Python pipeline
│   ├── error_log.md                  # Self-annealing issue ledger (Issues documented & fixed)
│   ├── scrapers/                     # ATS and feed ingestion modules
│   │   ├── models.py                 # JobPosting clean dataclass schema
│   │   ├── url_utils.py              # Canonical URL cleaner & ATS detector
│   │   ├── qualification_matcher.py  # Weighted qualification matching engine
│   │   ├── link_validator.py         # Concurrent 5-thread live URL validator
│   │   └── pipeline.py               # Main ATS harvesting & normalization script
│   ├── parsers/                      # JD qualification and 75% keyword extractors
│   ├── tailor/                       # Resume Guide 2.0 What-How-Result bullet formatters
│   ├── notifier/                     # Daily Top 10 email dispatcher (Resend API)
│   └── tests/                        # TDD unit and integration test suites
└── output/                           # Generated runtime outputs
    ├── scraped_jobs/                 # Raw/normalized JSON job payloads
    ├── clean_csvs/                   # Structured deduplicated spreadsheets
    └── tailored_resumes/             # Exported tailored resumes (Markdown format)
```

---

## 5. Anti-Hallucination & Hardware Canary Guards

* **Canary A (Context Warning)**: Warn PM at 10–12 turns; persist active state to `progress_log.md`.
* **Canary B (Filesystem Verification)**: Verify files physically exist before proposing edits or imports.
* **Canary C (Credential Guard)**: Verify `.gitignore` is active and scan files for raw API keys before saving.
* **Canary D (Scraping Rate-Limit Guard)**: On HTTP 429/403, halt, inject jittered backoff, rotate User-Agent, and fall back to public ATS JSON endpoints.
* **Canary E (Resume Truth Guard)**: Cross-reference all generated bullets with candidate's real experience. Never invent unheld skills.
* **Canary F (Chromebook Resource Guard)**: Avoid memory-heavy headless browsers. Use lightweight direct HTTP requests.
* **Canary G (Git Safety Guard)**: Never force-push `main`. All GitHub pushes require explicit PM authorization.

---

## 6. Approved PM Architectural Decisions (The 15 Decisions)

> [!NOTE]
> Recorded architectural alignment between Product Manager (Neftali) and Software Engineer (Agent):

### Architecture & Pipeline Ingestion
1. **Garbage Company Name Resolution**: **APPROVED** — Extract the company brand from the subdomain (e.g., `boeing.wd1...` $\to$ `Boeing`) using a title-cased fallback mapping when the upstream scraper injects an indent arrow (`↳`) or empty string.
2. **Workday Requisition Deduplication**: **APPROVED** — Pick the first primary board URL (preferring `EXTERNAL_CAREERS` or standard carrier domains), store secondary board links in `alternate_urls`, and hash the unique requisition ID (`company::requisition_id`).
3. **LinkedIn Guest Ingest**: **APPROVED** — Cap queries at 25 results per search term to avoid Cloudflare bot-challenges on shared IP pools.
4. **Indeed Aggregator**: **APPROVED** — Query Indeed via date-sorted RSS feeds and Google Jobs endpoints. Keep `JobSpy` strictly as an opt-in fallback (`--enable-jobspy`).
5. **Live Link Validator Concurrency**: **APPROVED** — Run concurrently with 5 worker threads bounded by a 5-second connection timeout.

### Qualification Matching & Scoring
6. **Weighted Skill Scoring**: **APPROVED** — Simple, transparent weighted scoring: Core Technical Pillars (Python, RAG, FastAPI, SQL, Docker) carry weight $1.5\times$; Secondary tools (Git, frontend) carry weight $0.5\times$. Explain simply for novices.
7. **Redundant Keyword Deduplication**: **APPROVED** — Count as a single higher-tier match. Sort target patterns by token length descending and consume parent tokens (e.g., matching "data analytics" suppresses the duplicate match on "analytics").
8. **Role Precedence**: **APPROVED** — Default to **AI/ML & GenAI** priority when a role touches both AI and general data analytics.

### Cleanliness & Deliverables
9. **Multi-Location Sanitization**: **APPROVED** — Shorten multi-city blobs to `"Dallas, TX (Multi-Location)"` (or the matching DFW city).
10. **Application Freshness Hard Cap**: **APPROVED** — Exclude postings older than 7 days from the daily email dispatch and CSV, but retain them in SQLite `career.db` for deduplication history.
11. **Applicant Count Filtering & Job Market Telemetry**: **APPROVED** — Place high-applicant jobs (>100) at the bottom with a warning badge (⚠️ `>100 Applicants`). Build a telemetry profile tracking role demand, time-of-day posted, and time-to-close.

### Daily Runner, Email & Tailoring
12. **Daily Email Layout**: **APPROVED** — Clean summary table of the **Top 10 positions** with 1-click direct apply links, linking to the full CSV/dashboard.
13. **Resume Tailoring Experiment Priority**: **APPROVED** — Implement **Experiment 2 (Multi-Persona Routing)** first.
14. **Tailored Resume File Format**: **APPROVED** — Export tailored resumes as clean **Markdown (.md)** files.
15. **Private GitHub Setup**: **APPROVED** — Name the repository `career-surge-engine`.


---

## 7. Living Current State & Handoff Protocol

### Current Sprint Snapshot
* **Active Sprint**: Sprint 1 — ATS Pipeline Hardening, Normalization Bug Fixes & Link Validation
* **Status**: 4 Core Bugs cataloged in `execution/error_log.md`. 27 positions harvested.
* **Immediate Next Step**: Await PM feedback on the 15 alignment questions, then execute the bug fixes in `url_utils.py` and `qualification_matcher.py` step-by-step.
