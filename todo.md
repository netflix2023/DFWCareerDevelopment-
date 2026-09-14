# Career Surge Engine: 4-Module Agile Master Roadmap (`todo.md`)

> **Collaboration Contract**: Neftali = Product Manager (The What & All Decisions) | Agent = Software Engineer (Code & The How)  
> **Rule**: Agent NEVER decides product, architectural, or interface direction. All decisions belong to Neftali.  
> **Git Worktrees**: Use isolated worktrees for parallel competing technical experiments (e.g. `Career-web` vs `Career-extension`).  

---

## Master Architecture: The 4 Core Modules

### 🟢 Module 1: Direct ATS Ingestion, Rate-Limiting & Notifications
*Status: Completed & Verified (Preserved in Git release tag `v0.1.0-prototype`)*

- [x] **1.1 Canonical Normalization & Deduplication**
  - [x] Workday requisition regex extraction (`f"{company}::{requisition_id}"`) and secondary URL merging
  - [x] Subdomain brand resolution fallback for arrow (`↳`) or empty strings
  - [x] Multi-location blob cleaning to `"Dallas, TX (Multi-Location)"`
- [x] **1.2 High-Throughput Ingestion & Rate-Limiting Protocol**
  - [x] Unauthenticated guest scraping mode (zero personal cookies, batch 25–50 listings, jitter delays 2–5s)
  - [x] Stream ingestion across active internship boards with exponential backoff
- [x] **1.3 Live Link Health & Verification**
  - [x] 5-worker concurrent validator (`ThreadPoolExecutor`) with HEAD-then-GET check (5s timeout)
  - [x] Pruning of 404s, 410s, and closed requisition redirects
- [x] **1.4 Daily Morning Notification Dispatcher**
  - [x] Responsive HTML email digest with Top 10 positions and 1-click apply links
  - [x] Free native Gmail SMTP (`smtp.gmail.com:587`) + Resend API integration

---

### 🟡 Module 2: Multi-Persona Resume Builder, Claim Linter & Differential Generator
*Status: Active Sprint (Implementation Pending PM Decisions)*

- [ ] **2.1 Role Persona Clustering (Vector Mapping)**
  - [ ] Categorize target roles into 4 core architectural archetypes: Systems/Backend, AI/ML & GenAI, Data Platform, Cloud/DevOps
  - [ ] Embed candidate project catalog into vector space for automated relevance re-ranking
  - [ ] *Worktree Experiment A*: Local FastEmbed / sentence-transformers
  - [ ] *Worktree Experiment B*: Dockerized Qdrant / pgvector
- [ ] **2.2 Deterministic Semantic Claim Linter**
  - [ ] Linter checks candidate bullets against job posting priorities
  - [ ] Prompts candidate to quantify claims: throughput (QPS/RPS), latency (p99/ms), and data scale (GB/TB)
- [ ] **2.3 Differential Resume Compilation**
  - [ ] *Worktree Experiment A (`feature/resume-typst`)*: Typst compiler producing ATS-verified single-page vector PDFs
  - [ ] *Worktree Experiment B (`feature/resume-html-pdf`)*: Tailwind/HTML templates rendered via Headless Chromium

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
