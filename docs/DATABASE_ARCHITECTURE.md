# Database Architecture & Connection Rationale (`DATABASE_ARCHITECTURE.md`)

> **Location**: `docs/DATABASE_ARCHITECTURE.md`  
> **Target Database**: Neon Serverless PostgreSQL + `pgvector`  
> **Architectural Pattern**: Dual Connection Model (Pooled HTTP for Next.js, Unpooled Direct TCP for Python ETL)  

---

## 1. Overview & Rationale

Our platform requires high-speed applicant tracking, live ATS job scraping, role qualification scoring, and AI-driven candidate project relevance matching. We use **Neon Serverless PostgreSQL** with the **`pgvector`** extension to unify transactional data and high-dimensional vector embeddings in a single database.

### Why Neon Serverless PostgreSQL?
1. **Serverless Auto-Scaling**: Scales compute to zero when idle, eliminating hosting costs during off-peak periods while instantly waking up when students submit queries.
2. **Native Vector Search (`pgvector`)**: Stores embeddings (e.g. 1536-dimensional or 768-dimensional) directly alongside candidate project bullets and job qualification descriptions, enabling lightning-fast cosine similarity search via HNSW indexes.
3. **Branching Workflows**: Neon provides instant copy-on-write database branches, allowing GitHub Pull Request previews on Vercel to test schema changes against isolated preview databases.

---

## 2. Dual-Connection Architecture Contract

| Environment Variable | Target Runtime | Client Library | Rationale |
|---|---|---|---|
| **`DATABASE_URL`** (Pooled) | **Next.js (TypeScript)** in `apps/frontend` | `@neondatabase/serverless` (and Drizzle ORM) | One-shot HTTP/WebSocket queries fit serverless lambda lifecycles; Neon's PgBouncer pooler prevents connection spikes and exhaustion. |
| **`DATABASE_URL_UNPOOLED`** (Direct) | **Python Data Pipeline** in `apps/data` | `psycopg` / `SQLAlchemy` | DDL schema creation, Alembic migrations, and high-volume ETL bulk upserts require a direct, persistent TCP session with transaction support. |

---

## 3. Database Schema Overview (`apps/data/db/schema.sql`)

The schema organizes data into 4 core domain areas:

1. **`jobs`**: Canonical job postings harvested across Greenhouse, Lever, Ashby, and Workday. Includes company, title, location, direct ATS link, role category, match score, and posting timestamp.
2. **`candidate_personas`**: Candidate ground-truth profile (skills, education, contact info, work history).
3. **`candidate_projects`**: Individual candidate projects with STAR-method descriptions and high-dimensional vector embeddings (`vector(1536)`).
4. **`applications`**: Application lifecycle tracking (Saved, Applied, Interviewing, Offer, Rejected) with tailored resume snapshots.

---

## 4. Reusable Connection Clients

### A. Next.js / TypeScript (`apps/frontend/lib/db.ts`)
```typescript
import { neon } from "@neondatabase/serverless";

// Shared pooled HTTP client for one-shot queries in Next.js Server Components and Route Handlers
export const sql = neon(process.env.DATABASE_URL!);
```

### B. Python Pipeline (`apps/data/db/connection.py`)
```python
import os
import psycopg

def get_direct_connection():
    """Returns a direct unpooled connection for Python ETL workers and schema DDL."""
    unpooled_url = os.environ.get("DATABASE_URL_UNPOOLED") or os.environ.get("DATABASE_URL")
    return psycopg.connect(unpooled_url)
```

---

## 5. Initialization & Seed Verification

```bash
# 1. Initialize schema DDL
psql "$DATABASE_URL_UNPOOLED" -f apps/data/db/schema.sql

# 2. Seed mock data & run smoke tests (exercises tables and HNSW vector index)
psql "$DATABASE_URL_UNPOOLED" -f apps/data/db/seed_mock.sql
```
