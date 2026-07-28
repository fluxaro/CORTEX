import React from 'react';
import { CheckCircle2, FileText, GitBranch, TestTube } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { ProgressBar } from '../components/ui/ProgressBar';

export const DocumentationPage: React.FC = () => {
  const readmeSections = [
    { title: 'Title & Tagline', status: true },
    { title: 'Project Description', status: true },
    { title: 'Installation Guide', status: true },
    { title: 'Quick Start', status: true },
    { title: 'License Information', status: true },
    { title: 'Architecture Overview', status: true },
    { title: 'API Documentation', status: true },
    { title: 'Contributing Guidelines', status: true },
    { title: 'Testing Instructions', status: true },
    { title: 'Configuration & Env Vars', status: true },
  ];

  return (
    <div className="space-y-6">
      {/* README & Doc Coverage Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card glass className="p-6 text-center">
          <FileText className="h-8 w-8 text-primary-400 mx-auto mb-2" />
          <h3 className="text-3xl font-extrabold text-white">96.0%</h3>
          <p className="text-xs text-gray-400 mt-1">README Completeness Score</p>
        </Card>

        <Card glass className="p-6 text-center">
          <TestTube className="h-8 w-8 text-emerald-400 mx-auto mb-2" />
          <h3 className="text-3xl font-extrabold text-emerald-400">90.0</h3>
          <p className="text-xs text-gray-400 mt-1">Testing Maturity Score (Pytest)</p>
        </Card>

        <Card glass className="p-6 text-center">
          <GitBranch className="h-8 w-8 text-purple-400 mx-auto mb-2" />
          <h3 className="text-3xl font-extrabold text-purple-400">100%</h3>
          <p className="text-xs text-gray-400 mt-1">CI/CD Pipeline Automation</p>
        </Card>
      </div>

      {/* README Section Checklist */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card glass>
          <CardHeader>
            <CardTitle>README Section Coverage</CardTitle>
            <CardDescription>Evaluating 19 standard engineering documentation sections.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <ProgressBar value={96.0} label="README Completeness" color="emerald" />
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-2">
              {readmeSections.map((sec, idx) => (
                <div key={idx} className="flex items-center gap-2 p-2 rounded-lg bg-surface-card border border-border/40 text-xs text-gray-300">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
                  <span>{sec.title}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card glass>
          <CardHeader>
            <CardTitle>CI/CD & Release Cadence</CardTitle>
            <CardDescription>Automation providers and conventional commit standards.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 text-xs">
            <div className="flex items-center justify-between p-3 rounded-xl bg-surface-card border border-border/40">
              <span className="text-gray-300">CI/CD Provider</span>
              <Badge variant="purple">GitHub Actions</Badge>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl bg-surface-card border border-border/40">
              <span className="text-gray-300">Conventional Commits %</span>
              <Badge variant="success">98.5% Conventional</Badge>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl bg-surface-card border border-border/40">
              <span className="text-gray-300">Semantic Versioning</span>
              <Badge variant="info">v1.0.0 Tagged</Badge>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
