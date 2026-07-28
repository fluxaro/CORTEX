import React from 'react';
import { GitCompare } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';

export const RepoComparisonPage: React.FC = () => {
  const repos = [
    { name: 'me-hv/ProjectIQ', language: 'Python', iq: 92.4, sec: 88.0, arch: 91.5, debt: '12h', status: 'Enterprise Ready' },
    { name: 'tiangolo/fastapi-ms', language: 'Python', iq: 88.0, sec: 85.0, arch: 89.0, debt: '18h', status: 'Production Ready' },
    { name: 'vercel/react-boilerplate', language: 'TypeScript', iq: 95.1, sec: 92.0, arch: 96.0, debt: '6h', status: 'Enterprise Ready' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="pb-4 border-b border-border/80">
        <h1 className="text-2xl font-bold text-white tracking-tight">Repository Comparison Matrix</h1>
        <p className="text-xs text-gray-400">Side-by-side comparative analysis of code quality, architecture, security, and technical debt.</p>
      </div>

      <Card glass>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <GitCompare className="h-5 w-5 text-primary-400" />
            <span>Cross-Repository Benchmark Matrix</span>
          </CardTitle>
          <CardDescription>Evaluating 3 selected repositories against engineering standards.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left text-gray-200">
              <thead className="text-[11px] uppercase bg-surface-card text-gray-400 border-b border-border">
                <tr>
                  <th className="px-4 py-3">Metric</th>
                  {repos.map((r, i) => (
                    <th key={i} className="px-4 py-3 font-semibold text-white">{r.name}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border/40">
                <tr>
                  <td className="px-4 py-3 font-semibold text-gray-400">Primary Language</td>
                  {repos.map((r, i) => <td key={i} className="px-4 py-3">{r.language}</td>)}
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-gray-400">Repository IQ Score</td>
                  {repos.map((r, i) => (
                    <td key={i} className="px-4 py-3"><Badge variant="success">IQ {r.iq}</Badge></td>
                  ))}
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-gray-400">Security Posture</td>
                  {repos.map((r, i) => <td key={i} className="px-4 py-3 text-purple-400 font-bold">{r.sec}/100</td>)}
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-gray-400">Architecture Modularity</td>
                  {repos.map((r, i) => <td key={i} className="px-4 py-3 text-blue-400 font-bold">{r.arch}/100</td>)}
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-gray-400">Estimated Tech Debt</td>
                  {repos.map((r, i) => <td key={i} className="px-4 py-3 text-amber-400 font-bold">{r.debt}</td>)}
                </tr>
                <tr>
                  <td className="px-4 py-3 font-semibold text-gray-400">Maturity Level</td>
                  {repos.map((r, i) => <td key={i} className="px-4 py-3"><Badge variant="purple">{r.status}</Badge></td>)}
                </tr>
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
