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

  let colorClasses = 'bg-amber-50 text-amber-700 border-amber-200';
  if (['A+', 'A', 'A-'].includes(g)) {
    colorClasses = 'bg-emerald-50 text-emerald-700 border-emerald-200 shadow-sm';
  } else if (['B+', 'B', 'B-'].includes(g)) {
    colorClasses = 'bg-blue-50 text-blue-700 border-blue-200 shadow-sm';
  } else if (['C+', 'C', 'C-'].includes(g)) {
    colorClasses = 'bg-amber-50 text-amber-700 border-amber-200 shadow-sm';
  } else if (['D', 'F'].includes(g)) {
    colorClasses = 'bg-rose-50 text-rose-700 border-rose-200 shadow-sm';
  }

  const sizeClasses = {
    sm: 'px-2.5 py-0.5 text-xs font-black rounded-full border',
    md: 'px-3.5 py-1 text-sm font-black rounded-full border',
    lg: 'px-5 py-1.5 text-xl font-black rounded-full border-2',
    xl: 'px-7 py-2.5 text-3xl font-black rounded-full border-2 shadow-sm',
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
