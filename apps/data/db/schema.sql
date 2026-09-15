-- Career Platform: Neon PostgreSQL Database Schema with pgvector
-- Target: apps/data/db/schema.sql
-- Enables vector embeddings for candidate project matching and semantic search

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Jobs Table (Direct ATS Harvested Postings)
CREATE TABLE IF NOT EXISTS jobs (
    id VARCHAR(128) PRIMARY KEY,
    company VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    is_dfw BOOLEAN DEFAULT FALSE,
    is_remote BOOLEAN DEFAULT FALSE,
    apply_url TEXT NOT NULL,
    alternate_urls JSONB DEFAULT '[]'::jsonb,
    role_category VARCHAR(100) NOT NULL,
    match_score NUMERIC(4, 2) DEFAULT 0.0,
    matched_keywords JSONB DEFAULT '[]'::jsonb,
    missing_keywords JSONB DEFAULT '[]'::jsonb,
    age_days INT,
    source VARCHAR(64) NOT NULL,
    requisition_id VARCHAR(128),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_role_category ON jobs(role_category);
CREATE INDEX IF NOT EXISTS idx_jobs_is_dfw ON jobs(is_dfw);
CREATE INDEX IF NOT EXISTS idx_jobs_match_score ON jobs(match_score DESC);

-- 2. Candidate Personas (Ground Truth Profile)
CREATE TABLE IF NOT EXISTS candidate_personas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(64),
    linkedin_url TEXT,
    github_url TEXT,
    metro_location VARCHAR(128) DEFAULT 'Dallas-Fort Worth, TX',
    work_authorization VARCHAR(128) NOT NULL,
    skills_matrix JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Candidate Projects (STAR Grounding with pgvector embeddings)
CREATE TABLE IF NOT EXISTS candidate_projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    persona_id UUID REFERENCES candidate_personas(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    archetype VARCHAR(100) NOT NULL, -- e.g. 'Systems/Backend', 'AI/ML & GenAI', 'Data Platform', 'Cloud/DevOps'
    problem_statement TEXT NOT NULL,
    architecture_action TEXT NOT NULL,
    quantifiable_metric TEXT NOT NULL,
    star_debugging_story TEXT,
    tech_stack JSONB NOT NULL DEFAULT '[]'::jsonb,
    embedding vector(1536), -- OpenAI text-embedding-3-small or compatible 1536-dim vector
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- HNSW Vector Index for sub-millisecond approximate nearest neighbor semantic search
CREATE INDEX IF NOT EXISTS idx_candidate_projects_embedding 
ON candidate_projects USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 4. Application Tracking
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    persona_id UUID REFERENCES candidate_personas(id) ON DELETE CASCADE,
    job_id VARCHAR(128) REFERENCES jobs(id) ON DELETE CASCADE,
    status VARCHAR(64) DEFAULT 'Saved', -- 'Saved', 'Applied', 'Interviewing', 'Offer', 'Rejected'
    tailored_resume_url TEXT,
    star_custom_answers JSONB DEFAULT '{}'::jsonb,
    applied_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);

-- 5. Job Subscribers Table (Issue 1 & 2: Email Alert Subscriptions)
CREATE TABLE IF NOT EXISTS job_subscribers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    frequency VARCHAR(32) DEFAULT 'daily_24h', -- 'instant', 'daily_24h', 'weekly'
    is_active BOOLEAN DEFAULT TRUE,
    target_metro VARCHAR(64) DEFAULT 'DFW',
    unsubscribe_token VARCHAR(64) NOT NULL,
    last_notified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_subscribers_active ON job_subscribers(is_active);
CREATE INDEX IF NOT EXISTS idx_subscribers_email ON job_subscribers(email);
