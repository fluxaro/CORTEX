import React from 'react';
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { TrendingUp } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { MOCK_TREND_METRICS } from '../services/mockEnterpriseData';

export const TrendAnalysisPage: React.FC = () => {
  const chartData = MOCK_TREND_METRICS.map((t) => ({
    date: t.recorded_at.split('T')[0],
    IQ: t.overall_iq,
    Security: t.security_score,
    Architecture: t.architecture_score,
    Maintainability: t.complexity_score,
  }));

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4">
      <div className="pb-4 border-b border-border/80">
        <h1 className="text-2xl font-bold text-white tracking-tight">Time-Series Trend Analysis</h1>
        <p className="text-xs text-gray-400">Track repository IQ, security posture, and technical debt over time.</p>
      </div>

      <Card glass>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-emerald-400" />
            <span>Repository Intelligence Trajectory</span>
          </CardTitle>
          <CardDescription>Historical trajectory of Repository IQ, Security, Architecture, and Maintainability scores.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="w-full h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 10, right: 30, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#232d42" />
                <XAxis dataKey="date" stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <YAxis domain={[60, 100]} stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#232d42', borderRadius: '12px' }}
                />
                <Line type="monotone" dataKey="IQ" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="Security" stroke="#8b5cf6" strokeWidth={2} />
                <Line type="monotone" dataKey="Architecture" stroke="#10b981" strokeWidth={2} />
                <Line type="monotone" dataKey="Maintainability" stroke="#f59e0b" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
