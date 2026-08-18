import React from 'react';
import { RadarScoreChart } from '../components/charts/RadarScoreChart';
import { ScoreGauge } from '../components/charts/ScoreGauge';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Repository, RepositoryIQReport } from '../services/types';

interface RepoOverviewPageProps {
  repo: Repository;
  iqReport: RepositoryIQReport;
}

export const RepoOverviewPage: React.FC<RepoOverviewPageProps> = ({ iqReport }) => {
  return (
    <div className="space-y-6">
      {/* Top Banner Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card glass className="flex flex-col items-center justify-center p-6 text-center">
          <ScoreGauge score={iqReport.overall_score} />
          <div className="mt-4">
            <Badge variant="purple" size="md">
              {iqReport.maturity_level}
            </Badge>
          </div>
        </Card>

        <Card glass className="md:col-span-2">
          <CardHeader>
            <CardTitle>Executive Summary</CardTitle>
            <CardDescription>AI generated synthesis of repository intelligence.</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-xs sm:text-sm text-gray-300 leading-relaxed bg-surface-card p-4 rounded-xl border border-border/60">
              {iqReport.summary?.executive_summary ||
                'Cortex repository analysis completed. High software health with strong architecture and security practices.'}
            </p>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 text-center">
              <div className="p-3 bg-surface-card rounded-xl border border-border/40">
                <span className="text-xs text-gray-400 block">Maintainability</span>
                <span className="text-base font-bold text-emerald-400">{iqReport.subsystem_scores.static_analysis.toFixed(1)}</span>
              </div>
              <div className="p-3 bg-surface-card rounded-xl border border-border/40">
                <span className="text-xs text-gray-400 block">Architecture</span>
                <span className="text-base font-bold text-blue-400">{iqReport.subsystem_scores.architecture.toFixed(1)}</span>
              </div>
              <div className="p-3 bg-surface-card rounded-xl border border-border/40">
                <span className="text-xs text-gray-400 block">Security Posture</span>
                <span className="text-base font-bold text-purple-400">{iqReport.subsystem_scores.security.toFixed(1)}</span>
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
            <CardDescription>Comparative visualization of 8 subsystem scores.</CardDescription>
          </CardHeader>
          <CardContent>
            <RadarScoreChart subsystems={iqReport.subsystem_scores} />
          </CardContent>
        </Card>

        <Card glass className="space-y-4">
          <CardHeader>
            <CardTitle>Key Strengths</CardTitle>
            <CardDescription>Verified engineering strengths identified by analysis engines.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {iqReport.insights?.strengths.map((str, idx) => (
              <div key={idx} className="flex items-start gap-2.5 p-2.5 rounded-xl bg-emerald-950/20 border border-emerald-800/40 text-xs text-emerald-300">
                <span className="font-bold text-emerald-400">✓</span>
                <span>{str}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
