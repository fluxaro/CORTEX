import { Workflow } from 'lucide-react';
import { DependencyGraphVisualizer } from '../components/charts/DependencyGraphVisualizer';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { ArchitectureReport } from '../services/types';

interface ArchitecturePageProps {
  architectureReport: ArchitectureReport;
}

export const ArchitecturePage: React.FC<ArchitecturePageProps> = ({ architectureReport }) => {
  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <Card glass className="p-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-3">
              <h2 className="text-xl font-bold text-white">{architectureReport.architecture_style}</h2>
              <Badge variant="purple" size="md">
                {(architectureReport.confidence_score * 100).toFixed(0)}% Confidence
              </Badge>
            </div>
            <p className="text-xs text-gray-400">Detected software architecture style and modular design pattern compliance.</p>
          </div>

          <div className="flex items-center gap-3 text-center">
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-[10px] text-gray-400 block">Modularity Score</span>
              <span className="text-lg font-bold text-emerald-400">{architectureReport.modularity_score}</span>
            </div>
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-[10px] text-gray-400 block">Layer Separation</span>
              <span className="text-lg font-bold text-blue-400">{architectureReport.layer_separation_score}</span>
            </div>
          </div>
        </div>
      </Card>

      {/* Module Dependency Graph Visualizer */}
      <Card glass>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Workflow className="h-5 w-5 text-primary-400" />
            <span>Interactive Module Dependency Graph</span>
          </CardTitle>
          <CardDescription>Visualizing module coupling and directed imports across layers.</CardDescription>
        </CardHeader>
        <CardContent>
          <DependencyGraphVisualizer />
        </CardContent>
      </Card>

      {/* Design Patterns & Frameworks */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card glass>
          <CardHeader>
            <CardTitle>Detected Design Patterns</CardTitle>
            <CardDescription>Recognized GOF design patterns in codebase.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {architectureReport.patterns.map((pat, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-surface-card border border-border/40 text-xs">
                <div>
                  <h4 className="font-semibold text-gray-200">{pat.pattern_name}</h4>
                  <span className="text-[10px] text-gray-400 font-mono line-clamp-1">{pat.file_path}</span>
                </div>
                <Badge variant="info">{(pat.confidence * 100).toFixed(0)}% Match</Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card glass>
          <CardHeader>
            <CardTitle>Technology Stack & Frameworks</CardTitle>
            <CardDescription>Detected frameworks, ORMs, and libraries.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {architectureReport.frameworks.map((fw, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-surface-card border border-border/40 text-xs">
                <div>
                  <h4 className="font-semibold text-gray-200">{fw.framework_name}</h4>
                  <span className="text-[10px] text-gray-400">{fw.category}</span>
                </div>
                <Badge variant="outline">{fw.version || 'Latest'}</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
