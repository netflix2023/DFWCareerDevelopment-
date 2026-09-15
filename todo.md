# Career Surge Engine: 4-Module Agile Master Roadmap (`todo.md`)

> **Collaboration Contract**: Neftali = Product Manager (The What & All Decisions) | Agent = Software Engineer (Code & The How)  
> **Rule**: Agent NEVER decides product, architectural, or interface direction. All decisions belong to Neftali.  
> **Git Worktrees**: Use isolated worktrees for parallel competing technical experiments (e.g. `Career-web` vs `Career-extension`).  

---

## Master Architecture: The 4 Core Modules

### 🟡 Phase 0: Prototyping, Research & Ingestion Pipeline (Active Sprint)
*Status: In Progress (Active Prototyping & Scraper Research)*

- [x] **0.1 Canonical Normalization & Deduplication (Prototype)**
  - [x] Workday requisition regex extraction (`f"{company}::{requisition_id}"`) and secondary URL merging
  - [x] Subdomain brand resolution fallback for arrow (`↳`) or empty strings
  - [x] Multi-location blob cleaning to `"Dallas, TX (Multi-Location)"`
- [ ] **0.2 Scraper Prototyping & High-Throughput Research (In Progress)**
  - [x] Direct markdown feed harvester prototype (`execution/prototype/scrapers/pipeline.py`)
  - [ ] Unauthenticated guest scraper testing (LinkedIn guest API, Indeed aggregator, JobSpy evaluation)
  - [ ] Rate-limiting queues & jitter backoff calibration
- [x] **0.3 Live Link Health & Verification (Prototype)**
  - [x] 5-worker concurrent validator (`ThreadPoolExecutor`) with HEAD-then-GET check (5s timeout)
  - [x] Pruning of 404s, 410s, and closed requisition redirects
- [x] **0.4 Daily Morning Notification Dispatcher (Prototype)**
  - [x] Responsive HTML email digest with Top 10 positions and 1-click apply links
  - [x] Free native Gmail SMTP (`smtp.gmail.com:587`) + Resend API integration

---

### 🟡 Module 1: Multi-Persona Resume Builder, Neon Vector Persistence & Web Studio
*Status: Active Sprint (Architecture Approved)*

- [x] **1.0 Database Architecture (Neon Serverless PostgreSQL + `pgvector`)**
  - [x] Dual-connection design: pooled HTTP (`DATABASE_URL`) for Next.js and unpooled direct (`DATABASE_URL_UNPOOLED`) for Python
  - [x] Authored DDL schema: [`apps/data/db/schema.sql`](file:///g:/My%20Drive/AntigravityProjects/Career/apps/data/db/schema.sql) with HNSW vector index
  - [x] Authored idempotent mock seed & smoke tests: [`apps/data/db/seed_mock.sql`](file:///g:/My%20Drive/AntigravityProjects/Career/apps/data/db/seed_mock.sql)
  - [x] Authored rationale documentation: [`docs/DATABASE_ARCHITECTURE.md`](file:///g:/My%20Drive/AntigravityProjects/Career/docs/DATABASE_ARCHITECTURE.md)
- [ ] **1.1 Web Application Setup (`apps/frontend`)**
  - [ ] Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS + Shadcn UI
  - [ ] Shared Neon pooled database client ([`apps/frontend/lib/db.ts`](file:///g:/My%20Drive/AntigravityProjects/Career/apps/frontend/lib/db.ts))
  - [ ] Developer-only testing playground route (`/dev/chat-test`)
- [ ] **1.2 Ingestion Pipeline Adaptation (`apps/data/scrapers`)**
  - [ ] Direct Neon PostgreSQL bulk upsert adapter (`apps/data/scrapers/db_loader.py`)
  - [ ] Multi-archetype keyword clustering (Systems/Backend, AI/ML & GenAI, Data Platform, Cloud/DevOps)
- [ ] **1.3 Role Persona Clustering (Vector Mapping)**
  - [ ] Embed candidate project catalog into 1536-dim vector space for relevance re-ranking via `pgvector`
- [ ] **1.4 Deterministic Semantic Claim Linter**
  - [ ] Linter checks candidate bullets against job posting priorities
  - [ ] Prompts candidate to quantify claims: throughput (QPS/RPS), latency (p99/ms), and data scale (GB/TB)
- [ ] **1.5 Differential Resume Compilation**
  - [ ] Single-page ATS-verified vector PDF generator (Typst compiler or Tailwind-to-PDF)

---

### ⚪ Module 3: Application Automation & Smart Apply
*Status: Approved PM Direction — Option C (Hybrid: React Web Dashboard first, Companion Chrome Extension second)*

- [ ] **3.1 STAR-Method Custom Question Synthesis**
  - [ ] Local RAG grounded strictly in candidate project documentation
  - [ ] Drafts authentic, structured answers for bespoke questions (e.g., "Describe a difficult bug you fixed")
- [ ] **3.2 Submission Velocity & Anti-Bot Protection**
  - [ ] Natural typing pacing (jittered delays) across long-form answer boxes
  - [ ] Maximum 50 fields per form cycle to avoid ATS velocity blacklisting
- [ ] **3.3 Client Interface: Hybrid Architecture (PM Approved)**
  - [ ] *Primary Hub*: AI Club Web Dashboard (React 19 + TypeScript + Tailwind CSS)
  - [ ] *Companion Plugin*: Manifest V3 Chrome Extension & Side Panel for on-page form pre-fill

---

### ⚪ Module 4: DFW Market Intelligence, Trends & Temporal Telemetry
*Status: Upcoming Phase*

- [ ] **4.1 Temporal Cadence Modeling & First-Mover Index**
  - [ ] Track company posting schedules (e.g. cadence by day-of-week and time-of-day)
  - [ ] Alert club members to apply in the first 15–30 minutes before 50–100 candidate caps hit
- [ ] **4.2 Ghost Job & Stale Requisition Detection**
  - [ ] Cross-reference posting ID longevity, re-indexing dates, and team turnover
  - [ ] Flag stale or abandoned listings before candidates waste time applying
- [ ] **4.3 DFW Tech Stack Market Demand Analytics**
  - [ ] Aggregate skill frequency across Dallas, Plano, Irving, Richardson, and Fort Worth
  - [ ] Provide club members with high-ROI skill recommendations for upcoming hiring cycles
