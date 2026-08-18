import React from 'react';
import { CheckCircle2, FileText, GitBranch, TestTube } from 'lucide-react';
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
    <div className="space-y-8">
      {/* Top 3 KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Card 1: README Completeness */}
        <div className="bg-white rounded-3xl p-6 border-2 border-slate-200/90 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold text-slate-500 uppercase tracking-wider">README Completeness</span>
            <div className="w-9 h-9 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <FileText className="h-4 w-4" />
            </div>
          </div>
          <div className="font-display text-3xl font-extrabold text-slate-900">
            96.0%
          </div>
          <p className="text-[11px] font-semibold text-slate-500">Evaluating 19 Standard Documentation Sections</p>
        </div>

        {/* Card 2: Testing Maturity */}
        <div className="bg-white rounded-3xl p-6 border-2 border-slate-200/90 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold text-slate-500 uppercase tracking-wider">Testing Maturity</span>
            <div className="w-9 h-9 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <TestTube className="h-4 w-4" />
            </div>
          </div>
          <div className="font-display text-3xl font-extrabold text-slate-900">
            90.0
          </div>
          <p className="text-[11px] font-semibold text-slate-500">Automated Test Suite & Pytest Coverage</p>
        </div>

        {/* Card 3: CI/CD Pipeline Automation */}
        <div className="bg-white rounded-3xl p-6 border-2 border-slate-200/90 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold text-slate-500 uppercase tracking-wider">CI/CD Automation</span>
            <div className="w-9 h-9 rounded-2xl bg-purple-50 text-purple-600 flex items-center justify-center">
              <GitBranch className="h-4 w-4" />
            </div>
          </div>
          <div className="font-display text-3xl font-extrabold text-slate-900">
            100%
          </div>
          <p className="text-[11px] font-semibold text-slate-500">GitHub Actions Pipeline Configured</p>
        </div>

      </div>

      {/* README Section Coverage & CI/CD Cadence Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* README Section Checklist */}
        <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm space-y-6">
          <div className="pb-3 border-b border-slate-100">
            <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight">
              README Section Coverage
            </h3>
            <p className="text-xs font-semibold text-slate-500">
              Evaluating documentation completeness against industry standard section specifications.
            </p>
          </div>

          <ProgressBar value={96.0} label="Documentation Completeness Ratio" color="emerald" />

          <div className="space-y-3 pt-2">
            <h4 className="text-xs font-extrabold text-slate-500 uppercase tracking-wider">
              Audited Documentation Sections:
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {readmeSections.map((sec, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-2xl bg-slate-50/80 border border-slate-200 text-xs font-bold text-slate-800 flex items-center gap-2.5 shadow-2xs"
                >
                  <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
                  <span>{sec.title}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* CI/CD & Release Cadence */}
        <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm space-y-6">
          <div className="pb-3 border-b border-slate-100">
            <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight">
              CI/CD & Release Cadence
            </h3>
            <p className="text-xs font-semibold text-slate-500">
              Automation providers, conventional commit compliance, and versioning tags.
            </p>
          </div>

          <div className="space-y-3.5 text-xs font-bold text-slate-800">
            <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-50/80 border border-slate-200 shadow-2xs">
              <span className="text-slate-600">CI/CD Automation Provider</span>
              <span className="px-3 py-1 rounded-full bg-purple-50 text-purple-700 border border-purple-200 font-extrabold text-[11px]">
                GitHub Actions
              </span>
            </div>

            <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-50/80 border border-slate-200 shadow-2xs">
              <span className="text-slate-600">Conventional Commits Ratio</span>
              <span className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-extrabold text-[11px]">
                98.5% Conventional
              </span>
            </div>

            <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-50/80 border border-slate-200 shadow-2xs">
              <span className="text-slate-600">Semantic Versioning</span>
              <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-extrabold text-[11px]">
                v1.0.0 Tagged
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
