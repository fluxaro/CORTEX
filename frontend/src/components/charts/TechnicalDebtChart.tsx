import React from 'react';
import {
  Bar,
  BarChart,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

interface TechnicalDebtChartProps {
  categoryBreakdown: Record<string, number>;
}

export const TechnicalDebtChart: React.FC<TechnicalDebtChartProps> = ({ categoryBreakdown }) => {
  const data = Object.entries(categoryBreakdown).map(([key, value]) => ({
    category: key,
    hours: value,
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#f43f5e', '#06b6d4'];

  return (
    <div className="w-full h-60">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <XAxis dataKey="category" stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
          <YAxis stroke="#6b7280" tick={{ fill: '#9ca3af', fontSize: 11 }} />
          <Tooltip
            contentStyle={{ backgroundColor: '#111827', borderColor: '#232d42', borderRadius: '12px' }}
            itemStyle={{ color: '#60a5fa' }}
            formatter={(val: number) => [`${val} hours`, 'Technical Debt']}
          />
          <Bar dataKey="hours" radius={[6, 6, 0, 0]}>
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
