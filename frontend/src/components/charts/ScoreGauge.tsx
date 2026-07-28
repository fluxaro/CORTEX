import React from 'react';

interface ScoreGaugeProps {
  score: number;
  size?: number;
  strokeWidth?: number;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({
  score,
  size = 140,
  strokeWidth = 12,
}) => {
  const safeScore = Math.min(Math.max(score, 0), 100);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (safeScore / 100) * circumference;

  const getColor = (s: number) => {
    if (s >= 85) return '#10b981'; // emerald
    if (s >= 70) return '#3b82f6'; // blue
    if (s >= 50) return '#f59e0b'; // amber
    return '#f43f5e'; // rose
  };

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#1f293d"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={getColor(safeScore)}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          fill="transparent"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center">
        <span className="text-3xl font-extrabold text-white tracking-tight">{safeScore.toFixed(1)}</span>
        <span className="text-[10px] uppercase font-semibold text-gray-400">IQ Score</span>
      </div>
    </div>
  );
};
