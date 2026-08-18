import React, { useState } from 'react';
import { AlertOctagon, CheckCircle2, Key, Lock, ShieldAlert, ShieldCheck } from 'lucide-react';
import { SecurityReport } from '../services/types';

interface SecurityPageProps {
  securityReport: SecurityReport;
}

export const SecurityPage: React.FC<SecurityPageProps> = ({ securityReport }) => {
  const [activeFilter, setActiveFilter] = useState<string>('ALL');

  const filteredFindings = (securityReport.findings || []).filter((f) => {
    if (activeFilter === 'ALL') return true;
    return f.severity.toUpperCase() === activeFilter.toUpperCase();
  });

  return (
    <div className="space-y-8">
      {/* 5 Security KPI Stat Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 sm:gap-6">
        
        {/* Critical */}
        <div className="bg-white rounded-3xl p-5 border-2 border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider">Critical</span>
            <div className="w-8 h-8 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
              <AlertOctagon className="h-4 w-4" />
            </div>
          </div>
          <div className="font-display text-3xl font-extrabold text-slate-900">
            {securityReport.critical_count || 0}
          </div>
          <p className="text-[10px] font-semibold text-slate-500">Critical CVE Leaks</p>
        </div>

        {/* High Severity */}
        <div className="bg-white rounded-3xl p-5 border-2 border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider">High Severity</span>
            <div className="w-8 h-8 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
              <ShieldAlert className="h-4 w-4" />
            </div>
          </div>
          <div className="font-display text-3xl font-extrabold text-slate-900">
            {securityReport.high_count || 0}
          </div>
          <p className="text-[10px] font-semibold text-slate-500">High Risk Code Defects</p>
        </div>

        {/* Hardcoded Secrets */}
        <div className="bg-white rounded-3xl p-5 border-2 border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider">Secrets Leaked</span>
            <div className="w-8 h-8 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
              <Key className="h-4 w-4" />
            </div>
          </div>
          <div className="font-display text-3xl font-extrabold text-slate-900">
            {securityReport.secret_count || 0}
          </div>
          <p className="text-[10px] font-semibold text-slate-500">Shannon Entropy Leaks</p>
        </div>

        {/* Vulnerable Packages */}
        <div className="bg-white rounded-3xl p-5 border-2 border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider">Vulnerabilities</span>
            <div className="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Lock className="h-4 w-4" />
            </div>
          </div>
          <div className="font-display text-3xl font-extrabold text-slate-900">
            {securityReport.dependency_vuln_count || 0}
          </div>
          <p className="text-[10px] font-semibold text-slate-500">Outdated Packages</p>
        </div>

        {/* Config Warnings */}
        <div className="bg-white rounded-3xl p-5 border-2 border-slate-200/90 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider">Config Warnings</span>
            <div className="w-8 h-8 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <ShieldCheck className="h-4 w-4" />
            </div>
          </div>
          <div className="font-display text-3xl font-extrabold text-slate-900">
            {securityReport.config_issues_count || 0}
          </div>
          <p className="text-[10px] font-semibold text-slate-500">Security Rule Checks</p>
        </div>

      </div>

      {/* Security SAST Findings Table / List */}
      <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm space-y-6">
        
        {/* Card Header & Filter Control */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4 border-b border-slate-100">
          <div>
            <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight">
              Static Application Security Testing (SAST) Findings
            </h3>
            <p className="text-xs font-semibold text-slate-500">
              Verified security weaknesses, hardcoded credentials, and infrastructure misconfigurations.
            </p>
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
            {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'].map((filter) => (
              <button
                key={filter}
                onClick={() => setActiveFilter(filter)}
                className={`px-3 py-1.5 rounded-xl text-xs font-extrabold transition-all whitespace-nowrap ${
                  activeFilter === filter
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                }`}
              >
                {filter}
              </button>
            ))}
          </div>
        </div>

        {/* Findings List */}
        {filteredFindings.length === 0 ? (
          <div className="p-12 text-center space-y-3">
            <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto border border-emerald-200">
              <CheckCircle2 className="h-6 w-6" />
            </div>
            <h4 className="font-display text-base font-bold text-slate-900">Zero Security Findings</h4>
            <p className="text-xs text-slate-500 max-w-sm mx-auto font-medium">
              No SAST security vulnerabilities match the selected severity filter for this codebase.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredFindings.map((finding) => (
              <div
                key={finding.id}
                className="p-5 rounded-2xl bg-slate-50/80 border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-xs shadow-2xs hover:bg-white transition-all"
              >
                <div className="space-y-1.5">
                  <div className="flex flex-wrap items-center gap-2">
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-[11px] font-extrabold uppercase ${
                        finding.severity === 'Critical' || finding.severity === 'High'
                          ? 'bg-rose-100 text-rose-800 border border-rose-200'
                          : finding.severity === 'Medium'
                          ? 'bg-amber-100 text-amber-800 border border-amber-200'
                          : 'bg-blue-100 text-blue-800 border border-blue-200'
                      }`}
                    >
                      {finding.severity}
                    </span>
                    <h4 className="font-bold text-slate-900">{finding.rule_name}</h4>
                    <span className="text-slate-400 font-mono text-[10px]">({finding.rule_id})</span>
                  </div>
                  <p className="text-slate-600 font-medium leading-relaxed">{finding.description}</p>
                  <span className="text-slate-500 font-mono text-[11px] block">
                    File: {finding.file_path}:{finding.line_number}
                  </span>
                </div>

                <div className="text-left sm:text-right shrink-0">
                  <span className="text-xs font-extrabold text-slate-900 block">CVSS {finding.cvss_score}</span>
                  <span className="text-[11px] font-semibold text-slate-500">Confidence: {finding.confidence}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
