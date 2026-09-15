# Production Technology Stack & Technical Proposals (`TECH_STACK.md`)

> **Location**: `directives/research/TECH_STACK.md`  
> **Status**: Living Reference & Flexible Architectural Proposals  
> **Owner**: Neftali (Product Manager)  

---

## 1. Production Architecture Layers (5-Layer Model)

The full platform is designed across 5 modular layers to showcase modern, industry-standard AI and full-stack software engineering practices:

| Layer | Component | Proposed Stack | Purpose & Role |
|---|---|---|---|
| **Layer 5: Client Layer** | Interactive Interface | **React 19 + TypeScript + Tailwind CSS** (Vercel) + Companion Manifest V3 Chrome Extension | High-polish web studio for AI Club members integrated into the main club GitHub Pages site, with optional companion Chrome extension for on-page apply assistance. |
| **Layer 4: Output Pipeline** | Differential Resume Compiler | **Typst CLI / Headless Chromium** | Generates pixel-perfect, ATS-verified 1-page vector PDFs without hidden tables or parser-breaking CSS. |
| **Layer 3: AI & Vector Engine** | Archetype Clustering & STAR RAG | **Python + FastEmbed / Qdrant + LangChain** | Local embeddings for matching candidate projects to role requirements; grounded STAR-method answer synthesis. |
| **Layer 2: Data & Queue** | Persistence & Scheduling | **PostgreSQL / SQLite + Celery / Redis** | ACID transaction storage, temporal cadence modeling, and rate-limit queues. |
| **Layer 1: Ingestion Pipeline** | Direct ATS Harvesters | **Python Asyncio + HTTP REST / GraphQL** | Polling Greenhouse, Lever, Ashby, Workday, and unauthenticated guest sources. |

---

## 2. Technical Stack Flexibility Principle (Canary H)

- All technical proposals (FastAPI, React/TS, Typst, PostgreSQL, Qdrant, Chrome Extension) are **flexible candidate proposals, NOT set in stone**.
- They serve as a modular menu of high-ROI technologies that can be swapped, adapted, or redesigned whenever the Product Manager (**Neftali**) decides.
- For all architectural decisions and trade-offs, consult [`directives/research/ARCHITECTURAL_DECISION_RECORDS.md`](file:///g:/My%20Drive/AntigravityProjects/Career/directives/research/ARCHITECTURAL_DECISION_RECORDS.md).
