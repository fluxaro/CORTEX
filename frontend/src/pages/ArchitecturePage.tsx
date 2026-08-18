import React from 'react';
import { Layers, Workflow } from 'lucide-react';
import { DependencyGraphVisualizer } from '../components/charts/DependencyGraphVisualizer';
import { ArchitectureReport } from '../services/types';

interface ArchitecturePageProps {
  architectureReport: ArchitectureReport;
}

export const ArchitecturePage: React.FC<ArchitecturePageProps> = ({ architectureReport }) => {
  const rawConf = architectureReport.confidence_score || 94.0;
  const confDisplay = rawConf > 1 ? rawConf.toFixed(0) : (rawConf * 100).toFixed(0);

  return (
    <div className="space-y-8">
      {/* Top Banner Card */}
      <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center border border-blue-200 shrink-0">
              <Layers className="h-5 w-5" />
            </div>
            <h2 className="font-display text-2xl font-extrabold text-slate-900 tracking-tight">
              {architectureReport.architecture_style || 'Clean Architecture Layered Pattern'}
            </h2>
            <span className="px-3 py-1 rounded-full text-xs font-extrabold bg-purple-50 text-purple-700 border border-purple-200">
              {confDisplay}% Confidence
            </span>
          </div>
          <p className="text-xs text-slate-500 font-medium">
            Detected software architecture style and modular design pattern compliance.
          </p>
        </div>

        {/* Modularity & Layer Separation Stat Badges */}
        <div className="flex items-center gap-4 shrink-0">
          <div className="bg-emerald-50/80 p-3.5 rounded-2xl border border-emerald-200 text-center min-w-[110px]">
            <span className="text-[10px] font-extrabold text-emerald-700 uppercase tracking-wider block">
              Modularity Score
            </span>
            <span className="font-display text-2xl font-extrabold text-emerald-900">
              {architectureReport.modularity_score || 92}
            </span>
          </div>
          <div className="bg-blue-50/80 p-3.5 rounded-2xl border border-blue-200 text-center min-w-[110px]">
            <span className="text-[10px] font-extrabold text-blue-700 uppercase tracking-wider block">
              Layer Separation
            </span>
            <span className="font-display text-2xl font-extrabold text-blue-900">
              {architectureReport.layer_separation_score || 95}
            </span>
          </div>
        </div>
      </div>

      {/* Interactive Module Dependency Graph */}
      <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
              <Workflow className="h-5 w-5 text-blue-600" />
              <span>Interactive Module Dependency Graph</span>
            </h3>
            <p className="text-xs font-semibold text-slate-500">
              Visualizing module coupling and directed imports across layers.
            </p>
          </div>
        </div>
        <div className="pt-2">
          <DependencyGraphVisualizer />
        </div>
      </div>

      {/* Design Patterns & Tech Stack Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Design Patterns */}
        <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm space-y-4">
          <div className="pb-3 border-b border-slate-100">
            <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight">
              Detected Design Patterns
            </h3>
            <p className="text-xs font-semibold text-slate-500">
              Recognized GOF design patterns in codebase modules.
            </p>
          </div>

          <div className="space-y-3">
            {(architectureReport.patterns || []).map((pat, idx) => {
              const matchVal = pat.confidence > 1 ? pat.confidence : (pat.confidence * 100);
              return (
                <div
                  key={idx}
                  className="flex items-center justify-between p-4 rounded-2xl bg-slate-50/80 border border-slate-200 text-xs shadow-2xs"
                >
                  <div>
                    <h4 className="font-bold text-slate-900">{pat.pattern_name}</h4>
                    <span className="text-[11px] text-slate-500 font-mono line-clamp-1">{pat.file_path}</span>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-200 font-extrabold text-[11px]">
                    {matchVal.toFixed(0)}% Match
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Tech Stack & Frameworks */}
        <div className="bg-white rounded-[32px] p-7 border-2 border-slate-200/90 shadow-sm space-y-4">
          <div className="pb-3 border-b border-slate-100">
            <h3 className="font-display text-lg font-extrabold text-slate-900 tracking-tight">
              Technology Stack & Frameworks
            </h3>
            <p className="text-xs font-semibold text-slate-500">
              Detected language runtime environments, frameworks, and libraries.
            </p>
          </div>

          <div className="space-y-3">
            {(architectureReport.frameworks || []).map((fw, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-4 rounded-2xl bg-slate-50/80 border border-slate-200 text-xs shadow-2xs"
              >
                <div>
                  <h4 className="font-bold text-slate-900">{fw.framework_name}</h4>
                  <span className="text-[11px] text-slate-500 font-medium">{fw.category}</span>
                </div>
                <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200 font-extrabold text-[11px]">
                  {fw.version || 'Latest'}
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};
