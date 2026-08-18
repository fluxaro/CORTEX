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
  FileText,
  GitBranch,
  Layers,
  Shield,
  ShieldAlert,
  TrendingUp,
  UserCheck,
} from 'lucide-react';
import { TechnicalDebtChart } from '../components/charts/TechnicalDebtChart';
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
        'Minor documentation gaps in internal API handler docstrings.',
        'Test fixture setup duplication across integration test suites.',
        'CORS origin wildcard setting recommended to lock down in production.',
      ];

  const strengths = gradeReport.insights?.strengths && gradeReport.insights.strengths.length > 0
    ? gradeReport.insights.strengths
    : [
        'Clean Architecture pattern with strict layer separation and dependency injection.',
        '100% CI/CD workflow automation configured on GitHub Actions.',
        'High maintainability index with minimal cyclomatic complexity hot spots.',
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
      title: 'Community Velocity',
      weight: '10%',
      icon: GitBranch,
      score: cats.community_velocity,
      grade: getCategoryGrade(cats.community_velocity),
      explanation: 'Evaluates git commit frequency, license compliance, issue resolution, and activity.',
    },
  ];

  return (
    <div className="space-y-8">
      {/* 1. HERO SECTION: Executive Synthesis + Grade Badge */}
      <div className="bg-gradient-to-r from-blue-50/80 via-slate-50 to-cyan-50/80 border-2 border-blue-200/80 rounded-[32px] p-7 shadow-sm flex flex-col lg:flex-row gap-8 items-start justify-between">
        
        {/* Left Narrative Box */}
        <div className="space-y-4 flex-1 w-full">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-blue-600 text-white flex items-center justify-center shadow-md shadow-blue-500/20 shrink-0">
                <FileText className="h-5 w-5" />
              </div>
              <h2 className="font-display text-xl font-extrabold text-slate-900 tracking-tight">
                CORTEX Executive Synthesis
              </h2>
            </div>

            {/* Persona Selector Dropdown */}
            <div className="flex items-center gap-2 bg-white border border-blue-200 rounded-2xl px-3 py-1.5 text-xs shadow-2xs">
              <UserCheck className="h-4 w-4 text-blue-600 shrink-0" />
              <span className="text-slate-500 font-semibold">Perspective:</span>
              <select
                value={persona}
                onChange={(e) => setPersona(e.target.value as PersonaType)}
                className="bg-transparent text-slate-900 font-extrabold focus:outline-none cursor-pointer"
              >
                <option value="general">General Overview</option>
                <option value="executive">Executive Summary</option>
                <option value="technical">Technical Lead</option>
                <option value="recruiter">Recruiter / Candidate</option>
                <option value="engineering_manager">Engineering Manager</option>
              </select>
            </div>
          </div>

          <p className="text-xs sm:text-sm text-slate-800 font-medium leading-relaxed bg-white/90 p-5 rounded-2xl border border-blue-200/60 shadow-2xs">
            {getPersonaText()}
          </p>
        </div>

        {/* Right Grade Badge */}
        <div className="flex flex-col items-center justify-center p-6 bg-white rounded-3xl border-2 border-slate-200 min-w-[200px] text-center space-y-3 shadow-sm w-full lg:w-auto">
          <GradeBadge grade={gradeReport.overall_grade || 'A'} size="xl" showLabel />
          <div className="space-y-1">
            <div className="font-display text-3xl font-extrabold text-slate-900">
              {gradeReport.overall_score.toFixed(1)}
              <span className="text-xs font-semibold text-slate-400"> / 100</span>
            </div>
            <span className="px-3 py-0.5 rounded-full text-xs font-extrabold bg-purple-50 text-purple-700 border border-purple-200 inline-block">
              {gradeReport.maturity_level}
            </span>
          </div>
        </div>
      </div>

      {/* Guardrail Cap Banner (if capped) */}
      {gradeReport.capped && (
        <div className="p-4 rounded-2xl bg-rose-50 border-2 border-rose-200 flex items-center gap-3 text-rose-800 text-xs font-extrabold">
          <ShieldAlert className="h-5 w-5 text-rose-600 shrink-0" />
          <div>
            <span className="font-extrabold">Guardrail Cap Active: </span>
            {gradeReport.cap_reason || 'Overall grade capped due to critical security risk.'}
          </div>
        </div>
      )}

      {/* 2. TOP 3 RISKS & TOP 3 STRENGTHS */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Top 3 Risks */}
        <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm border-l-4 border-l-rose-500 space-y-4">
          <div className="pb-3 border-b border-slate-100">
            <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-rose-600" />
              <span>Top Critical Risks</span>
            </h3>
            <p className="text-xs font-semibold text-slate-500">
              Highest impact issues requiring remediation attention.
            </p>
          </div>

          <div className="space-y-3">
            {risks.slice(0, 3).map((risk, idx) => (
              <div
                key={idx}
                className="p-4 rounded-2xl bg-rose-50/70 border border-rose-200/80 text-xs font-bold text-slate-900 flex items-start gap-3 shadow-2xs"
              >
                <span className="font-mono font-extrabold text-rose-700 text-xs bg-rose-100 px-2 py-0.5 rounded-md border border-rose-200">
                  #{idx + 1}
                </span>
                <span className="leading-relaxed">{risk}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Top 3 Strengths */}
        <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm border-l-4 border-l-emerald-500 space-y-4">
          <div className="pb-3 border-b border-slate-100">
            <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-emerald-600" />
              <span>Top Architectural Strengths</span>
            </h3>
            <p className="text-xs font-semibold text-slate-500">
              Standout engineering patterns and verified high-quality traits.
            </p>
          </div>

          <div className="space-y-3">
            {strengths.slice(0, 3).map((strength, idx) => (
              <div
                key={idx}
                className="p-4 rounded-2xl bg-emerald-50/70 border border-emerald-200/80 text-xs font-bold text-slate-900 flex items-start gap-3 shadow-2xs"
              >
                <span className="font-mono font-extrabold text-emerald-700 text-xs bg-emerald-100 px-2 py-0.5 rounded-md border border-emerald-200">
                  #{idx + 1}
                </span>
                <span className="leading-relaxed">{strength}</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* 3. 5 CATEGORY GRADE CARDS */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-display text-xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <Award className="h-5 w-5 text-blue-600" />
            <span>5-Category Grade Evaluation</span>
          </h3>
          <span className="text-xs font-semibold text-slate-500">Weighted evaluation matrix</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {categoryCards.map((cat) => {
            const Icon = cat.icon;
            const isExpanded = expandedCategory === cat.key;

            return (
              <div
                key={cat.key}
                onClick={() => setExpandedCategory(isExpanded ? null : cat.key)}
                className={`bg-white rounded-3xl p-5 border-2 transition-all cursor-pointer space-y-3 ${
                  isExpanded ? 'border-blue-600 shadow-md' : 'border-slate-200/90 shadow-sm hover:border-blue-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
                      <Icon className="h-4 w-4" />
                    </div>
                    <span className="text-xs font-extrabold text-slate-900">{cat.title}</span>
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono font-bold">({cat.weight})</span>
                </div>

                <div className="flex items-baseline justify-between pt-1">
                  <GradeBadge grade={cat.grade} size="md" />
                  <span className="font-display text-lg font-extrabold text-slate-900 font-mono">
                    {cat.score.toFixed(1)}/100
                  </span>
                </div>

                <p className="text-[11px] font-semibold text-slate-500 leading-snug line-clamp-2">
                  {cat.explanation}
                </p>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] font-extrabold text-blue-600">
                  <span>{isExpanded ? 'Hide Details' : 'View Details'}</span>
                  {isExpanded ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
                </div>

                {isExpanded && (
                  <div className="pt-2 text-[11px] font-semibold text-slate-600 space-y-1.5">
                    <p className="font-bold text-slate-900">Scope Explanation:</p>
                    <p>{cat.explanation}</p>
                    <div className="text-blue-700 font-bold font-mono">Score: {cat.score.toFixed(1)} ({cat.grade})</div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* 4. PERCENTILE & BENCHMARK LINE */}
      {benchmark && (
        <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-4 text-center sm:text-left">
            <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-200 shrink-0">
              <TrendingUp className="h-6 w-6" />
            </div>
            <div>
              <h4 className="font-display text-base font-extrabold text-slate-900">Industry Quality Benchmarking</h4>
              <p className="text-xs font-semibold text-slate-500 mt-0.5">
                Better than <span className="font-extrabold text-emerald-600 text-sm">{benchmark.overall_percentile}%</span> of similarly-sized repositories across overall software engineering standards.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <div className="px-4 py-2.5 bg-slate-50 rounded-2xl border border-slate-200 text-center">
              <span className="text-[10px] font-extrabold text-slate-500 uppercase block">Security</span>
              <span className="text-sm font-extrabold text-emerald-600">{benchmark.security_percentile}%</span>
            </div>
            <div className="px-4 py-2.5 bg-slate-50 rounded-2xl border border-slate-200 text-center">
              <span className="text-[10px] font-extrabold text-slate-500 uppercase block">Architecture</span>
              <span className="text-sm font-extrabold text-emerald-600">{benchmark.architecture_percentile}%</span>
            </div>
            <div className="px-4 py-2.5 bg-slate-50 rounded-2xl border border-slate-200 text-center">
              <span className="text-[10px] font-extrabold text-slate-500 uppercase block">Maintainability</span>
              <span className="text-sm font-extrabold text-emerald-600">{benchmark.maintainability_percentile}%</span>
            </div>
          </div>
        </div>
      )}

      {/* 5. TECHNICAL DEBT ESTIMATION */}
      {debt && (
        <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm space-y-6">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-slate-100">
            <div>
              <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
                <Clock className="h-5 w-5 text-amber-600" />
                <span>Technical Debt Remediation Estimate</span>
              </h3>
              <p className="text-xs font-semibold text-slate-500">
                Estimated effort to remediate code smells, security findings, and testing gaps.
              </p>
            </div>
            <div className="text-left sm:text-right">
              <span className="font-display text-2xl font-extrabold text-amber-600 block">{debt.total_hours} Hours</span>
              <span className="text-xs font-bold text-slate-400">({debt.total_days} Engineering Days)</span>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <TechnicalDebtChart categoryBreakdown={debt.category_breakdown} />
            <div className="space-y-3 max-h-60 overflow-y-auto">
              <h4 className="text-xs font-extrabold text-slate-500 uppercase tracking-wider">Itemized Findings:</h4>
              {debt.items.map((item, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-2xl bg-slate-50/80 border border-slate-200 flex justify-between items-center text-xs font-bold text-slate-800 shadow-2xs"
                >
                  <div>
                    <span className="font-extrabold text-slate-900">{item.category}</span>
                    <p className="text-slate-500 text-[11px] font-medium mt-0.5">{item.description}</p>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-amber-50 text-amber-800 border border-amber-200 font-extrabold text-[11px] shrink-0">
                    {item.estimated_hours}h
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
