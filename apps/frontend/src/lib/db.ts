import { neon } from "@neondatabase/serverless";

/**
 * Shared pooled HTTP client for Neon Serverless PostgreSQL.
 * Used for fast, one-shot SQL queries in Next.js Server Components and Route Handlers.
 * Eliminates connection limits and pool exhaustion during Vercel serverless execution.
 */
export const sql = neon(process.env.DATABASE_URL || "");
