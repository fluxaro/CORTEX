import React from 'react';
import { Code, FileCode, Layers, Scale } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { ProgressBar } from '../components/ui/ProgressBar';
import { StaticMetrics } from '../services/types';

interface StaticAnalysisPageProps {
  staticMetrics: StaticMetrics;
}

export const StaticAnalysisPage: React.FC<StaticAnalysisPageProps> = ({ staticMetrics }) => {
  return (
    <div className="space-y-6">
      {/* Metrics Banner */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card glass className="p-4 text-center">
          <FileCode className="h-5 w-5 text-blue-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-white">{staticMetrics.total_files}</span>
          <span className="text-xs text-gray-400 block">Total Source Files</span>
        </Card>

        <Card glass className="p-4 text-center">
          <Code className="h-5 w-5 text-emerald-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-white">{staticMetrics.total_loc.toLocaleString()}</span>
          <span className="text-xs text-gray-400 block">Total Lines of Code</span>
        </Card>

        <Card glass className="p-4 text-center">
          <Scale className="h-5 w-5 text-purple-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-white">{staticMetrics.average_cyclomatic_complexity}</span>
          <span className="text-xs text-gray-400 block">Avg Cyclomatic Complexity</span>
        </Card>

        <Card glass className="p-4 text-center">
          <Layers className="h-5 w-5 text-amber-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-emerald-400">{staticMetrics.maintainability_index.toFixed(1)}</span>
          <span className="text-xs text-gray-400 block">Maintainability Rank: Grade {staticMetrics.complexity_rank}</span>
        </Card>
      </div>

      {/* LOC Breakdown & Duplication */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card glass>
          <CardHeader>
            <CardTitle>Lines of Code Breakdown</CardTitle>
            <CardDescription>Code vs. Comments vs. Blank lines distribution.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <ProgressBar value={(staticMetrics.code_loc / staticMetrics.total_loc) * 100} label="Executable Code Lines" color="primary" />
            <ProgressBar value={(staticMetrics.comment_loc / staticMetrics.total_loc) * 100} label="Documentation Comments" color="emerald" />
            <ProgressBar value={(staticMetrics.blank_loc / staticMetrics.total_loc) * 100} label="Formatting Blank Lines" color="purple" />
          </CardContent>
        </Card>

        <Card glass>
          <CardHeader>
            <CardTitle>Code Duplication & Smells</CardTitle>
            <CardDescription>Cross-file duplication and code smell detections.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between p-3 rounded-xl bg-surface-card border border-border/40 text-xs">
              <span className="text-gray-300">Duplication Percentage</span>
              <Badge variant={staticMetrics.duplication_percentage > 5 ? 'warning' : 'success'}>
                {staticMetrics.duplication_percentage}% Duplication
              </Badge>
            </div>

            <div className="space-y-2">
              <h4 className="text-xs font-semibold text-gray-300">Code Smell Rules Audited:</h4>
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-400">
                <div className="p-2 rounded-lg bg-surface-card border border-border/40">✓ Long Method (&gt;50 LOC)</div>
                <div className="p-2 rounded-lg bg-surface-card border border-border/40">✓ Large Class (&gt;20 Methods)</div>
                <div className="p-2 rounded-lg bg-surface-card border border-border/40">✓ Deep Nesting (&gt;4 Levels)</div>
                <div className="p-2 rounded-lg bg-surface-card border border-border/40">✓ Too Many Params (&gt;5 Params)</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
