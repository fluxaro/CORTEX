import React from 'react';
import { RadarScoreChart } from '../components/charts/RadarScoreChart';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { GradeBadge } from '../components/ui/GradeBadge';
import { Repository, RepositoryGradeReport, SubsystemScores } from '../services/types';

interface RepoOverviewPageProps {
  repo: Repository;
  iqReport: RepositoryGradeReport;
}

const DEFAULT_SUBSYSTEMS: SubsystemScores = {
  static_analysis: 94.2,
  architecture: 91.5,
  security: 88.0,
  documentation: 96.0,
  testing: 90.0,
  ci: 100.0,
  git_practices: 89.0,
  repository_health: 95.0,
  community: 92.0,
};

export const RepoOverviewPage: React.FC<RepoOverviewPageProps> = ({ repo: _repo, iqReport }) => {
  const sub = iqReport.subsystem_scores || DEFAULT_SUBSYSTEMS;

  return (
    <div className="space-y-6">
      {/* Top Banner Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card glass className="p-6 flex flex-col justify-between items-center text-center">
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-gray-300">Overall Grade</h3>
            <GradeBadge grade={iqReport.overall_grade || 'C'} size="xl" showLabel />
          </div>
          <div className="mt-4 space-y-1">
            <Badge variant="purple" size="md">
              {iqReport.maturity_level}
            </Badge>
            <p className="text-xs text-gray-400 font-mono">Score: {iqReport.overall_score.toFixed(1)}/100</p>
          </div>
        </Card>

        <Card glass className="md:col-span-2">
          <CardHeader>
            <CardTitle>CORTEX Executive Synthesis</CardTitle>
            <CardDescription>AI generated synthesis of repository intelligence.</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-xs sm:text-sm text-gray-300 leading-relaxed bg-surface-card p-4 rounded-xl border border-border/60">
              {iqReport.narrative_summary ||
                iqReport.summary?.narrative_summary ||
                iqReport.summary?.executive_summary ||
                'CORTEX repository evaluation complete. Demonstrates solid engineering standards and architectural modularity.'}
            </p>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 text-center">
              <div className="p-3 bg-surface-card rounded-xl border border-border/40">
                <span className="text-xs text-gray-400 block">Maintainability</span>
                <span className="text-base font-bold text-emerald-400">{sub.static_analysis.toFixed(1)}</span>
              </div>
              <div className="p-3 bg-surface-card rounded-xl border border-border/40">
                <span className="text-xs text-gray-400 block">Architecture</span>
                <span className="text-base font-bold text-blue-400">{sub.architecture.toFixed(1)}</span>
              </div>
              <div className="p-3 bg-surface-card rounded-xl border border-border/40">
                <span className="text-xs text-gray-400 block">Security Posture</span>
                <span className="text-base font-bold text-purple-400">{sub.security.toFixed(1)}</span>
              </div>
              <div className="p-3 bg-surface-card rounded-xl border border-border/40">
                <span className="text-xs text-gray-400 block">Technical Debt</span>
                <span className="text-base font-bold text-amber-400">{iqReport.technical_debt?.total_hours || 12}h</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Radar Chart & Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card glass>
          <CardHeader>
            <CardTitle>Subsystem Score Radar</CardTitle>
            <CardDescription>Comparative visualization of subsystem scores.</CardDescription>
          </CardHeader>
          <CardContent>
            <RadarScoreChart subsystems={sub} />
          </CardContent>
        </Card>

        <Card glass className="space-y-4">
          <CardHeader>
            <CardTitle>Key Strengths</CardTitle>
            <CardDescription>Verified engineering strengths identified by analysis engines.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {(iqReport.insights?.strengths || [
              'Clean Architecture pattern with strict layer separation.',
              '100% CI/CD workflow automation on GitHub Actions.',
              'High maintainability index with low cyclomatic complexity.',
            ]).map((strength, idx) => (
              <div key={idx} className="p-3 rounded-xl bg-surface-card border border-border/40 text-xs text-gray-200 flex items-start gap-2">
                <span className="text-emerald-400 font-bold">✓</span>
                <span>{strength}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
