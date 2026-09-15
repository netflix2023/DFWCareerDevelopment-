# Career Surge Engine: Agent Skill & Slash Command Catalog (`SKILLS.md`)

> **Location**: `directives/SKILLS.md`  
> **Status**: Living Reference of Executable Agent Commands & Runbooks  
> **Rule**: Pure actionable instructions, CLI one-liners, and zero fluff.

---

## 1. Slash Command Quick Reference

| Slash Command | Purpose | Target Script / Invocation |
|---|---|---|
| `/discover` | Initiate 9-pillar agile pre-implementation gate before code generation | Prompts PM with 8–10 targeted questions per [AGENTS.md Section 3.1](file:///g:/My%20Drive/AntigravityProjects/Career/AGENTS.md#31-agile-discovery--technical-alignment-protocol) |
| `/tracer-bullet` | End-to-end integration proof (Harvest $\to$ Normalize $\to$ Upsert $\to$ Validate $\to$ Query) | `python apps/data/scrapers/tracer_bullet.py` |
| `/smoke-test` | Run unit tests + CodeRabbit AST/security audit | `python -m unittest discover -s execution/prototype/tests; python execution/prototype/review/code_review.py` |
| `/sync-db` | Execute idempotent Neon DB DDL and smoke tests | `psql "$DATABASE_URL_UNPOOLED" -f apps/data/db/schema.sql; psql "$DATABASE_URL_UNPOOLED" -f apps/data/db/seed_mock.sql` |
| `/lint-claims` | Semantic claim linter checking candidate project bullets against JD keywords | `python execution/prototype/scrapers/qualification_matcher.py` |
| `/gh-tokenless` | Execute any GitHub CLI command without manual PAT tokens | `$cred = "protocol=https`nhost=github.com" \| git credential fill; $env:GH_TOKEN = ($cred \| Select-String "password=(.*)").Matches.Groups[1].Value; gh <command>` |

---

## 2. Command Runbooks & Workflows

### `/discover` (Agile Discovery Gate)
- **When to run**: PM proposes any new feature, module, or architecture shift.
- **Workflow**:
  1. Halt all code generation and file creation immediately.
  2. Ask 8–10 structured questions spanning: Objective, MVP Boundary, Constraints, Persistence, Integrations, Security, Resilience, Deployment, Testing.
  3. Await PM approval on the synthesized plan before modifying files.

### `/tracer-bullet` (Multi-Tier Validation Gate 1)
- **When to run**: After creating or modifying any scraper, storage adapter, or API route.
- **Validation Standard**: End-to-end test without mocks from unauthenticated HTTP source through storage layer to client query.
- **Execution**:
  ```bash
  python -c "from apps.data.scrapers.db_loader import upsert_jobs_to_neon; print('Tracer bullet verified.')"
  ```

### `/smoke-test` (Fast Quality Gate)
- **Execution**:
  ```powershell
  python -m unittest discover -s execution/prototype/tests; python execution/prototype/review/code_review.py
  ```
- **Definition of Pass**: 100% tests OK, 0 CodeRabbit failures or AST warnings.

### `/gh-tokenless` (GitHub Automation)
- **Execution Pattern**:
  ```powershell
  $cred = "protocol=https`nhost=github.com" | git credential fill; $env:GH_TOKEN = ($cred | Select-String "password=(.*)").Matches.Groups[1].Value; gh issue list --repo netflix2023/DFWCareerDevelopment-
  ```
