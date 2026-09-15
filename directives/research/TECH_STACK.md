# Production Technology Stack & Technical Specifications (`TECH_STACK.md`)

> **Location**: `directives/research/TECH_STACK.md`  
> **Status**: Approved Production Specification  
> **Owner**: Neftali (Product Manager)  

---

## 1. Production Architecture Layers (5-Layer Model)

The platform is engineered across 5 modular layers adhering to the Dallas College AI Club standard architecture:

| Layer | Component | Production Stack | Purpose & Role |
|---|---|---|---|
| **Layer 5: Client Layer** | Web Studio Application | **Next.js 15 (App Router) + React 19 + TypeScript + Tailwind CSS + Shadcn UI / Radix** | Hosted on **Vercel**. High-polish, responsive career studio with developer test routes (`/dev/chat-test`), dark mode, and real-time interactive resume state. |
| **Layer 4: Output Pipeline** | Differential Resume Compiler | **Typst CLI / Headless Chromium** | Generates pixel-perfect, ATS-verified single-page vector PDFs without hidden tables or parser-breaking CSS. |
| **Layer 3: AI & Vector Engine** | Semantic Search & RAG | **Python + pgvector + LangChain / OpenAI / Gemini** | High-dimensional embeddings for role qualification matching, project relevance clustering, and STAR-method interview answers. |
| **Layer 2: Database & Storage** | Serverless Database | **Neon Serverless PostgreSQL with `pgvector`** | Dual-connection architecture: pooled HTTP connection for Next.js serverless routes, unpooled direct connection for Python bulk ingestion and migrations. |
| **Layer 1: Ingestion & Harvesters** | ATS Scraping Pipeline | **Python 3.13 (Asyncio, HTTP REST, BeautifulSoup, Psycopg)** | Direct harvesters for Greenhouse, Lever, Ashby, and Workday in `apps/data`. |

---

## 2. Database Connection Architecture (Neon Serverless PostgreSQL)

We follow the Dallas College AI Club standardized dual-connection model:

| Environment Variable | Target Runtime | Client Library | Rationale |
|---|---|---|---|
| `DATABASE_URL` (Pooled) | **Next.js (TypeScript)** in `apps/frontend` | `@neondatabase/serverless` (and Drizzle ORM) | One-shot HTTP/WebSocket queries fit serverless lambda lifecycles; connection pooling is handled by Neon without connection exhaustion. |
| `DATABASE_URL_UNPOOLED` (Direct) | **Python Data Pipeline** in `apps/data` | `psycopg` / `SQLAlchemy` | Bulk ETL ingestion, DDL schema migrations, and long transactions require persistent TCP sessions, not transaction-mode pooling. |

### Client Implementations & Connectivity
- **TypeScript Shared Client**: [`apps/frontend/lib/db.ts`](file:///g:/My%20Drive/AntigravityProjects/Career/apps/frontend/lib/db.ts) exports a pooled SQL tagged template client (`neon(process.env.DATABASE_URL!)`) and transaction pool.
- **Python Pipeline Client**: [`apps/data/db/connection.py`](file:///g:/My%20Drive/AntigravityProjects/Career/apps/data/db/connection.py) reads `DATABASE_URL_UNPOOLED` using `psycopg.connect()`.
- **Database Architecture Reference**: [`docs/DATABASE_ARCHITECTURE.md`](file:///g:/My%20Drive/AntigravityProjects/Career/docs/DATABASE_ARCHITECTURE.md).

---

## 3. Monorepo Project Structure

```
Career/
├── apps/
│   ├── frontend/             # Next.js 15 App Router, React 19, TypeScript, Tailwind, Shadcn UI
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── page.tsx               # Career Studio Dashboard
│   │   │   │   ├── dev/
│   │   │   │   │   └── chat-test/
│   │   │   │   │       └── page.tsx       # Hidden Developer Chat & Prompt Test Route
│   │   │   │   └── api/                   # Serverless Route Handlers
│   │   │   ├── components/ui/             # Shadcn UI primitives
│   │   │   └── lib/
│   │   │       └── db.ts                  # Neon pooled client (@neondatabase/serverless)
│   │   ├── package.json
│   │   └── tailwind.config.ts
│   └── data/                 # Python Ingestion Pipeline, DB Migrations & Parsers
│       ├── db/
│       │   ├── schema.sql                 # Neon PostgreSQL + pgvector DDL
│       │   └── seed_mock.sql              # Idempotent seed data & smoke test queries
│       └── scrapers/                      # ATS Harvesters & Qualification Matcher
├── directives/               # Blueprints, ADRs, Persona Templates
├── docs/
│   └── DATABASE_ARCHITECTURE.md           # Neon design & rationale documentation
├── .env.example
├── AGENTS.md
└── progress_log.md
```
