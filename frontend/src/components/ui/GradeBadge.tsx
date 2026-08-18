import React from 'react';

interface GradeBadgeProps {
  grade: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showLabel?: boolean;
  className?: string;
}

export const GradeBadge: React.FC<GradeBadgeProps> = ({
  grade,
  size = 'md',
  showLabel = false,
  className = '',
}) => {
  const g = grade.toUpperCase().trim();

  let colorClasses = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
  if (['A+', 'A', 'A-'].includes(g)) {
    colorClasses = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-emerald-500/10';
  } else if (['B+', 'B', 'B-'].includes(g)) {
    colorClasses = 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30 shadow-cyan-500/10';
  } else if (['C+', 'C', 'C-'].includes(g)) {
    colorClasses = 'bg-amber-500/10 text-amber-400 border-amber-500/30 shadow-amber-500/10';
  } else if (['D', 'F'].includes(g)) {
    colorClasses = 'bg-rose-500/10 text-rose-400 border-rose-500/30 shadow-rose-500/10';
  }

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs font-bold rounded-md border',
    md: 'px-3 py-1 text-base font-extrabold rounded-lg border',
    lg: 'px-5 py-2 text-2xl font-black rounded-xl border-2',
    xl: 'px-7 py-3 text-4xl font-black rounded-2xl border-2 shadow-lg',
  }[size];

  return (
    <div className={`inline-flex items-center gap-2 ${className}`}>
      <span className={`font-mono tracking-tight ${colorClasses} ${sizeClasses}`}>
        {g}
      </span>
      {showLabel && (
        <span className="text-xs uppercase tracking-wider font-semibold text-gray-400">
          Grade
        </span>
      )}
    </div>
  );
};
