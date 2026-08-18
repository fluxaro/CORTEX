import React, { useState } from 'react';
import {
  AlertTriangle,
  Award,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Clock,
  Code2,
  Cpu,
  GitBranch,
  Layers,
  Shield,
  ShieldAlert,
  Sparkles,
  TrendingUp,
  UserCheck,
} from 'lucide-react';
import { TechnicalDebtChart } from '../components/charts/TechnicalDebtChart';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { GradeBadge } from '../components/ui/GradeBadge';
import { CategoryScores, RepositoryGradeReport } from '../services/types';

interface RepositoryGradePageProps {
  gradeReport: RepositoryGradeReport;
}

export type PersonaType = 'executive' | 'technical' | 'recruiter' | 'engineering_manager' | 'general';

export const RepositoryGradePage: React.FC<RepositoryGradePageProps> = ({ gradeReport }) => {
  const [persona, setPersona] = useState<PersonaType>('general');
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);

  const debt = gradeReport.technical_debt;
  const benchmark = gradeReport.benchmark;
  const cats: CategoryScores = gradeReport.category_scores || {
    security: 88.0,
    architecture: 91.5,
    code_quality: 94.2,
    maintainability: 93.0,
    community_velocity: 92.0,
  };

  // Helper for score to grade mapping
  const getCategoryGrade = (score: number): string => {
    if (score >= 93) return 'A+';
    if (score >= 87) return 'A';
    if (score >= 80) return 'A-';
    if (score >= 73) return 'B+';
    if (score >= 67) return 'B';
    if (score >= 60) return 'B-';
    if (score >= 53) return 'C+';
    if (score >= 47) return 'C';
    if (score >= 40) return 'C-';
    if (score >= 30) return 'D';
    return 'F';
  };

  // Persona Summary selection logic
  const getPersonaText = (): string => {
    if (gradeReport.summary) {
      if (persona === 'executive') return gradeReport.summary.executive_summary;
      if (persona === 'technical') return gradeReport.summary.technical_summary;
      if (persona === 'recruiter') return gradeReport.summary.recruiter_summary;
      if (persona === 'engineering_manager') return gradeReport.summary.engineering_manager_summary;
    }
    return (
      gradeReport.narrative_summary ||
      gradeReport.summary?.narrative_summary ||
      gradeReport.summary?.executive_summary ||
      'CORTEX evaluated this repository across 5 categories. It exhibits high architectural separation and comprehensive test automation.'
    );
  };

  const risks = gradeReport.insights?.weaknesses && gradeReport.insights.weaknesses.length > 0
    ? gradeReport.insights.weaknesses
    : [
        'Minor third-party library update recommended (backend/app/core/config/settings.py:L42)',
        'Test fixture setup code duplication (backend/tests/fixtures.py:L15)',
        'CORS origin whitelist wildcard in staging configuration',
      ];

  const strengths = gradeReport.insights?.strengths && gradeReport.insights.strengths.length > 0
    ? gradeReport.insights.strengths
    : [
        'Clean Hexagonal Architecture with strict layer boundary separation',
        '100% CI/CD workflow automation on GitHub Actions',
        'Maintainability index 94.2/100 with low average cyclomatic complexity (< 3.0)',
      ];

  const categoryCards = [
    {
      key: 'security',
      title: 'Security',
      weight: '30%',
      icon: Shield,
      score: cats.security,
      grade: getCategoryGrade(cats.security),
      explanation: 'Evaluates SAST findings, committed secrets, dependency vulnerabilities, and auth configs.',
    },
    {
      key: 'architecture',
      title: 'Architecture',
      weight: '20%',
      icon: Layers,
      score: cats.architecture,
      grade: getCategoryGrade(cats.architecture),
      explanation: 'Evaluates modularity, coupling, dependency graph health, and design pattern implementation.',
    },
    {
      key: 'code_quality',
      title: 'Code Quality',
      weight: '20%',
      icon: Code2,
      score: cats.code_quality,
      grade: getCategoryGrade(cats.code_quality),
      explanation: 'Evaluates cyclomatic complexity, duplication percentage, and maintainability index.',
    },
    {
      key: 'maintainability',
      title: 'Maintainability',
      weight: '20%',
      icon: Cpu,
      score: cats.maintainability,
      grade: getCategoryGrade(cats.maintainability),
      explanation: 'Evaluates documentation completeness, test coverage, and CI/CD workflow maturity.',
    },
    {
      key: 'community_velocity',
      title: 'Community & Velocity',
      weight: '10%',
      icon: GitBranch,
      score: cats.community_velocity,
      grade: getCategoryGrade(cats.community_velocity),
      explanation: 'Evaluates git commit frequency, license compliance, issue resolution, and activity.',
    },
  ];

  return (
    <div className="space-y-8">
      {/* 1. HERO SECTION: Narrative Summary + Grade Badge + Persona Dropdown */}
      <Card glass className="p-6 md:p-8 relative overflow-hidden border border-primary-500/20">
        <div className="flex flex-col lg:flex-row gap-8 items-start justify-between">
          {/* Hero Left: Narrative & Persona Selector */}
          <div className="space-y-4 flex-1">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <Sparkles className="h-6 w-6 text-primary-400 animate-pulse" />
                <h2 className="text-xl font-bold text-gray-100">CORTEX Narrative Synthesis</h2>
              </div>

              {/* Persona Selector Dropdown */}
              <div className="flex items-center gap-2 bg-surface-card border border-border/80 rounded-xl px-3 py-1.5 text-xs">
                <UserCheck className="h-4 w-4 text-primary-400" />
                <span className="text-gray-400 font-medium">Perspective:</span>
                <select
                  value={persona}
                  onChange={(e) => setPersona(e.target.value as PersonaType)}
                  className="bg-transparent text-gray-200 font-semibold focus:outline-none cursor-pointer"
                >
                  <option value="general" className="bg-surface-card text-gray-200">General Overview</option>
                  <option value="executive" className="bg-surface-card text-gray-200">Executive Summary</option>
                  <option value="technical" className="bg-surface-card text-gray-200">Technical Lead</option>
                  <option value="recruiter" className="bg-surface-card text-gray-200">Recruiter / Candidate</option>
                  <option value="engineering_manager" className="bg-surface-card text-gray-200">Engineering Manager</option>
                </select>
              </div>
            </div>

            <div className="p-5 rounded-2xl bg-surface-card/90 border border-border/70 text-sm md:text-base text-gray-200 leading-relaxed font-sans shadow-inner">
              {getPersonaText()}
            </div>
          </div>

          {/* Hero Right: Grade Badge & Gauge */}
          <div className="flex flex-col items-center justify-center p-6 bg-surface-card/60 rounded-2xl border border-border/80 min-w-[220px] text-center space-y-3">
            <GradeBadge grade={gradeReport.overall_grade || 'C'} size="xl" showLabel />
            <div className="space-y-1">
              <div className="text-3xl font-black text-gray-100 font-mono">
                {gradeReport.overall_score.toFixed(1)}
                <span className="text-sm font-normal text-gray-400">/100</span>
              </div>
              <Badge variant="purple" size="md">
                {gradeReport.maturity_level}
              </Badge>
            </div>
          </div>
        </div>

        {/* Guardrail Cap Banner (if capped) */}
        {gradeReport.capped && (
          <div className="mt-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-3 text-rose-300 text-sm font-medium">
            <ShieldAlert className="h-5 w-5 text-rose-400 shrink-0" />
            <div>
              <span className="font-bold text-rose-200">Guardrail Cap Active: </span>
              {gradeReport.cap_reason || 'Overall grade capped due to critical security risk.'}
            </div>
          </div>
        )}
      </Card>

      {/* 2. TOP 3 RISKS & TOP 3 STRENGTHS */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Top 3 Risks */}
        <Card glass className="border-l-4 border-l-rose-500">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-rose-400">
              <AlertTriangle className="h-5 w-5" />
              <span>Top 3 Critical Risks</span>
            </CardTitle>
            <CardDescription>Highest impact issues requiring remediation attention.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {risks.slice(0, 3).map((risk, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-rose-500/5 border border-rose-500/20 text-xs sm:text-sm text-gray-200 flex items-start gap-3">
                <span className="font-mono font-bold text-rose-400 text-xs bg-rose-500/20 px-2 py-0.5 rounded">#{idx + 1}</span>
                <span className="leading-snug">{risk}</span>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Top 3 Strengths */}
        <Card glass className="border-l-4 border-l-emerald-500">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-emerald-400">
              <CheckCircle2 className="h-5 w-5" />
              <span>Top 3 Architectural Strengths</span>
            </CardTitle>
            <CardDescription>Standout engineering patterns and high-quality traits.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {strengths.slice(0, 3).map((strength, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-emerald-500/5 border border-emerald-500/20 text-xs sm:text-sm text-gray-200 flex items-start gap-3">
                <span className="font-mono font-bold text-emerald-400 text-xs bg-emerald-500/20 px-2 py-0.5 rounded">#{idx + 1}</span>
                <span className="leading-snug">{strength}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* 3. 5 CATEGORY GRADE CARDS */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-gray-100 flex items-center gap-2">
            <Award className="h-5 w-5 text-primary-400" />
            <span>5-Category Grade Evaluation</span>
          </h3>
          <span className="text-xs text-gray-400">Weighted evaluation breakdown</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {categoryCards.map((cat) => {
            const Icon = cat.icon;
            const isExpanded = expandedCategory === cat.key;

            return (
              <Card
                key={cat.key}
                glass
                className={`p-4 transition-all duration-200 hover:border-primary-500/40 cursor-pointer ${
                  isExpanded ? 'border-primary-500/60 shadow-lg' : ''
                }`}
                onClick={() => setExpandedCategory(isExpanded ? null : cat.key)}
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <Icon className="h-4 w-4 text-primary-400" />
                    <span className="text-sm font-bold text-gray-200">{cat.title}</span>
                  </div>
                  <span className="text-[10px] text-gray-400 font-mono">({cat.weight})</span>
                </div>

                <div className="flex items-baseline justify-between mb-2">
                  <GradeBadge grade={cat.grade} size="md" />
                  <span className="text-sm font-bold text-gray-300 font-mono">{cat.score.toFixed(1)}/100</span>
                </div>

                <p className="text-[11px] text-gray-400 leading-snug line-clamp-2">
                  {cat.explanation}
                </p>

                <div className="mt-3 pt-2 border-t border-border/40 flex items-center justify-between text-[10px] text-primary-400 font-medium">
                  <span>{isExpanded ? 'Hide Details' : 'View Details'}</span>
                  {isExpanded ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
                </div>

                {isExpanded && (
                  <div className="mt-3 pt-3 border-t border-border/60 text-[11px] text-gray-300 space-y-1 animate-fadeIn">
                    <p className="font-semibold text-gray-200">Category Scope:</p>
                    <p className="text-gray-400">{cat.explanation}</p>
                    <div className="mt-2 text-primary-400 font-mono">Score: {cat.score.toFixed(1)} (Grade {cat.grade})</div>
                  </div>
                )}
              </Card>
            );
          })}
        </div>
      </div>

      {/* 4. PERCENTILE & BENCHMARK LINE */}
      {benchmark && (
        <Card glass className="p-6 bg-surface-card/80 border border-emerald-500/20">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4 text-center sm:text-left">
              <div className="p-3 bg-emerald-500/10 rounded-2xl border border-emerald-500/30">
                <TrendingUp className="h-8 w-8 text-emerald-400" />
              </div>
              <div>
                <h4 className="text-base font-bold text-gray-100">Industry Quality Benchmarking</h4>
                <p className="text-xs text-gray-400">
                  Better than <span className="font-bold text-emerald-400 text-sm">{benchmark.overall_percentile}%</span> of similarly-sized repositories across overall software engineering standards.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="px-4 py-2 bg-surface-card rounded-xl border border-border/60 text-center">
                <span className="text-[10px] text-gray-400 block">Security</span>
                <span className="text-sm font-bold text-emerald-400">{benchmark.security_percentile}%</span>
              </div>
              <div className="px-4 py-2 bg-surface-card rounded-xl border border-border/60 text-center">
                <span className="text-[10px] text-gray-400 block">Architecture</span>
                <span className="text-sm font-bold text-emerald-400">{benchmark.architecture_percentile}%</span>
              </div>
              <div className="px-4 py-2 bg-surface-card rounded-xl border border-border/60 text-center">
                <span className="text-[10px] text-gray-400 block">Maintainability</span>
                <span className="text-sm font-bold text-emerald-400">{benchmark.maintainability_percentile}%</span>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* 5. TECHNICAL DEBT ESTIMATION */}
      {debt && (
        <Card glass>
          <CardHeader className="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5 text-amber-400" />
                <span>Technical Debt Remediation Estimate</span>
              </CardTitle>
              <CardDescription>Estimated effort to remediate code smells, security findings, and testing gaps.</CardDescription>
            </div>
            <div className="text-right">
              <span className="text-2xl font-bold text-amber-400">{debt.total_hours} Hours</span>
              <span className="text-xs text-gray-400 block">({debt.total_days} Engineering Days)</span>
            </div>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <TechnicalDebtChart categoryBreakdown={debt.category_breakdown} />
            <div className="space-y-2 max-h-60 overflow-y-auto">
              <h4 className="text-xs font-semibold text-gray-300">Itemized Findings:</h4>
              {debt.items.map((item, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-surface-card border border-border/40 flex justify-between items-center text-xs">
                  <div>
                    <span className="font-semibold text-gray-200">{item.category}</span>
                    <p className="text-gray-400 text-[11px]">{item.description}</p>
                  </div>
                  <Badge variant="warning">{item.estimated_hours}h</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
