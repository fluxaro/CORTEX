import { Clock, Sparkles, TrendingUp } from 'lucide-react';
import { ScoreGauge } from '../components/charts/ScoreGauge';
import { TechnicalDebtChart } from '../components/charts/TechnicalDebtChart';
import { Badge } from '../components/ui/Badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { RepositoryIQReport } from '../services/types';

interface RepositoryIQPageProps {
  iqReport: RepositoryIQReport;
}

export const RepositoryIQPage: React.FC<RepositoryIQPageProps> = ({ iqReport }) => {
  const debt = iqReport.technical_debt;
  const benchmark = iqReport.benchmark;

  return (
    <div className="space-y-6">
      {/* Top Banner Score & Maturity */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card glass className="flex flex-col items-center justify-center p-6 text-center">
          <ScoreGauge score={iqReport.overall_score} size={150} />
          <div className="mt-4 space-y-1">
            <Badge variant="purple" size="md">
              {iqReport.maturity_level}
            </Badge>
            <p className="text-[11px] text-gray-400">Weighted Repository IQ Score</p>
          </div>
        </Card>

        <Card glass className="md:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary-400" />
              <span>AI Executive Synthesis</span>
            </CardTitle>
            <CardDescription>Deterministic AI summary generated strictly from stored database metrics.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="p-4 rounded-xl bg-surface-card border border-border/60 text-xs sm:text-sm text-gray-200 leading-relaxed">
              {iqReport.summary?.executive_summary}
            </div>
            <div className="p-4 rounded-xl bg-surface-card border border-border/60 text-xs text-gray-300 leading-relaxed font-mono">
              <span className="text-primary-400 font-semibold block mb-1">Technical Summary:</span>
              {iqReport.summary?.technical_summary}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Technical Debt Estimation */}
      {debt && (
        <Card glass>
          <CardHeader className="flex flex-col sm:flex-row justify-between sm:items-center gap-3">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5 text-amber-400" />
                <span>Technical Debt Estimation</span>
              </CardTitle>
              <CardDescription>Estimated effort to remediate identified code smells, security findings, and testing gaps.</CardDescription>
            </div>
            <div className="text-right">
              <span className="text-2xl font-bold text-amber-400">{debt.total_hours} Hours</span>
              <span className="text-xs text-gray-400 block">({debt.total_days} Engineering Days)</span>
            </div>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <TechnicalDebtChart categoryBreakdown={debt.category_breakdown} />
            <div className="space-y-2 max-h-60 overflow-y-auto">
              <h4 className="text-xs font-semibold text-gray-300">Itemized Findings:</h4>
              {debt.items.map((item, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-surface-card border border-border/40 flex justify-between items-center text-xs">
                  <div>
                    <span className="font-semibold text-gray-200">{item.category}</span>
                    <p className="text-gray-400 text-[11px]">{item.description}</p>
                  </div>
                  <Badge variant="warning">{item.estimated_hours}h</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Industry Benchmarking & Percentiles */}
      {benchmark && (
        <Card glass>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-emerald-400" />
              <span>Industry Quality Benchmarking</span>
            </CardTitle>
            <CardDescription>Percentile rankings compared against open-source and enterprise quality standards.</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-2 sm:grid-cols-5 gap-4 text-center">
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-[10px] text-gray-400 block">Overall Percentile</span>
              <span className="text-xl font-bold text-emerald-400">{benchmark.overall_percentile}%</span>
            </div>
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-[10px] text-gray-400 block">Quality Percentile</span>
              <span className="text-xl font-bold text-blue-400">{benchmark.quality_percentile}%</span>
            </div>
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-[10px] text-gray-400 block">Security Percentile</span>
              <span className="text-xl font-bold text-purple-400">{benchmark.security_percentile}%</span>
            </div>
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-[10px] text-gray-400 block">Architecture Percentile</span>
              <span className="text-xl font-bold text-cyan-400">{benchmark.architecture_percentile}%</span>
            </div>
            <div className="p-3 bg-surface-card rounded-xl border border-border/40">
              <span className="text-[10px] text-gray-400 block">Maintainability Percentile</span>
              <span className="text-xl font-bold text-amber-400">{benchmark.maintainability_percentile}%</span>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
