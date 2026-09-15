# September Surge Fast-Track: Agent Operating Manual & Repository Context

> **Project Title**: September Surge Fast-Track: Automated Career Prep, Job Scraper & Resume Tailoring Engine  
> **Repository**: `https://github.com/netflix2023/DFWCareerDevelopment-`  
> **Environment**: Antigravity IDE | Windows PowerShell + Google Drive Persistence  
> **Collaboration Model**: **Neftali = Product Manager (Design, Product & The What)** | **Agent = Senior Software Engineer (Code, Testing & The How)**  
> **Synchronized Files**: `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md`

---

## ⚡ Quickstart For New Agent Conversations

When starting any new conversation, **follow this sequence before taking action**:
1. **Read the Living State**: Read [`progress_log.md`](file:///g:/My%20Drive/AntigravityProjects/Career/progress_log.md) to know the exact current sprint status, recent commits, and immediate next objectives.
2. **Review the Roadmap**: Check [`todo.md`](file:///g:/My%20Drive/AntigravityProjects/Career/todo.md) for active tasks and verification checkboxes.
3. **Inspect the Self-Annealing Log**: Inspect [`execution/prototype/error_log.md`](file:///g:/My%20Drive/AntigravityProjects/Career/execution/prototype/error_log.md) before writing or refactoring scraper/storage code to avoid repeating past bugs.
4. **Adhere to the Non-Negotiables**: The Product Manager owns all architectural and design decisions; tech stack specifics live in [`directives/research/TECH_STACK.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/research/TECH_STACK.md) and [`directives/research/ARCHITECTURAL_DECISION_RECORDS.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/research/ARCHITECTURAL_DECISION_RECORDS.md).

---

## 0. Mission & Non-Negotiable Principles

### Primary Mission
Discover active technical internships and entry-level SWE, Data Science, and AI roles **within hours of posting**, parse qualifications based on the **Resume Guide 2.0** standard, auto-tailor authentic resumes, and synthesize custom application answers so applicants apply **within 24–48 hours before automated ATS candidate caps hit**.

### Non-Negotiable Principles
1. **Speed to Application (First-In, First-Reviewed)**: Beat ATS applicant volume caps (first 50–100 candidates get screened). Rapid discovery (< 24–48 hrs) and first-mover timing are paramount.
2. **Maximize True Keyword Match (Zero Hallucinations)**: Extract real qualifications from JDs to target a 75% keyword match. NEVER fabricate or invent candidate skills.
3. **No-Spam & Clean Applications**: Strict human review gate before any resume export or application submission. Quality over robotic spam.
4. **Karpathy Simplicity**: "As complex as needed, as simple as possible." Direct HTTP REST/JSON endpoints over brittle headless browsers whenever possible.
5. **Strict Product Manager Decision Gate**: 
   * **ALL architectural, design, product, and interface decisions belong strictly to Neftali (Product Manager).**
   * The Software Engineer **NEVER** makes autonomous product decisions or assumptions.
   * When technical choices exist, the Engineer **MUST ALWAYS ask clarifying questions** and present trade-offs for Neftali's explicit decision.
   * The Engineer **ONLY automates** code building, testing, error-logging, and terminal command execution once approved.
6. **Public Club Safety Guard (Canary C Protection)**:
   * This repository is **public** for Neftali's AI Club and student tech community.
   * **Absolute Zero-Leak Rule**: Never commit private API keys (`.env`), database caches (`career.db`), or personal identifying resumes.
   * All candidate profiles in the codebase must remain generic templates ([`directives/user_stories/PERSONA_TEMPLATE.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/user_stories/PERSONA_TEMPLATE.md)).
7. **Module-by-Module Agile Delivery**: Deliver and test ONE isolated module at a time. Never combine multiple unfinished features.
8. **Novice-Friendly Technical Clarity (Feynman Style)**: Explain technical concepts in clear, simple language with real-world analogies so the Product Manager and club members easily understand system mechanics.

---

## 1. Project Directory Structure

```
Career/
├── directives/
│   ├── research/               # ADRs, JobSpy analysis, MVP specs, TECH_STACK.md
│   │   ├── ARCHITECTURAL_DECISION_RECORDS.md
│   │   ├── JOBSPY_RESEARCH_AND_ANALYSIS.md
│   │   ├── MVP_SPECIFICATION_AND_DOD.md
│   │   └── TECH_STACK.md       # Full production stack specifications & proposals
│   └── user_stories/          # Clean persona templates
├── execution/
│   ├── output/                # Job scraped data, CSVs, resumes
│   ├── parsers/               # (Reserved for Module 1 resume parsing)
│   ├── prototype/             # Encapsulated Phase 0 prototype pipeline
│   │   ├── error_log.md       # Self-annealing error footprint
│   │   ├── notifier/          # Email notification service (Gmail SMTP / Resend)
│   │   ├── review/            # Automated CodeRabbit AST & security reviewer
│   │   ├── scrapers/          # ATS harvesters, geo-filters, link validator
│   │   ├── storage/           # SQLite persistence & link maintenance
│   │   └── tests/             # Unit test suite
│   └── tailor/                # (Reserved for Module 1 resume tailoring)
├── .env.example               # Sanitized environment variable template
├── .gitignore                 # Zero-leak public protection rules
├── README.md                  # Public overview & getting started
├── progress_log.md            # Living chronological session log (START HERE)
└── todo.md                    # Active sprint tracking & verification checklist
```

---

## 2. Project History & Agile Evolution

1. **Sprint 1 (Phase 0 Prototype MVP)**:
   - Built direct public ATS harvester targeting Greenhouse, Lever, Ashby, and Workday.
   - Built canonical URL sanitizer, Workday requisition regex deduplicator, and subdomain brand resolver.
   - Implemented 5-worker concurrent link validator and native Gmail SMTP morning email digest.
   - Tagged and preserved on GitHub as release `v0.1.0-prototype`.
2. **Architecture & Scope Expansion**:
   - Encapsulated prototype into [`execution/prototype/`](file:///g:/My%20Drive/AntigravityProjects/Career/execution/prototype) and moved deliverables to [`execution/output/`](file:///g:/My%20Drive/AntigravityProjects/Career/execution/output).
   - Adopted dynamic Vercel web application model linked via Dallas College AI Club GitHub Pages gateway.
   - Standardized 4 milestones on GitHub tracking: Phase 0 (Prototyping & Ingestion), Module 1 (Resume Builder), Module 2 (Smart Apply), and Module 3 (DFW Market Telemetry).

---

## 3. Team Dynamics & Engineering Workflow

* **Product Manager (Neftali)**:
  * Owns the product vision, design direction, user interface choices, feature priorities, and "the what".
  * Reviews and decides on all architectural decision gates and clarifying questions.
* **Software Engineer (Agent)**:
  * Owns technical architecture, code quality, unit testing, error logging, and "the how".
  * Suggests modern technical implementations (delegated in [`directives/research/TECH_STACK.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/research/TECH_STACK.md)).
  * Always asks clarifying questions before implementing new directions.
  * Executes approved plans step-by-step and module-by-module.
* **Self-Annealing System (`execution/prototype/error_log.md`)**:
  * Any runtime error, parser failure, or rate-limit issue must be recorded in `execution/prototype/error_log.md` with root-cause fixes.
  * The Engineer must inspect this log before proposing code modifications to prevent repeating errors.
* **Code Review Protocol (CodeRabbit Style)**:
  * Run `python execution/prototype/review/code_review.py` before committing or merging:
    1. *Correctness & Regressions*: Does it resolve root cause without breaking existing features?
    2. *Input Sanitization*: Are URLs, company names, and multi-location strings cleaned?
    3. *Type Safety & Exceptions*: Are types hinted and HTTP exceptions caught gracefully?

---

## 4. Storage, Git Worktree & Branching Architecture

### A. Core Storage & Sync Model
* **Drive Persistence**: `g:\My Drive\AntigravityProjects\Career` (Chromebook: `/home/neftalibautista1415/AntigravityProjects/Career`).
* **Directives Stay in Root**: All blueprints, schemas, source guides, and persona templates live centrally in `directives/`.
* **Git Remote**: `https://github.com/netflix2023/DFWCareerDevelopment-.git` (`main` branch).
* **Protected Public Sync**: `.gitignore` strictly protects `.env`, secrets, local SQLite caches (`career.db`), logs, and private candidate artifacts.

### B. Git Worktree Architecture for Competing Implementations
When developing separate implementation paths or competing technical experiments (e.g., comparing a **Chrome Side Panel** vs an **AI Club Web Page**, or **Typst vector PDF** vs **HTML-to-PDF**), use **Git Worktrees** instead of switching branches in place.

* **Standard Worktree Directory Layout**:
  ```
  AntigravityProjects/
  ├── Career/                 # Main branch (Core engine, directives, pipeline)
  ├── Career-web/             # Worktree: feature/club-web-dashboard
  └── Career-extension/       # Worktree: feature/smart-apply-extension
  ```

* **Standard Worktree Commands**:
  ```bash
  # 1. Create a new worktree folder for an experimental feature branch:
  git worktree add ../Career-web -b feature/club-web-dashboard

  # 2. View all active worktrees and their branches:
  git worktree list

  # 3. Clean up and remove a worktree when merged or finished:
  git worktree remove ../Career-web
  ```

### C. Tokenless GitHub CLI/API Automation via Git Credential Manager
When automating GitHub tasks (creating milestones, opening issues, querying releases) without manually generating or hardcoding personal access tokens in `.env`:
* **The Technique**: Use Git's internal credential helper (`git credential fill`) to securely borrow the active GitHub OAuth session token stored in Windows Credential Manager:
  ```bash
  # Query the system Git Credential Manager for the active GitHub OAuth token
  echo "protocol=https`nhost=github.com" | git credential fill
  ```
* **Python Automation Recipe**:
  ```python
  import subprocess, urllib.request, json

  # 1. Fetch token from Windows Git Credential Manager
  p = subprocess.Popen(["git", "credential", "fill"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
  stdout, _ = p.communicate(input="protocol=https\nhost=github.com\n")
  token = next(line.split("password=", 1)[1].strip() for line in stdout.splitlines() if line.startswith("password="))

  # 2. Authenticate REST call to GitHub API
  headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json", "User-Agent": "Agent-CLI"}
  data = json.dumps({"title": "Phase 0: Prototyping & Ingestion", "state": "open"}).encode("utf-8")
  req = urllib.request.Request("https://api.github.com/repos/netflix2023/DFWCareerDevelopment-/milestones", data=data, headers=headers, method="POST")
  with urllib.request.urlopen(req) as resp:
      print("Created:", json.loads(resp.read().decode("utf-8"))["title"])
  ```
* **Benefits**: Works out-of-the-box without requiring `gh` CLI installation or manual token management, keeping `.env` completely free of sensitive GitHub tokens.

---

## 5. Anti-Hallucination & Anti-Scraping Guards

* **Canary A (Context Warning)**: Warn PM at 10–12 turns; persist active state to [`progress_log.md`](file:///g:/My%20Drive/AntigravityProjects/Career/progress_log.md).
* **Canary B (Filesystem Verification)**: Verify files physically exist before proposing edits or imports.
* **Canary C (Public Security & Privacy Guard)**: Verify `.gitignore` is active and scan files for raw API keys or personal candidate PII before committing.
* **Canary D (Guest Scraping Protocol)**:
  * **Never scrape logged in**: Never feed personal session cookies into scripts. Always use unauthenticated/guest endpoints.
  * **Keep batch sizes small**: Fetch 25–50 listings every 6–12 hours. Never hammer endpoints with 2,000 requests.
  * **Add random jitter**: Insert random delays (`time.sleep(random.uniform(2, 5))`) between requests.
* **Canary E (Resume Truth Guard)**: Ground all tailored bullets and STAR answers strictly in candidate project documentation. Never invent unheld skills.
* **Canary F (Submission Velocity Guard)**: Never autofill forms instantaneously. Simulate human keystroke delays to avoid bot blacklists.
* **Canary G (Git Safety Guard - Commits & Pushes)**:
  * **Zero Autonomous Git Actions**: The Engineer NEVER commits or pushes code without explicit, written Product Manager (Neftali) approval.
  * Never force-push `main`. All commits, branches, and pushes require explicit PM authorization.
* **Canary H (Flexible Tech Stack Guard)**:
  * Tech recommendations are **flexible candidate proposals, NOT set in stone** (see [`directives/research/TECH_STACK.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/research/TECH_STACK.md)).
