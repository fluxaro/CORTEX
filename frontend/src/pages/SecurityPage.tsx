import React, { useState } from 'react';
import { AlertOctagon, Key, Lock, ShieldAlert } from 'lucide-react';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { SecurityReport } from '../services/types';

interface SecurityPageProps {
  securityReport: SecurityReport;
}

export const SecurityPage: React.FC<SecurityPageProps> = ({ securityReport }) => {
  const [activeFilter, setActiveFilter] = useState<string>('ALL');

  const filteredFindings = securityReport.findings.filter((f) => {
    if (activeFilter === 'ALL') return true;
    return f.severity.toUpperCase() === activeFilter.toUpperCase();
  });

  return (
    <div className="space-y-6">
      {/* Security Banner Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
        <Card glass className="p-4 text-center border-rose-500/30">
          <AlertOctagon className="h-5 w-5 text-rose-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-rose-400">{securityReport.critical_count}</span>
          <span className="text-[11px] text-gray-400 block">Critical Issues</span>
        </Card>

        <Card glass className="p-4 text-center border-amber-500/30">
          <ShieldAlert className="h-5 w-5 text-amber-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-amber-400">{securityReport.high_count}</span>
          <span className="text-[11px] text-gray-400 block">High Severity</span>
        </Card>

        <Card glass className="p-4 text-center">
          <Key className="h-5 w-5 text-purple-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-purple-400">{securityReport.secret_count}</span>
          <span className="text-[11px] text-gray-400 block">Hardcoded Secrets</span>
        </Card>

        <Card glass className="p-4 text-center">
          <Lock className="h-5 w-5 text-blue-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-blue-400">{securityReport.dependency_vuln_count}</span>
          <span className="text-[11px] text-gray-400 block">Vulnerable Packages</span>
        </Card>

        <Card glass className="p-4 text-center">
          <ShieldAlert className="h-5 w-5 text-emerald-400 mx-auto mb-1" />
          <span className="text-2xl font-bold text-emerald-400">{securityReport.config_issues_count}</span>
          <span className="text-[11px] text-gray-400 block">Config Warnings</span>
        </Card>
      </div>

      {/* Security SAST Findings Table */}
      <Card glass>
        <CardHeader className="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
          <div>
            <CardTitle>Static Application Security Testing (SAST) Findings</CardTitle>
            <CardDescription>Verified security weaknesses, hardcoded credentials, and misconfigurations.</CardDescription>
          </div>

          <div className="flex gap-1.5 bg-surface-card p-1 rounded-xl border border-border/40 text-xs">
            {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((filter) => (
              <button
                key={filter}
                onClick={() => setActiveFilter(filter)}
                className={`px-2.5 py-1 rounded-lg transition-colors ${
                  activeFilter === filter ? 'bg-primary-600 text-white font-medium' : 'text-gray-400 hover:text-white'
                }`}
              >
                {filter}
              </button>
            ))}
          </div>
        </CardHeader>
        <CardContent>
          {filteredFindings.length === 0 ? (
            <div className="p-8 text-center text-xs text-gray-400">
              No security findings match the selected severity filter.
            </div>
          ) : (
            <div className="space-y-3">
              {filteredFindings.map((finding) => (
                <div
                  key={finding.id}
                  className="p-4 rounded-xl bg-surface-card border border-border/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={
                          finding.severity === 'Critical' || finding.severity === 'High'
                            ? 'danger'
                            : finding.severity === 'Medium'
                            ? 'warning'
                            : 'info'
                        }
                      >
                        {finding.severity}
                      </Badge>
                      <span className="font-semibold text-gray-200">{finding.rule_name}</span>
                      <span className="text-gray-500 font-mono text-[10px]">({finding.rule_id})</span>
                    </div>
                    <p className="text-gray-400 leading-relaxed">{finding.description}</p>
                    <span className="text-gray-500 font-mono text-[10px] block">
                      File: {finding.file_path}:{finding.line_number}
                    </span>
                  </div>

                  <div className="text-right shrink-0">
                    <span className="text-xs font-bold text-gray-300 block">CVSS {finding.cvss_score}</span>
                    <span className="text-[10px] text-gray-500">Confidence: {finding.confidence}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
