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

  const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#8b5cf6', '#f43f5e', '#06b6d4'];

  return (
    <div className="w-full h-60">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <XAxis dataKey="category" stroke="#cbd5e1" tick={{ fill: '#475569', fontSize: 11, fontWeight: 700 }} />
          <YAxis stroke="#cbd5e1" tick={{ fill: '#475569', fontSize: 11, fontWeight: 700 }} />
          <Tooltip
            contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '16px', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
            itemStyle={{ color: '#0f172a', fontWeight: 800 }}
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
