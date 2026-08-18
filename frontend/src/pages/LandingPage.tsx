import React from 'react';
import {
  ArrowRight,
  CheckCircle2,
  Code2,
  Cpu,
  FileSearch,
  FolderGit2,
  Layers,
  ShieldCheck,
  Zap,
} from 'lucide-react';
import { Button } from '../components/ui/Button';

interface LandingPageProps {
  onNavigate: (page: string) => void;
  onOpenAddRepo: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate, onOpenAddRepo }) => {
  return (
    <div className="space-y-20 pb-20 relative overflow-hidden tech-grid-bg min-h-screen">
      
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
      <section className="relative pt-12 pb-6 text-center space-y-6 max-w-5xl mx-auto px-4 z-10">
        
        {/* Main Headline with Fredoka Display Font */}
        <h1 className="font-display text-4xl sm:text-6xl md:text-7xl font-bold text-slate-900 tracking-tight leading-[1.1] max-w-4xl mx-auto">
          Revolutionizing Your Operations with <br />
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
            badgeColor="bg-rose-300"
            size="lg"
          >
            Get In Touch
          </Button>

          <Button
            onClick={onOpenAddRepo}
            icon={<ArrowRight className="h-4 w-4 text-slate-900" />}
            badgeColor="bg-amber-300"
            size="lg"
          >
            Learn More
          </Button>
        </div>

        {/* Hero 3D Render Asset */}
        <div className="pt-8 max-w-md sm:max-w-lg mx-auto relative group">
          <div className="absolute -inset-4 bg-gradient-to-r from-blue-400/20 via-cyan-400/20 to-indigo-400/20 rounded-3xl blur-2xl opacity-60 group-hover:opacity-100 transition duration-1000"></div>
          <div className="relative rounded-3xl overflow-hidden bg-white p-3 border border-slate-200/80 shadow-2xl shadow-blue-500/10 transform transition-transform hover:scale-[1.02]">
            <img
              src="/hero_3d_asset.jpg"
              alt="Cortex 3D Cloud Technology"
              className="w-full h-auto object-cover rounded-2xl"
            />
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="max-w-7xl mx-auto px-4 z-10 relative">
        <div className="text-center space-y-2 mb-12">
          <h2 className="font-display text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight">
            Enterprise Inspection Engines
          </h2>
          <p className="text-sm text-slate-500 font-medium max-w-xl mx-auto">
            Deterministic, non-executing engineering analysis powered by specialized AST & SAST scanners.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all duration-300 space-y-4">
            <div className="p-3 bg-blue-50 text-blue-600 rounded-2xl w-fit">
              <Code2 className="h-6 w-6" />
            </div>
            <h3 className="font-display text-xl font-bold text-slate-900">Static Analysis Engine</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Multi-language AST & pattern parsers for Python, TS, JS, Go, Java, Rust.
            </p>
            <div className="text-xs text-slate-600 space-y-2 pt-2 border-t border-slate-100">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Cyclomatic complexity & Maintainability Index</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Code smell detector & window hash duplication</div>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all duration-300 space-y-4">
            <div className="p-3 bg-purple-50 text-purple-600 rounded-2xl w-fit">
              <Layers className="h-6 w-6" />
            </div>
            <h3 className="font-display text-xl font-bold text-slate-900">Architecture Intelligence</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              20+ design pattern detectors and module dependency graphs.
            </p>
            <div className="text-xs text-slate-600 space-y-2 pt-2 border-t border-slate-100">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Hexagonal, Clean, MVC, Microservices style detection</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> React Flow interactive module graph visualizer</div>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all duration-300 space-y-4">
            <div className="p-3 bg-rose-50 text-rose-600 rounded-2xl w-fit">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <h3 className="font-display text-xl font-bold text-slate-900">Security Engine (SAST)</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Committed secrets, vulnerable dependencies, and config scanning.
            </p>
            <div className="text-xs text-slate-600 space-y-2 pt-2 border-t border-slate-100">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Secret detection with Shannon entropy math</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Docker, K8s, GitHub Actions misconfig scanner</div>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all duration-300 space-y-4">
            <div className="p-3 bg-emerald-50 text-emerald-600 rounded-2xl w-fit">
              <FileSearch className="h-6 w-6" />
            </div>
            <h3 className="font-display text-xl font-bold text-slate-900">Maintainability Engine</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              README section parsing, testing maturity, and Git practices.
            </p>
            <div className="text-xs text-slate-600 space-y-2 pt-2 border-t border-slate-100">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> 19 markdown standard section completeness check</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Conventional Commits % & release cadence</div>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all duration-300 space-y-4">
            <div className="p-3 bg-amber-50 text-amber-600 rounded-2xl w-fit">
              <Cpu className="h-6 w-6" />
            </div>
            <h3 className="font-display text-xl font-bold text-slate-900">Repository IQ Engine</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Weighted 0-100 overall score and maturity classification.
            </p>
            <div className="text-xs text-slate-600 space-y-2 pt-2 border-t border-slate-100">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Configurable subsystem score weighting matrix</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Technical debt estimation in hours & days</div>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all duration-300 space-y-4">
            <div className="p-3 bg-cyan-50 text-cyan-600 rounded-2xl w-fit">
              <Zap className="h-6 w-6" />
            </div>
            <h3 className="font-display text-xl font-bold text-slate-900">AI Intelligence Layer</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Extensible LLM provider abstraction (OpenAI, Gemini, Anthropic, Ollama, Mock).
            </p>
            <div className="text-xs text-slate-600 space-y-2 pt-2 border-t border-slate-100">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Deterministic summaries using database findings only</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0" /> Prioritized improvement roadmap generator</div>
            </div>
          </div>

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

