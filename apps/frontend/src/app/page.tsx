import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#09090b] text-[#fafafa] flex flex-col font-sans">
      {/* Top Navigation Bar */}
      <header className="border-b border-zinc-800 bg-zinc-950/70 backdrop-blur sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="w-3 h-3 rounded-full bg-emerald-500 shadow-md shadow-emerald-500/50" />
            <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-zinc-200 to-zinc-400 bg-clip-text text-transparent">
              Dallas College AI Club · Career Studio
            </span>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/dev/chat-test"
              className="text-xs font-mono px-3 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-emerald-400 hover:border-emerald-500/50 transition-colors"
            >
              ⚡ /dev/chat-test
            </Link>
            <a
              href="https://github.com/netflix2023/DFWCareerDevelopment-"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-zinc-400 hover:text-white transition-colors"
            >
              GitHub ↗
            </a>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 max-w-6xl mx-auto px-6 py-16 w-full flex flex-col justify-center">
        <div className="max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/60 text-emerald-400 text-xs font-mono">
            <span>Live Direct ATS Intelligence</span>
            <span>·</span>
            <span>DFW Tech & Internships</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight leading-[1.1] text-white">
            Fast-Track Tech Careers & AI Resume Studio.
          </h1>

          <p className="text-lg text-zinc-400 leading-relaxed max-w-2xl">
            Harvest authentic technical internships across Greenhouse, Lever, Ashby, and Workday within hours of posting. Tailor authentic resumes with zero hallucinations using Neon PostgreSQL and pgvector.
          </p>

          <div className="flex flex-wrap gap-4 pt-4">
            <Link
              href="/dev/chat-test"
              className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm transition-colors shadow-lg shadow-emerald-950/60 flex items-center gap-2"
            >
              Launch Dev Chat Sandbox ↗
            </Link>
            <a
              href="https://github.com/netflix2023/DFWCareerDevelopment-"
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-3 rounded-xl bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-200 font-medium text-sm transition-colors flex items-center gap-2"
            >
              View Open Source Repo
            </a>
          </div>
        </div>

        {/* 3 Pillar Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          <div className="p-6 rounded-2xl bg-zinc-950/60 border border-zinc-800/80 hover:border-zinc-700 transition-colors">
            <div className="text-2xl mb-3">⚡</div>
            <h3 className="font-semibold text-white mb-2 text-base">Direct ATS Harvesters</h3>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Unauthenticated REST and Markdown feeds scrape genuine requisitions in under 24 hours, beating candidate caps.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-zinc-950/60 border border-zinc-800/80 hover:border-zinc-700 transition-colors">
            <div className="text-2xl mb-3">🎯</div>
            <h3 className="font-semibold text-white mb-2 text-base">Grounded Resume Tailoring</h3>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Resume Guide 2.0 standard. Never fabricates skills. Aligns candidate projects with exact role keywords.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-zinc-950/60 border border-zinc-800/80 hover:border-zinc-700 transition-colors">
            <div className="text-2xl mb-3">🧬</div>
            <h3 className="font-semibold text-white mb-2 text-base">Neon Serverless pgvector</h3>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Dual-connection PostgreSQL with HNSW indexes for sub-millisecond semantic search and candidate project clustering.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-900 py-6 text-center text-xs text-zinc-600">
        Dallas College AI Club · Career Surge Engine · Built for Student Success
      </footer>
    </div>
  );
}
