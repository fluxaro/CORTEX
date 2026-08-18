import React from 'react';
import {
  ArrowRight,
  Code2,
  Cpu,
  FileSearch,
  Layers,
  ShieldCheck,
  Zap,
  Sparkles,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { PlayfulCard } from '../components/ui/Card';

interface LandingPageProps {
  onNavigate: (page: string) => void;
  onOpenAddRepo: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate, onOpenAddRepo }) => {
  return (
    <div className="space-y-16 pb-20 overflow-x-hidden tech-grid-bg min-h-screen">
      
      {/* Background Subtle Tech Circuit Trace Side SVG Accents */}
      <div className="absolute top-10 left-0 w-72 h-[600px] pointer-events-none opacity-20 hidden lg:block">
        <svg viewBox="0 0 200 600" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full stroke-slate-400">
          <path d="M0 50 H80 L120 90 V250 L160 290 H200" strokeWidth="1.5" strokeDasharray="4 4" />
          <path d="M0 180 H50 L90 220 V380 L140 430 H200" strokeWidth="1.5" />
          <circle cx="80" cy="50" r="4" fill="#2563eb" />
          <circle cx="120" cy="90" r="4" fill="#2563eb" />
          <circle cx="160" cy="290" r="4" fill="#2563eb" />
        </svg>
      </div>

      <div className="absolute top-10 right-0 w-72 h-[600px] pointer-events-none opacity-20 hidden lg:block">
        <svg viewBox="0 0 200 600" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full stroke-slate-400">
          <path d="M200 50 H120 L80 90 V250 L40 290 H0" strokeWidth="1.5" strokeDasharray="4 4" />
          <path d="M200 180 H150 L110 220 V380 L60 430 H0" strokeWidth="1.5" />
          <circle cx="120" cy="50" r="4" fill="#2563eb" />
          <circle cx="80" cy="90" r="4" fill="#2563eb" />
          <circle cx="40" cy="290" r="4" fill="#2563eb" />
        </svg>
      </div>

      {/* Hero Section */}
      <section className="text-center space-y-6 pt-10 sm:pt-16 max-w-4xl mx-auto px-4 z-10 relative">
        {/* Title */}
        <h1 className="font-display text-4xl sm:text-6xl lg:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.1]">
          Revolutionizing Your Operations with <br className="hidden sm:inline" />
          <span className="text-blue-600">Scalable Technology</span>
        </h1>

        {/* Subtitle */}
        <p className="text-slate-500 text-base sm:text-lg max-w-xl mx-auto font-medium leading-relaxed">
          Empowering you with next-gen financial & repository intelligence solutions.
        </p>

        {/* Hero Pill CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
          <Button
            onClick={() => onNavigate('repositories')}
            icon={<ArrowRight className="h-4 w-4 text-slate-900" />}
            badgeColor="bg-blue-200 text-blue-900"
            size="lg"
          >
            Get In Touch
          </Button>

          <Button
            onClick={onOpenAddRepo}
            icon={<ArrowRight className="h-4 w-4 text-slate-900" />}
            badgeColor="bg-cyan-200 text-cyan-900"
            size="lg"
          >
            Learn More
          </Button>
        </div>
      </section>

      {/* Floating Badges & Expert Team Header (Page-Aligned Blue/Slate Theme) */}
      <section className="max-w-7xl mx-auto px-4 z-10 relative">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6 mb-10 px-2">
          {/* Left: Team Avatar Badge Pill */}
          <div className="inline-flex items-center gap-3 px-5 py-2.5 rounded-full bg-white border border-slate-200/80 shadow-sm">
            <div className="flex -space-x-2 overflow-hidden">
              <img className="inline-block h-8 w-8 rounded-full ring-2 ring-white object-cover" src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop&q=80" alt="Team 1" />
              <img className="inline-block h-8 w-8 rounded-full ring-2 ring-white object-cover" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80" alt="Team 2" />
              <img className="inline-block h-8 w-8 rounded-full ring-2 ring-white object-cover" src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80" alt="Team 3" />
            </div>
            <div className="text-left">
              <p className="text-xs font-bold text-slate-900 leading-tight">Enterprise Code Intelligence</p>
              <p className="text-[11px] font-semibold text-slate-500">Know your code before you clone it</p>
            </div>
          </div>

          {/* Right: Floating Tag Pills in Page-Aligned Color Palette */}
          <div className="flex flex-wrap items-center justify-center md:justify-end gap-3">
            <span className="px-4 py-1.5 rounded-full bg-blue-100 text-blue-900 font-extrabold text-xs tracking-wide shadow-sm rotate-[-4deg] border border-blue-300/60">
              STATIC AST
            </span>
            <span className="px-4 py-1.5 rounded-full bg-cyan-100 text-cyan-900 font-extrabold text-xs tracking-wide shadow-sm rotate-[3deg] border border-cyan-300/60">
              SAST SCAN
            </span>
            <span className="px-4 py-1.5 rounded-full bg-indigo-100 text-indigo-900 font-extrabold text-xs tracking-wide shadow-sm rotate-[-2deg] border border-indigo-300/60">
              ARCH GRAPH
            </span>
            <span className="px-4 py-1.5 rounded-full bg-emerald-100 text-emerald-900 font-extrabold text-xs tracking-wide shadow-sm rotate-[4deg] border border-emerald-300/60">
              REPO IQ
            </span>
          </div>
        </div>

        {/* Feature Highlights Grid using PlayfulCard aligned with Cortex Blue/Slate Palette */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Card 1: Soft Blue Variant */}
          <PlayfulCard
            tag="Static Analysis"
            title="AST Code Inspector"
            subtitle="Deterministic multi-language AST & pattern parsers for Python, TS, JS, Go, Java & Rust."
            variant="blue"
            arrowPosition="top-right"
            starburstType="blue"
            onClick={() => onNavigate('static-analysis')}
          >
            <div className="flex items-center gap-2 text-xs font-extrabold text-blue-950 bg-white/60 p-2.5 rounded-2xl backdrop-blur-sm border border-blue-200/60">
              <Code2 className="h-4 w-4 shrink-0 text-blue-600" />
              <span>Cyclomatic Complexity & Maintainability Index</span>
            </div>
          </PlayfulCard>

          {/* Card 2: Deep Slate Variant (High Contrast Dark Card matching Navbar/CTA) */}
          <PlayfulCard
            tag="Architecture"
            title="System Graph Visualizer"
            subtitle="20+ architectural design pattern detectors & interactive module dependency graphs."
            variant="slate"
            arrowPosition="bottom-right"
            starburstType="scribble"
            centerIcon={<Layers className="h-10 w-10 text-cyan-400" />}
            onClick={() => onNavigate('architecture')}
          >
            <div className="flex items-center gap-2 text-xs font-extrabold text-cyan-200 bg-slate-800/80 p-2.5 rounded-2xl backdrop-blur-sm border border-slate-700">
              <Sparkles className="h-4 w-4 shrink-0 text-cyan-400" />
              <span>Clean Architecture, Hexagonal & Microservices</span>
            </div>
          </PlayfulCard>

          {/* Card 3: Soft Cyan Variant */}
          <PlayfulCard
            tag="Security SAST"
            title="Vulnerability Scanner"
            subtitle="Committed secrets, vulnerable dependencies, and Docker / K8s misconfig scanning."
            variant="cyan"
            arrowPosition="bottom-right"
            starburstType="cyan"
            onClick={() => onNavigate('security')}
          >
            <div className="flex items-center gap-2 text-xs font-extrabold text-cyan-950 bg-white/60 p-2.5 rounded-2xl backdrop-blur-sm border border-cyan-200/60">
              <ShieldCheck className="h-4 w-4 shrink-0 text-cyan-600" />
              <span>Shannon Entropy Secrets & Misconfig Scanners</span>
            </div>
          </PlayfulCard>

          {/* Card 4: Soft Indigo Variant */}
          <PlayfulCard
            tag="Code Health"
            title="Maintainability Index"
            subtitle="Testing maturity, documentation completeness, and Conventional Commit cadence."
            variant="indigo"
            arrowPosition="top-right"
            starburstType="indigo"
            onClick={() => onNavigate('repositories')}
          >
            <div className="flex items-center gap-2 text-xs font-extrabold text-indigo-950 bg-white/60 p-2.5 rounded-2xl backdrop-blur-sm border border-indigo-200/60">
              <FileSearch className="h-4 w-4 shrink-0 text-indigo-600" />
              <span>19 Standard Markdown Section Audits</span>
            </div>
          </PlayfulCard>

          {/* Card 5: Soft Emerald Variant */}
          <PlayfulCard
            tag="Repo IQ"
            title="Technical Debt Rating"
            subtitle="Weighted overall 0-100 score matrix and estimated debt reduction in engineering hours."
            variant="emerald"
            arrowPosition="bottom-right"
            starburstType="emerald"
            onClick={() => onNavigate('repositories')}
          >
            <div className="flex items-center gap-2 text-xs font-extrabold text-emerald-950 bg-white/60 p-2.5 rounded-2xl backdrop-blur-sm border border-emerald-200/60">
              <Cpu className="h-4 w-4 shrink-0 text-emerald-600" />
              <span>Configurable Score Weighting Matrix</span>
            </div>
          </PlayfulCard>

          {/* Card 6: Soft Sky Blue Variant */}
          <PlayfulCard
            tag="AI Layer"
            title="LLM Intelligence"
            subtitle="Prioritized AI improvement roadmaps grounded in deterministic scan findings."
            variant="sky"
            arrowPosition="bottom-right"
            starburstType="blue"
            onClick={() => onNavigate('repositories')}
          >
            <div className="flex items-center gap-2 text-xs font-extrabold text-sky-950 bg-white/60 p-2.5 rounded-2xl backdrop-blur-sm border border-sky-200/60">
              <Zap className="h-4 w-4 shrink-0 text-sky-600" />
              <span>OpenAI, Gemini & Anthropic LLM Providers</span>
            </div>
          </PlayfulCard>

        </div>
      </section>

      {/* Call to Action */}
      <section className="max-w-4xl mx-auto px-4 text-center z-10 relative">
        <div className="p-10 sm:p-14 rounded-3xl bg-slate-900 text-white border border-slate-800 shadow-2xl relative overflow-hidden space-y-6">
          <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
          <h2 className="font-display text-3xl sm:text-4xl font-bold tracking-tight">
            Ready to inspect your codebase?
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 max-w-lg mx-auto font-medium">
            Ingest any public GitHub repository URL and receive instant intelligence reports on architecture, security, static metrics, and overall Repository IQ score.
          </p>
          <div className="flex justify-center">
            <Button
              onClick={() => onNavigate('repositories')}
              icon={<ArrowRight className="h-4 w-4 text-slate-900" />}
              badgeColor="bg-cyan-300"
              size="lg"
            >
              Browse Repositories
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};
