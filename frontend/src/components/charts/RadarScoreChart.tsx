import React from 'react';
import {
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from 'recharts';
import { SubsystemScores } from '../../services/types';

interface RadarScoreChartProps {
  subsystems: SubsystemScores;
}

export const RadarScoreChart: React.FC<RadarScoreChartProps> = ({ subsystems }) => {
  const data = [
    { subject: 'Static Analysis', score: subsystems.static_analysis },
    { subject: 'Architecture', score: subsystems.architecture },
    { subject: 'Security', score: subsystems.security },
    { subject: 'Documentation', score: subsystems.documentation },
    { subject: 'Testing', score: subsystems.testing },
    { subject: 'CI/CD', score: subsystems.ci },
    { subject: 'Git Practices', score: subsystems.git_practices },
    { subject: 'Repo Health', score: subsystems.repository_health },
  ];

  return (
    <div className="w-full h-64 sm:h-80">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
          <PolarGrid stroke="#232d42" />
          <PolarAngleAxis dataKey="subject" stroke="#9ca3af" tick={{ fill: '#9ca3af', fontSize: 11 }} />
          <Radar
            name="Subsystem Score"
            dataKey="score"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.35}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
