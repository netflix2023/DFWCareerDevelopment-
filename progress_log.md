# September Surge Fast-Track: Living Progress Log (`progress_log.md`)

> Living record of session handoffs, active sprint states, and immediate next objectives. Always read this file first when resuming work.

---

## Sprint 1: ATS Job Intelligence Pipeline & Live Harvesting - Session Handoff
- **Timestamp**: 2026-09-08 20:25
- **Lead Developer**: Neftali
- **Status**: Sprint 1 Prototype MVP Completed & Verified; 67 Live Direct ATS Roles Harvested
- **Active Branch**: `main` (Local Commit: `60a2eb4`)

### Completed in this Session:
- [x] **MVP Definition of Done Formulated**: Defined clear gates for data ingestion, deduplication, live link health, persistent SQLite storage, dynamic geo-targeting, and CodeRabbit review.
- [x] **Critical Bug Fixes**:
  1. *Requisition Deduplication Hash*: Fixed `generate_job_id` in [url_utils.py](file:///g:/My%20Drive/AntigravityProjects/Career/execution/scrapers/url_utils.py) to hash on `(norm_company, req_id or title)` WITHOUT `canonical_url`. Duplicate postings across alternate internal boards (e.g. Boeing `EXTERNAL_CAREERS` vs `INTERN`) now match identical job IDs and merge secondary URLs into `alternate_urls`.
  2. *Parent Company Inheritance Leak*: Enforced alphanumeric verification on company names in [base_harvester.py](file:///g:/My%20Drive/AntigravityProjects/Career/execution/scrapers/base_harvester.py); if missing or starting with non-alphanumeric punctuation (↳), falls back immediately to subdomain company resolution.
  3. *Sorting Key Recency Guard*: Updated sorting key in [pipeline.py](file:///g:/My%20Drive/AntigravityProjects/Career/execution/scrapers/pipeline.py) to `-(j.age_days if j.age_days is not None else 99)` under `reverse=True` so missing ages are penalized rather than outranking 1-day-old postings.
- [x] **Pipeline Order & Early Filtering Optimization**:
  - Extracted location and age check upfront before expensive URL canonicalization, regex resolution, hashing, and token scoring. Filters 4,324 candidates down to ~70 in milliseconds.
- [x] **Stream Ingestion & Network Resilience**:
  - Expanded feeds to include `Summer2027-Internships`, `Summer2026-Internships`, `Summer2025-Internships`, and `New-Grad-Positions`.
  - Built [base_harvester.py](file:///g:/My%20Drive/AntigravityProjects/Career/execution/scrapers/base_harvester.py) defining `BaseHarvester` abstract interface and `MarkdownFeedHarvester` with 3-attempt exponential backoff retry against 503/429 network errors.
- [x] **Code Quality & Agent Master Protocol**:
  - Updated [AGENTS.md](file:///g:/My%20Drive/AntigravityProjects/Career/AGENTS.md), [GEMINI.md](file:///g:/My%20Drive/AntigravityProjects/Career/GEMINI.md), and [CLAUDE.md](file:///g:/My%20Drive/AntigravityProjects/Career/CLAUDE.md) requiring agents to always read documentation and use latest packages, querying MCP or browser tools if needed.
  - Ran [code_review.py](file:///g:/My%20Drive/AntigravityProjects/Career/execution/review/code_review.py): **15 files analyzed, 15 Passed, 0 Failed, 0 Warnings**.
- [x] **Feynman Technical Explainer Created**: Authored [docs/FEYNMAN_TECHNICAL_EXPLAINER.md](file:///g:/My%20Drive/AntigravityProjects/Career/docs/FEYNMAN_TECHNICAL_EXPLAINER.md) explaining all 12 core system concepts non-technically using real-world analogies.
- [x] **Future Roadmap & Blueprint Stored**: Authored [directives/FUTURE_ROADMAP_AND_ARCHITECTURE_PLAN.md](file:///g:/My%20Drive/AntigravityProjects/Career/directives/FUTURE_ROADMAP_AND_ARCHITECTURE_PLAN.md) preserving all 3 architectural pillars, 5-layer stack, and feature branching strategy for future sessions.
- [x] **Native Gmail SMTP Dispatcher**: Updated [execution/notifier/email_dispatcher.py](file:///g:/My%20Drive/AntigravityProjects/Career/execution/notifier/email_dispatcher.py) with standard library SMTP; ready for `GMAIL_APP_PASSWORD`.

### Next Session Handoff & Objectives:
- [x] **Connected GitHub Remote**: Linked `origin` to `https://github.com/netflix2023/DFWCareerDevelopment-.git` and pushed `main` successfully. Tagged `v0.1.0-prototype`.
- [x] **Agile Architecture Formalized (4 Modules)**: Restructured project blueprint into 4 core agile modules (Ingestion, Resumes, Automation, Market Telemetry).
- [x] **PM Sovereignty & Git Worktree Protocol**: Updated [AGENTS.md](file:///g:/My%20Drive/AntigravityProjects/Career/AGENTS.md) requiring the Agent to always ask clarifying questions (PM owns all decisions) and establishing Git Worktree guidelines for parallel experiments.
- [x] **Public Club Privacy & Safety**: Added customizable [PERSONA_TEMPLATE.md](file:///g:/My%20Drive/AntigravityProjects/Career/directives/user_stories/PERSONA_TEMPLATE.md) and enforced `.gitignore` zero-leak guard.
- [x] **PM Decision - Client Interface**: Approved **Option C (Hybrid Architecture)** — React 19 + TypeScript + Tailwind CSS Web Dashboard as the main club hub, with a lightweight Manifest V3 Chrome Extension as a companion power tool.
- [x] **PM Decision - GitHub Organization**: Approved 4 Milestones mapping to the 4 modules on GitHub. Issues held until planning phase concludes.
- [x] **Directory Reorganization & Prototype Encapsulation**:
  - Moved Phase 1 prototype pipeline into `execution/prototype/` (`scrapers/`, `storage/`, `notifier/`, `review/`, `tests/`, `error_log.md`).
  - Moved deliverables folder `output/` into `execution/output/` (`scrapers/`, `clean_csvs/`, `tailored_resumes/`).
  - Removed redundant `docs/` folder.
  - Updated all Python relative imports and root directory traversal paths (`sys.path.insert` and `DEFAULT_DB_PATH`).
  - Verified all 11/11 unit tests and 15/15 CodeRabbit security/AST review checks pass cleanly.
- [x] **Milestone Realignment & Status Clarification**:
  - Reopened and updated GitHub Milestone #1 to: `Phase 0: Prototyping, Research & Direct ATS Ingestion Pipeline` (Status: In Progress).
- [x] **Agent Manual & Context Refactoring**:
  - Delegated tech stack details and candidate proposals from `AGENTS.md` to [`directives/research/TECH_STACK.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/research/TECH_STACK.md).
  - Streamlined `AGENTS.md` (and synced `GEMINI.md`/`CLAUDE.md`) to focus on core operating rules, engineering workflow, project structure, project history, and explicit quickstart instructions requiring new agent conversations to start by reading [`progress_log.md`](file:///g:/My%20Drive/AntigravityProjects/Career/progress_log.md).
- **Immediate Next Phase**: Complete Phase 0 scraper research and proceed to Module 1 (Resume Builder) & Web Dashboard data contracts.

---

## Sprint 2: Module 1 Architecture, Neon Database & Next.js Monorepo Transition
- **Timestamp**: 2026-09-14 19:30
- **Lead Developer & Product Manager**: Neftali
- **Status**: Architecture Approved & Blueprint Synchronized
- **Active Decisions & Milestones**:
  - [x] **Database Formalized (Neon Serverless PostgreSQL + `pgvector`)**:
    - Decided on **Neon Serverless PostgreSQL** with `pgvector` extension.
    - Updated [`directives/research/TECH_STACK.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/research/TECH_STACK.md) and [`directives/research/ARCHITECTURAL_DECISION_RECORDS.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/research/ARCHITECTURAL_DECISION_RECORDS.md) (ADR-003).
    - Established strict dual-connection contract:
      - `DATABASE_URL` (Pooled): Next.js API routes & TypeScript via `@neondatabase/serverless`.
      - `DATABASE_URL_UNPOOLED` (Direct): Python ETL workers & DDL schema migrations via `psycopg`.
    - Created [`docs/DATABASE_ARCHITECTURE.md`](file:///g:/My%20Drive/AntigravityProjects/Career/docs/DATABASE_ARCHITECTURE.md), DDL schema [`apps/data/db/schema.sql`](file:///g:/My%20Drive/AntigravityProjects/Career/apps/data/db/schema.sql), and idempotent mock seed with smoke tests [`apps/data/db/seed_mock.sql`](file:///g:/My%20Drive/AntigravityProjects/Career/apps/data/db/seed_mock.sql).
    - Updated [`.env.example`](file:///g:/My%20Drive/AntigravityProjects/Career/.env.example) with pooled and unpooled Neon connection templates.
  - [x] **Frontend Stack Confirmed**:
    - **Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS + Shadcn UI**.
    - Clarified React vs. Tailwind vs. Shadcn UI synergy.
    - Monorepo structure defined: `apps/frontend` (Next.js studio with hidden `/dev/chat-test` dev route) and `apps/data` (Python scrapers & db).
  - [x] **Node.js Environment Setup**: Successfully installed Node.js LTS (v24.19.0) and npm (v11.17.0).
  - [x] **Milestone 0 Issues Scoped & Formalized**:
    - **Issue 1**: Web Prototype Job Feed (<24hr Listings, Qualifications Summary, Active Link Pruning & Email Digest Dispatch).
    - **Issue 2**: Neon DB Subscriber Registry (`job_subscribers`), Unsubscribe Routing & Scraper Direct Sync.
    - Updated [`todo.md`](file:///g:/My%20Drive/AntigravityProjects/Career/todo.md), [`apps/data/db/schema.sql`](file:///g:/My%20Drive/AntigravityProjects/Career/apps/data/db/schema.sql), and [`implementation_plan.md`](file:///C:/Users/neftali/.gemini/antigravity-ide/brain/45e83b63-20ca-429d-b761-89dbd2f0b982/implementation_plan.md).
