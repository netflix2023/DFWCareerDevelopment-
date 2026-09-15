-- Idempotent Mock Seed & Smoke-Test Script
-- Target: apps/data/db/seed_mock.sql
-- Proves core query patterns: table lookups, jsonb operations, and pgvector cosine similarity

-- 1. Insert Mock Persona
INSERT INTO candidate_personas (id, full_name, email, phone, metro_location, work_authorization, skills_matrix)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'Alex Rivera',
    'alex.rivera@example.com',
    '214-555-0199',
    'Dallas-Fort Worth, TX',
    'US Citizen',
    '{"languages": ["Python", "TypeScript", "SQL"], "frameworks": ["FastAPI", "React", "Next.js"], "databases": ["PostgreSQL", "Neon", "Redis"]}'::jsonb
) ON CONFLICT (id) DO NOTHING;

-- 2. Insert Candidate Projects with Vector Placeholders
INSERT INTO candidate_projects (id, persona_id, title, archetype, problem_statement, architecture_action, quantifiable_metric, star_debugging_story, tech_stack, embedding)
VALUES (
    'b0000000-0000-0000-0000-000000000001',
    'a0000000-0000-0000-0000-000000000001',
    'Direct ATS Career Scraper & Harvester',
    'Systems/Backend',
    'Students struggled to discover live technical internships before applicant volume caps filled within 48 hours.',
    'Engineered an unauthenticated ATS harvester in Python supporting Greenhouse, Lever, Ashby, and Workday with canonical deduplication.',
    'Harvested 67 live DFW opportunities with sub-second regex deduplication and concurrent health validation.',
    'Resolved non-deterministic Workday requisition hash collisions across alternate internal board instances.',
    '["Python", "Asyncio", "PostgreSQL", "Regex"]'::jsonb,
    array_fill(0.05::real, ARRAY[1536])::vector(1536)
) ON CONFLICT (id) DO NOTHING;

-- 3. Insert Sample Harvested Jobs
INSERT INTO jobs (id, company, title, location, is_dfw, is_remote, apply_url, role_category, match_score, matched_keywords, missing_keywords, age_days, source, requisition_id)
VALUES (
    'j_capital_one_swe_2026',
    'Capital One',
    'Technology Early Internship Program - Summer 2026',
    'Plano, TX',
    TRUE,
    FALSE,
    'https://capitalone.wd1.myworkdayjobs.com/Capital_One/job/Plano-TX/Early-Internship_R189421',
    'Systems/Backend',
    0.88,
    '["python", "sql", "rest api", "git", "data structures"]'::jsonb,
    '["aws", "ci/cd"]'::jsonb,
    1,
    'Workday',
    'R189421'
) ON CONFLICT (id) DO NOTHING;

-- ====================================================================
-- SMOKE TESTS (Proving core query patterns)
-- ====================================================================

-- Smoke Test 1: Count rows by table
SELECT 'candidate_personas' AS table_name, count(*) AS total_rows FROM candidate_personas
UNION ALL
SELECT 'candidate_projects' AS table_name, count(*) AS total_rows FROM candidate_projects
UNION ALL
SELECT 'jobs' AS table_name, count(*) AS total_rows FROM jobs;

-- Smoke Test 2: High match score jobs lookup in DFW
SELECT company, title, location, match_score, role_category 
FROM jobs 
WHERE is_dfw = TRUE 
ORDER BY match_score DESC 
LIMIT 5;

-- Smoke Test 3: pgvector Cosine Similarity Match
SELECT 
    title,
    archetype,
    1 - (embedding <=> array_fill(0.05::real, ARRAY[1536])::vector(1536)) AS cosine_similarity
FROM candidate_projects
ORDER BY embedding <=> array_fill(0.05::real, ARRAY[1536])::vector(1536)
LIMIT 1;
