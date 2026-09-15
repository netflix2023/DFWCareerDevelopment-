# Architectural Decision Records (ADR)

> **Quick Summary**: Concise record of core system architecture decisions. All decisions are approved by Product Manager (**Neftali**).

---

## Decision Summary Table

| ADR | Topic | Decision | Why (Core Reason) |
|---|---|---|---|
| **001** | **Web Architecture** | **Dynamic Web App on Vercel Integrated & Linked via Club GitHub Pages Card** | Gives users a powerful, real-time AI & resume studio on Vercel while integrating cleanly into the main club GitHub Pages site, with automatic 1-click PR preview links. |
| **002** | **Forkability & Scope** | **City-Agnostic Metro Configuration (`metro_profiles.json`)** | Allows any student or contributor in Austin, Houston, NYC, etc. to fork the repository and change the target city with 1 setting. |
| **003** | **Database Architecture** | **Neon Serverless PostgreSQL with `pgvector` & Dual Connection Routing** | Provides serverless auto-scaling Postgres with pgvector embeddings; uses pooled HTTP connection for Next.js and unpooled direct connection for Python data ingestion. |

---

## Detailed Decision Records

### ADR-001: Dynamic Web App on Vercel Integrated via Club GitHub Pages Card
* **Decision**: 
  1. **Club Website Integration**: The official Dallas College AI Club website (hosted on GitHub Pages) features an interactive project showcase card with a prominent **`Launch Career Studio ↗`** button.
  2. **Dynamic Application on Vercel**: Clicking the button opens the dedicated web app hosted on **Vercel** (running Next.js / React 19 + TypeScript + Tailwind CSS + Shadcn UI).
  3. **Vercel 1-Click PR Previews**: Every Pull Request (PR) on GitHub automatically generates an isolated live test link so our team and CodeRabbit can test UI changes on mobile or desktop before merging.
* **Why**:
  - **Dynamic Power**: Vercel enables real-time server-side API processing, secure API key management, and live data handling without slowing down client devices.
  - **Zero Club Bloat**: The main club website stays clean and fast on GitHub Pages, acting as the welcoming gateway that launches the full studio.
  - **Review Speed**: Eliminates local terminal build requirements when reviewing PRs.

---

### ADR-002: City-Agnostic Forkability (`metro_profiles.json`)
* **Decision**: 
  1. All city-specific hiring clusters, target tech companies, and localized skill demands are decoupled into a centralized config: [`config/metro_profiles.json`](file:///g:/My%20Drive/AntigravityProjects/Career/config/metro_profiles.json).
  2. The web application includes a top-level metro switcher dropdown defaulting to **Dallas–Fort Worth (DFW)**.
* **Why**:
  - Open-source contributors in Austin, Houston, Seattle, or NYC can fork the repository and immediately adapt it to their university/city by editing just one configuration block or toggling the dropdown.

---

### ADR-003: Neon Serverless PostgreSQL with `pgvector` & Dual-Connection Strategy
* **Decision**:
  1. Use **Neon Serverless PostgreSQL** with the `pgvector` extension enabled for both tabular application state and high-dimensional semantic search.
  2. Maintain a strict two-connection contract:
     - `DATABASE_URL` (Pooled): Used by Next.js API routes / TypeScript via `@neondatabase/serverless` for lightweight, one-shot HTTP queries that fit serverless lifecycles.
     - `DATABASE_URL_UNPOOLED` (Direct): Used by Python workers via `psycopg` / `SQLAlchemy` for schema migrations, bulk ETL data scraping ingest, and long transactions.
  3. Provide idempotent DDL (`apps/data/db/schema.sql`) and sample seed (`apps/data/db/seed_mock.sql`) with smoke-test queries verifying HNSW vector indexes.
* **Why**:
  - Zero-maintenance serverless architecture scales to zero during idle periods with instant wake-up.
  - Eliminates serverless connection pool exhaustion on Vercel while granting Python data pipelines full TCP transaction power.
