"use client";

import React, { useState } from "react";

interface TestMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
  tokens?: number;
  matchScore?: number;
}

export default function DevChatTestPage() {
  const [messages, setMessages] = useState<TestMessage[]>([
    {
      id: "sys-1",
      role: "system",
      content:
        "Developer Sandbox Activated. Ground truth candidate profile loaded (Dallas College AI Club Persona). Ready to test tailoring, bullet quantification, and STAR question responses.",
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [inputPrompt, setInputPrompt] = useState("");
  const [targetJobRole, setTargetJobRole] = useState("Software Engineering Intern");
  const [targetArchetype, setTargetArchetype] = useState("Systems/Backend");
  const [isSynthesizing, setIsSynthesizing] = useState(false);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputPrompt.trim()) return;

    const userMsg: TestMessage = {
      id: `usr-${Date.now()}`,
      role: "user",
      content: inputPrompt,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputPrompt("");
    setIsSynthesizing(true);

    // Simulated local prompt synthesis response based on candidate persona grounding
    setTimeout(() => {
      const assistantMsg: TestMessage = {
        id: `ast-${Date.now()}`,
        role: "assistant",
        content: `[Grounded Output for ${targetJobRole} | Archetype: ${targetArchetype}]\n\n` +
          `• Architected asynchronous ATS harvester in Python using unauthenticated REST endpoints across Greenhouse, Lever, and Workday, capturing 67 live technical requisitions within 24 hours of posting.\n` +
          `• Formulated regex deduplication hash (company::requisition_id) resolving multi-location internal requisition board collisions with sub-second execution.\n` +
          `• Integrated 5-worker concurrent link health validator using HEAD-then-GET fallback, eliminating 404/410 closed postings from student applicant queues.`,
        timestamp: new Date().toLocaleTimeString(),
        matchScore: 0.88,
        tokens: 142,
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsSynthesizing(false);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0c] text-[#ededed] p-6 font-sans">
      <div className="max-w-5xl mx-auto space-y-6">
        {/* Header Banner */}
        <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-zinc-800 pb-5 gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-xs font-mono uppercase tracking-widest text-emerald-400">
                Developer Route · Module 1
              </span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white mt-1">
              Interactive Chat & Prompt Testing Studio
            </h1>
            <p className="text-sm text-zinc-400">
              Test candidate project grounding, STAR question synthesis, and ATS keyword tailoring against candidate persona.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-3 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-xs font-mono text-zinc-300">
              Neon DB: <span className="text-emerald-400">pgvector ready</span>
            </div>
            <div className="px-3 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-xs font-mono text-zinc-300">
              Vercel: <span className="text-sky-400">Serverless App Router</span>
            </div>
          </div>
        </div>

        {/* Configuration Bar */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-zinc-900/60 border border-zinc-800 p-4 rounded-xl">
          <div>
            <label className="block text-xs font-medium text-zinc-400 mb-1">
              Target Role Category
            </label>
            <input
              type="text"
              value={targetJobRole}
              onChange={(e) => setTargetJobRole(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-200 focus:outline-none focus:ring-1 focus:ring-emerald-500 font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-zinc-400 mb-1">
              Architectural Archetype
            </label>
            <select
              value={targetArchetype}
              onChange={(e) => setTargetArchetype(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm text-zinc-200 focus:outline-none focus:ring-1 focus:ring-emerald-500 font-mono"
            >
              <option value="Systems/Backend">Systems/Backend</option>
              <option value="AI/ML & GenAI">AI/ML & GenAI</option>
              <option value="Data Platform">Data Platform</option>
              <option value="Cloud/DevOps">Cloud/DevOps</option>
            </select>
          </div>
        </div>

        {/* Chat Stream Display */}
        <div className="bg-zinc-950/80 border border-zinc-800 rounded-xl p-5 min-h-[420px] max-h-[520px] overflow-y-auto space-y-4 flex flex-col">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`p-4 rounded-lg text-sm max-w-[85%] leading-relaxed ${
                msg.role === "system"
                  ? "bg-zinc-900/40 border border-zinc-800/80 text-zinc-400 self-center text-center font-mono text-xs w-full"
                  : msg.role === "user"
                  ? "bg-emerald-950/40 border border-emerald-800/50 text-emerald-100 self-end ml-auto"
                  : "bg-zinc-900 border border-zinc-800 text-zinc-200 self-start"
              }`}
            >
              <div className="flex items-center justify-between text-[11px] text-zinc-500 mb-1.5">
                <span className="font-semibold uppercase tracking-wider font-mono">
                  {msg.role}
                </span>
                <span>{msg.timestamp}</span>
              </div>
              <p className="whitespace-pre-line">{msg.content}</p>
              {msg.matchScore !== undefined && (
                <div className="mt-2.5 pt-2 border-t border-zinc-800/70 flex gap-4 text-xs font-mono text-zinc-400">
                  <span>Match Score: <strong className="text-emerald-400">{(msg.matchScore * 100).toFixed(0)}%</strong></span>
                  <span>Tokens: <strong className="text-sky-400">{msg.tokens}</strong></span>
                </div>
              )}
            </div>
          ))}

          {isSynthesizing && (
            <div className="bg-zinc-900 border border-zinc-800 p-4 rounded-lg text-xs font-mono text-zinc-400 self-start animate-pulse">
              Synthesizing grounded response using Dallas College AI Club candidate persona...
            </div>
          )}
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSendMessage} className="flex gap-3">
          <input
            type="text"
            placeholder="Paste job description bullet or ask a STAR question (e.g. 'Describe a challenging bug you fixed')..."
            value={inputPrompt}
            onChange={(e) => setInputPrompt(e.target.value)}
            className="flex-1 bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none focus:ring-1 focus:ring-emerald-500 font-sans"
          />
          <button
            type="submit"
            disabled={isSynthesizing || !inputPrompt.trim()}
            className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-medium px-6 py-3 rounded-xl text-sm transition-colors shadow-lg shadow-emerald-950"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
