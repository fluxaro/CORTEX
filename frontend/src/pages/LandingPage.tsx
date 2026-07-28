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
  Sparkles,
  Zap,
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';

interface LandingPageProps {
  onNavigate: (page: string) => void;
  onOpenAddRepo: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate, onOpenAddRepo }) => {
  return (
    <div className="space-y-16 pb-16">
      {/* Hero Section */}
      <section className="relative pt-12 pb-8 text-center space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary-500/10 border border-primary-500/20 text-xs font-semibold text-primary-400">
          <Sparkles className="h-4 w-4" />
          <span>AI-Powered Repository Intelligence Platform</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-none max-w-4xl mx-auto">
          Know your code <br />
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-emerald-400 to-purple-500">
            before you clone it.
          </span>
        </h1>

        <p className="text-gray-400 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
          ProjectIQ inspects GitHub repositories using multi-language static code analysis, architectural pattern detection, SAST security scanners, and deterministic AI summaries—without running untrusted code.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Button onClick={() => onNavigate('repositories')} variant="primary" size="lg">
            <span>Explore Repositories</span>
            <ArrowRight className="h-5 w-5" />
          </Button>
          <Button onClick={onOpenAddRepo} variant="glass" size="lg">
            <FolderGit2 className="h-5 w-5 text-primary-400" />
            <span>Ingest New Repo</span>
          </Button>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="max-w-7xl mx-auto px-4">
        <div className="text-center space-y-2 mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">Enterprise Inspection Engines</h2>
          <p className="text-xs sm:text-sm text-gray-400">Deterministic, non-executing engineering analysis powered by specialized engines.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card glass className="hover:border-primary-500/50 transition-all">
            <CardHeader>
              <div className="p-2.5 bg-blue-500/10 text-blue-400 rounded-xl w-fit mb-2">
                <Code2 className="h-6 w-6" />
              </div>
              <CardTitle>Static Analysis Engine</CardTitle>
              <CardDescription>Multi-language AST & pattern parsers for Python, TS, JS, Go, Java, Rust.</CardDescription>
            </CardHeader>
            <CardContent className="text-xs text-gray-400 space-y-2">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Cyclomatic complexity & Maintainability Index</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Code smell detector & window hash duplication</div>
            </CardContent>
          </Card>

          <Card glass className="hover:border-purple-500/50 transition-all">
            <CardHeader>
              <div className="p-2.5 bg-purple-500/10 text-purple-400 rounded-xl w-fit mb-2">
                <Layers className="h-6 w-6" />
              </div>
              <CardTitle>Architecture Intelligence</CardTitle>
              <CardDescription>20+ design pattern detectors and module dependency graphs.</CardDescription>
            </CardHeader>
            <CardContent className="text-xs text-gray-400 space-y-2">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Hexagonal, Clean, MVC, Microservices style detection</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> React Flow interactive module graph visualizer</div>
            </CardContent>
          </Card>

          <Card glass className="hover:border-rose-500/50 transition-all">
            <CardHeader>
              <div className="p-2.5 bg-rose-500/10 text-rose-400 rounded-xl w-fit mb-2">
                <ShieldCheck className="h-6 w-6" />
              </div>
              <CardTitle>Security Engine (SAST)</CardTitle>
              <CardDescription>Committed secrets, vulnerable dependencies, and config scanning.</CardDescription>
            </CardHeader>
            <CardContent className="text-xs text-gray-400 space-y-2">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Secret detection with Shannon entropy math</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Docker, K8s, GitHub Actions misconfig scanner</div>
            </CardContent>
          </Card>

          <Card glass className="hover:border-emerald-500/50 transition-all">
            <CardHeader>
              <div className="p-2.5 bg-emerald-500/10 text-emerald-400 rounded-xl w-fit mb-2">
                <FileSearch className="h-6 w-6" />
              </div>
              <CardTitle>Maintainability Engine</CardTitle>
              <CardDescription>README section parsing, testing maturity, and Git practices.</CardDescription>
            </CardHeader>
            <CardContent className="text-xs text-gray-400 space-y-2">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> 19 markdown standard section completeness check</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Conventional Commits % & release cadence</div>
            </CardContent>
          </Card>

          <Card glass className="hover:border-amber-500/50 transition-all">
            <CardHeader>
              <div className="p-2.5 bg-amber-500/10 text-amber-400 rounded-xl w-fit mb-2">
                <Cpu className="h-6 w-6" />
              </div>
              <CardTitle>Repository IQ Engine</CardTitle>
              <CardDescription>Weighted 0-100 overall score and maturity classification.</CardDescription>
            </CardHeader>
            <CardContent className="text-xs text-gray-400 space-y-2">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Configurable subsystem score weighting matrix</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Technical debt estimation in hours & days</div>
            </CardContent>
          </Card>

          <Card glass className="hover:border-cyan-500/50 transition-all">
            <CardHeader>
              <div className="p-2.5 bg-cyan-500/10 text-cyan-400 rounded-xl w-fit mb-2">
                <Zap className="h-6 w-6" />
              </div>
              <CardTitle>AI Intelligence Layer</CardTitle>
              <CardDescription>Extensible LLM provider abstraction (OpenAI, Gemini, Anthropic, Ollama, Mock).</CardDescription>
            </CardHeader>
            <CardContent className="text-xs text-gray-400 space-y-2">
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Deterministic summaries using database findings only</div>
              <div className="flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" /> Prioritized improvement roadmap generator</div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Call to Action */}
      <section className="max-w-4xl mx-auto px-4 text-center">
        <div className="p-8 sm:p-12 rounded-3xl glass-panel border border-primary-500/30 bg-gradient-to-b from-primary-950/20 to-surface-card relative overflow-hidden space-y-4">
          <h2 className="text-2xl sm:text-3xl font-bold text-white">Ready to inspect your code?</h2>
          <p className="text-xs sm:text-sm text-gray-400 max-w-xl mx-auto">
            Ingest any public GitHub repository URL and receive instant intelligence reports on architecture, security, static metrics, and overall Repository IQ score.
          </p>
          <Button onClick={() => onNavigate('repositories')} variant="primary" size="lg">
            <span>Browse Repositories</span>
            <ArrowRight className="h-5 w-5" />
          </Button>
        </div>
      </section>
    </div>
  );
};
